#!/usr/bin/env python3
"""Composite an elegant readable title onto a fitted cover still.

Type sits on a lower-third veil. The still still touches every trim edge.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "assets" / "fonts"
CREAM = (244, 235, 208, 255)
GILT = (212, 175, 106, 255)
VEIL = (8, 6, 4)
LIB_BOLD = "/usr/share/fonts/truetype/liberation2/LiberationSerif-Bold.ttf"
LIB_ITAL = "/usr/share/fonts/truetype/liberation2/LiberationSerif-Italic.ttf"


def load_face(path: Path, px: int, weight: int | None = None) -> ImageFont.FreeTypeFont | None:
    if not path.is_file():
        return None
    try:
        font = ImageFont.truetype(str(path), size=px)
    except OSError:
        return None
    if weight and hasattr(font, "set_variation_by_axes"):
        try:
            font.set_variation_by_axes([weight])
        except OSError:
            pass
    return font


def title_font(px: int) -> ImageFont.FreeTypeFont:
    return (
        load_face(FONTS / "Cinzel-Variable.ttf", px, 700)
        or load_face(FONTS / "PlayfairDisplay-Variable.ttf", px, 700)
        or load_face(Path(LIB_BOLD), px)
        or ImageFont.load_default()
    )


def sub_font(px: int) -> ImageFont.FreeTypeFont:
    return (
        load_face(FONTS / "CormorantGaramond-Italic-Variable.ttf", px, 500)
        or load_face(Path(LIB_ITAL), px)
        or ImageFont.load_default()
    )


def wrap(draw: ImageDraw.ImageDraw, text: str, font, max_w: int, limit: int = 3) -> list[str]:
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    cur = words[0]
    for word in words[1:]:
        trial = f"{cur} {word}"
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines[:limit]


def add_veil(base: Image.Image) -> Image.Image:
    w, h = base.size
    veil = Image.new("L", (1, h), 0)
    start = int(h * 0.58)
    pix = veil.load()
    for y in range(start, h):
        t = (y - start) / max(1, (h - 1) - start)
        pix[0, y] = int(168 * (t ** 1.2))
    veil = veil.resize((w, h), Image.Resampling.BILINEAR)
    tint = Image.new("RGB", (w, h), VEIL)
    return Image.composite(tint, base.convert("RGB"), veil)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("src", type=Path)
    p.add_argument("out", type=Path)
    p.add_argument("--title", required=True)
    p.add_argument("--subtitle", default="")
    p.add_argument("--owner", default="Digital Marketing Company")
    args = p.parse_args()
    if not args.src.is_file():
        print(f"missing source: {args.src}")
        return 1
    with Image.open(args.src) as im:
        cover = add_veil(im.convert("RGB"))
    w, h = cover.size
    draw = ImageDraw.Draw(cover)
    max_w = int(w * 0.84)
    t_size = max(48, int(h * 0.055))
    tf = title_font(t_size)
    lines = wrap(draw, args.title.strip(), tf, max_w)
    while len(lines) > 2 and t_size > 36:
        t_size -= 4
        tf = title_font(t_size)
        lines = wrap(draw, args.title.strip(), tf, max_w)
    s_size = max(28, int(h * 0.028))
    sf = sub_font(s_size)
    of = sub_font(max(22, int(h * 0.022)))
    block_h = len(lines) * int(t_size * 1.15)
    if args.subtitle:
        block_h += int(h * 0.05) + int(s_size * 1.3)
    block_h += int(h * 0.04)
    y = h - int(h * 0.08) - block_h
    for line in lines:
        tw = draw.textlength(line, font=tf)
        x = (w - tw) / 2
        draw.text((x, y), line, font=tf, fill=CREAM)
        y += int(t_size * 1.12)
    rule_w = int(w * 0.22)
    rule_y = y + int(h * 0.012)
    x0 = (w - rule_w) // 2
    draw.rectangle((x0, rule_y, x0 + rule_w, rule_y + max(2, h // 900)), fill=GILT)
    y = rule_y + int(h * 0.02)
    if args.subtitle:
        for line in wrap(draw, args.subtitle.strip(), sf, max_w, 2):
            tw = draw.textlength(line, font=sf)
            draw.text(((w - tw) / 2, y), line, font=sf, fill=CREAM)
            y += int(s_size * 1.2)
    if args.owner:
        tw = draw.textlength(args.owner, font=of)
        draw.text(((w - tw) / 2, y + int(h * 0.008)), args.owner, font=of, fill=CREAM)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    cover.save(args.out, format="PNG", optimize=True)
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
