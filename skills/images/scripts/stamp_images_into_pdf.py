#!/usr/bin/env python3
"""Insert full-bleed 16-9 stills into an existing letter PDF.

Manifest JSON
{
  "source_pdf": "path.pdf",
  "output_pdf": "path-out.pdf",
  "items": [
    {
      "kind": "banner" | "figure",
      "path": "banners/banner-01.png",
      "after_page": 2,
      "heading": "I. Introduction",
      "href": "https://digitalmarketingco.org/r/?src=images-banner&section=intro"
    }
  ]
}

after_page is 1-indexed. The still is inserted as a new page immediately
after that page so the heading stays with its prior text and the plate
opens the following spread. x = 0, full page width, height from 16-9.
"""
from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as rl_canvas


PAGE_W, PAGE_H = letter


def still_page(png: Path, href: str = "") -> bytes:
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=letter)
    # 16-9 of letter width
    h = PAGE_W * 9 / 16
    y = PAGE_H - h
    c.drawImage(
        str(png),
        0,
        y,
        width=PAGE_W,
        height=h,
        mask="auto",
        preserveAspectRatio=True,
        anchor="n",
    )
    if href:
        c.linkURL(href, (0, y, PAGE_W, PAGE_H), relative=0)
    c.showPage()
    c.save()
    return buf.getvalue()


def stamp(manifest_path: Path) -> Path:
    spec = json.loads(manifest_path.read_text(encoding="utf-8"))
    src = Path(spec["source_pdf"]).expanduser().resolve()
    out = Path(spec["output_pdf"]).expanduser().resolve()
    items = spec.get("items") or []
    if not src.is_file():
        raise FileNotFoundError(src)
    reader = PdfReader(str(src))
    n = len(reader.pages)
    by_after: dict[int, list[dict]] = {}
    for item in items:
        page = int(item["after_page"])
        if page < 1 or page > n:
            raise ValueError(f"after_page {page} out of range 1..{n}")
        png = Path(item["path"]).expanduser()
        if not png.is_absolute():
            png = (manifest_path.parent / png).resolve()
        if not png.is_file():
            raise FileNotFoundError(png)
        by_after.setdefault(page, []).append({**item, "_png": png})

    writer = PdfWriter()
    for i, page in enumerate(reader.pages, start=1):
        writer.add_page(page)
        for item in by_after.get(i, []):
            raw = still_page(item["_png"], item.get("href") or "")
            plate = PdfReader(io.BytesIO(raw))
            writer.add_page(plate.pages[0])
    if reader.metadata:
        writer.add_metadata({k: v for k, v in reader.metadata.items() if v})
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as fh:
        writer.write(fh)
    print(out)
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("manifest")
    args = p.parse_args()
    stamp(Path(args.manifest))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"stamp_images_into_pdf: {exc}", file=sys.stderr)
        sys.exit(1)
