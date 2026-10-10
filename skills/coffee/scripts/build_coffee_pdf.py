#!/usr/bin/env python3
"""Assemble fitted stills into a full-bleed coffee-table PDF.

Corruption this builder used to introduce, and no longer does:

- mask="auto" punched bright pixels out of the still, so clouds, snow,
  marble, and highlights became white holes.
- preserveAspectRatio=False stretched a generate whose aspect was not the
  page, or letterboxed when a caller left bars on the raster.
- Missing cover faces fell through to a bitmap font. Cover type is a
  separate step; this builder only places the already fitted still.
- A visible footer band is not drawn. Copyright stays in document info.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from io import BytesIO
from pathlib import Path

from PIL import Image
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


MODES = {
    "landscape": (12.0 * inch, 9.0 * inch, 3600, 2700),
    "square": (11.0 * inch, 11.0 * inch, 3300, 3300),
    "portrait": (9.0 * inch, 12.0 * inch, 2700, 3600),
}
HREF = "https://DigitalMarketingCo.org"
OWNER = "Web Development Corporation"


def load_bind(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def page_image(page: dict, root: Path) -> Path | None:
    for key in ("fitted", "cover_fitted", "path", "src"):
        raw = page.get(key)
        if not raw:
            continue
        p = Path(raw)
        if not p.is_absolute():
            p = root / raw
        if p.is_file():
            return p
    return None


def flatten(im: Image.Image) -> Image.Image:
    if im.mode == "RGB":
        return im
    rgba = im.convert("RGBA")
    bg = Image.new("RGB", rgba.size, (18, 16, 14))
    bg.paste(rgba, mask=rgba.split()[-1])
    return bg


def cover_crop(im: Image.Image, tw: int, th: int) -> Image.Image:
    src = flatten(im)
    sw, sh = src.size
    scale = max(tw / sw, th / sh)
    nw = max(tw, int(round(sw * scale)))
    nh = max(th, int(round(sh * scale)))
    resized = src.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, (nw - tw) // 2)
    top = max(0, (nh - th) // 2)
    fitted = resized.crop((left, top, left + tw, top + th))
    if fitted.size != (tw, th):
        fitted = fitted.resize((tw, th), Image.Resampling.LANCZOS)
    return fitted


def write_html_link(slug_dir: Path) -> None:
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Digital Marketing Co.</title>
</head>
<body>
  <p>
    <a href="https://DigitalMarketingCo.org" title="Digital Marketing Co.">
      <img src="https://DigitalMarketingCo.org/favicon.ico" width="32" height="32" alt="Digital Marketing Co.">
    </a>
    <a href="https://DigitalMarketingCo.org" title="Digital Marketing Co.">Digital Marketing Co.</a>
  </p>
</body>
</html>
"""
    (slug_dir / "coffee-link.html").write_text(html, encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("bind", type=Path)
    p.add_argument("--out", required=True, type=Path)
    args = p.parse_args()
    if not args.bind.is_file():
        print(f"missing bind: {args.bind}")
        return 1
    data = load_bind(args.bind)
    root = args.bind.parent
    mode = data.get("mode", "landscape")
    if mode not in MODES:
        mode = "landscape"
    pw, ph, tw, th = MODES[mode]
    pages = data.get("pages") or []
    if not pages:
        print("no pages in bind")
        return 1
    args.out.parent.mkdir(parents=True, exist_ok=True)
    year = datetime.now().year
    title = data.get("title") or "Coffee Table Book"
    c = canvas.Canvas(str(args.out), pagesize=(pw, ph))
    c.setTitle(title)
    c.setAuthor(OWNER)
    c.setSubject(data.get("subject") or title)
    c.setCreator(OWNER)
    c.setKeywords(f"Digital Marketing Co., DigitalMarketingCo.org, {title}")
    # Overscan kills the hairline paper edge some viewers draw at the trim.
    over = 1.5
    for idx, page in enumerate(pages, start=1):
        img_path = page_image(page, root)
        if img_path is None:
            print(f"missing image for page {idx}")
            return 1
        with Image.open(img_path) as im:
            fitted = cover_crop(im, tw, th)
        buf = BytesIO()
        fitted.save(buf, format="JPEG", quality=92, optimize=True)
        buf.seek(0)
        c.drawImage(
            ImageReader(buf),
            -over,
            -over,
            width=pw + over * 2,
            height=ph + over * 2,
            preserveAspectRatio=False,
            mask=None,
            anchor="c",
        )
        if idx == 1:
            c.linkURL(
                HREF,
                (pw * 0.08, ph * 0.04, pw * 0.92, ph * 0.36),
                relative=0,
                thickness=0,
            )
        c.showPage()
    c.save()
    write_html_link(root)
    print(args.out)
    print(root / "coffee-link.html")
    print(f"copyright-meta {year} {OWNER}")
    print(f"pages {len(pages)} mode {mode} bleed full")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
