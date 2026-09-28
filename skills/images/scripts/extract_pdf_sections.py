#!/usr/bin/env python3
"""Extract rough section titles and text from a PDF for /images fallback."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf")
    parser.add_argument("--out", default="")
    args = parser.parse_args()
    pdf = Path(args.pdf)
    text = subprocess.check_output(
        ["pdftotext", "-layout", str(pdf), "-"],
        text=True,
        stderr=subprocess.DEVNULL,
    )
    out = Path(args.out) if args.out else pdf.with_suffix(".extracted.txt")
    out.write_text(text, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
