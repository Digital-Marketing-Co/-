#!/usr/bin/env python3
"""Scan text for /negative blocklist hits. Exit 1 if any remain."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIST = ROOT / "references" / "blocklist.md"


def terms_from_file() -> list[str]:
    out: list[str] = []
    if LIST.exists():
        in_skip = False
        for line in LIST.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.startswith("## Replacement") or s.startswith("## Do not"):
                in_skip = True
                continue
            if s.startswith("## "):
                in_skip = False
            if in_skip:
                continue
            if s.startswith("- "):
                t = s[2:].split("(")[0].strip().lower()
                t = t.split("\u2014")[0].strip()
                t = t.strip("`")
                if t and t not in {"x", "y"}:
                    out.append(t)
    uniq = sorted(set(out), key=lambda x: (-len(x), x))
    return uniq


def find_hits(text: str) -> list[tuple[int, str]]:
    hits: list[tuple[int, str]] = []
    seen: set[tuple[int, int]] = set()
    for term in terms_from_file():
        if not term:
            continue
        # Match complete phrases with flexible whitespace, not substrings in words.
        # Unicode alphanumerics bound tokens; compounds remain separate tokens.
        escaped = r"\s+".join(re.escape(part) for part in term.split())
        pat = re.compile(rf"(?<![^\W_]){escaped}(?![^\W_])", re.I)
        for m in pat.finditer(text):
            span = (m.start(), m.end())
            if span in seen:
                continue
            seen.add(span)
            hits.append((m.start(), m.group(0)))
    hits.sort()
    return hits


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("path", nargs="?", help="file to scan; stdin if omitted")
    p.add_argument("--count", action="store_true")
    args = p.parse_args()
    if args.count:
        print(len(terms_from_file()))
        return 0
    text = Path(args.path).read_text(encoding="utf-8") if args.path else sys.stdin.read()
    hits = find_hits(text)
    if not hits:
        print("CLEAN")
        return 0
    for pos, tok in hits:
        print(f"{pos}\t{tok}")
    print(f"HITS\t{len(hits)}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
