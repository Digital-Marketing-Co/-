#!/usr/bin/env python3
"""Cover-crop a generate to the locked coffee-table pixel size."""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageFilter


MODES = {
    "landscape": (3600, 2700),
    "square": (3300, 3300),
    "portrait": (2700, 3600),
}


def cover_crop(im: Image.Image, tw: int, th: int) -> Image.Image:
    src = im.convert("RGB")
    sw, sh = src.size
    if sw < 1 or sh < 1:
        raise ValueError("empty source")
    scale = max(tw / sw, th / sh)
    nw = max(1, int(round(sw * scale)))
    nh = max(1, int(round(sh * scale)))
    resized = src.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, (nw - tw) // 2)
    top = max(0, (nh - th) // 2)
    box = (left, top, left + tw, top + th)
    fitted = resized.crop(box)
    if scale > 1.01:
        fitted = fitted.filter(ImageFilter.UnsharpMask(radius=1.2, percent=80, threshold=3))
    return fitted


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("src", type=Path)
    p.add_argument("dst", type=Path)
    p.add_argument("--mode", default="landscape", choices=sorted(MODES))
    args = p.parse_args()
    if not args.src.is_file():
        print(f"missing source: {args.src}")
        return 1
    tw, th = MODES[args.mode]
    with Image.open(args.src) as im:
        fitted = cover_crop(im, tw, th)
    args.dst.parent.mkdir(parents=True, exist_ok=True)
    fitted.save(args.dst, format="PNG", optimize=True)
    print(f"{args.dst} {fitted.size[0]}x{fitted.size[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
