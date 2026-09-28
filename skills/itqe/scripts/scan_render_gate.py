#!/usr/bin/env python3
"""Fail-closed render gate: no raw TeX/KaTeX/AMS on a visible page; intended glyphs only; every display plate has ITQE."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

LATEX_SCAN = Path("/home/workdir/.grok/skills/latex/scripts/scan_raw_tex.py")
ITQE_KEYS = ("identifier", "term", "quantity", "explanation")
GREEK_SPELL = re.compile(
    r"^(theta|lambda|sigma|tau|phi|varphi|omega|alpha|beta|gamma|delta|epsilon|nabla|pi|mu|nu|xi|psi|chi|eta|zeta|iota|kappa|rho|upsilon)(_[A-Za-z0-9]+)?$",
    re.I,
)
GREEK_CHAR = re.compile(r"[αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ∇∂ℓħℵ]")

CELL_TEX = (
    r"\\(?:frac|sum|int|mathrm|mathbf|mathbb|mathcal|begin|alpha|beta|gamma|delta|theta|lambda|sigma|phi|omega|partial|nabla|rho|times)",
    r"\$\$",
    r"\\\(|\\\)|\\\[|\\\]",
    r"\^\{",
    r"_\{",
    r"[A-Za-z]\^-?\d",
    r"[A-Za-z]\^[A-Za-z]",
    r"m\^-\d",
    r"kg m\^",
    r"\b(?:I_tot|B_k|p_k|N_j|P_30|Λ_int|Lambda_int)\b",
    r"\b[A-Za-z]_(?:tot|int|GEM)\b",
)
MISSING_GLYPH = re.compile(
    r"[\ufffd\ufffc\u2612\u2610\u25a1\u25a0\u25fb\u25fc\u25a3\u2b1c\u25a2\u25a4]"
)


def run_latex_scan(root: Path, pdfs: list[Path]) -> list[str]:
    cmd = [sys.executable, str(LATEX_SCAN), str(root)]
    for pdf in pdfs:
        cmd.extend(["--also-pdf", str(pdf), "--pages"])
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0:
        return []
    lines = [ln[3:] for ln in (r.stdout or "").splitlines() if ln.startswith(" - ")]
    if not lines:
        lines = [(r.stdout or r.stderr or "scan_raw_tex failed").strip()]
    return lines


def check_equation_objects(obj, pointer: str, hits: list[str]) -> None:
    if isinstance(obj, dict):
        if str(obj.get("type", "")).lower() == "equation":
            plate = obj.get("plate") or obj.get("unicode") or obj.get("svg")
            if not plate:
                hits.append(f"{pointer}: equation object has no plate/unicode/svg")
            vis = " ".join(
                str(obj.get(k, ""))
                for k in ("unicode", "caption")
                if obj.get(k)
            )
            if "\\" in vis and any(
                tok in vis
                for tok in ("\\frac", "\\sum", "\\int", "\\mathrm", "\\begin", "\\alpha")
            ):
                hits.append(f"{pointer}: printable equation field still holds raw TeX")
            rows = obj.get("itqe") or []
            if not rows:
                hits.append(f"{pointer}: display equation missing ITQE rows")
            for i, row in enumerate(rows):
                if not isinstance(row, dict):
                    hits.append(f"{pointer}/itqe/{i}: row is not an object")
                    continue
                for key in ITQE_KEYS:
                    val = row.get(key)
                    if val is None or str(val).strip() == "":
                        hits.append(f"{pointer}/itqe/{i}: blank {key}")
                        continue
                    text = str(val)
                    if key == "identifier" and GREEK_SPELL.match(text.strip()):
                        hits.append(f"{pointer}/itqe/{i}/identifier: Latin stand-in {text!r} — print the glyph")
                    if MISSING_GLYPH.search(text):
                        hits.append(
                            f"{pointer}/itqe/{i}/{key}: missing-glyph stand-in {text[:80]!r}"
                        )
                    for pat in CELL_TEX:
                        if re.search(pat, text):
                            hits.append(
                                f"{pointer}/itqe/{i}/{key}: uncompiled math {text[:80]!r}"
                            )
                            break
            blob = " ".join(str(r.get("identifier") or "") for r in rows if isinstance(r, dict))
            glyphs_used = set(GREEK_CHAR.findall(blob))
            if glyphs_used:
                legend = obj.get("legend") or []
                have = set()
                for item in legend:
                    if isinstance(item, dict):
                        g = str(item.get("glyph") or "")
                        have.update(GREEK_CHAR.findall(g))
                        if not item.get("name") or not (item.get("role") or item.get("spoken")):
                            hits.append(f"{pointer}: glyph row missing name or role")
                missing = glyphs_used - have
                if missing:
                    hits.append(f"{pointer}: missing ITQE glyph rows for {''.join(sorted(missing))}")
        for key, val in obj.items():
            check_equation_objects(val, f"{pointer}/{key}", hits)
    elif isinstance(obj, list):
        for i, val in enumerate(obj):
            check_equation_objects(val, f"{pointer}/{i}", hits)


def scan_json_file(path: Path) -> list[str]:
    hits: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return hits
    check_equation_objects(data, str(path), hits)
    return hits


def walk_json(root: Path) -> list[str]:
    hits: list[str] = []
    paths = [root] if root.is_file() else list(root.rglob("*.json"))
    skip = {".git", "__pycache__", "node_modules"}
    for p in paths:
        if any(part in skip for part in p.parts):
            continue
        if p.name in {"citation-map.json", "package.json", "package-lock.json"}:
            continue
        hits.extend(scan_json_file(p))
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description="ITQE + LaTeX fail-closed render gate")
    ap.add_argument("root", help="draft folder, JSON, or PDF")
    ap.add_argument("--also-pdf", action="append", default=[])
    args = ap.parse_args()
    root = Path(args.root).resolve()
    pdfs = [Path(p).resolve() for p in args.also_pdf]
    if root.suffix.lower() == ".pdf":
        pdfs.append(root)
        scan_root = root.parent
    else:
        scan_root = root

    hits = run_latex_scan(scan_root if scan_root.exists() else root, pdfs)
    hits.extend(walk_json(root if root.suffix.lower() == ".json" else scan_root))

    if not hits:
        print("scan_render_gate: clean")
        return 0
    print("scan_render_gate: FAIL")
    for h in hits:
        print(" -", h)
    return 1


if __name__ == "__main__":
    sys.exit(main())
