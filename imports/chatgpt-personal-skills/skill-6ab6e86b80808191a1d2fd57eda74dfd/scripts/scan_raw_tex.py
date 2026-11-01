#!/usr/bin/env python3
"""Flag leftover TeX source and replacement characters on every page and printable string."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SKIP_DIR = {
    ".git",
    "__pycache__",
    "node_modules",
    "imagine_images",
}
SKIP_SUFFIX = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".woff", ".woff2", ".ttf", ".otf"}
# Files that may hold TeX *source*. Visible JSON/HTML strings are not source.
SOURCE_OK = {".tex", ".py", ".js", ".ts", ".tsx"}
ALLOWED_JSON_KEYS = {"tex", "latex", "source", "preamble", "prompt"}

COMMANDS = (
    r"frac|cfrac|dfrac|tfrac|sum|int|oint|prod|mathrm|mathbf|mathbb|mathcal|operatorname|"
    r"times|cdot|partial|nabla|infty|sqrt|leq|geq|neq|approx|sim|equiv|propto|"
    r"left|right|begin|end|over|hat|bar|vec|tilde|dot|ddot|"
    r"text|textbf|textrm|textit|displaystyle|limits|notag|tag|"
    r"alpha|beta|gamma|delta|epsilon|varepsilon|zeta|eta|theta|vartheta|"
    r"iota|kappa|lambda|mu|nu|xi|pi|varpi|rho|sigma|tau|upsilon|phi|varphi|"
    r"chi|psi|omega|Gamma|Delta|Theta|Lambda|Xi|Pi|Sigma|Phi|Psi|Omega|"
    r"quad|qquad|hspace|vspace|phantom|color|binom|choose|matrix|pmatrix|bmatrix|"
    r"align|aligned|equation|eqnarray|gather|multline|split|cases|"
    r"overline|underline|overset|underset|xrightarrow|iff|implies|"
    r"ce|mhchem|katex|ensuremath"
)
RAW = [
    re.compile(r"\$\$[\s\S]{1,800}?\$\$"),
    re.compile(r"\\\[[\s\S]{1,800}?\\\]"),
    re.compile(r"\\\([\s\S]{1,400}?\\\)"),
    # Inline $...$ only when the payload looks like TeX, not currency ($45 or $0.00 ... $2,528).
    # Bare underscore inside two dollar amounts is not enough (rank tables).
    re.compile(
        r"(?<![`$\\])\$(?=.*?(?:\\[A-Za-z]+|\^\{|_{|\\frac|\\sum|\\mathrm))[^$\n]{1,240}\$(?![`])"
    ),
    re.compile(rf"(?<!\\)\\(?:{COMMANDS})\b"),
    re.compile(r"\\begin\{(?:equation|align|gather|multline|eqnarray)\*?\}"),
    re.compile(r"\[tex\]|\[/tex\]|\[math\]|\[/math\]", re.I),
    re.compile(r"(?:katex|mathjax|asciimath)\s*\.(?:render|tex)", re.I),
    re.compile("\ufffd"),
    re.compile("\ufffc"),
    re.compile(r"[\u2612\u2610]"),  # ☒ ☐ often stand in for a missing math glyph
    re.compile(r"[\u25a1\u25a0\u25fb\u25fc\u25a3\u2b1c\u25a2]{1,}"),
    re.compile(r"[\u25a1\u25a0\u25fb\u25fc]{2,}"),  # runs of empty boxes
    re.compile(r"\^\{[^}]{1,80}\}"),
    re.compile(r"_\{[^}]{1,80}\}"),
    re.compile(r"(?<![A-Za-z0-9/])[A-Za-z][A-Za-z0-9]*\^-\d"),
    # ASCII-TeX identifiers left in a visible page or ITQE cell
    re.compile(r"\b(?:I_tot|B_k|p_k|N_j|P_30|p_t|Lambda_int|Λ_int|p\^bi|I_tot\^[0-9A-Za-z]+)\b"),
    re.compile(r"\b[A-Za-z]_(?:tot|int|GEM)\b"),
    re.compile(r"\b[A-Za-z](?:_[A-Za-z0-9]{1,6})+\^[A-Za-z0-9]{1,4}\b"),
]


def scan_text(label: str, text: str, allow_source: bool) -> list[str]:
    hits = []
    if not text:
        return hits
    if "\ufffd" in text:
        hits.append(f"{label}: replacement character U+FFFD")
    if allow_source:
        return hits
    for rx in RAW:
        m = rx.search(text)
        if m:
            snippet = m.group(0)[:80].replace("\n", " ")
            hits.append(f"{label}: raw TeX {snippet!r}")
            break
    return hits


def walk_json_strings(obj, pointer: str, hits: list[str], file_label: str) -> None:
    if isinstance(obj, dict):
        for key, val in obj.items():
            child = f"{pointer}/{key}"
            if str(key).lower() in ALLOWED_JSON_KEYS:
                continue
            walk_json_strings(val, child, hits, file_label)
    elif isinstance(obj, list):
        for i, val in enumerate(obj):
            walk_json_strings(val, f"{pointer}/{i}", hits, file_label)
    elif isinstance(obj, str):
        hits.extend(scan_text(f"{file_label}{pointer}", obj, allow_source=False))


def scan_file(path: Path) -> list[str]:
    suffix = path.suffix.lower()
    if suffix in SKIP_SUFFIX:
        return []
    if suffix == ".pdf":
        return scan_pdf_pages(path)
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    if suffix == ".json":
        try:
            data = json.loads(raw)
        except Exception:
            return scan_text(str(path), raw, allow_source=False)
        hits: list[str] = []
        walk_json_strings(data, "", hits, str(path))
        return hits
    if suffix == ".md":
        raw = re.sub(r"```(?:tex|latex)[\s\S]*?```", "", raw, flags=re.I)
        return scan_text(str(path), raw, allow_source=False)
    allow = suffix in SOURCE_OK or path.name.endswith(".tex")
    return scan_text(str(path), raw, allow_source=allow)


def walk(root: Path) -> list[str]:
    hits: list[str] = []
    paths = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file()]
    for p in paths:
        if any(part in SKIP_DIR for part in p.parts):
            continue
        hits.extend(scan_file(p))
    return hits


def pdf_page_count(pdf: Path) -> int:
    r = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True)
    for line in r.stdout.splitlines():
        if line.lower().startswith("pages:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except ValueError:
                return 0
    return 0


def scan_pdf_pages(pdf: Path) -> list[str]:
    hits: list[str] = []
    pages = pdf_page_count(pdf)
    if pages <= 0:
        r = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True)
        if r.returncode != 0:
            return [f"{pdf}: pdftotext failed"]
        return scan_text(str(pdf), r.stdout, allow_source=False)
    for n in range(1, pages + 1):
        r = subprocess.run(
            ["pdftotext", "-layout", "-f", str(n), "-l", str(n), str(pdf), "-"],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            hits.append(f"{pdf} p.{n}: pdftotext failed")
            continue
        hits.extend(scan_text(f"{pdf} p.{n}", r.stdout, allow_source=False))
    return hits


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("root", help="file or directory to scan")
    p.add_argument("--also-pdf", action="append", default=[])
    p.add_argument("--pages", action="store_true", help="Accepted for compatibility; PDFs always scan every page.")
    args = p.parse_args()
    hits = walk(Path(args.root))
    for pdf in args.also_pdf:
        hits.extend(scan_pdf_pages(Path(pdf)))
    if not hits:
        print("scan_raw_tex: clean")
        return 0
    print("scan_raw_tex: FAIL")
    for h in hits:
        print(" -", h)
    return 1


if __name__ == "__main__":
    sys.exit(main())
