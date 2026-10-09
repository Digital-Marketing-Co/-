#!/usr/bin/env python3
"""Fit a raster to page-width trim without changing its aspect ratio.

Repeat Lanczos upscale until width meets the floor. Never squash, never
letterbox the sides, never downscale. Left and right stay picture, not matte.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

FLOOR_W = 2550
PREFER_W = 3300


def upscale_to_width(im: Image.Image, target_w: int) -> Image.Image:
    w, h = im.size
    if w <= 0 or h <= 0:
        raise ValueError("empty raster")
    if w >= target_w:
        return im
    while w < target_w:
        step = min(2.0, target_w / w)
        nw = max(w + 1, int(round(w * step)))
        nh = max(1, int(round(h * (nw / float(w)))))
        im = im.resize((nw, nh), Image.Resampling.LANCZOS)
        w, h = im.size
    return im


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def fit_file(src: Path, dest: Path, target_w: int) -> tuple[int, int]:
    im = Image.open(src)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
    fitted = upscale_to_width(im, target_w)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fitted.save(dest)
    return fitted.size


def audit_dir(folder: Path) -> int:
    seen: dict[str, Path] = {}
    failed = 0
    for path in sorted(folder.rglob("*")):
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        digest = sha256(path)
        if digest in seen:
            print(f"DUPLICATE {path} == {seen[digest]}")
            failed += 1
        else:
            seen[digest] = path
    return failed


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("dest")
    p.add_argument("--width", type=int, default=PREFER_W)
    p.add_argument("--audit-dir", default="")
    args = p.parse_args()
    size = fit_file(Path(args.src), Path(args.dest), args.width)
    print(f"{args.dest} {size[0]}x{size[1]}")
    if args.audit_dir:
        code = audit_dir(Path(args.audit_dir))
        if code:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
