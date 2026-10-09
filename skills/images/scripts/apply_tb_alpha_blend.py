#!/usr/bin/env python3
"""Top and bottom alpha only. Left and right stay opaque picture.

Does not squash to 16:9. Width is raised to the page floor with repeated
Lanczos passes. Height follows the source aspect ratio.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None
FLOOR_W = 2550


def cosine_ramp(t: float) -> float:
    t = min(1.0, max(0.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def upscale_to_width(im: Image.Image, target_w: int) -> Image.Image:
    w, h = im.size
    if w >= target_w:
        return im
    while w < target_w:
        step = min(2.0, target_w / float(w))
        nw = max(w + 1, int(round(w * step)))
        nh = max(1, int(round(h * (nw / float(w)))))
        im = im.resize((nw, nh), Image.Resampling.LANCZOS)
        w, h = im.size
    return im


def apply_tb_blend(src: Path, dest: Path, frac: float = 0.08, target_w: int = FLOOR_W) -> None:
    im = Image.open(src).convert("RGBA")
    im = upscale_to_width(im, target_w)
    w, h = im.size
    pix = im.load()
    band = max(8, int(h * frac))
    for y in range(h):
        if y < band:
            a_scale = cosine_ramp(y / band)
        elif y >= h - band:
            a_scale = cosine_ramp((h - 1 - y) / band)
        else:
            a_scale = 1.0
        if a_scale >= 0.999:
            continue
        for x in range(w):
            r, g, b, a = pix[x, y]
            pix[x, y] = (r, g, b, int(round(a * a_scale)))
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "PNG")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("dest")
    p.add_argument("--frac", type=float, default=0.08)
    p.add_argument("--width", type=int, default=FLOOR_W)
    args = p.parse_args()
    apply_tb_blend(Path(args.src), Path(args.dest), args.frac, args.width)
    return 0


if __name__ == "__main__":
    sys.exit(main())
