#!/usr/bin/env python3
"""Locate raw TeX that would print on a page. Writes latex-inventory.jsonl."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ALLOWED_KEYS = {"tex", "latex", "source", "preamble", "prompt"}
SKIP_DIR = {".git", "__pycache__", "node_modules", "imagine_images"}
TEXT_SUFFIX = {".json", ".md", ".html", ".htm", ".txt", ".csv", ".tex"}

COMMANDS = (
    r"frac|sum|int|mathrm|mathbf|mathbb|mathcal|times|cdot|partial|nabla|"
    r"alpha|beta|gamma|delta|epsilon|theta|lambda|mu|nu|pi|sigma|omega|"
    r"infty|sqrt|leq|geq|neq|left|right|begin|end|over|hat|bar|vec|"
    r"text|tfrac|dfrac|displaystyle|limits"
)
RAW = [
    ("dollardollar", re.compile(r"\$\$[\s\S]{1,800}?\$\$")),
    ("bracket", re.compile(r"\\\[[\s\S]{1,800}?\\\]")),
    ("paren", re.compile(r"\\\([\s\S]{1,400}?\\\)")),
    ("dollar", re.compile(r"(?<![`$\\])\$[^$\n]{1,240}\$(?![`])")),
    ("command", re.compile(rf"(?<!\\)\\(?:{COMMANDS})\b")),
    ("replacement", re.compile("\ufffd")),
]


def classify(snippet: str) -> str:
    s = snippet.strip()
    if s.startswith("$$") or s.startswith("\\[") or "\\begin{" in s:
        return "display"
    if s.startswith("$") or s.startswith("\\("):
        return "inline"
    return "command"


def scan_string(pointer: str, text: str) -> list[dict]:
    hits = []
    if not text:
        return hits
    seen_spans: list[tuple[int, int]] = []
    for kind, rx in RAW:
        for m in rx.finditer(text):
            span = m.span()
            if any(span[0] >= a and span[1] <= b for a, b in seen_spans):
                continue
            seen_spans.append(span)
            snippet = m.group(0).replace("\n", " ")[:200]
            hits.append(
                {
                    "pointer": pointer,
                    "kind": "replacement" if kind == "replacement" else classify(m.group(0)),
                    "pattern": kind,
                    "source": snippet,
                }
            )
    return hits


def walk_json(obj, pointer: str, hits: list[dict]) -> None:
    if isinstance(obj, dict):
        for key, val in obj.items():
            child = f"{pointer}/{key}" if pointer else f"/{key}"
            if str(key).lower() in ALLOWED_KEYS:
                continue
            walk_json(val, child, hits)
    elif isinstance(obj, list):
        for i, val in enumerate(obj):
            walk_json(val, f"{pointer}/{i}", hits)
    elif isinstance(obj, str):
        hits.extend(scan_string(pointer or "/", obj))


def harvest_path(path: Path) -> list[dict]:
    hits: list[dict] = []
    suffix = path.suffix.lower()
    if suffix == ".json":
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            return [{"pointer": str(path), "kind": "error", "pattern": "json", "source": str(exc)}]
        file_hits: list[dict] = []
        walk_json(data, "", file_hits)
        for h in file_hits:
            h["file"] = str(path)
        return file_hits
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return hits
    if suffix in {".tex"}:
        return hits
    if suffix == ".md":
        # Drop fenced tex/latex listings; those are source on purpose.
        text = re.sub(r"```(?:tex|latex)[\s\S]*?```", "", text, flags=re.I)
    for h in scan_string(str(path), text):
        h["file"] = str(path)
        hits.append(h)
    return hits


def walk_root(root: Path) -> list[dict]:
    if root.is_file():
        return harvest_path(root)
    hits: list[dict] = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if any(part in SKIP_DIR for part in p.parts):
            continue
        if p.suffix.lower() not in TEXT_SUFFIX:
            continue
        hits.extend(harvest_path(p))
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Harvest raw TeX that would print on a page.")
    parser.add_argument("root")
    parser.add_argument("--out", help="Write JSONL inventory")
    args = parser.parse_args()
    hits = walk_root(Path(args.root))
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8") as fh:
            for h in hits:
                fh.write(json.dumps(h, ensure_ascii=False) + "\n")
        print(f"harvest_raw_tex: {len(hits)} hit(s) → {out}")
    else:
        print(json.dumps(hits, indent=2, ensure_ascii=False))
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
