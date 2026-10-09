#!/usr/bin/env python3
"""Build a full-bleed snippet PDF. No header, nav, sidebar, or footer.

Each manifest page is one PDF page. The page box equals the image, so the
bitmap touches the top, right, bottom, and left trim. Images are never
cropped. A plate marked keep=false is refused.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image
from reportlab.pdfgen import canvas


PAGE_WIDTH_PT = 8.5 * 72.0


def build(manifest_path: Path, out_path: Path) -> dict:
    manifest = json.loads(manifest_path.read_text())
    pages = manifest.get("pages") or []
    if not pages:
        raise SystemExit("manifest has no pages")
    root = manifest_path.parent
    out_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(out_path))
    drawn = 0
    for page in pages:
        if page.get("keep") is False:
            raise SystemExit("refusing a page that would end on a heading: %s" % page.get("text"))
        img_path = root / page["file"]
        if not img_path.exists():
            raise SystemExit("missing snippet: %s" % img_path)
        with Image.open(img_path) as im:
            w, h = im.size
        if w < 2 or h < 2:
            raise SystemExit("empty snippet: %s" % img_path)
        page_h = PAGE_WIDTH_PT * (h / float(w))
        c.setPageSize((PAGE_WIDTH_PT, page_h))
        c.drawImage(
            str(img_path),
            0,
            0,
            width=PAGE_WIDTH_PT,
            height=page_h,
            preserveAspectRatio=True,
            anchor="sw",
            mask="auto",
        )
        c.showPage()
        drawn += 1
    c.save()
    return {"pages": drawn, "out": str(out_path), "title": manifest.get("title") or ""}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    info = build(Path(args.manifest), Path(args.out))
    print(json.dumps(info))


if __name__ == "__main__":
    main()
