#!/usr/bin/env python3
"""Build a Computer Modern (Latin Modern Roman) PDF from article.json.

Images are unique, full-bleed left-to-right at page width, aspect-preserved,
LANCZOS-upscaled when the source bitmap is narrower than print resolution,
and emitted in the same reading-order slot they occupied in the source.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from publication_notice import notice_for

from PIL import Image as PILImage
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable,
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from image_util import is_duplicate, upscale_to_width  # noqa: E402

INK = HexColor("#111111")
MUTED = HexColor("#444444")
RULE = HexColor("#222222")

# Print raster target: letter width at 150 dpi.
PAGE_W, PAGE_H = letter
TARGET_PX = int(round(PAGE_W / 72.0 * 150))
MAX_BLEED_H = PAGE_H - 0.95 * inch


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def register_cm_fonts() -> None:
    font_dir = skill_root() / "assets" / "fonts"
    pdfmetrics.registerFont(TTFont("CM", str(font_dir / "lmroman10-regular.ttf")))
    pdfmetrics.registerFont(TTFont("CM-Bold", str(font_dir / "lmroman10-bold.ttf")))
    pdfmetrics.registerFont(TTFont("CM-Italic", str(font_dir / "lmroman10-italic.ttf")))
    pdfmetrics.registerFont(TTFont("CM-BoldItalic", str(font_dir / "lmroman10-bolditalic.ttf")))
    pdfmetrics.registerFontFamily(
        "CM",
        normal="CM",
        bold="CM-Bold",
        italic="CM-Italic",
        boldItalic="CM-BoldItalic",
    )


EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002700-\U000027BF"
    "\U0001F000-\U0001F2FF"
    "\ufe0f"
    "]+"
)


def escape(text: str) -> str:
    text = EMOJI_RE.sub("", text)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return text.strip()


class FullBleedImage(Flowable):
    """Paint an image at 100% page width. Origin at the left paper edge. No side pad."""

    def __init__(self, path: str, left_margin: float, page_w: float = PAGE_W):
        super().__init__()
        self.path = path
        self.left_margin = left_margin
        self.page_w = page_w
        im = PILImage.open(path)
        w, h = im.size
        if w <= 0 or h <= 0:
            raise ValueError(f"bad image size {path}")
        self.draw_w = page_w
        self.draw_h = page_w * (h / w)
        # Cap to the text frame so platypus can place the plate on a page.
        frame_h = 620  # stay inside Later/first frames after title+rule
        if self.draw_h > frame_h:
            # Height-clip the bitmap from the top (keep the face on portraits)
            # while remaining 100 percent page width.
            keep_h = max(1, int(round(w * (frame_h / page_w))))
            im = im.crop((0, 0, w, min(h, keep_h)))
            crop_path = Path(path)
            clipped = crop_path.with_name(crop_path.stem + "_clip" + crop_path.suffix)
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGB")
            im.save(clipped)
            self.path = str(clipped)
            w, h = im.size
            self.draw_h = page_w * (h / w)

    def wrap(self, availWidth, availHeight):
        return (availWidth, self.draw_h)

    def draw(self):
        canv = self.canv
        x = -self.left_margin
        canv.drawImage(
            self.path,
            x,
            0,
            width=self.draw_w,
            height=self.draw_h,
            preserveAspectRatio=True,
            anchor="c",
            mask="auto",
        )


def styles() -> dict[str, ParagraphStyle]:
    return {
        "title": ParagraphStyle(
            "TitleCM",
            fontName="CM-Bold",
            fontSize=18,
            leading=22,
            alignment=TA_LEFT,
            textColor=INK,
            spaceAfter=8,
        ),
        "meta": ParagraphStyle(
            "MetaCM",
            fontName="CM-Italic",
            fontSize=10,
            leading=13,
            alignment=TA_LEFT,
            textColor=MUTED,
            spaceAfter=10,
        ),
        "heading": ParagraphStyle(
            "HeadCM",
            fontName="CM-Bold",
            fontSize=13,
            leading=17,
            alignment=TA_LEFT,
            textColor=INK,
            spaceBefore=12,
            spaceAfter=7,
        ),
        "body": ParagraphStyle(
            "BodyCM",
            fontName="CM",
            fontSize=11.5,
            leading=16.5,
            alignment=TA_JUSTIFY,
            textColor=INK,
            spaceAfter=10,
        ),
        "caption": ParagraphStyle(
            "CapCM",
            fontName="CM-Italic",
            fontSize=9,
            leading=12,
            alignment=TA_LEFT,
            textColor=MUTED,
            spaceBefore=5,
            spaceAfter=12,
        ),
        "src": ParagraphStyle(
            "SrcCM",
            fontName="CM",
            fontSize=8.5,
            leading=11,
            alignment=TA_LEFT,
            textColor=MUTED,
            spaceBefore=14,
        ),
    }


def slug(title: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_")
    return (s[:72] or "article") + ".pdf"


def unique_images(images: list[dict]) -> list[dict]:
    seen_hash: set[str] = set()
    seen_phash: set[str] = set()
    out = []
    for im in images:
        path = Path(im.get("file") or "")
        if not path.exists():
            continue
        if is_duplicate(path, seen_hash, seen_phash):
            continue
        out.append(im)
    return out


def bleed_block(im: dict, st: dict, left_margin: float) -> list:
    path = Path(im["file"])
    prepared = upscale_to_width(path, TARGET_PX)
    items: list = [FullBleedImage(str(prepared), left_margin=left_margin)]
    cap = (im.get("caption") or "").strip()
    if cap:
        items.append(Paragraph(escape(cap), st["caption"]))
    else:
        items.append(Spacer(1, 8))
    return items


def blocks_from_legacy(data: dict) -> list[dict]:
    """When article.json has no blocks, attach each unique image to its caption slot."""
    paras = list(data.get("paragraphs") or [])
    images = unique_images(list(data.get("images") or []))
    used = set()
    blocks: list[dict] = []

    def match_image(text: str) -> dict | None:
        t = (text or "").lower()
        if len(t) < 12:
            return None
        for i, im in enumerate(images):
            if i in used:
                continue
            cap = (im.get("caption") or "").lower()
            alt = (im.get("alt") or "").lower()
            if cap and (cap[:80] in t or t[:80] in cap):
                return i, im
            if alt and alt[:80] in t:
                return i, im
        return None

    for para in paras:
        hit = match_image(para)
        if hit:
            i, im = hit
            # caption-only paragraph: emit image instead of repeating the caption as body
            cap = (im.get("caption") or "").strip()
            if cap and para.strip() == cap:
                blocks.append({"type": "image", **im})
                used.add(i)
                continue
            blocks.append({"type": "para", "text": para})
            blocks.append({"type": "image", **im})
            used.add(i)
        else:
            blocks.append({"type": "para", "text": para})

    # leftover unique images keep list order after the last matched slot
    for i, im in enumerate(images):
        if i not in used:
            blocks.append({"type": "image", **im})
    return blocks


def build(article_json: Path, out_pdf: Path | None) -> Path:
    register_cm_fonts()
    data = json.loads(article_json.read_text(encoding="utf-8"))
    if out_pdf is None:
        out_pdf = article_json.parent / slug(data.get("title") or "article")

    st = styles()
    left = 0.85 * inch
    right = 0.85 * inch
    doc = SimpleDocTemplate(
        str(out_pdf),
        pagesize=letter,
        leftMargin=left,
        rightMargin=right,
        topMargin=0.7 * inch,
        bottomMargin=0.72 * inch,
        title=data.get("title") or "",
        author=data.get("author") or "",
        subject=data.get("url") or "",
    )
    story = []

    story.append(Paragraph(escape(data.get("title") or "Untitled"), st["title"]))

    meta_bits = []
    if data.get("author"):
        meta_bits.append(f"By {escape(data['author'])}")
    if data.get("date"):
        meta_bits.append(escape(str(data["date"])[:16]))
    if meta_bits:
        story.append(Paragraph(" &nbsp;&middot;&nbsp; ".join(meta_bits), st["meta"]))

    story.append(
        HRFlowable(width="100%", thickness=0.6, color=RULE, spaceBefore=0, spaceAfter=12)
    )

    raw_blocks = data.get("blocks")
    if raw_blocks:
        # Dedupe image blocks by file identity even if the source repeated a plate.
        blocks = []
        seen_hash: set[str] = set()
        seen_phash: set[str] = set()
        for b in raw_blocks:
            if b.get("type") != "image":
                blocks.append(b)
                continue
            path = Path(b.get("file") or "")
            if not path.exists() or is_duplicate(path, seen_hash, seen_phash):
                continue
            blocks.append(b)
    else:
        blocks = blocks_from_legacy(data)

    for b in blocks:
        kind = b.get("type")
        if kind == "image":
            story.extend(bleed_block(b, st, left))
        elif kind == "heading":
            story.append(Paragraph(escape(b.get("text") or ""), st["heading"]))
        else:
            text = (b.get("text") or "").strip()
            if text:
                story.append(Paragraph(escape(text), st["body"]))

    source = data.get("url") or ""
    if source:
        host = re.sub(r"^https?://(www\.)?", "", source).rstrip("/")
        story.append(Paragraph(escape(f"Source: {host}"), st["src"]))

    footer_label = data.get("source_name") or "Article"

    def footer(canvas, doc_):
        canvas.saveState()
        canvas.setFont("CM", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(left, 0.48 * inch, footer_label[:48])
        canvas.drawRightString(PAGE_W - right, 0.48 * inch, str(doc_.page))
        canvas.setFont("CM", 7)
        canvas.drawCentredString(
            PAGE_W / 2.0,
            0.32 * inch,
            notice_for(data),
        )
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Wrote {out_pdf}")
    return out_pdf


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("article_json")
    ap.add_argument("--out", default=None, help="Output PDF path")
    args = ap.parse_args()
    build(Path(args.article_json), Path(args.out) if args.out else None)


if __name__ == "__main__":
    main()
