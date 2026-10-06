#!/usr/bin/env python3
"""Create /home/workdir/artifacts/transcribe-<slug>/ and lock a source copy."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--slug", required=True)
    p.add_argument("--source", required=True)
    args = p.parse_args()

    root = Path("/home/workdir/artifacts") / f"transcribe-{args.slug}"
    root.mkdir(parents=True, exist_ok=True)
    src = Path(args.source)
    if not src.is_file():
        raise SystemExit(f"source not found: {src}")

    dest = root / f"source{src.suffix.lower()}"
    if not dest.exists():
        shutil.copy2(src, dest)

    skeleton = {
        "slug": args.slug,
        "source": {"path": str(dest), "kind": "raster"},
        "raw": {"path": str(root / "raw.txt"), "lock_path": str(root / "raw.lock.txt"), "sha256": ""},
        "devices": [],
        "passes": {
            "summary": str(root / "summary.md"),
            "expand_1": str(root / "expand-1.md"),
            "expand_2": str(root / "expand-2.md"),
        },
        "stack": {"folio": None, "book": None, "ran": False},
    }
    out = root / "transcript.json"
    if not out.exists():
        out.write_text(json.dumps(skeleton, indent=2) + "\n", encoding="utf-8")
    print(root)


if __name__ == "__main__":
    main()
