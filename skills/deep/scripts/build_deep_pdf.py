#!/usr/bin/env python3
"""Build a letter-size /deep Chicago monograph with locked Georgia type and bleed banners."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from publication_notice import notice_for

from PIL import Image as PILImage
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    HRFlowable,
    Image,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT / "assets"))
from typography import (  # noqa: E402
    ABSTRACT_LEADING,
    ABSTRACT_PT,
    BANNER_BLEED_WIDTH_IN,
    BANNER_HREF_TEMPLATE,
    BANNER_TOTAL_HEIGHT_IN,
    BIBLIO_LEADING,
    BIBLIO_PT,
    BODY_LEADING,
    BODY_PT,
    CAPTION_LEADING,
    CAPTION_PT,
    FONT_BOLD,
    FONT_BOLDITALIC,
    FONT_ITALIC,
    FONT_REGULAR,
    FOOTER_LEADING,
    FOOTER_PT,
    H1_LEADING,
    H1_PT,
    KICKER_PT,
    MARGIN_BOTTOM_IN,
    MARGIN_LEFT_IN,
    MARGIN_RIGHT_IN,
    MARGIN_TOP_IN,
    NOTE_LEADING,
    NOTE_PT,
    PAGENUM_PT,
    SUBTITLE_LEADING,
    SUBTITLE_PT,
    TITLE_LEADING,
    TITLE_PT,
)

INK = HexColor("#1a1a1a")
MUTED = HexColor("#444444")
RULE = HexColor("#222222")
RULE_SOFT = HexColor("#888888")
PAGE_FILL = Color(0.98, 0.98, 0.97)

NOTE_GROUP = re.compile(r"(?:\{\{(\d+(?:\s*,\s*\d+)*)\}\})+")
NOTE_ONE = re.compile(r"\{\{(\d+(?:\s*,\s*\d+)*)\}\}")
EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002700-\U000027BF"
    "\U0001F000-\U0001F2FF"
    "\ufe0f"
    "]+"
)


def register_fonts() -> None:
    font_dir = SKILL_ROOT / "assets" / "fonts"
    pdfmetrics.registerFont(TTFont("ITQEDejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"))
    pdfmetrics.registerFont(TTFont("ITQEDejaVuBold", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"))
    pdfmetrics.registerFont(TTFont(FONT_REGULAR, str(font_dir / "Gelasio-Regular.ttf")))
    pdfmetrics.registerFont(TTFont(FONT_BOLD, str(font_dir / "Gelasio-Bold.ttf")))
    pdfmetrics.registerFont(TTFont(FONT_ITALIC, str(font_dir / "Gelasio-Italic.ttf")))
    pdfmetrics.registerFont(TTFont(FONT_BOLDITALIC, str(font_dir / "Gelasio-BoldItalic.ttf")))
    pdfmetrics.registerFontFamily(
        FONT_REGULAR,
        normal=FONT_REGULAR,
        bold=FONT_BOLD,
        italic=FONT_ITALIC,
        boldItalic=FONT_BOLDITALIC,
    )


def clean(text: str) -> str:
    text = EMOJI_RE.sub("", text or "")
    return text.replace("\u00a0", " ").strip()


def xml_escape(text: str) -> str:
    text = clean(text)
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def allow_markup(text: str) -> str:
    text = clean(text)
    holders: list[str] = []

    def stash(match: re.Match) -> str:
        holders.append(match.group(0))
        return f"@@TAG{len(holders) - 1}@@"

    pattern = re.compile(
        r"</?(?:i|em|b|sup|a)(?:\s+href=(?:\"[^\"]+\"|'[^']+'))?\s*>",
        re.I,
    )
    protected = pattern.sub(stash, text)
    protected = protected.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
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
    for inner in NOTE_ONE.findall(text or ""):
        for part in inner.split(","):
            part = part.strip()
            if not part:
                continue
            n = int(part)
            if n not in nums:
                nums.append(n)
    return nums


def inject_notes(text: str) -> str:
    """Turn {{1}} and {{1, 4, 9}} into superscript runs with comma-space."""

    def join_run(match: re.Match) -> str:
        blob = match.group(0)
        nums: list[str] = []
        for inner in NOTE_ONE.findall(blob):
            for part in inner.split(","):
                n = part.strip()
                if n and n not in nums:
                    nums.append(n)
        joined = ", ".join(nums)
        return f"<super>{joined}</super>"

    return NOTE_GROUP.sub(join_run, allow_markup(text))


class CitedParagraph(Paragraph):
    def __init__(self, text, style, cited=None, **kwargs):
        super().__init__(text, style, **kwargs)
        self.cited = list(cited or [])

    def split(self, availWidth, availHeight):
        pieces = super().split(availWidth, availHeight)

        def superscripts(fragments):
            for fragment in fragments:
                if isinstance(fragment, tuple) and len(fragment) == 2 and hasattr(fragment[0], "rise"):
                    if fragment[0].rise > 0:
                        yield str(fragment[1])
                elif isinstance(fragment, (list, tuple)):
                    yield from superscripts(fragment)
                elif getattr(fragment, "rise", 0) > 0:
                    yield str(getattr(fragment, "text", ""))

        for piece in pieces:
            numbers = {int(n) for text in superscripts(piece.frags) for n in re.findall(r"\b\d+\b", text)}
            piece.cited = [n for n in self.cited if n in numbers]
        return pieces


def make_styles() -> dict[str, ParagraphStyle]:
    return {
        "cover_kicker": ParagraphStyle(
            "CoverKicker",
            fontName=FONT_REGULAR,
            fontSize=KICKER_PT,
            leading=FOOTER_LEADING,
            alignment=TA_CENTER,
            textColor=MUTED,
            spaceAfter=16,
        ),
        "cover_title": ParagraphStyle(
            "CoverTitle",
            fontName=FONT_BOLD,
            fontSize=TITLE_PT,
            leading=TITLE_LEADING,
            alignment=TA_CENTER,
            textColor=INK,
            spaceAfter=12,
        ),
        "cover_sub": ParagraphStyle(
            "CoverSub",
            fontName=FONT_ITALIC,
            fontSize=SUBTITLE_PT,
            leading=SUBTITLE_LEADING,
            alignment=TA_CENTER,
            textColor=INK,
            spaceAfter=20,
        ),
        "cover_meta": ParagraphStyle(
            "CoverMeta",
            fontName=FONT_REGULAR,
            fontSize=BODY_PT,
            leading=BODY_LEADING,
            alignment=TA_CENTER,
            textColor=INK,
            spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "H1",
            fontName=FONT_BOLD,
            fontSize=H1_PT,
            leading=H1_LEADING,
            alignment=TA_LEFT,
            textColor=INK,
            spaceBefore=18,
            spaceAfter=10,
        ),
        "body": ParagraphStyle(
            "Body",
            fontName=FONT_REGULAR,
            fontSize=BODY_PT,
            leading=BODY_LEADING,
            alignment=TA_JUSTIFY,
            textColor=INK,
            spaceAfter=12,
            firstLineIndent=22,
        ),
        "body_first": ParagraphStyle(
            "BodyFirst",
            fontName=FONT_REGULAR,
            fontSize=BODY_PT,
            leading=BODY_LEADING,
            alignment=TA_JUSTIFY,
            textColor=INK,
            spaceAfter=12,
            firstLineIndent=0,
        ),
        "abstract_label": ParagraphStyle(
            "AbsLabel",
            fontName=FONT_BOLD,
            fontSize=H1_PT,
            leading=H1_LEADING,
            alignment=TA_CENTER,
            textColor=INK,
            spaceAfter=10,
        ),
        "abstract": ParagraphStyle(
            "Abstract",
            fontName=FONT_REGULAR,
            fontSize=ABSTRACT_PT,
            leading=ABSTRACT_LEADING,
            alignment=TA_JUSTIFY,
            textColor=INK,
            spaceAfter=10,
        ),
        "keywords": ParagraphStyle(
            "Keywords",
            fontName=FONT_ITALIC,
            fontSize=CAPTION_PT,
            leading=CAPTION_LEADING,
            alignment=TA_LEFT,
            textColor=INK,
            spaceBefore=8,
            spaceAfter=14,
        ),
        "caption": ParagraphStyle(
            "Caption",
            fontName=FONT_ITALIC,
            fontSize=CAPTION_PT,
            leading=CAPTION_LEADING,
            alignment=TA_LEFT,
            textColor=MUTED,
            spaceBefore=4,
            spaceAfter=14,
        ),
        "itqe_kicker": ParagraphStyle(
            "ItqeKicker",
            fontName="ITQEDejaVu",
            fontSize=NOTE_PT,
            leading=NOTE_LEADING,
            alignment=TA_LEFT,
            textColor=MUTED,
            spaceBefore=8,
            spaceAfter=2,
        ),
        "itqe_head": ParagraphStyle(
            "ItqeHead",
            fontName="ITQEDejaVuBold",
            fontSize=NOTE_PT,
            leading=NOTE_LEADING,
            alignment=TA_LEFT,
            textColor=INK,
        ),
        "itqe_cell": ParagraphStyle(
            "ItqeCell",
            fontName="ITQEDejaVu",
            fontSize=NOTE_PT,
            leading=NOTE_LEADING,
            alignment=TA_LEFT,
            textColor=INK,
        ),
        "note": ParagraphStyle(
            "Note",
            fontName=FONT_REGULAR,
            fontSize=NOTE_PT,
            leading=NOTE_LEADING,
            alignment=TA_JUSTIFY,
            textColor=INK,
            leftIndent=22,
            firstLineIndent=-22,
            spaceAfter=8,
        ),
        "bib": ParagraphStyle(
            "Bib",
            fontName=FONT_REGULAR,
            fontSize=BIBLIO_PT,
            leading=BIBLIO_LEADING,
            alignment=TA_LEFT,
            textColor=INK,
            leftIndent=28,
            firstLineIndent=-28,
            spaceAfter=10,
        ),
        "toc_item": ParagraphStyle(
            "TocItem",
            fontName=FONT_REGULAR,
            fontSize=BODY_PT,
            leading=BODY_LEADING,
            alignment=TA_LEFT,
            textColor=INK,
            spaceAfter=6,
        ),
    }


class BleedBanner(Flowable):
    """Full-bleed (x=0) banner with real alpha and a hidden link over the plate."""

    def __init__(self, path: Path, href: str):
        super().__init__()
        self.path = path
        self.href = href
        self.page_w = letter[0]
        self.w = BANNER_BLEED_WIDTH_IN * inch
        try:
            with PILImage.open(path) as im:
                iw, ih = im.size
            ratio = (ih / float(iw)) if iw else (9 / 16)
        except Exception:
            ratio = 9 / 16
        self.h = self.w * ratio

    def wrap(self, availWidth, availHeight):
        # Report a width inside the frame so Platypus accepts the flowable,
        # but draw at page x=0.
        return (availWidth, self.h)

    def draw(self) -> None:
        canvas = self.canv
        x_on_page = canvas.absolutePosition(0, 0)[0]
        shift = -x_on_page
        canvas.saveState()
        try:
            canvas.drawImage(
                str(self.path),
                shift,
                0,
                width=self.w,
                height=self.h,
                mask="auto",
                preserveAspectRatio=True,
                anchor="c",
            )
        except Exception:
            canvas.setFillColor(MUTED)
            canvas.setFont(FONT_REGULAR, CAPTION_PT)
            canvas.drawString(6, self.h / 2, "[Banner missing]")
        if self.href:
            canvas.linkURL(
                self.href,
                (shift, 0, shift + self.w, self.h),
                relative=0,
                thickness=0,
            )
        canvas.restoreState()


class DeepDoc(BaseDocTemplate):
    def __init__(self, out_path: Path, house: dict, notes_by_n: dict[int, str] | None = None, **kwargs):
        super().__init__(str(out_path), **kwargs)
        self.house = house
        self.notes_by_n = notes_by_n or {}
        self.notes_on_page: dict[int, list[int]] = {}
        left = MARGIN_LEFT_IN * inch
        right = MARGIN_RIGHT_IN * inch
        top = MARGIN_TOP_IN * inch
        # Raise the body frame so cited notes can sit in a page-local band
        # above the living copyright line. Locked type sizes stay untouched.
        bottom = 2.15 * inch
        frame = Frame(
            left,
            bottom,
            letter[0] - left - right,
            letter[1] - top - bottom,
            id="body",
        )
        cover = Frame(
            left,
            bottom,
            letter[0] - left - right,
            letter[1] - top - bottom,
            id="cover",
        )
        self.addPageTemplates(
            [
                PageTemplate(id="cover", frames=[cover], onPage=self._draw_page, onPageEnd=self._draw_page_end),
                PageTemplate(id="body", frames=[frame], onPage=self._draw_page, onPageEnd=self._draw_page_end),
            ]
        )

    def afterFlowable(self, flowable) -> None:
        cited = getattr(flowable, "cited", None)
        if not cited:
            return
        bucket = self.notes_on_page.setdefault(int(self.page), [])
        for n in cited:
            if n not in bucket:
                bucket.append(n)

    def _draw_page(self, canvas: Canvas, doc) -> None:
        canvas.saveState()
        canvas.setFillColor(PAGE_FILL)
        canvas.rect(0, 0, letter[0], letter[1], stroke=0, fill=1)
        canvas.setStrokeColor(RULE_SOFT)
        canvas.setLineWidth(0.3)
        y_head = letter[1] - 0.42 * inch
        canvas.line(MARGIN_LEFT_IN * inch, y_head, letter[0] - MARGIN_RIGHT_IN * inch, y_head)
        y = 0.82 * inch
        canvas.line(MARGIN_LEFT_IN * inch, y + 12, letter[0] - MARGIN_RIGHT_IN * inch, y + 12)
        canvas.setFillColor(MUTED)
        if doc.page > 1:
            canvas.setFont(FONT_REGULAR, PAGENUM_PT)
            canvas.drawRightString(letter[0] - MARGIN_RIGHT_IN * inch, y, str(doc.page))
        canvas.setFont(FONT_REGULAR, 8)
        canvas.drawCentredString(
            letter[0] / 2.0,
            0.22 * inch,
            self.copyright_notice,
        )
        canvas.restoreState()

    def _draw_page_end(self, canvas: Canvas, doc) -> None:
        canvas.saveState()
        self._draw_page_footnotes(canvas, doc)
        canvas.restoreState()

    def _draw_page_footnotes(self, canvas: Canvas, doc) -> None:
        nums = sorted(self.notes_on_page.get(int(doc.page), []))
        if not nums:
            return
        left = MARGIN_LEFT_IN * inch
        usable_w = letter[0] - (MARGIN_LEFT_IN + MARGIN_RIGHT_IN) * inch
        band_top = 2.15 * inch - 6
        band_bottom = 0.98 * inch
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.5)
        canvas.line(left, band_top, left + 1.6 * inch, band_top)
        style = ParagraphStyle(
            "DeepPageFN",
            fontName=FONT_REGULAR,
            fontSize=9,
            leading=11,
            alignment=TA_LEFT,
            textColor=INK,
            leftIndent=12,
            firstLineIndent=-12,
        )
        y = band_top - 3
        for n in nums:
            raw = self.notes_by_n.get(n, f"[Note {n} missing from notes array.]")
            p = Paragraph(f"{n}. {allow_markup(raw)}", style)
            _w, h = p.wrap(usable_w, y - band_bottom)
            if y - h < band_bottom:
                canvas.setFillColor(MUTED)
                canvas.setFont(FONT_ITALIC, 8)
                canvas.drawString(left, band_bottom + 1, "Notes continue where next cited.")
                break
            p.drawOn(canvas, left, y - h)
            y -= h + 1


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data.get("title") or not data.get("author"):
        raise SystemExit("document JSON needs title and author")
    data.setdefault(
        "house",
        {
            "anchor": "Digital Marketing Company",
            "href": "https://digitalmarketingco.org",
            "domain_plain": "DigitalMarketingCo.org",
            "wdc_anchor": "Web Development Corporation",
            "wdc_href": "https://WebDevelopment.tv",
        },
    )
    house = data["house"]
    house.setdefault("anchor", "Digital Marketing Company")
    house.setdefault("href", "https://digitalmarketingco.org")
    house.setdefault("domain_plain", "DigitalMarketingCo.org")
    house.setdefault("wdc_anchor", "Web Development Corporation")
    house.setdefault("wdc_href", "https://WebDevelopment.tv")
    return data


def resolve_path(raw: str, json_dir: Path) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = json_dir / path
    return path


def banner_block(sec: dict, json_dir: Path, styles: dict):
    banner = sec.get("banner") or {}
    raw = banner.get("path") or ""
    if not raw:
        return None
    path = resolve_path(raw, json_dir)
    section_id = sec.get("id") or "section"
    href = banner.get("href") or BANNER_HREF_TEMPLATE.format(section_id=section_id)
    bits = []
    if path.exists():
        bits.append(BleedBanner(path, href))
    else:
        bits.append(Paragraph(xml_escape(f"[Banner missing: {raw}]"), styles["caption"]))
    cap = banner.get("caption") or ""
    if cap:
        bits.append(Paragraph(xml_escape(cap), styles["caption"]))
    return KeepTogether(bits)


def flow_equation(eq: dict, json_dir: Path, styles: dict):
    bits = []
    plate = eq.get("plate") or eq.get("path") or ""
    if plate:
        path = resolve_path(plate, json_dir)
        if path.is_file():
            im = PILImage.open(path)
            max_w = 6.4 * inch
            max_h = 1.6 * inch
            w, h = im.size
            scale = min(max_w / w, max_h / h)
            bits.append(Image(str(path), width=w * scale, height=h * scale))
    elif eq.get("unicode"):
        bits.append(Paragraph(allow_markup(eq["unicode"]), styles["body"]))
    cap = eq.get("caption") or ""
    if cap:
        bits.append(Paragraph(xml_escape(cap), styles["caption"]))
    rows = eq.get("itqe") or []
    if rows:
        bits.append(Paragraph("ITQE", styles["itqe_kicker"]))
        data = [[
            Paragraph("Identifier", styles["itqe_head"]),
            Paragraph("Term", styles["itqe_head"]),
            Paragraph("Quantity", styles["itqe_head"]),
            Paragraph("Explanation", styles["itqe_head"]),
        ]]
        for row in rows:
            data.append([
                Paragraph(xml_escape(str(row.get("identifier") or "")), styles["itqe_cell"]),
                Paragraph(xml_escape(str(row.get("term") or "")), styles["itqe_cell"]),
                Paragraph(xml_escape(str(row.get("quantity") or "")), styles["itqe_cell"]),
                Paragraph(xml_escape(str(row.get("explanation") or "")), styles["itqe_cell"]),
            ])
        max_w = 6.55 * inch
        table = Table(data, colWidths=[max_w * x for x in (0.16, 0.22, 0.18, 0.44)], hAlign="LEFT", repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), HexColor("#EFEAE2")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LINEBELOW", (0, 0), (-1, 0), 0.4, RULE),
            ("LINEBELOW", (0, 1), (-1, -1), 0.2, RULE_SOFT),
            ("BOX", (0, 0), (-1, -1), 0.3, RULE_SOFT),
        ]))
        bits.append(table)
    legend = eq.get("legend") or []
    if legend:
        bits.append(Paragraph("ITQE — glyphs", styles["itqe_kicker"]))
        gdata = [[
            Paragraph("Glyph", styles["itqe_head"]),
            Paragraph("Name and case", styles["itqe_head"]),
            Paragraph("Role in this equation", styles["itqe_head"]),
            Paragraph("Operators on this figure", styles["itqe_head"]),
        ]]
        for item in legend:
            name = str(item.get("name") or "")
            case = str(item.get("case") or "")
            name_case = f"{name} ({case})" if case and case.lower() not in name.lower() else name
            gdata.append([
                Paragraph(xml_escape(str(item.get("glyph") or "")), styles["itqe_cell"]),
                Paragraph(xml_escape(name_case), styles["itqe_cell"]),
                Paragraph(xml_escape(str(item.get("role") or "")), styles["itqe_cell"]),
                Paragraph(xml_escape(str(item.get("operators") or "none on this figure")), styles["itqe_cell"]),
            ])
        max_w = 6.55 * inch
        gtable = Table(gdata, colWidths=[max_w * x for x in (0.14, 0.24, 0.32, 0.30)], hAlign="LEFT", repeatRows=1)
        gtable.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), HexColor("#EFEAE2")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LINEBELOW", (0, 0), (-1, 0), 0.4, RULE),
            ("LINEBELOW", (0, 1), (-1, -1), 0.2, RULE_SOFT),
            ("BOX", (0, 0), (-1, -1), 0.3, RULE_SOFT),
        ]))
        bits.append(gtable)
        bits.append(Spacer(1, 8))
    return KeepTogether(bits)


def build(data: dict, json_dir: Path, out_path: Path) -> None:
    register_fonts()
    styles = make_styles()
    house = data["house"]
    notes_by_n = {}
    for note in data.get("notes") or []:
        try:
            notes_by_n[int(note.get("n"))] = note.get("text") or ""
        except (TypeError, ValueError):
            continue
    doc = DeepDoc(
        out_path,
        house,
        notes_by_n,
        pagesize=letter,
        title=data["title"],
        author=data["author"],
    )
    doc.copyright_notice = notice_for(data)
    href = house["href"]
    anchor = house["anchor"]
    wdc_href = house.get("wdc_href") or "https://WebDevelopment.tv"
    wdc_anchor = house.get("wdc_anchor") or "Web Development Corporation"
    story = []

    story.append(NextPageTemplate("cover"))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("A HOUSE RESEARCH COMPENDIUM", styles["cover_kicker"]))
    story.append(
        HRFlowable(width="60%", thickness=0.6, color=RULE, spaceBefore=2, spaceAfter=16, hAlign="CENTER")
    )
    story.append(Paragraph(xml_escape(data["title"]), styles["cover_title"]))
    if data.get("subtitle"):
        story.append(Paragraph(xml_escape(data["subtitle"]), styles["cover_sub"]))
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph(xml_escape(data["author"]), styles["cover_meta"]))
    story.append(Paragraph(xml_escape(data.get("date", "")), styles["cover_meta"]))
    story.append(Spacer(1, 0.35 * inch))
    story.append(
        Paragraph(
            "Sourced notes-bibliography monograph with house citation order. "
            "Generated illustrations are identified separately from documentary evidence.",
            styles["abstract"],
        )
    )

    story.append(NextPageTemplate("body"))
    story.append(PageBreak())
    story.append(Paragraph("Abstract", styles["abstract_label"]))
    abs_raw = data.get("abstract", "")
    story.append(CitedParagraph(inject_notes(abs_raw), styles["abstract"], cited=extract_note_ns(abs_raw)))
    kws = data.get("keywords") or []
    if kws:
        joined = ", ".join(xml_escape(k) for k in kws)
        story.append(Paragraph(f"<i>Keywords:</i> {joined}", styles["keywords"]))

    body_sections = [s for s in data.get("sections", []) if s.get("kind", "body") == "body"]
    if body_sections:
        story.append(Paragraph("Contents", styles["h1"]))
        for sec in body_sections:
            story.append(Paragraph(xml_escape(sec.get("title", "")), styles["toc_item"]))

    for sec in data.get("sections", []):
        kind = sec.get("kind", "body")
        title = sec.get("title") or ""
        if kind == "notes":
            story.append(PageBreak())
            story.append(Paragraph(xml_escape(title or "Notes"), styles["h1"]))
            story.append(HRFlowable(width="100%", thickness=0.4, color=RULE, spaceBefore=0, spaceAfter=10))
            notes = sorted(data.get("notes") or [], key=lambda n: int(n.get("n", 0)))
            for note in notes:
                n = note.get("n")
                text = allow_markup(note.get("text", ""))
                story.append(Paragraph(f"{n}. {text}", styles["note"]))
            continue
        if kind == "bibliography":
            story.append(PageBreak())
            story.append(Paragraph(xml_escape(title or "Bibliography"), styles["h1"]))
            story.append(HRFlowable(width="100%", thickness=0.4, color=RULE, spaceBefore=0, spaceAfter=10))
            for entry in data.get("bibliography") or []:
                story.append(Paragraph(allow_markup(entry), styles["bib"]))
            continue

        heading = Paragraph(xml_escape(title), styles["h1"])
        rule = HRFlowable(width="100%", thickness=0.4, color=RULE, spaceBefore=0, spaceAfter=8)
        block = banner_block(sec, json_dir, styles)
        if block:
            story.append(KeepTogether([heading, rule, block]))
        else:
            heading.keepWithNext = 1
            rule.keepWithNext = 1
            story.extend([heading, rule])
        paras = sec.get("paragraphs") or []
        string_i = 0
        for para in paras:
            if isinstance(para, dict) and (para.get("type") or "").lower() == "equation":
                story.append(flow_equation(para, json_dir, styles))
                continue
            if isinstance(para, dict) and isinstance(para.get("text"), str):
                text = para["text"]
            elif isinstance(para, str):
                text = para
            else:
                continue
            string_i += 1
            style = styles["body_first"] if string_i == 1 else styles["body"]
            story.append(CitedParagraph(inject_notes(text), style, cited=extract_note_ns(text)))

    doc.build(story)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build /deep monograph PDF")
    parser.add_argument("json_path")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    json_path = Path(args.json_path).resolve()
    out_path = Path(args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    data = load_json(json_path)
    build(data, json_path.parent, out_path)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
