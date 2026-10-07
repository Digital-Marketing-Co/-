#!/usr/bin/env python3
"""Fail closed when a document reuses path, bytes, or a near-duplicate still."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def average_hash(path: Path, size: int = 16) -> int | None:
    if Image is None:
        return None
    with Image.open(path) as im:
        rgb = im.convert("RGB").resize((size, size), Image.Resampling.LANCZOS)
        pixels = list(rgb.getdata())
        mean = sum(p[0] * 0.299 + p[1] * 0.587 + p[2] * 0.114 for p in pixels) / len(pixels)
        bits = 0
        for i, p in enumerate(pixels):
            y = p[0] * 0.299 + p[1] * 0.587 + p[2] * 0.114
            if y >= mean:
                bits |= 1 << i
        return bits


def hamming(a: int, b: int) -> int:
    return (a ^ b).bit_count()


def collect(data: dict) -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []
    for sec in data.get("sections") or []:
        sid = str(sec.get("id") or sec.get("title") or "")
        banner = sec.get("banner") or {}
        if banner.get("path"):
            rows.append((sid, "banner", str(banner["path"]), str(banner.get("prompt") or "")))
        fig = sec.get("figure") or {}
        if fig.get("path"):
            rows.append((sid, "figure", str(fig["path"]), str(fig.get("prompt") or "")))
        for para in sec.get("paragraphs") or []:
            if isinstance(para, dict) and para.get("path"):
                kind = str(para.get("type") or "figure")
                if kind in {"figure", "image", "banner"}:
                    rows.append((sid, kind, str(para["path"]), str(para.get("prompt") or "")))
            if isinstance(para, dict):
                for key in ("figures", "images"):
                    for item in para.get(key) or []:
                        if isinstance(item, dict) and item.get("path"):
                            rows.append(
                                (
                                    sid,
                                    str(item.get("type") or "figure"),
                                    str(item["path"]),
                                    str(item.get("prompt") or ""),
                                )
                            )
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("json_path")
    ap.add_argument("--min-hamming", type=int, default=10)
    args = ap.parse_args()
    json_path = Path(args.json_path).resolve()
    data = json.loads(json_path.read_text(encoding="utf-8"))
    root = json_path.parent
    rows = collect(data)
    by_path: dict[str, list[str]] = defaultdict(list)
    by_hash: dict[str, list[str]] = defaultdict(list)
    by_prompt: dict[str, list[str]] = defaultdict(list)
    hashes: list[tuple[str, int | None, str]] = []
    missing: list[str] = []
    for sid, kind, raw, prompt in rows:
        label = f"{sid}:{kind}:{raw}"
        by_path[raw].append(label)
        if prompt.strip():
            by_prompt[prompt.strip()].append(label)
        path = Path(raw)
        if not path.is_absolute():
            path = root / raw
        if not path.exists():
            missing.append(label)
            continue
        digest = sha256(path)
        by_hash[digest].append(label)
        hashes.append((label, average_hash(path), digest))
    hits: list[str] = []
    for raw, users in by_path.items():
        if len(users) > 1:
            hits.append(f"shared path {raw} -> {users}")
    for digest, users in by_hash.items():
        if len(users) > 1:
            hits.append(f"shared bytes {digest[:16]} -> {users}")
    for prompt, users in by_prompt.items():
        if len(users) > 1:
            hits.append(f"shared prompt -> {users}")
    for i, (la, ha, _) in enumerate(hashes):
        if ha is None:
            continue
        for lb, hb, _ in hashes[i + 1 :]:
            if hb is None:
                continue
            dist = hamming(ha, hb)
            if dist <= args.min_hamming:
                hits.append(f"near-duplicate aHash d={dist} {la} ~ {lb}")
    for m in missing:
        hits.append(f"missing {m}")
    report = root / "figures" / "qa-uniqueness.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Uniqueness audit", ""]
    if hits:
        lines.append("FAIL")
        lines.extend(f"- {h}" for h in hits)
    else:
        lines.append(
            f"PASS {len(rows)} rasters, {len(by_hash)} unique SHA-256, prompts={len(by_prompt)}"
        )
        for digest, users in sorted(by_hash.items()):
            lines.append(f"- {digest[:16]} {users[0]}")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(report.read_text(), end="")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
