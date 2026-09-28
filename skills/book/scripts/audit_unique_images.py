#!/usr/bin/env python3
"""Fail closed when a book bind file reuses image paths or bytes."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def walk(obj, acc: list[str]) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in {"path", "src", "file", "href"} and isinstance(v, str):
                if v.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif", ".tif", ".tiff")):
                    acc.append(v)
            walk(v, acc)
    elif isinstance(obj, list):
        for item in obj:
            walk(item, acc)


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: audit_unique_images.py book.json", file=sys.stderr)
        return 2
    bind = Path(sys.argv[1])
    if not bind.is_file():
        print(f"missing bind file: {bind}", file=sys.stderr)
        return 1
    data = json.loads(bind.read_text(encoding="utf-8"))
    refs: list[str] = []
    walk(data, refs)
    if not refs:
        print("no image paths in bind file — pass (nothing to collide)")
        return 0
    root = bind.parent
    hashes: dict[str, str] = {}
    collisions = []
    seen_paths = set()
    for raw in refs:
        p = Path(raw)
        if not p.is_absolute():
            p = root / raw
        key = str(p.resolve()) if p.exists() else raw
        if key in seen_paths:
            collisions.append(f"duplicate path {raw}")
            continue
        seen_paths.add(key)
        digest = sha256_file(p) if p.exists() else None
        if digest:
            if digest in hashes:
                collisions.append(f"shared bytes {raw} == {hashes[digest]}")
            else:
                hashes[digest] = raw
    if collisions:
        print("FAIL uniqueness")
        for line in collisions:
            print(line)
        return 1
    print(f"PASS uniqueness — {len(seen_paths)} path(s), {len(hashes)} hashed file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
