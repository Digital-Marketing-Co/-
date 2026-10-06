#!/usr/bin/env python3
"""Fail closed if raw.txt diverges from raw.lock.txt or is missing."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: qa_transcript.py <workdir>")
    root = Path(sys.argv[1])
    raw = root / "raw.txt"
    lock = root / "raw.lock.txt"
    missing = [p.name for p in (raw, lock) if not p.is_file()]
    if missing:
        raise SystemExit("missing " + ", ".join(missing))
    a, b = sha256(raw), sha256(lock)
    if a != b:
        raise SystemExit("raw.txt does not match raw.lock.txt — restore the lock, do not rewrite it")
    print(a)


if __name__ == "__main__":
    main()
