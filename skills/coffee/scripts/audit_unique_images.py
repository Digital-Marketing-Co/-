#!/usr/bin/env python3
"""Fail closed when two coffee pages share a path, a hash, or a prompt."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


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
    pages = data.get("pages") or []
    root = bind.parent
    collisions: list[str] = []
    missing: list[str] = []
    seen_paths: set[str] = set()
    hashes: dict[str, str] = {}
    prompts: dict[str, int] = {}
    lines = ["# coffee uniqueness", ""]
    if not pages:
        print("no pages — fail")
        return 1
    for i, page in enumerate(pages, start=1):
        prompt = (page.get("prompt") or "").strip()
        if prompt:
            if prompt in prompts:
                collisions.append(f"duplicate prompt page {i} == page {prompts[prompt]}")
            else:
                prompts[prompt] = i
        raw = page.get("fitted") or page.get("cover_fitted")
        if not raw:
            missing.append(f"page {i} has no fitted still")
            continue
        p = Path(raw)
        if not p.is_absolute():
            p = root / raw
        key = str(p.resolve()) if p.exists() else raw
        if key in seen_paths:
            collisions.append(f"duplicate path {raw}")
            continue
        seen_paths.add(key)
        digest = sha256_file(p)
        if digest is None:
            missing.append(raw)
            continue
        if digest in hashes:
            collisions.append(f"duplicate bytes {raw} == {hashes[digest]}")
        else:
            hashes[digest] = raw
            lines.append(f"- {digest[:12]}  {raw}")
    qa = bind.parent / "stills"
    qa.mkdir(parents=True, exist_ok=True)
    lines.append("")
    if missing:
        lines.append("MISSING")
        lines.extend(f"- {m}" for m in missing)
    if collisions:
        lines.append("FAIL")
        lines.extend(f"- {c}" for c in collisions)
        (qa / "qa.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("\n".join(collisions + missing))
        return 1
    if missing:
        (qa / "qa.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("missing files")
        return 1
    lines.append("PASS")
    lines.append(f"pages {len(pages)}")
    (qa / "qa.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("PASS")
    print(f"pages {len(pages)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
