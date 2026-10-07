#!/usr/bin/env python3
"""Fail a PDF whose last content line is a heading with no paragraph under it."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

FOOTER = re.compile(
    r"copyright|all rights reserved|digital marketing|page\s+\d+\s*$|^\s*\d+\s*$",
    re.I,
)
SENTENCE_END = re.compile(r"[.!?…][\"'”’)]?\s*$")
HEADING_NUM = re.compile(
    r"^(?:chapter\s+\d+|(?:\d+\.){0,4}\d+)\s+\S",
    re.I,
)


def page_text(pdf: Path, n: int) -> str:
    r = subprocess.run(
        ["pdftotext", "-layout", "-f", str(n), "-l", str(n), str(pdf), "-"],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        return ""
    return r.stdout


def page_count(pdf: Path) -> int:
    r = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True)
    for line in r.stdout.splitlines():
        if line.lower().startswith("pages:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except ValueError:
                return 0
    return 0


def content_lines(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if FOOTER.search(line) and len(line) < 90:
            continue
        lines.append(line)
    return lines


def looks_like_heading(line: str) -> bool:
    if len(line) < 3 or len(line) > 88:
        return False
    if SENTENCE_END.search(line):
        return False
    if line.endswith((",", ";", ":")):
        return False
    words = line.split()
    if len(words) > 14:
        return False
    if HEADING_NUM.match(line):
        return True
    letters = [c for c in line if c.isalpha()]
    if not letters:
        return False
    upper = sum(1 for c in letters if c.isupper())
    if upper / len(letters) > 0.55:
        return True
    # Title case: most words start uppercase, no terminal period.
    caps = sum(1 for w in words if w[:1].isupper())
    return caps >= max(1, len(words) - 1)


def scan(pdf: Path) -> list[str]:
    hits: list[str] = []
    n_pages = page_count(pdf)
    if n_pages <= 0:
        return [f"{pdf}: pdfinfo failed"]
    for n in range(1, n_pages + 1):
        lines = content_lines(page_text(pdf, n))
        if not lines:
            continue
        last = lines[-1]
        if not looks_like_heading(last):
            continue
        # A heading is followed by paragraph text only if a non-heading line
        # sits under it on this page.
        body_after = False
        # last line is the heading; nothing after it on this page.
        hits.append(
            f"{pdf} p.{n}: orphan heading {last!r} is not followed by paragraph text; move it to the next page"
        )
        _ = body_after
    return hits


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--pdf", required=True)
    args = p.parse_args()
    hits = scan(Path(args.pdf))
    if not hits:
        print("scan_orphan_headings: clean")
        return 0
    print("scan_orphan_headings: FAIL")
    for h in hits:
        print(" -", h)
    return 1


if __name__ == "__main__":
    sys.exit(main())
