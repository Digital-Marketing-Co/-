#!/usr/bin/env python3
"""Fail closed when a coffee bind file reuses image paths or bytes."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


KEYS = {"path", "src", "file", "fitted", "cover_fitted", "raw"}


def walk(obj, acc: list[str]) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in KEYS and isinstance(v, str):
                if v.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff")):
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
        print("usage: audit_unique_images.py coffee.json", file=sys.stderr)
        return 2
    bind = Path(sys.argv[1])
    if not bind.is_file():
        print(f"missing bind file: {bind}", file=sys.stderr)
        return 1
    data = json.loads(bind.read_text(encoding="utf-8"))
    refs: list[str] = []
    walk(data, refs)
    fitted_only = [
        r
        for r in refs
        if "raw-" not in Path(r).name
    ]
    check = fitted_only or refs
    if not check:
        print("no image paths in bind file — fail")
        return 1
    root = bind.parent
    collisions = []
    seen_paths: set[str] = set()
    hashes: dict[str, str] = {}
    missing = []
    for raw in check:
        p = Path(raw)
        if not p.is_absolute():
            p = root / raw
        key = str(p.resolve()) if p.exists() else raw
        if key in seen_paths:
            collisions.append(f"duplicate path {raw}")
            continue
        seen_paths.add(key)
        digest = sha256_file(p) if p.exists() else None
        if digest is None:
            missing.append(raw)
            continue
        if digest in hashes:
            collisions.append(f"duplicate bytes {raw} == {hashes[digest]}")
        else:
            hashes[digest] = raw
    qa = bind.parent / "stills"
    qa.mkdir(parents=True, exist_ok=True)
    lines = ["# coffee uniqueness", ""]
    for digest, raw in hashes.items():
        lines.append(f"- {digest[:12]}  {raw}")
    lines.append("")
    if missing:
        lines.append("MISSING")
        lines.extend(f"- {m}" for m in missing)
    if collisions:
        lines.append("FAIL")
        lines.extend(f"- {c}" for c in collisions)
        (qa / "qa.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("\n".join(collisions))
        return 1
    if missing:
        (qa / "qa.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("missing files")
        return 1
    lines.append("PASS")
    (qa / "qa.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
