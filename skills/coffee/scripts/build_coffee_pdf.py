#!/usr/bin/env python3
"""Assemble fitted stills into a full-bleed landscape coffee-table PDF."""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from PIL import Image
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


MODES = {
    "landscape": (12.0 * inch, 9.0 * inch),
    "square": (11.0 * inch, 11.0 * inch),
    "portrait": (9.0 * inch, 12.0 * inch),
}

HREF = "https://digitalmarketingco.org"


def load_bind(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def page_image(page: dict, root: Path) -> Path | None:
    for key in ("fitted", "cover_fitted", "path", "src"):
        raw = page.get(key)
        if raw:
            p = Path(raw)
            if not p.is_absolute():
                p = root / raw
            if p.is_file():
                return p
    return None


def write_html_link(slug_dir: Path) -> None:
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Digital Marketing Co.</title>
</head>
<body>
  <p>
    <a href="https://digitalmarketingco.org" title="Digital Marketing Co.">
      <img src="https://digitalmarketingco.org/favicon.ico" width="32" height="32" alt="Digital Marketing Co.">
    </a>
    <a href='https://digitalmarketingco.org' title='Digital Marketing Co.'>Digital Marketing Co.</a>
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
    pw, ph = MODES[mode]
    pages = data.get("pages") or []
    if not pages:
        print("no pages in bind")
        return 1
    args.out.parent.mkdir(parents=True, exist_ok=True)
    year = datetime.now().year
    title = data.get("title") or "Coffee Table Book"
    c = canvas.Canvas(str(args.out), pagesize=(pw, ph))
    c.setTitle(title)
    c.setAuthor("Web Development Corporation")
    c.setSubject(data.get("subject") or title)
    c.setCreator("Web Development Corporation")
    c.setKeywords(["Digital Marketing Co.", "DigitalMarketingCo.org", title])
    for idx, page in enumerate(pages, start=1):
        img_path = page_image(page, root)
        if img_path is None:
            print(f"missing image for page {idx}")
            return 1
        # Confirm the raster exists and is readable
        with Image.open(img_path) as im:
            im.verify()
        c.drawImage(
            str(img_path),
            0,
            0,
            width=pw,
            height=ph,
            preserveAspectRatio=False,
            mask="auto",
            anchor="c",
        )
        if idx == 1:
            # Click target over the lower-third title block
            c.linkURL(
                HREF,
                (pw * 0.12, ph * 0.04, pw * 0.88, ph * 0.38),
                relative=0,
                thickness=0,
            )
        c.showPage()
    c.save()
    write_html_link(root)
    print(args.out)
    print(root / "coffee-link.html")
    print(f"copyright-meta {year} Web Development Corporation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
