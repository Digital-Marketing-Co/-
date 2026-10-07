#!/usr/bin/env python3
"""Run the /negative skill across a document that /latex is about to deliver."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

SWEEP = Path("/root/.grok/server-skills/negative/scripts/sweep_negative.py")
REWRITE = Path("/root/.grok/server-skills/negative/scripts/rewrite_negative.py")


def extract(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        r = subprocess.run(
            ["pdftotext", "-layout", str(path), "-"],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            return path.read_text(encoding="utf-8", errors="replace")
        return r.stdout
    return path.read_text(encoding="utf-8", errors="replace")


def sweep_text(label: str, text: str) -> int:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as fh:
        fh.write(text)
        tmp = fh.name
    r = subprocess.run([sys.executable, str(SWEEP), tmp], capture_output=True, text=True)
    Path(tmp).unlink(missing_ok=True)
    if r.returncode == 0:
        print(f"{label}: CLEAN")
        return 0
    print(f"{label}: FAIL")
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    return 1


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("paths", nargs="+", help="PDF, JSON, Markdown, or extracted text about to ship")
    p.add_argument("--rewrite", action="store_true", help="Apply default swaps on non-PDF text files in place, then re-sweep")
    args = p.parse_args()
    if not SWEEP.is_file():
        print("negative sweep missing", file=sys.stderr)
        return 1
    failed = 0
    for raw in args.paths:
        path = Path(raw)
        if not path.is_file():
            print(f"{path}: missing", file=sys.stderr)
            failed = 1
            continue
        if args.rewrite and path.suffix.lower() != ".pdf":
            subprocess.run([sys.executable, str(REWRITE), str(path), "--in-place"], check=False)
        failed |= sweep_text(str(path), extract(path))
    if failed:
        print("negative gate: FAIL — rewrite hits to atlas, gazette, or plate when a noun must stay, then re-scan")
        return 1
    print("negative gate: CLEAN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
