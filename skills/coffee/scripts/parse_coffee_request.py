#!/usr/bin/env python3
"""Parse `/coffee SUBJECT … N` into subject, page_count, and a slug."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


PAGE_WORDS = re.compile(
    r"\b(pages?|pgs?|leaves|leafs|spreads?)\b",
    re.IGNORECASE,
)
INT_TOKEN = re.compile(r"\b(\d{1,2})\b")
MODE_WORDS = re.compile(r"\b(square|portrait|landscape)\b", re.IGNORECASE)


def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return (s[:60] or "coffee_table").rstrip("_")


def parse_request(raw: str) -> dict:
    text = raw.strip()
    text = re.sub(r"^/coffee\b", "", text, flags=re.IGNORECASE).strip()
    mode = "landscape"
    mode_hit = MODE_WORDS.search(text)
    if mode_hit:
        mode = mode_hit.group(1).lower()
        text = (text[: mode_hit.start()] + text[mode_hit.end() :]).strip()
    page_count = 12
    ints = list(INT_TOKEN.finditer(text))
    if ints:
        last = ints[-1]
        value = int(last.group(1))
        if 2 <= value <= 40:
            page_count = value
            text = (text[: last.start()] + text[last.end() :]).strip()
    text = PAGE_WORDS.sub(" ", text)
    text = re.sub(r"[,\s]+$", "", text)
    text = re.sub(r"\s+", " ", text).strip(" -–,")
    subject = text.strip()
    return {
        "subject": subject,
        "page_count": page_count,
        "mode": mode,
        "slug": slugify(subject or "coffee_table"),
        "ok": bool(subject),
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("text", nargs="?", default="")
    p.add_argument("--out", type=Path)
    args = p.parse_args()
    raw = args.text or sys.stdin.read()
    data = parse_request(raw)
    blob = json.dumps(data, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(blob + "\n", encoding="utf-8")
    print(blob)
    return 0 if data["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
