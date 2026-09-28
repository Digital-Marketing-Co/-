#!/usr/bin/env python3
"""Apply real alpha ramps on the top and bottom of a landscape banner.

Left and right columns stay opaque. No checkerboard is written into RGB.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

from PIL import Image


def cosine_ramp(t: float) -> float:
    # t in [0, 1] from transparent edge toward opaque interior
    t = min(1.0, max(0.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def apply_tb_blend(src: Path, dest: Path, frac: float = 0.08) -> None:
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    target_h = max(1, round(w * 9 / 16))
    if abs(h - target_h) > 2:
        im = im.resize((w, target_h), Image.Resampling.LANCZOS)
        h = target_h
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
    args = p.parse_args()
    apply_tb_blend(Path(args.src), Path(args.dest), args.frac)
    return 0


if __name__ == "__main__":
    sys.exit(main())
