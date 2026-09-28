#!/usr/bin/env python3
"""Fail-closed intended-glyph sweep.

Detects characters that house PDF faces (Literata / EB Garamond / Libre Franklin)
commonly draw as .notdef white or black boxes. Run after the builder and after
scan_raw_tex.py. Exit 1 blocks delivery.

Usage:
  python3 scan_intended_glyphs.py --pdf path.pdf [--also-json path.json]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

# Operators and combining marks that reportlab + Literata often replace with tofu.
UNSAFE = {
    "\u21d2",  # ⇒
    "\u21d0",  # ⇐
    "\u21d4",  # ⇔
    "\u226b",  # ≫
    "\u226a",  # ≪
    "\u22d9",  # ⋙
    "\u22d8",  # ⋘
    "\u27f9",  # ⟹
    "\u27fa",  # ⟺
    "\ufffd",
    "\ufffc",
    "\u2612",
    "\u2610",
    "\u25a1",
    "\u25a0",
    "\u25fb",
    "\u25fc",
    "\u25a3",
    "\u2b1c",
    "\u25a2",
}

COMBINING = range(0x0300, 0x0370)

SAFE_JSON_KEYS = {"tex", "latex", "source", "preamble", "prompt"}


def pdf_text(path: Path) -> str:
    r = subprocess.run(
        ["pdftotext", "-layout", str(path), "-"],
        capture_output=True,
        text=True,
        check=False,
    )
    return (r.stdout or "") + (r.stderr or "")


def flag_text(label: str, text: str) -> list[str]:
    hits = []
    if not text:
        return hits
    seen = set()
    for ch in text:
        if ch in UNSAFE:
            key = f"{label}: unsafe glyph U+{ord(ch):04X} {ch!r}"
            if key not in seen:
                seen.add(key)
                hits.append(key)
        elif ord(ch) in COMBINING:
            key = f"{label}: combining mark U+{ord(ch):04X} (use Latin alias or a compiled plate)"
            if key not in seen:
                seen.add(key)
                hits.append(key)
    return hits


def walk_json(obj, pointer: str, hits: list[str]) -> None:
    if isinstance(obj, dict):
        for key, val in obj.items():
            if str(key).lower() in SAFE_JSON_KEYS:
                continue
            walk_json(val, f"{pointer}/{key}", hits)
    elif isinstance(obj, list):
        for i, val in enumerate(obj):
            walk_json(val, f"{pointer}/{i}", hits)
    elif isinstance(obj, str):
        hits.extend(flag_text(pointer, obj))


def main() -> int:
    parser = argparse.ArgumentParser(description="Intended-glyph sweep")
    parser.add_argument("--pdf", action="append", default=[], help="PDF to extract")
    parser.add_argument("--also-json", action="append", default=[], help="Draft JSON")
    parser.add_argument("root", nargs="?", help="Optional folder of JSON/PDF")
    args = parser.parse_args()

    hits: list[str] = []
    pdfs = [Path(p) for p in args.pdf]
    jsons = [Path(p) for p in args.also_json]
    if args.root:
        root = Path(args.root)
        if root.is_dir():
            pdfs.extend(sorted(root.rglob("*.pdf")))
            jsons.extend(sorted(root.rglob("*.json")))
        elif root.suffix.lower() == ".pdf":
            pdfs.append(root)
        elif root.suffix.lower() == ".json":
            jsons.append(root)

    for pdf in pdfs:
        if not pdf.exists():
            hits.append(f"{pdf}: missing")
            continue
        hits.extend(flag_text(str(pdf), pdf_text(pdf)))
    for js in jsons:
        if not js.exists():
            continue
        if js.name.endswith("rank.json") or "inventory" in js.name:
            continue
        try:
            data = json.loads(js.read_text(encoding="utf-8"))
        except Exception:
            continue
        walk_json(data, str(js), hits)

    if hits:
        print("FAIL intended-glyph sweep")
        for h in hits:
            print(f" - {h}")
        return 1
    print("PASS intended-glyph sweep")
    return 0


if __name__ == "__main__":
    sys.exit(main())
