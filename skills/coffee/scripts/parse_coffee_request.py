#!/usr/bin/env python3
"""Parse `/coffee SUBJECT … N` into subject, page budget, and a slug.

Page budget is the iteration ceiling, not a small default. A named count
is honored up to that ceiling. A rerun against an existing coffee.json
adds another ceiling of pages instead of replacing the book.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


# One skill run can return this many new full-bleed stills. Do not plan fewer
# unless the user named a smaller count. A later run adds this many again.
ITERATION_MAX = 24

PAGE_WORDS = re.compile(r"\b(pages?|pgs?|leaves|leafs|spreads?)\b", re.IGNORECASE)
INT_TOKEN = re.compile(r"\b(\d{1,3})\b")
MODE_WORDS = re.compile(r"\b(square|portrait|landscape)\b", re.IGNORECASE)
MORE_WORDS = re.compile(r"\b(more|again|append|add|continue|another)\b", re.IGNORECASE)


def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return (s[:60] or "coffee_table").rstrip("_")


def _take_count(text: str) -> tuple[str, int | None]:
    """Return (subject text, named count or None).

    A number is a page count only when it sits next to page/pages, or when
    it is the final token. Interior numbers stay in the subject (Route 66).
    """
    named = None
    # "8 pages" / "pages 8"
    pair = re.search(
        r"\b(\d{1,3})\s*(pages?|pgs?|leaves|spreads?)\b|\b(pages?|pgs?|leaves|spreads?)\s*(\d{1,3})\b",
        text,
        re.IGNORECASE,
    )
    if pair:
        raw = pair.group(1) or pair.group(4)
        named = int(raw)
        text = (text[: pair.start()] + " " + text[pair.end() :]).strip()
    else:
        stripped = text.strip()
        end = re.search(r"(\d{1,3})\s*$", stripped)
        if end:
            named = int(end.group(1))
            text = stripped[: end.start()].strip()
    text = PAGE_WORDS.sub(" ", text)
    text = MORE_WORDS.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip(" -–,")
    return text, named


def parse_request(raw: str, existing: dict | None = None) -> dict:
    text = raw.strip()
    text = re.sub(r"^/coffee\b", "", text, flags=re.IGNORECASE).strip()
    mode = "landscape"
    mode_hit = MODE_WORDS.search(text)
    if mode_hit:
        mode = mode_hit.group(1).lower()
        text = (text[: mode_hit.start()] + " " + text[mode_hit.end() :]).strip()
    subject, named = _take_count(text)
    if not subject and existing:
        subject = str(existing.get("subject") or "")
        mode = existing.get("mode") or mode
    have = 0
    append = False
    if existing and existing.get("pages"):
        same = slugify(subject) == slugify(str(existing.get("subject") or subject))
        if same or not subject:
            append = True
            have = len(existing.get("pages") or [])
            subject = subject or str(existing.get("subject") or "")
            mode = existing.get("mode") or mode
    if named is None:
        add = ITERATION_MAX
    else:
        add = max(1, min(named, ITERATION_MAX))
    # First run with no number fills the ceiling. A named count on a rerun
    # is an add, not a replacement total.
    page_count = have + add if append else add
    remainder = 0
    if named is not None and named > ITERATION_MAX:
        remainder = named - ITERATION_MAX
    return {
        "subject": subject,
        "page_count": page_count,
        "pages_this_iteration": add,
        "existing_pages": have,
        "append": append,
        "remainder_for_later_runs": remainder,
        "iteration_max": ITERATION_MAX,
        "mode": mode,
        "slug": slugify(subject or "coffee_table"),
        "ok": bool(subject),
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("text", nargs="?", default="")
    p.add_argument("--out", type=Path)
    p.add_argument("--existing", type=Path, help="coffee.json from an earlier run")
    args = p.parse_args()
    raw = args.text or sys.stdin.read()
    existing = None
    if args.existing and args.existing.is_file():
        existing = json.loads(args.existing.read_text(encoding="utf-8"))
    data = parse_request(raw, existing)
    blob = json.dumps(data, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(blob + "\n", encoding="utf-8")
    print(blob)
    return 0 if data["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
