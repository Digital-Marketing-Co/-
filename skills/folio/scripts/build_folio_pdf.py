#!/usr/bin/env python3
"""Build a letter-size WCA Folio academic report PDF from folio.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    Image,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    Table,
    TableStyle,
)

SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT / "assets"))
import typography as T  # noqa: E402
import discoverability as D  # noqa: E402

INK = HexColor(T.INK)
MUTED = HexColor(T.MUTED)
RULE = HexColor(T.RULE)
RULE_SOFT = HexColor(T.RULE_SOFT)
CREAM = HexColor(T.CREAM)
LINK_C = HexColor(T.LINK)

NOTE_RUN = re.compile(r"\{\{\s*(\d+(?:\s*,\s*\d+)*)\s*\}\}")
ADJACENT_MARKS = re.compile(r"\}\}\s*\{\{")
NOTE_ONE = re.compile(r"\{\{(\d+(?:\s*,\s*\d+)*)\}\}")
EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002700-\U000027BF"
    "\U0001F000-\U0001F2FF"
    "\ufe0f"
    "]+"
)

OPEN_JS = (
    "var y = (new Date()).getFullYear();"
    "try {"
    " var f = this.getField('WCACopyrightYear');"
    " if (f) f.value = String(y);"
    "} catch (e) {}"
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


def allow_markup(text: str) -> str:
    text = clean(text)
    text = text.replace("&", "&amp;")
    holders: list[str] = []

    def stash(match: re.Match) -> str:
        holders.append(match.group(0))
        return f"@@TAG{len(holders) - 1}@@"

    pattern = re.compile(
        r"</?(?:i|em|b|sup|a)(?:\s+href=(?:\"[^\"]+\"|'[^']+'))?\s*>",
        re.I,
    )
    protected = pattern.sub(stash, text)
    protected = protected.replace("<", "&lt;").replace(">", "&gt;")
    for i, tag in enumerate(holders):
        t = tag
        t = re.sub(r"<a\s+href=", "<link href=", t, flags=re.I)
        t = re.sub(r"</a>", "</link>", t, flags=re.I)
        t = re.sub(r"<em\b", "<i", t, flags=re.I)
        t = re.sub(r"</em>", "</i>", t, flags=re.I)
        t = re.sub(r"<sup\b", "<super", t, flags=re.I)
        t = re.sub(r"</sup>", "</super>", t, flags=re.I)
        protected = protected.replace(f"@@TAG{i}@@", t)
    return protected


def extract_note_ns(text: str) -> list[int]:
    nums: list[int] = []
    for inner in NOTE_RUN.findall(text or ""):
        for part in inner.split(","):
            part = part.strip()
            if part.isdigit() and int(part) not in nums:
                nums.append(int(part))
    return nums


class CitedParagraph(Paragraph):
    def __init__(self, text, style: ParagraphStyle, cited: list[int] | None = None, **kwargs):
        super().__init__(text if text is not None else "", style, **kwargs)
        self.cited = list(cited or [])


def inject_notes(text: str) -> str:
    text = ADJACENT_MARKS.sub(", ", text)

    def repl(match: re.Match) -> str:
        nums = [n.strip() for n in match.group(1).split(",") if n.strip()]
        parts: list[str] = []
        last = len(nums) - 1
        for i, n in enumerate(nums):
            # Comma rides inside the superscript; a space follows every
            # number that is not last. No trailing comma on the last mark.
            inner = f"{n}," if i != last else n
            piece = f'<link href="#note-{n}"><super>{inner}</super></link>'
            if i != last:
                piece += " "
            parts.append(piece)
        return "".join(parts)

    return NOTE_RUN.sub(repl, allow_markup(text))


def make_styles() -> dict[str, ParagraphStyle]:
    return {
        "kicker": ParagraphStyle(
            "Kicker",
            fontName=T.CHROME,
            fontSize=T.KICKER_PT,
            leading=T.FOOTER_LEADING,
            alignment=TA_CENTER,
            textColor=MUTED,
            spaceAfter=14,
            tracking=1.4,
        ),
        "title": ParagraphStyle(
            "Title",
            fontName=T.DISPLAY,
            fontSize=T.TITLE_PT,
            leading=T.TITLE_LEADING,
            alignment=TA_CENTER,
            textColor=INK,
            spaceAfter=8,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            fontName=T.DISPLAY_ITALIC,
            fontSize=T.SUBTITLE_PT,
            leading=T.SUBTITLE_LEADING,
            alignment=TA_CENTER,
            textColor=INK,
            spaceAfter=18,
        ),
        "meta": ParagraphStyle(
            "Meta",
            fontName=T.BODY,
            fontSize=T.META_PT,
            leading=T.ABSTRACT_LEADING,
            alignment=TA_CENTER,
            textColor=INK,
            spaceAfter=3,
        ),
        "owner": ParagraphStyle(
            "Owner",
            fontName=T.CHROME,
            fontSize=T.KICKER_PT,
            leading=T.FOOTER_LEADING,
            alignment=TA_CENTER,
            textColor=MUTED,
            spaceBefore=8,
            spaceAfter=2,
        ),
        "h1": ParagraphStyle(
            "H1",
            fontName=T.DISPLAY,
            fontSize=T.H1_PT,
            leading=T.H1_LEADING,
            alignment=TA_LEFT,
            textColor=INK,
            spaceBefore=14,
            spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "H2",
            fontName=T.DISPLAY_ITALIC,
            fontSize=T.H2_PT,
            leading=T.H2_LEADING,
            alignment=TA_LEFT,
            textColor=INK,
            spaceBefore=10,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "Body",
            fontName=T.BODY,
            fontSize=T.BODY_PT,
            leading=T.BODY_LEADING,
            alignment=TA_JUSTIFY,
            textColor=INK,
            spaceAfter=6,
            firstLineIndent=12,
        ),
        "body_first": ParagraphStyle(
            "BodyFirst",
            fontName=T.BODY,
            fontSize=T.BODY_PT,
            leading=T.BODY_LEADING,
            alignment=TA_JUSTIFY,
            textColor=INK,
            spaceAfter=6,
            firstLineIndent=0,
        ),
        "abstract_label": ParagraphStyle(
            "AbsLabel",
            fontName=T.CHROME_BOLD,
            fontSize=T.KICKER_PT,
            leading=T.FOOTER_LEADING,
            alignment=TA_CENTER,
            textColor=INK,
            spaceBefore=16,
            spaceAfter=8,
            tracking=1.1,
        ),
        "abstract": ParagraphStyle(
            "Abstract",
            fontName=T.BODY_ITALIC,
            fontSize=T.ABSTRACT_PT,
            leading=T.ABSTRACT_LEADING,
            alignment=TA_JUSTIFY,
            textColor=INK,
            spaceAfter=8,
        ),
        "keywords": ParagraphStyle(
            "Keywords",
            fontName=T.BODY,
            fontSize=T.ABSTRACT_PT,
            leading=T.ABSTRACT_LEADING,
            alignment=TA_LEFT,
            textColor=INK,
            spaceBefore=6,
            spaceAfter=8,
        ),
        "fn": ParagraphStyle(
            "PageFootnote",
            fontName=T.BODY,
            fontSize=T.PAGE_FOOTNOTE_PT,
            leading=T.PAGE_FOOTNOTE_LEADING,
            alignment=TA_LEFT,
            textColor=INK,
            leftIndent=10,
            firstLineIndent=-10,
            spaceAfter=1,
        ),
        "caption": ParagraphStyle(
            "Caption",
            fontName=T.BODY_ITALIC,
            fontSize=T.CAPTION_PT,
            leading=T.CAPTION_LEADING,
            alignment=TA_LEFT,
            textColor=MUTED,
            spaceBefore=4,
            spaceAfter=12,
        ),
        "note": ParagraphStyle(
            "Note",
            fontName=T.BODY,
            fontSize=T.NOTE_PT,
            leading=T.NOTE_LEADING,
            alignment=TA_LEFT,
            textColor=INK,
            leftIndent=16,
            firstLineIndent=-16,
            spaceAfter=6,
        ),
        "bib": ParagraphStyle(
            "Bib",
            fontName=T.BODY,
            fontSize=T.BIBLIO_PT,
            leading=T.BIBLIO_LEADING,
            alignment=TA_LEFT,
            textColor=INK,
            leftIndent=18,
            firstLineIndent=-18,
            spaceAfter=7,
        ),
        "itqe_kicker": ParagraphStyle(
            "ITQEKicker",
            fontName=T.CHROME,
            fontSize=T.FOOTER_PT,
            leading=T.FOOTER_LEADING,
            alignment=TA_LEFT,
            textColor=MUTED,
            spaceBefore=2,
            spaceAfter=3,
        ),
        "itqe_head": ParagraphStyle(
            "ITQEHead",
            fontName=T.CHROME_BOLD,
            fontSize=T.NOTE_PT,
            leading=T.NOTE_LEADING,
            alignment=TA_LEFT,
            textColor=INK,
        ),
        "itqe_cell": ParagraphStyle(
            "ITQECell",
            fontName=T.BODY,
            fontSize=T.NOTE_PT,
            leading=T.NOTE_LEADING,
            alignment=TA_LEFT,
            textColor=INK,
        ),
        "colophon": ParagraphStyle(
            "Colophon",
            fontName=T.CHROME,
            fontSize=T.FOOTER_PT,
            leading=T.FOOTER_LEADING,
            alignment=TA_CENTER,
            textColor=MUTED,
            spaceBefore=3,
            spaceAfter=2,
        ),
    }


def fitted_image(path: Path, max_w: float, max_h: float) -> Image:
    im = PILImage.open(path)
    w, h = im.size
    if w <= 0 or h <= 0:
        raise ValueError(f"bad image size {path}")
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        bg = PILImage.new("RGB", im.size, (251, 247, 240))
        rgba = im.convert("RGBA")
        bg.paste(rgba, mask=rgba.split()[-1])
        flat = path.with_name(path.stem + "-flat.jpg")
        bg.save(flat, "JPEG", quality=90)
        path = flat
        w, h = bg.size
    scale = min(max_w / w, max_h / h)
    flow = Image(str(path), width=w * scale, height=h * scale)
    flow.hAlign = "CENTER"
    return flow


def biblio_text(entry) -> str:
    if isinstance(entry, dict):
        return entry.get("text") or ""
    return str(entry or "")


def flow_equation(eq: dict, styles: dict, source_dir: Path) -> list:
    """Plate + caption + ITQE table, kept together."""
    bits: list = []
    max_w = letter[0] - (T.MARGIN_LEFT_IN + T.MARGIN_RIGHT_IN) * inch
    plate = eq.get("plate") or eq.get("path") or ""
    plate_path = None
    if plate:
        cand = Path(plate)
        if not cand.is_file():
            cand = source_dir / plate
        if cand.is_file():
            plate_path = cand
    if plate_path is not None:
        bits.append(Spacer(1, 6))
        bits.append(fitted_image(plate_path, max_w, 2.4 * inch))
    elif eq.get("unicode"):
        bits.append(Paragraph(allow_markup(eq["unicode"]), styles["body"]))
    cap = eq.get("caption") or ""
    if cap:
        bits.append(CitedParagraph(inject_notes(cap), styles["caption"], cited=extract_note_ns(cap)))
    rows = eq.get("itqe") or []
    if rows:
        bits.append(Paragraph("ITQE", styles["itqe_kicker"]))
        header = [
            Paragraph("Identifier", styles["itqe_head"]),
            Paragraph("Term", styles["itqe_head"]),
            Paragraph("Quantity", styles["itqe_head"]),
            Paragraph("Explanation", styles["itqe_head"]),
        ]
        data_rows = [header]
        for row in rows:
            data_rows.append(
                [
                    Paragraph(allow_markup(str(row.get("identifier") or "")), styles["itqe_cell"]),
                    Paragraph(allow_markup(str(row.get("term") or "")), styles["itqe_cell"]),
                    Paragraph(allow_markup(str(row.get("quantity") or "")), styles["itqe_cell"]),
                    Paragraph(allow_markup(str(row.get("explanation") or "")), styles["itqe_cell"]),
                ]
            )
        col_w = [max_w * x for x in (0.16, 0.22, 0.18, 0.44)]
        table = Table(data_rows, colWidths=col_w, hAlign="LEFT")
        table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (-1, 0), T.CHROME_BOLD),
                    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#EFEAE2")),
                    ("TEXTCOLOR", (0, 0), (-1, -1), INK),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                    ("LINEBELOW", (0, 0), (-1, 0), 0.4, RULE),
                    ("LINEBELOW", (0, 1), (-1, -1), 0.2, RULE_SOFT),
                    ("BOX", (0, 0), (-1, -1), 0.3, RULE_SOFT),
                ]
            )
        )
        bits.append(table)
        bits.append(Spacer(1, 6))
        legend = eq.get("legend") or []
        if legend:
            bits.append(Paragraph("ITQE — glyphs", styles["itqe_kicker"]))
            ghead = [
                Paragraph("Glyph", styles["itqe_head"]),
                Paragraph("Name and case", styles["itqe_head"]),
                Paragraph("Role in this equation", styles["itqe_head"]),
                Paragraph("Operators on this figure", styles["itqe_head"]),
            ]
            grows = [ghead]
            for item in legend:
                if not isinstance(item, dict):
                    continue
                glyph = str(item.get("glyph") or "")
                name = str(item.get("name") or "")
                case = str(item.get("case") or "")
                if case and case.lower() not in name.lower():
                    name_case = f"{name} ({case})" if name else case
                else:
                    name_case = name or case
                role = str(item.get("role") or item.get("spoken") or "")
                ops = str(item.get("operators") or "none on this plate")
                grows.append(
                    [
                        Paragraph(allow_markup(glyph), styles["itqe_cell"]),
                        Paragraph(allow_markup(name_case), styles["itqe_cell"]),
                        Paragraph(allow_markup(role), styles["itqe_cell"]),
                        Paragraph(allow_markup(ops), styles["itqe_cell"]),
                    ]
                )
            gtable = Table(grows, colWidths=[max_w * x for x in (0.12, 0.22, 0.36, 0.30)], hAlign="LEFT")
            gtable.setStyle(
                TableStyle(
                    [
                        ("FONTNAME", (0, 0), (-1, 0), T.CHROME_BOLD),
                        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#EFEAE2")),
                        ("TEXTCOLOR", (0, 0), (-1, -1), INK),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 4),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                        ("TOPPADDING", (0, 0), (-1, -1), 3),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                        ("LINEBELOW", (0, 0), (-1, 0), 0.4, RULE),
                        ("LINEBELOW", (0, 1), (-1, -1), 0.2, RULE_SOFT),
                        ("BOX", (0, 0), (-1, -1), 0.3, RULE_SOFT),
                    ]
                )
            )
            bits.append(gtable)
            bits.append(Spacer(1, 8))
        else:
            bits.append(Spacer(1, 8))
    return [KeepTogether(bits)] if bits else []


class FolioDoc(BaseDocTemplate):
    def __init__(self, out_path: Path, meta: dict, year: int, notes_by_n: dict | None = None, **kwargs):
        super().__init__(str(out_path), **kwargs)
        self.meta = meta
        self.year = year
        self.notes_by_n = notes_by_n or {}
        self.notes_on_page: dict[int, list[int]] = {}
        self._copyright_field_drawn = False
        self._fn_style = make_styles()["fn"]
        ml = T.MARGIN_LEFT_IN * inch
        mr = T.MARGIN_RIGHT_IN * inch
        mt = T.MARGIN_TOP_IN * inch
        frame_bottom = (T.COPYRIGHT_BAND_IN + T.FOOTNOTE_BAND_IN) * inch
        frame = Frame(
            ml,
            frame_bottom,
            letter[0] - ml - mr,
            letter[1] - mt - frame_bottom,
            id="body",
        )
        cover_frame = Frame(
            ml,
            frame_bottom,
            letter[0] - ml - mr,
            letter[1] - mt - frame_bottom,
            id="cover",
        )
        self.addPageTemplates(
            [
                PageTemplate(
                    id="cover",
                    frames=[cover_frame],
                    onPage=self._draw_cover_page,
                    onPageEnd=self._draw_page_end,
                ),
                PageTemplate(
                    id="body",
                    frames=[frame],
                    onPage=self._draw_body_page,
                    onPageEnd=self._draw_page_end,
                ),
            ]
        )

    def afterFlowable(self, flowable) -> None:
        cited = getattr(flowable, "cited", None)
        if cited:
            bucket = self.notes_on_page.setdefault(int(self.page), [])
            for n in cited:
                if n not in bucket:
                    bucket.append(n)
        name = getattr(flowable, "_bookmarkName", None)
        if name:
            self.canv.bookmarkPage(name)
            self.canv.addOutlineEntry(str(flowable.getPlainText())[:80], name, level=0, closed=False)

    def _paint_page(self, canvas: Canvas) -> None:
        canvas.saveState()
        canvas.setFillColor(CREAM)
        canvas.rect(0, 0, letter[0], letter[1], stroke=0, fill=1)
        canvas.restoreState()

    def _draw_cover_page(self, canvas: Canvas, doc) -> None:
        self._paint_page(canvas)
        canvas.saveState()
        self._header_rule(canvas, running=False)
        self._footer(canvas, doc, page_number=False, live_year=True)
        self._attach_openaction_js(canvas)
        canvas.restoreState()

    def _draw_body_page(self, canvas: Canvas, doc) -> None:
        self._paint_page(canvas)
        canvas.saveState()
        self._header_rule(canvas, running=True)
        self._footer(canvas, doc, page_number=True, live_year=False)
        canvas.restoreState()

    def _draw_page_end(self, canvas: Canvas, doc) -> None:
        canvas.saveState()
        self._draw_page_footnotes(canvas, doc)
        canvas.restoreState()

    def _draw_page_footnotes(self, canvas: Canvas, doc) -> None:
        nums = self.notes_on_page.get(int(doc.page), [])
        if not nums:
            return
        nums = sorted(nums)
        ml = T.MARGIN_LEFT_IN * inch
        mr = T.MARGIN_RIGHT_IN * inch
        usable_w = letter[0] - ml - mr
        band_top = (T.COPYRIGHT_BAND_IN + T.FOOTNOTE_BAND_IN) * inch - 4
        band_bottom = T.COPYRIGHT_BAND_IN * inch + 14
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.35)
        canvas.line(ml, band_top, ml + 1.2 * inch, band_top)
        paras = [
            Paragraph(f"{n}. {allow_markup(self.notes_by_n.get(n, f'[Note {n} missing.]'))}", self._fn_style)
            for n in nums
        ]
        packed = 0.0
        for p in paras:
            _w, h = p.wrap(usable_w, T.FOOTNOTE_BAND_IN * inch)
            packed += h + 1
        if packed > (band_top - band_bottom):
            tight = ParagraphStyle(
                "PageFootnoteTight",
                parent=self._fn_style,
                fontSize=7,
                leading=9,
            )
            paras = [
                Paragraph(f"{n}. {allow_markup(self.notes_by_n.get(n, f'[Note {n} missing.]'))}", tight)
                for n in nums
            ]
        y = band_top - 3
        for p in paras:
            w, h = p.wrap(usable_w, y - band_bottom)
            if y - h < band_bottom:
                canvas.setFillColor(MUTED)
                canvas.setFont(T.BODY_ITALIC, 7)
                canvas.drawString(ml, band_bottom + 1, "Notes continue where next cited.")
                break
            p.drawOn(canvas, ml, y - h)
            y -= h + 1

    def _header_rule(self, canvas: Canvas, running: bool) -> None:
        canvas.setStrokeColor(RULE_SOFT)
        canvas.setLineWidth(0.35)
        y = letter[1] - 0.52 * inch
        canvas.line(T.MARGIN_LEFT_IN * inch, y, letter[0] - T.MARGIN_RIGHT_IN * inch, y)
        if running:
            canvas.setFillColor(MUTED)
            canvas.setFont(T.CHROME, T.FOOTER_PT)
            short = self.meta.get("running_title") or self.meta.get("title", "")
            if len(short) > 72:
                short = short[:70].rstrip() + "…"
            canvas.drawString(T.MARGIN_LEFT_IN * inch, y + 6, short.upper())

    def _footer(self, canvas: Canvas, doc, page_number: bool, live_year: bool) -> None:
        canvas.setStrokeColor(RULE_SOFT)
        canvas.setLineWidth(0.35)
        y = 0.55 * inch
        canvas.line(T.MARGIN_LEFT_IN * inch, y + 10, letter[0] - T.MARGIN_RIGHT_IN * inch, y + 10)
        canvas.setFillColor(MUTED)
        canvas.setFont(T.CHROME, T.FOOTER_PT)
        house = self.meta["house"]
        canvas.drawString(T.MARGIN_LEFT_IN * inch, y, house["anchor"])
        w = pdfmetrics.stringWidth(house["anchor"], T.CHROME, T.FOOTER_PT)
        canvas.linkURL(
            house["href"],
            (T.MARGIN_LEFT_IN * inch, y - 1, T.MARGIN_LEFT_IN * inch + w, y + 9),
            relative=0,
        )
        # Footer chrome: house name + copyright range + FOOTER_OWNER.
        # Never append a trailing class letter (" A"). That glyph was
        # leaking from OWNER_SHORT ("Web Development Corporation").
        owner_short = getattr(T, "FOOTER_OWNER", None) or self.meta["owner"]["short"]
        owner_short = re.sub(r"\s+A$", "", str(owner_short)).strip()
        if owner_short.endswith(" A"):
            owner_short = owner_short[:-2].rstrip()
        prefix = f"© {T.OWNER_FOUNDED}–"
        suffix = f"  {owner_short}"
        mid_w = (
            pdfmetrics.stringWidth(prefix, T.CHROME, T.FOOTER_PT)
            + 22
            + pdfmetrics.stringWidth(suffix, T.CHROME, T.FOOTER_PT)
        )
        mid_x = (letter[0] - mid_w) / 2
        canvas.drawString(mid_x, y, prefix)
        year_x = mid_x + pdfmetrics.stringWidth(prefix, T.CHROME, T.FOOTER_PT)
        if live_year and not self._copyright_field_drawn:
            self._copyright_field_drawn = True
            try:
                canvas.acroForm.textfield(
                    name=T.COPYRIGHT_FIELD,
                    tooltip="Copyright end year (updates on open)",
                    x=year_x,
                    y=y - 2,
                    width=24,
                    height=11,
                    value=str(self.year),
                    fontName="Helvetica",
                    fontSize=7,
                    textColor=MUTED,
                    fillColor=CREAM,
                    borderWidth=0,
                    borderStyle="underlined",
                    forceBorder=False,
                    fieldFlags="readOnly",
                )
            except Exception as exc:
                canvas.drawString(year_x, y, str(self.year))
                print("acroform field failed:", exc)
        else:
            canvas.drawString(year_x, y, str(self.year))
        canvas.drawString(year_x + 22, y, suffix)
        if page_number and doc.page > 1:
            canvas.drawRightString(letter[0] - T.MARGIN_RIGHT_IN * inch, y, str(doc.page))

    def _attach_openaction_js(self, canvas: Canvas) -> None:
        try:
            from reportlab.pdfbase.pdfdoc import PDFDictionary, PDFName, PDFString

            action = PDFDictionary()
            action["Type"] = PDFName("Action")
            action["S"] = PDFName("JavaScript")
            action["JS"] = PDFString(OPEN_JS)
            canvas._doc.Catalog.OpenAction = action
        except Exception:
            pass


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data.get("title") or not data.get("author"):
        raise SystemExit("folio.json needs title and author")
    data.setdefault(
        "house",
        {
            "anchor": T.HOUSE_ANCHOR,
            "href": T.HOUSE_HREF,
            "domain_plain": T.HOUSE_DOMAIN,
        },
    )
    data["house"]["anchor"] = T.HOUSE_ANCHOR
    data["house"]["href"] = T.HOUSE_HREF
    data["house"]["domain_plain"] = T.HOUSE_DOMAIN
    data.setdefault(
        "owner",
        {
            "legal": T.OWNER_LEGAL,
            "short": T.OWNER_SHORT,
            "founded": T.OWNER_FOUNDED,
        },
    )
    data["owner"]["legal"] = T.OWNER_LEGAL
    data["owner"]["short"] = T.OWNER_SHORT
    data["owner"]["founded"] = T.OWNER_FOUNDED
    origin = D.resolve_canonical_origin()
    data["house"]["href"] = origin
    data["house"]["origin"] = origin
    year = date.today().year
    filename = data.get("filename") or D.folio_filename(data["title"], year)
    if not str(filename).endswith(".pdf"):
        filename = str(filename) + ".pdf"
    data["filename"] = filename
    data["canonical_url"] = data.get("canonical_url") or D.canonical_record_url(
        filename, origin
    )
    data["document_id"] = D.document_id(filename, year)
    return data


def finalize_pdf(pdf_path: Path, data: dict, year: int) -> None:
    try:
        from pypdf import PdfReader, PdfWriter
        from pypdf.generic import NameObject, TextStringObject
    except Exception:
        return
    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    try:
        writer.clone_from(reader)
    except Exception:
        writer.append(reader)
    root = writer.root_object
    if root.get("/OpenAction") is None:
        try:
            writer.add_js(OPEN_JS)
        except Exception:
            pass
    info = D.info_dictionary(
        title=data["title"],
        author=data.get("author") or T.OWNER_SHORT,
        abstract=NOTE_RUN.sub("", ADJACENT_MARKS.sub(", ", data.get("abstract") or "")),
        keywords=list(data.get("keywords") or []),
        filename=data["filename"],
        origin=data["house"]["origin"],
        year=year,
        owner_legal=T.OWNER_LEGAL,
        house_anchor=T.HOUSE_ANCHOR,
    )
    try:
        writer.add_metadata(info)
    except Exception:
        pass
    try:
        xmp = D.xmp_payload(
            title=data["title"],
            author=data.get("author") or T.OWNER_SHORT,
            abstract=NOTE_RUN.sub("", ADJACENT_MARKS.sub(", ", data.get("abstract") or "")),
            keywords=list(data.get("keywords") or []),
            filename=data["filename"],
            origin=data["house"]["origin"],
            year=year,
            owner_legal=T.OWNER_LEGAL,
            house_anchor=T.HOUSE_ANCHOR,
        )
        writer.xmp_metadata = xmp
    except Exception:
        pass
    try:
        writer.root_object[NameObject("/Lang")] = TextStringObject("en-US")
    except Exception:
        pass
    tmp = pdf_path.with_suffix(".meta.pdf")
    with tmp.open("wb") as fh:
        writer.write(fh)
    tmp.replace(pdf_path)


def build(data: dict, out_path: Path, source_dir: Path) -> None:
    register_fonts()
    styles = make_styles()
    year = date.today().year
    notes_by_n = {int(n["n"]): n.get("text", "") for n in data.get("notes") or [] if "n" in n}
    meta = {
        "title": data["title"],
        "running_title": data.get("running_title") or data["title"],
        "house": data["house"],
        "owner": data["owner"],
        "genre": data.get("genre") or data.get("status") or "report",
    }
    kicker_map = {
        "monograph": "WCA COMPACT IVY  ·  MONOGRAPH",
        "working-paper": "WCA COMPACT IVY  ·  WORKING PAPER",
        "living-document": "WCA COMPACT IVY  ·  LIVING DOCUMENT",
        "think-tank": "WCA COMPACT IVY  ·  POLICY BRIEF",
        "paper": "WCA COMPACT IVY  ·  ACADEMIC PAPER",
    }
    kicker = kicker_map.get(str(meta["genre"]).lower(), "WCA COMPACT IVY  ·  ACADEMIC REPORT")
    doc = FolioDoc(
        out_path,
        meta=meta,
        year=year,
        notes_by_n=notes_by_n,
        pagesize=letter,
        title=data["title"],
        author=data.get("author", ""),
        creator=T.OWNER_LEGAL,
        subject=data.get("canonical_url") or data.get("subtitle") or "WCA compact Ivy academic report",
        keywords=", ".join(data.get("keywords") or []),
    )

    story: list = []
    story.append(Paragraph(kicker, styles["kicker"]))
    story.append(Paragraph(allow_markup(data["title"]), styles["title"]))
    if data.get("subtitle"):
        story.append(Paragraph(allow_markup(data["subtitle"]), styles["subtitle"]))
    else:
        story.append(Spacer(1, 8))
    story.append(Paragraph(allow_markup(data["author"]), styles["meta"]))
    story.append(Paragraph(allow_markup(data.get("date", "")), styles["meta"]))
    edition_bits = []
    if data.get("edition"):
        edition_bits.append(str(data["edition"]))
    if data.get("version"):
        edition_bits.append(f"Version {data['version']}")
    if data.get("revised"):
        edition_bits.append(f"Revised {data['revised']}")
    if edition_bits:
        story.append(Paragraph(" · ".join(edition_bits), styles["meta"]))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.4, color=RULE_SOFT, spaceBefore=4, spaceAfter=8))
    story.append(Paragraph(T.OWNER_LEGAL, styles["owner"]))
    story.append(
        Paragraph(
            f"Founded {T.OWNER_FOUNDED}.  © {T.OWNER_FOUNDED}–{year}.",
            styles["owner"],
        )
    )
    house = data["house"]
    story.append(
        Paragraph(
            f'<link href="{house["href"]}">{house["anchor"]}</link>'
            f"  ·  {house['domain_plain']}",
            styles["owner"],
        )
    )
    record = data.get("canonical_url") or house["href"]
    story.append(
        Paragraph(
            f'Canonical record  ·  <link href="{record}">{record}</link>',
            styles["owner"],
        )
    )

    if data.get("abstract"):
        story.append(Paragraph("ABSTRACT", styles["abstract_label"]))
        story.append(Paragraph(inject_notes(data["abstract"]), styles["abstract"]))
    if data.get("keywords"):
        kw = ", ".join(data["keywords"])
        story.append(Paragraph(f"<b>Keywords.</b>  {allow_markup(kw)}", styles["keywords"]))

    story.append(NextPageTemplate("body"))
    story.append(PageBreak())

    notes_by_n = {int(n["n"]): n.get("text", "") for n in data.get("notes") or [] if "n" in n}

    for section in data.get("sections") or []:
        kind = (section.get("kind") or "body").lower()
        title = section.get("title") or ""
        sid = section.get("id") or title[:24]
        if title:
            h = Paragraph(allow_markup(title), styles["h1"])
            h._bookmarkName = sid  # type: ignore[attr-defined]
            story.append(h)
            try:
                story[-1].keepWithNext = True
            except Exception:
                pass

        paragraphs = section.get("paragraphs") or []
        figure = section.get("figure") or None
        after_n = None
        fig_path = None
        if figure and figure.get("path"):
            after_n = int(figure.get("after_paragraphs") or 1)
            cand = Path(figure["path"])
            if not cand.is_file():
                cand = source_dir / figure["path"]
            fig_path = cand if cand.is_file() else None

        if kind == "notes":
            for n in data.get("notes") or []:
                num = int(n["n"])
                body = inject_notes(n.get("text") or notes_by_n.get(num, ""))
                block = f'<a name="note-{num}"/>{num}.  {body}'
                story.append(Paragraph(block, styles["note"]))
            continue

        if kind == "bibliography":
            for entry in data.get("bibliography") or []:
                story.append(Paragraph(allow_markup(biblio_text(entry)), styles["bib"]))
            continue

        string_index = 0
        for i, para in enumerate(paragraphs):
            if isinstance(para, dict) and (para.get("type") or para.get("kind") or "").lower() == "equation":
                story.extend(flow_equation(para, styles, source_dir))
            elif isinstance(para, dict) and isinstance(para.get("text"), str):
                style = styles["body_first"] if string_index == 0 else styles["body"]
                story.append(
                    CitedParagraph(
                        inject_notes(para["text"]),
                        style,
                        cited=extract_note_ns(para["text"]),
                    )
                )
                string_index += 1
            elif isinstance(para, str):
                style = styles["body_first"] if string_index == 0 else styles["body"]
                story.append(CitedParagraph(inject_notes(para), style, cited=extract_note_ns(para)))
                string_index += 1
            if fig_path is not None and after_n is not None and string_index == after_n:
                max_w = letter[0] - (T.MARGIN_LEFT_IN + T.MARGIN_RIGHT_IN) * inch
                story.append(Spacer(1, 6))
                story.append(fitted_image(fig_path, max_w, 3.4 * inch))
                cap = figure.get("caption") or ""
                if cap:
                    story.append(Paragraph(allow_markup(cap), styles["caption"]))
                fig_path = None

        for extra_eq in section.get("equations") or []:
            if isinstance(extra_eq, dict):
                extra_eq.setdefault("type", "equation")
                story.extend(flow_equation(extra_eq, styles, source_dir))

    has_notes_leaf = any((s.get("kind") or "").lower() == "notes" for s in data.get("sections") or [])
    if notes_by_n and not has_notes_leaf:
        h = Paragraph("Notes", styles["h1"])
        h._bookmarkName = "notes"
        story.append(h)
        for num in sorted(notes_by_n):
            body = inject_notes(notes_by_n[num])
            block = f'<a name="note-{num}"/>{num}.  {body}'
            story.append(Paragraph(block, styles["note"]))

    story.append(Spacer(1, 24))
    story.append(HRFlowable(width="40%", thickness=0.4, color=RULE_SOFT, spaceBefore=8, spaceAfter=10))
    story.append(Paragraph("COLOPHON", styles["abstract_label"]))
    story.append(
        Paragraph(
            f"This report is set in {T.STYLE_TOKEN} {T.STYLE_VERSION}, owned by {T.OWNER_LEGAL}, "
            f"founded {T.OWNER_FOUNDED}. Body is Literata 18pt optical cut, set at {T.BODY_PT} pt "
            f"on {T.BODY_LEADING} pt leading. Display is EB Garamond. Chrome is Libre Franklin. "
            f"Citations print as page-local Chicago footnotes in WCA Ivy first-appearance order; "
            f"a collected Notes leaf is optional concordance. Display equations carry an ITQE table.",
            styles["colophon"],
        )
    )
    record = data.get("canonical_url") or data["house"]["href"]
    story.append(
        Paragraph(
            f"© {T.OWNER_FOUNDED}–{year}  {T.OWNER_LEGAL}. "
            "The end year is a live field and refreshes on open in a JavaScript-capable viewer.",
            styles["colophon"],
        )
    )
    story.append(
        Paragraph(
            f'Cite and link this report at <link href="{record}">{record}</link>. '
            f"File name {data.get('filename') or ''}.",
            styles["colophon"],
        )
    )

    doc.build(story)
    finalize_pdf(out_path, data, year)


def main() -> None:
    p = argparse.ArgumentParser(description="Build a WCA Folio PDF")
    p.add_argument("json_path")
    p.add_argument("--out", default="")
    p.add_argument("--print-filename", action="store_true")
    args = p.parse_args()
    src = Path(args.json_path).resolve()
    data = load_json(src)
    if args.print_filename:
        print(data["filename"])
        print(data["canonical_url"])
        return
    if args.out:
        out = Path(args.out).resolve()
        if out.is_dir() or str(args.out).endswith("/"):
            out = out / data["filename"]
    else:
        out = Path("/home/workdir/artifacts") / data["filename"]
    out.parent.mkdir(parents=True, exist_ok=True)
    build(data, out, src.parent)
    print(f"wrote {out}")
    print(f"canonical {data['canonical_url']}")


if __name__ == "__main__":
    main()
