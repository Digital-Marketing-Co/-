#!/usr/bin/env python3
"""Build a letter-size /print PDF from print.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

from publication_notice import notice_for

from PIL import Image as PILImage
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Flowable,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
)

SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT / "assets"))
import typography as T  # noqa: E402

sys.path.insert(0, str(SKILL_ROOT / "scripts"))
from prepare_image import prepare  # noqa: E402

INK = HexColor(T.INK)
MUTED = HexColor(T.MUTED)
RULE = HexColor(T.RULE)
CREAM = HexColor(T.CREAM)
LINK_C = HexColor(T.LINK)

OPEN_JS = (
    "var y = (new Date()).getFullYear();"
    "try {"
    " var f = this.getField('WCACopyrightYear');"
    " if (f) f.value = String(y);"
    "} catch (e) {}"
)

EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002700-\U000027BF"
    "\U0001F000-\U0001F2FF"
    "\ufe0f"
    "]+"
)


def register_fonts() -> None:
    font_dir = T.FONT_DIR
    pdfmetrics.registerFont(TTFont(T.DISPLAY, str(font_dir / "EBGaramond-Regular.ttf")))
    pdfmetrics.registerFont(TTFont(T.DISPLAY_BOLD, str(font_dir / "EBGaramond-Bold.ttf")))
    pdfmetrics.registerFont(TTFont(T.DISPLAY_ITALIC, str(font_dir / "EBGaramond-Italic.ttf")))
    pdfmetrics.registerFont(TTFont(T.DISPLAY_BOLDITALIC, str(font_dir / "EBGaramond-BoldItalic.ttf")))
    pdfmetrics.registerFontFamily(
        T.DISPLAY,
        normal=T.DISPLAY,
        bold=T.DISPLAY_BOLD,
        italic=T.DISPLAY_ITALIC,
        boldItalic=T.DISPLAY_BOLDITALIC,
    )
    pdfmetrics.registerFont(TTFont(T.BODY, str(font_dir / "Literata_18pt-Regular.ttf")))
    pdfmetrics.registerFont(TTFont(T.BODY_BOLD, str(font_dir / "Literata_18pt-Bold.ttf")))
    pdfmetrics.registerFont(TTFont(T.BODY_ITALIC, str(font_dir / "Literata_18pt-Italic.ttf")))
    pdfmetrics.registerFont(TTFont(T.BODY_BOLDITALIC, str(font_dir / "Literata_18pt-BoldItalic.ttf")))
    pdfmetrics.registerFontFamily(
        T.BODY,
        normal=T.BODY,
        bold=T.BODY_BOLD,
        italic=T.BODY_ITALIC,
        boldItalic=T.BODY_BOLDITALIC,
    )
    pdfmetrics.registerFont(TTFont(T.CHROME, str(font_dir / "LibreFranklin-Regular.ttf")))
    pdfmetrics.registerFont(TTFont(T.CHROME_BOLD, str(font_dir / "LibreFranklin-Bold.ttf")))
    pdfmetrics.registerFont(TTFont(T.CHROME_ITALIC, str(font_dir / "LibreFranklin-Italic.ttf")))
    pdfmetrics.registerFont(TTFont(T.CHROME_BOLDITALIC, str(font_dir / "LibreFranklin-BoldItalic.ttf")))
    pdfmetrics.registerFontFamily(
        T.CHROME,
        normal=T.CHROME,
        bold=T.CHROME_BOLD,
        italic=T.CHROME_ITALIC,
        boldItalic=T.CHROME_BOLDITALIC,
    )


def clean(text: str) -> str:
    text = EMOJI_RE.sub("", text or "")
    return text.replace("\u00a0", " ").strip()


def escape(text: str) -> str:
    text = clean(text)
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def slugify_title(title: str) -> str:
    stop = {"a", "an", "the", "and", "or", "of", "for", "to", "in", "on", "at", "by", "with", "from"}
    words = re.sub(r"[^a-z0-9]+", " ", (title or "print").lower()).split()
    keep = [w for w in words if w not in stop][:10]
    return "-".join(keep) or "print"


def print_filename(title: str, year: int) -> str:
    return f"{year}-{slugify_title(title)}-wca-print.pdf"


class BleedImage(Flowable):
    """Image drawn at page x=0. Banner also hugs the top trim when first on a page."""

    def __init__(self, path: str, page_w: float, height: float, kind: str = "figure"):
        super().__init__()
        self.path = path
        self.page_w = page_w
        self._h = height
        self.kind = kind

    def wrap(self, aw, ah):
        return self.page_w, self._h

    def draw(self):
        canv = self.canv
        x = canv.absolutePosition(0, 0)[0]
        # Shift so the plate starts at page x = 0 regardless of frame origin.
        canv.drawImage(
            self.path,
            -x,
            0,
            width=self.page_w,
            height=self._h,
            preserveAspectRatio=True,
            mask="auto",
            anchor="c",
        )


def styles() -> dict[str, ParagraphStyle]:
    inset = T.TEXT_INSET_IN * inch
    common = dict(textColor=INK, leading=T.BODY_LEADING)
    return {
        "kicker": ParagraphStyle(
            "kicker",
            fontName=T.CHROME,
            fontSize=T.KICKER_PT,
            leading=T.FOOTER_LEADING,
            textColor=MUTED,
            leftIndent=inset,
            rightIndent=inset,
            spaceAfter=6,
        ),
        "title": ParagraphStyle(
            "title",
            fontName=T.DISPLAY_BOLD,
            fontSize=T.TITLE_PT,
            leading=T.TITLE_LEADING,
            textColor=INK,
            leftIndent=inset,
            rightIndent=inset,
            spaceAfter=8,
        ),
        "byline": ParagraphStyle(
            "byline",
            fontName=T.BODY_ITALIC,
            fontSize=T.SUBTITLE_PT,
            leading=T.SUBTITLE_LEADING,
            textColor=MUTED,
            leftIndent=inset,
            rightIndent=inset,
            spaceAfter=14,
        ),
        "h2": ParagraphStyle(
            "h2",
            fontName=T.DISPLAY_BOLD,
            fontSize=T.H1_PT,
            leading=T.H1_LEADING,
            textColor=INK,
            leftIndent=inset,
            rightIndent=inset,
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "h3",
            fontName=T.DISPLAY_BOLD,
            fontSize=T.H2_PT,
            leading=T.H2_LEADING,
            textColor=INK,
            leftIndent=inset,
            rightIndent=inset,
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "body",
            fontName=T.BODY,
            fontSize=T.BODY_PT,
            leading=T.BODY_LEADING,
            textColor=INK,
            alignment=TA_JUSTIFY,
            leftIndent=inset,
            rightIndent=inset,
            spaceAfter=8,
        ),
        "quote": ParagraphStyle(
            "quote",
            fontName=T.BODY_ITALIC,
            fontSize=T.BODY_PT,
            leading=T.BODY_LEADING,
            textColor=MUTED,
            leftIndent=inset + 12,
            rightIndent=inset + 12,
            spaceAfter=10,
        ),
        "li": ParagraphStyle(
            "li",
            fontName=T.BODY,
            fontSize=T.BODY_PT,
            leading=T.BODY_LEADING,
            textColor=INK,
            leftIndent=inset + 14,
            rightIndent=inset,
            bulletIndent=inset,
            spaceAfter=3,
        ),
        "caption": ParagraphStyle(
            "caption",
            fontName=T.CHROME_ITALIC,
            fontSize=T.CAPTION_PT,
            leading=T.CAPTION_LEADING,
            textColor=MUTED,
            leftIndent=inset,
            rightIndent=inset,
            spaceBefore=4,
            spaceAfter=10,
        ),
        "colophon": ParagraphStyle(
            "colophon",
            fontName=T.CHROME,
            fontSize=T.COPYRIGHT_PT,
            leading=T.FOOTER_LEADING,
            textColor=MUTED,
            leftIndent=inset,
            rightIndent=inset,
            alignment=TA_LEFT,
            spaceBefore=16,
        ),
    }


class PrintDoc(BaseDocTemplate):
    def __init__(self, out_path: str, meta: dict, year: int):
        self.meta = meta
        self.year = year
        super().__init__(
            out_path,
            pagesize=letter,
            leftMargin=0,
            rightMargin=0,
            topMargin=T.MARGIN_TOP_IN * inch,
            bottomMargin=T.MARGIN_BOTTOM_IN * inch,
            title=meta.get("title") or "Print",
            author=meta.get("author") or T.OWNER_SHORT,
            creator=T.OWNER_LEGAL,
        )
        frame = Frame(
            0,
            T.MARGIN_BOTTOM_IN * inch,
            letter[0],
            letter[1] - (T.MARGIN_TOP_IN + T.MARGIN_BOTTOM_IN) * inch,
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
            id="bleed",
        )
        self.addPageTemplates([PageTemplate(id="print", frames=[frame], onPage=self._on_page)])

    def _on_page(self, canvas: Canvas, doc) -> None:
        canvas.saveState()
        canvas.setFillColor(CREAM)
        canvas.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
        canvas.restoreState()
        self.handle_documentBegin = getattr(self, "handle_documentBegin", lambda: None)
        y = 0.42 * inch
        canvas.setFillColor(MUTED)
        canvas.setFont(T.CHROME, T.FOOTER_PT)
        canvas.drawString(T.TEXT_INSET_IN * inch, y, T.OWNER_SHORT)
        canvas.drawRightString(letter[0] - T.TEXT_INSET_IN * inch, y, str(doc.page))
        canvas.setFont(T.CHROME, 7)
        canvas.drawCentredString(letter[0] / 2, 0.22 * inch, notice_for(self.meta))


def fitted_height(path: Path, page_w: float, max_h: float) -> float:
    im = PILImage.open(path)
    w, h = im.size
    if w <= 0 or h <= 0:
        return max_h
    height = page_w * (h / float(w))
    return min(height, max_h)


def prepare_block_image(block: dict, work: Path) -> Path | None:
    raw = block.get("path") or ""
    if not raw:
        return None
    src = Path(raw)
    if not src.is_file():
        return None
    dest = work / "print-ready" / (src.stem + ".png")
    try:
        prepare(src, dest)
        return dest
    except Exception:
        return src


def build_story(data: dict, work: Path) -> list:
    s = styles()
    story: list = []
    page_w = letter[0]
    href = (data.get("house") or {}).get("href") or T.HOUSE_HREF
    anchor = (data.get("house") or {}).get("anchor") or T.HOUSE_ANCHOR

    site = escape(data.get("site") or "")
    kicker = site or T.HOUSE_DOMAIN
    story.append(Paragraph(kicker.upper(), s["kicker"]))
    story.append(Paragraph(escape(data.get("title") or "Untitled"), s["title"]))
    by = []
    if data.get("author"):
        by.append(escape(data["author"]))
    if data.get("date"):
        by.append(escape(data["date"][:10]))
    if by:
        story.append(Paragraph("  ·  ".join(by), s["byline"]))

    blocks = list(data.get("blocks") or [])
    i = 0
    while i < len(blocks):
        b = blocks[i]
        kind = b.get("type")
        if kind == "heading":
            level = int(b.get("level") or 2)
            style = s["h2"] if level <= 2 else s["h3"]
            heading = Paragraph(escape(b.get("text") or ""), style)
            following = None
            if i + 1 < len(blocks):
                following = flow_block(blocks[i + 1], s, page_w, work)
            story.append(CondPageBreak(T.HEADING_KEEP_IN * inch))
            if following is not None:
                packed = [heading]
                if isinstance(following, list):
                    packed.extend(following)
                else:
                    packed.append(following)
                story.append(KeepTogether(packed))
                i += 2
                continue
            story.append(KeepTogether([heading, Spacer(1, 8)]))
            i += 1
            continue
        piece = flow_block(b, s, page_w, work)
        if piece is None:
            i += 1
            continue
        if isinstance(piece, list):
            story.append(KeepTogether(piece))
        else:
            story.append(piece)
        i += 1

    year = date.today().year
    slug = data.get("slug") or slugify_title(data.get("title") or "print")
    record = f"{href.rstrip('/')}/print/{slug}"
    colo = (
        f'Reprint of {escape(data.get("source_url") or "")}. '
        f'Placeholder house backlink: <link href="{href}">{escape(anchor)}</link> '
        f'({escape(T.HOUSE_DOMAIN)}). Record path {escape(record)}.'
    )
    story.append(Paragraph(colo, s["colophon"]))
    return story


def flow_block(b: dict, s: dict, page_w: float, work: Path):
    kind = b.get("type")
    if kind == "paragraph":
        return Paragraph(escape(b.get("text") or ""), s["body"])
    if kind == "quote":
        return Paragraph(escape(b.get("text") or ""), s["quote"])
    if kind == "list_item":
        return Paragraph("•  " + escape(b.get("text") or ""), s["li"])
    if kind in {"banner", "figure"}:
        ready = prepare_block_image(b, work)
        if ready is None:
            return None
        max_h = (T.BANNER_HEIGHT_IN if kind == "banner" else T.FIGURE_MAX_HEIGHT_IN) * inch
        h = fitted_height(ready, page_w, max_h)
        plate = BleedImage(str(ready), page_w, h, kind=kind)
        group = [CondPageBreak(h + 24), plate]
        cap = clean(b.get("caption") or "")
        if cap:
            group.append(Paragraph(escape(cap), s["caption"]))
        else:
            group.append(Spacer(1, 8))
        return group
    if kind == "heading":
        level = int(b.get("level") or 2)
        style = s["h2"] if level <= 2 else s["h3"]
        return Paragraph(escape(b.get("text") or ""), style)
    return None


def finalize_pdf(pdf_path: Path, data: dict, year: int) -> None:
    try:
        from pypdf import PdfReader, PdfWriter
    except Exception:
        return
    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    try:
        writer.clone_from(reader)
    except Exception:
        writer.append(reader)
    root = writer.root_object
    href = (data.get("house") or {}).get("href") or T.HOUSE_HREF
    title = data.get("title") or "Print"
    try:
        writer.add_metadata(
            {
                "/Title": title,
                "/Author": data.get("author") or T.OWNER_SHORT,
                "/Creator": T.OWNER_LEGAL,
                "/Producer": T.OWNER_SHORT,
                "/Subject": f"Print reprint. Placeholder backlink {href}",
                "/Keywords": "print, WCA, DigitalMarketingCo.org",
                "/URL": href,
            }
        )
    except Exception:
        pass
    tmp = pdf_path.with_suffix(".tmp.pdf")
    with tmp.open("wb") as fh:
        writer.write(fh)
    tmp.replace(pdf_path)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("json_path")
    p.add_argument("--out")
    p.add_argument("--print-filename", action="store_true")
    args = p.parse_args()
    data = json.loads(Path(args.json_path).read_text(encoding="utf-8"))
    year = date.today().year
    fname = print_filename(data.get("title") or "print", year)
    if args.print_filename:
        print(fname)
        return
    if not args.out:
        raise SystemExit("--out is required unless --print-filename is set")
    register_fonts()
    work = Path(args.json_path).parent
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    doc = PrintDoc(str(out), data, year)
    story = build_story(data, work)
    doc.build(story)
    finalize_pdf(out, data, year)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
