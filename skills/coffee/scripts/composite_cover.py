#!/usr/bin/env python3
"""Composite an elegant readable title onto a fitted cover still."""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


CREAM = (244, 235, 208, 255)
GILT = (212, 175, 106, 255)
VEIL = (8, 6, 4)


def first_font(candidates: list[tuple[str, int]]) -> ImageFont.FreeTypeFont:
    for path, size in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def title_font(px: int) -> ImageFont.FreeTypeFont:
    return first_font(
        [
            ("/usr/share/fonts/SlidesCarnival/google/Cinzel/static/Cinzel-Bold.ttf", px),
            ("/usr/share/fonts/SlidesCarnival/google/Playfair Display/static/PlayfairDisplay-Bold.ttf", px),
            ("/usr/share/fonts/SlidesCarnival/google/Cinzel/static/Cinzel-SemiBold.ttf", px),
            ("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", px),
        ]
    )


def sub_font(px: int) -> ImageFont.FreeTypeFont:
    return first_font(
        [
            ("/usr/share/fonts/SlidesCarnival/google/Cormorant Garamond/static/CormorantGaramond-Italic.ttf", px),
            ("/usr/share/fonts/SlidesCarnival/google/EB Garamond/static/EBGaramond-Italic.ttf", px),
            ("/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf", px),
        ]
    )


def wrap(draw: ImageDraw.ImageDraw, text: str, font, max_w: int) -> list[str]:
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    cur = words[0]
    for w in words[1:]:
        trial = f"{cur} {w}"
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines[:2]


def add_veil(base: Image.Image) -> Image.Image:
    w, h = base.size
    veil = Image.new("L", (1, h), 0)
    start = int(h * 0.52)
    pix = veil.load()
    for y in range(start, h):
        t = (y - start) / max(1, (h - 1) - start)
        pix[0, y] = int(170 * (t**1.15))
    veil = veil.resize((w, h), Image.Resampling.BILINEAR)
    tint = Image.new("RGB", (w, h), VEIL)
    return Image.composite(tint, base.convert("RGB"), veil)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("src", type=Path)
    p.add_argument("--title", required=True)
    p.add_argument("--subtitle", default="")
    p.add_argument("--owner", default="")
    p.add_argument("--out", required=True, type=Path)
    args = p.parse_args()
    if not args.src.is_file():
        print(f"missing cover: {args.src}")
        return 1
    with Image.open(args.src) as im:
        cover = add_veil(im)
    w, h = cover.size
    draw = ImageDraw.Draw(cover)
    t_size = max(48, int(h * 0.072))
    s_size = max(22, int(h * 0.028))
    o_size = max(16, int(h * 0.018))
    tf = title_font(t_size)
    sf = sub_font(s_size)
    of = sub_font(o_size)
    max_w = int(w * 0.82)
    title = args.title.strip().upper()
    lines = wrap(draw, title, tf, max_w)
    # Measure block
    line_h = int(t_size * 1.12)
    block_h = line_h * len(lines)
    if args.subtitle:
        block_h += int(s_size * 1.8)
    if args.owner:
        block_h += int(o_size * 1.6)
    y = int(h * 0.78) - block_h // 2
    y = max(int(h * 0.58), min(y, h - block_h - int(h * 0.06)))
    for line in lines:
        tw = draw.textlength(line, font=tf)
        x = (w - tw) / 2
        draw.text((x + 2, y + 2), line, font=tf, fill=(0, 0, 0, 180))
        draw.text((x, y), line, font=tf, fill=CREAM)
        y += line_h
    rule_w = int(w * 0.28)
    rule_y = y + int(h * 0.012)
    x0 = (w - rule_w) // 2
    draw.rectangle((x0, rule_y, x0 + rule_w, rule_y + max(2, h // 900)), fill=GILT)
    y = rule_y + int(h * 0.022)
    if args.subtitle:
        slines = wrap(draw, args.subtitle.strip(), sf, max_w)
        for line in slines:
            tw = draw.textlength(line, font=sf)
            x = (w - tw) / 2
            draw.text((x, y), line, font=sf, fill=CREAM)
            y += int(s_size * 1.25)
    if args.owner:
        tw = draw.textlength(args.owner, font=of)
        x = (w - tw) / 2
        draw.text((x, y + int(h * 0.01)), args.owner, font=of, fill=CREAM)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    cover.save(args.out, format="PNG", optimize=True)
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
