#!/usr/bin/env python3
"""Fail closed when a document reuses the same raster bytes or the same path."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path


def md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def collect(data: dict) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for sec in data.get("sections") or []:
        sid = str(sec.get("id") or sec.get("title") or "")
        banner = sec.get("banner") or {}
        if banner.get("path"):
            rows.append((sid, "banner", str(banner["path"])))
        for para in sec.get("paragraphs") or []:
            if isinstance(para, dict) and para.get("path"):
                kind = str(para.get("type") or "figure")
                if kind in {"figure", "image", "banner"}:
                    rows.append((sid, kind, str(para["path"])))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("json_path")
    args = ap.parse_args()
    json_path = Path(args.json_path).resolve()
    data = json.loads(json_path.read_text(encoding="utf-8"))
    root = json_path.parent
    rows = collect(data)
    by_path: dict[str, list[str]] = defaultdict(list)
    by_hash: dict[str, list[str]] = defaultdict(list)
    missing: list[str] = []
    for sid, kind, raw in rows:
        by_path[raw].append(f"{sid}:{kind}")
        path = Path(raw)
        if not path.is_absolute():
            path = root / raw
        if not path.exists():
            missing.append(f"{sid}:{kind}:{raw}")
            continue
        by_hash[md5(path)].append(f"{sid}:{kind}:{raw}")
    hits: list[str] = []
    for raw, users in by_path.items():
        if len(users) > 1:
            hits.append(f"shared path {raw} -> {users}")
    for digest, users in by_hash.items():
        if len(users) > 1:
            hits.append(f"shared bytes {digest[:12]} -> {users}")
    for m in missing:
        hits.append(f"missing {m}")
    report = root / "figures" / "qa-uniqueness.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Uniqueness audit", ""]
    if hits:
        lines.append("FAIL")
        lines.extend(f"- {h}" for h in hits)
    else:
        lines.append(f"PASS {len(rows)} rasters, {len(by_hash)} unique hashes")
        for digest, users in sorted(by_hash.items()):
            lines.append(f"- {digest[:12]} {users[0]}")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(report.read_text(), end="")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
