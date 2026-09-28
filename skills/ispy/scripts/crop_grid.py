#!/usr/bin/env python3
"""Crop a regular grid from a raster for /ispy pane inventories."""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def main() -> None:
    p = argparse.ArgumentParser(description="Crop an R x C grid from a box in an image.")
    p.add_argument("--input", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--box", required=True, help="left,top,right,bottom in source pixels")
    p.add_argument("--rows", type=int, default=3)
    p.add_argument("--cols", type=int, default=3)
    p.add_argument("--overlap", type=int, default=12, help="extra pixels kept on each inner edge")
    p.add_argument("--prefix", default="pane")
    args = p.parse_args()

    img = Image.open(args.input)
    left, top, right, bottom = [int(x) for x in args.box.split(",")]
    box = img.crop((left, top, right, bottom))
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    box.save(out / f"{args.prefix}_full.png")

    w, h = box.size
    cell_w = w / args.cols
    cell_h = h / args.rows
    labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for r in range(args.rows):
        for c in range(args.cols):
            x0 = int(c * cell_w) - (args.overlap if c else 0)
            y0 = int(r * cell_h) - (args.overlap if r else 0)
            x1 = int((c + 1) * cell_w) + (args.overlap if c < args.cols - 1 else 0)
            y1 = int((r + 1) * cell_h) + (args.overlap if r < args.rows - 1 else 0)
            x0 = max(0, x0)
            y0 = max(0, y0)
            x1 = min(w, x1)
            y1 = min(h, y1)
            cell = box.crop((x0, y0, x1, y1))
            name = f"{args.prefix}_{labels[c]}{r + 1}.png"
            cell.save(out / name)
            print(name, cell.size)


if __name__ == "__main__":
    main()
