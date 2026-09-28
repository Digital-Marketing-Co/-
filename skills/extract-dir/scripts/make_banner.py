#!/usr/bin/env python3
"""Compose a geometric house banner from a title. No baked checkerboard."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from PIL import Image, ImageDraw


def hue_rgb(h: float, s: float = 0.45, v: float = 0.22) -> tuple[int, int, int]:
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i = i % 6
    r, g, b = [
        (v, t, p),
        (q, v, p),
        (p, v, t),
        (p, q, v),
        (t, p, v),
        (v, p, q),
    ][i]
    return int(r * 255), int(g * 255), int(b * 255)


def compose(title: str, dest: Path) -> None:
    digest = hashlib.sha256(title.encode("utf-8")).digest()
    h1 = digest[0] / 255.0
    h2 = digest[1] / 255.0
    w, h = 1275, 653  # 8.5 x 4.35 in at 150 dpi
    im = Image.new("RGB", (w, h), hue_rgb(h1, 0.35, 0.10))
    dr = ImageDraw.Draw(im)
    c1 = hue_rgb(h1, 0.55, 0.38)
    c2 = hue_rgb((h1 + 0.18) % 1.0, 0.40, 0.55)
    c3 = hue_rgb(h2, 0.20, 0.78)
    # Perspective-like planes — objects only, no caption text.
    dr.polygon([(0, h * 0.62), (w, h * 0.38), (w, h), (0, h)], fill=c1)
    dr.polygon([(int(w * 0.12), h), (int(w * 0.48), int(h * 0.22)), (int(w * 0.52), int(h * 0.22)), (int(w * 0.88), h)], fill=c2)
    for i in range(9):
        x = int(w * (0.08 + i * 0.10))
        dr.line([(x, int(h * 0.18)), (x + int(w * 0.18), h)], fill=c3, width=2)
    dr.ellipse([int(w * 0.72), int(h * 0.08), int(w * 0.92), int(h * 0.30)], outline=c3, width=3)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "PNG")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    compose(args.title, Path(args.out))
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
