#!/usr/bin/env python3
"""Append new leaf records to an existing coffee.json. Never drop old pages."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("bind", type=Path)
    p.add_argument("--add", type=Path, required=True, help="JSON list of {scene, prompt}")
    args = p.parse_args()
    data = json.loads(args.bind.read_text(encoding="utf-8"))
    incoming = json.loads(args.add.read_text(encoding="utf-8"))
    if isinstance(incoming, dict):
        incoming = incoming.get("pages") or []
    pages = list(data.get("pages") or [])
    seen = {(pg.get("prompt") or "").strip() for pg in pages}
    start = len(pages)
    added = 0
    for item in incoming:
        prompt = (item.get("prompt") or "").strip()
        if not prompt or prompt in seen:
            continue
        start += 1
        pages.append(
            {
                "n": start,
                "role": "leaf",
                "scene": item.get("scene") or "",
                "prompt": prompt,
                "fitted": item.get("fitted") or "",
            }
        )
        seen.add(prompt)
        added += 1
    data["pages"] = pages
    data["page_count"] = len(pages)
    data["iteration"] = int(data.get("iteration") or 1) + 1
    args.bind.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"added {added} total {len(pages)}")
    return 0 if added else 1


if __name__ == "__main__":
    raise SystemExit(main())
