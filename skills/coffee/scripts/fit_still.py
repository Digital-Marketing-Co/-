#!/usr/bin/env python3
"""Cover-crop a generate to the locked coffee-table pixel size.

No letterbox, no pillarbox, no paper band. Alpha is flattened onto the
image itself before the crop so a transparent edge cannot become a margin.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageFilter


MODES = {
    "landscape": (3600, 2700),
    "square": (3300, 3300),
    "portrait": (2700, 3600),
}


def flatten(im: Image.Image) -> Image.Image:
    if im.mode == "RGB":
        return im
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        rgba = im.convert("RGBA")
        # Sample a corner of opaque pixels so a transparent rim does not
        # composite onto white paper.
        bg_color = (18, 16, 14)
        px = rgba.getpixel((rgba.size[0] // 2, rgba.size[1] // 2))
        if isinstance(px, tuple) and len(px) >= 3 and px[-1] > 200:
            bg_color = px[:3]
        bg = Image.new("RGB", rgba.size, bg_color)
        bg.paste(rgba, mask=rgba.split()[-1])
        return bg
    return im.convert("RGB")


def cover_crop(im: Image.Image, tw: int, th: int) -> Image.Image:
    src = flatten(im)
    sw, sh = src.size
    if sw < 1 or sh < 1:
        raise ValueError("empty source")
    scale = max(tw / sw, th / sh)
    nw = max(tw, int(round(sw * scale)))
    nh = max(th, int(round(sh * scale)))
    resized = src.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, (nw - tw) // 2)
    top = max(0, (nh - th) // 2)
    fitted = resized.crop((left, top, left + tw, top + th))
    if fitted.size != (tw, th):
        fitted = fitted.resize((tw, th), Image.Resampling.LANCZOS)
    if scale > 1.01:
        fitted = fitted.filter(ImageFilter.UnsharpMask(radius=1.1, percent=70, threshold=3))
    return fitted


def paper_bar(im: Image.Image) -> bool:
    """True when an edge strip is a near-uniform light margin."""
    w, h = im.size
    strips = [
        im.crop((0, 0, w, 10)),
        im.crop((0, h - 10, w, h)),
        im.crop((0, 0, 10, h)),
        im.crop((w - 10, 0, w, h)),
    ]
    for strip in strips:
        gray = list(strip.convert("L").resize((24, 6)).tobytes())
        mean = sum(gray) / len(gray)
        var = sum((p - mean) ** 2 for p in gray) / len(gray)
        if mean > 228 and var < 30:
            return True
    return False


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
    if paper_bar(fitted):
        print(f"paper bar on edge: {args.src}")
        return 1
    args.dst.parent.mkdir(parents=True, exist_ok=True)
    fitted.save(args.dst, format="PNG", optimize=True)
    print(f"{args.dst} {fitted.size[0]}x{fitted.size[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
