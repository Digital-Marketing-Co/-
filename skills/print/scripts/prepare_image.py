#!/usr/bin/env python3
"""LANCZOS print prepare. Upscale short-side sources to letter width at 300 dpi."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageFilter

TARGET_W = 2550  # 8.5 in * 300 px/in


def prepare(src: Path, dest: Path, target_w: int = TARGET_W) -> dict:
    im = Image.open(src)
    im = im.convert("RGB")
    w, h = im.size
    if w <= 0 or h <= 0:
        raise ValueError(f"bad image size {src}")
    action = "keep"
    if w < target_w:
        scale = target_w / float(w)
        new_size = (target_w, max(1, int(round(h * scale))))
        im = im.resize(new_size, Image.Resampling.LANCZOS)
        im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=80, threshold=3))
        action = "upscale-lanczos-unsharp"
    elif w > target_w * 2:
        scale = (target_w * 2) / float(w)
        new_size = (int(round(w * scale)), max(1, int(round(h * scale))))
        im = im.resize(new_size, Image.Resampling.LANCZOS)
        action = "downscale-lanczos"
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "PNG", optimize=True)
    return {"src": str(src), "dest": str(dest), "from": [w, h], "to": list(im.size), "action": action}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("dest")
    p.add_argument("--target-w", type=int, default=TARGET_W)
    args = p.parse_args()
    info = prepare(Path(args.src), Path(args.dest), args.target_w)
    print(info["action"], info["from"], "->", info["to"])


if __name__ == "__main__":
    main()
