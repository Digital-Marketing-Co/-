#!/usr/bin/env python3
"""Stamp a living centered copyright footer onto every page of a PDF."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from io import BytesIO
from pathlib import Path

import fitz
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    BooleanObject,
    DictionaryObject,
    FloatObject,
    NameObject,
    NumberObject,
    TextStringObject,
)
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

try:
    from notice import notice_text as canonical_notice
except ImportError:
    import importlib.util
    _spec = importlib.util.spec_from_file_location('canonical_notice', Path(__file__).with_name('notice.py'))
    _notice_module = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_notice_module)
    canonical_notice = _notice_module.notice_text

FIELD_NAME = "WCACopyrightYear"
DEFAULT_OWNER = "Web Development Corporation"
DEFAULT_LEGAL = "Web Development Corporation, a Delaware Corporation"
DEFAULT_START = 2012
FOOTER_PT = 8
BAND_H = 56.0
TEXT_Y = 24.0
CREAM_HEX = "#FBF7F0"
MUTED = Color(0.28, 0.28, 0.28)
CREAM = HexColor(CREAM_HEX)
NOTICE_LINE = re.compile(r"^\s*(?:Copyright\s*)?©\s*\d{4}(?:\s*[–-]\s*\d{4})?\s+.+?All rights reserved\.?\s*$", re.I)


def remove_prior_notices(src: Path) -> bytes:
    """Remove standalone prior notices from the text layer before painting new ones."""
    doc = fitz.open(src)
    try:
        if doc.needs_pass:
            raise ValueError("Encrypted PDF requires decryption before copyright stamping")
        for page in doc:
            found = 0
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    spans = line.get("spans", [])
                    line_text = "".join(span["text"] for span in spans).strip()
                    footer_label = line_text in ('Digital Marketing Co.', 'Digital Marketing Co.', 'Web Development, Inc.') and line.get('bbox', (0,0,0,0))[1] >= page.rect.height-BAND_H
                    if NOTICE_LINE.fullmatch(line_text) or footer_label:
                        rect = fitz.Rect(spans[0]["bbox"])
                        for span in spans[1:]:
                            rect |= fitz.Rect(span["bbox"])
                        page.add_redact_annot(rect, fill=False)
                        found += 1
            if found:
                page.apply_redactions(images=0, graphics=0, text=0)
            for link in page.get_links():
                if link.get('from') and link['from'].y0 >= page.rect.height-BAND_H:
                    page.delete_link(link)
        return doc.tobytes(garbage=4, deflate=True)
    finally:
        doc.close()


def verify_single_notice(pdf_bytes: bytes) -> None:
    """Fail closed if a page contains a missing or repeated extractable notice."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    try:
        for number, page in enumerate(doc, 1):
            count = sum(
                bool(NOTICE_LINE.fullmatch("".join(s["text"] for s in line.get("spans", [])).strip()))
                for block in page.get_text("dict")["blocks"]
                for line in block.get("lines", [])
            )
            if count != 1:
                raise ValueError(f"Page {number}: expected one extractable copyright notice, found {count}")
    finally:
        doc.close()


def en_dash_range(start: int, year: int) -> str:
    if year > start:
        return f"{start}\u2013{year}"
    return str(start)


def notice_text(start: int, year: int, owner: str) -> str:
    return canonical_notice(start, year, owner)


def open_js(start: int, owner: str) -> str:
    owner_js = json.dumps(owner, ensure_ascii=True)
    return (
        f"var start = {int(start)};"
        "var y = (new Date()).getFullYear();"
        'var range = (y > start) ? (String(start) + "\\u2013" + String(y)) : String(start);'
        "try {"
        f" var f = this.getField('{FIELD_NAME}');"
        f' if (f) f.value = "\\u00a9 " + range + " " + {owner_js} + ". All rights reserved.";'
        "} catch (e) {}"
    )


def strip_class_a(owner: str) -> str:
    text = re.sub(r"\s+A$", "", owner.strip())
    return text


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Restamp every PDF page footer with a living copyright line.")
    p.add_argument("input", type=Path, help="Source PDF")
    p.add_argument("--start", type=int, default=DEFAULT_START, help="First year of the copyright range")
    p.add_argument("--owner", default=DEFAULT_OWNER, help="Footer owner name")
    p.add_argument("--legal", default=DEFAULT_LEGAL, help="PDF Info legal owner")
    p.add_argument("--out", type=Path, default=None, help="Output PDF path")
    p.add_argument("--overwrite", action="store_true", help="Write back onto the input path")
    return p.parse_args()


def cover_and_paint(width: float, height: float, text: str) -> bytes:
    buf = BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(width, height))
    c.setFillColor(CREAM)
    c.rect(0, 0, width, BAND_H, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 7)
    labels = [('Digital Marketing Co.', 'https://DigitalMarketingCo.org', width/6),
              ('Web Development, Inc.', 'https://WebDevelopment.tv', width/2)]
    for label, href, center in labels:
        extent = stringWidth(label, 'Helvetica', 7)
        c.drawCentredString(center, 7, label)
        c.linkURL(href, (center-extent/2, 5, center+extent/2, 15), relative=0)
    if DEFAULT_OWNER in text:
        # Upper legal label uses the exact lower Web Development target.
        prefix = text.split(DEFAULT_OWNER, 1)[0]
        start_x = (width-stringWidth(text,'Helvetica',8))/2 + stringWidth(prefix,'Helvetica',8)
        c.linkURL('https://WebDevelopment.tv',
                  (start_x, 14, start_x+stringWidth(DEFAULT_OWNER,'Helvetica',8), 36), relative=0)
    # The field supplies both the fallback appearance and the living-year text.
    # Painting text here as well would create two extractable notices.
    c.save()
    return buf.getvalue()


def _as_dict(obj):
    try:
        if hasattr(obj, "get_object"):
            obj = obj.get_object()
    except Exception:
        return obj
    return obj


def _field_name(annot) -> str:
    try:
        obj = _as_dict(annot)
        name = obj.get("/T")
        if not name and obj.get("/Parent"):
            name = _as_dict(obj.get("/Parent")).get("/T")
        return str(name) if name is not None else ""
    except Exception:
        return ""


def strip_old_copyright_widgets(writer: PdfWriter) -> None:
    for page in writer.pages:
        annots = page.get("/Annots")
        if not annots:
            continue
        kept = [a for a in annots if _field_name(a) != FIELD_NAME]
        page[NameObject("/Annots")] = ArrayObject(kept)

    root = writer._root_object
    acro = _as_dict(root.get("/AcroForm"))
    if not acro or not hasattr(acro, "get"):
        return
    fields = acro.get("/Fields")
    if not fields:
        return
    kept_fields = []
    for field in fields:
        try:
            obj = _as_dict(field)
            if str(obj.get("/T") or "") == FIELD_NAME:
                continue
        except Exception:
            pass
        kept_fields.append(field)
    acro[NameObject("/Fields")] = ArrayObject(kept_fields)


def attach_openaction(writer: PdfWriter, javascript: str) -> None:
    action = DictionaryObject()
    action[NameObject("/Type")] = NameObject("/Action")
    action[NameObject("/S")] = NameObject("/JavaScript")
    action[NameObject("/JS")] = TextStringObject(javascript)
    writer._root_object[NameObject("/OpenAction")] = action


def add_footer_widget(writer: PdfWriter, page, rect: list[float], value: str) -> None:
    widget = DictionaryObject()
    widget[NameObject("/Type")] = NameObject("/Annot")
    widget[NameObject("/Subtype")] = NameObject("/Widget")
    widget[NameObject("/FT")] = NameObject("/Tx")
    widget[NameObject("/T")] = TextStringObject(FIELD_NAME)
    widget[NameObject("/V")] = TextStringObject(value)
    widget[NameObject("/DV")] = TextStringObject(value)
    widget[NameObject("/Ff")] = NumberObject(1)  # ReadOnly
    widget[NameObject("/F")] = NumberObject(4)  # Print
    widget[NameObject("/Q")] = NumberObject(1)  # centered
    widget[NameObject("/DA")] = TextStringObject("/Helv 8 Tf 0.28 0.28 0.28 rg")
    widget[NameObject("/MK")] = DictionaryObject(
        {
            NameObject("/BC"): ArrayObject(),
            NameObject("/BG"): ArrayObject(
                [FloatObject(0.984), FloatObject(0.969), FloatObject(0.941)]
            ),
        }
    )
    widget[NameObject("/Rect")] = ArrayObject([FloatObject(v) for v in rect])
    annot = writer._add_object(widget)
    page.setdefault(NameObject("/Annots"), ArrayObject())
    if not isinstance(page[NameObject("/Annots")], ArrayObject):
        page[NameObject("/Annots")] = ArrayObject(page[NameObject("/Annots")])
    page[NameObject("/Annots")].append(annot)


def stamp(src: Path, dest: Path, start: int, owner: str, legal: str) -> dict:
    if start < 1900 or start > 2200:
        raise SystemExit(f"Refusing start year {start}")
    owner = strip_class_a(owner) or DEFAULT_OWNER
    if any(ord(char)<32 for char in owner):
        raise ValueError('Owner must not contain control characters')
    year = date.today().year
    text = notice_text(start, year, owner)
    reader = PdfReader(BytesIO(remove_prior_notices(src)))
    writer = PdfWriter()
    writer.append(reader)
    strip_old_copyright_widgets(writer)

    for page in writer.pages:
        box = page.mediabox
        width = float(box.width)
        height = float(box.height)
        if stringWidth(text, 'Helvetica', FOOTER_PT)>width-72:
            raise ValueError('Notice exceeds available footer width; use a wider page or shorter owner')
        overlay = PdfReader(BytesIO(cover_and_paint(width, height, text)))
        page.merge_page(overlay.pages[0])
        margin = max(36.0, width * 0.08)
        rect = [margin, 14.0, width - margin, 36.0]
        add_footer_widget(writer, page, rect, text)

    js = open_js(start, owner)
    writer.set_need_appearances_writer(True)
    writer.add_js(js)
    attach_openaction(writer, js)
    acro = _as_dict(writer._root_object.get("/AcroForm"))
    if acro is None:
        acro = DictionaryObject()
        writer._root_object[NameObject("/AcroForm")] = acro
    field_refs = ArrayObject(list(acro.get("/Fields") or []))
    for page in writer.pages:
        for annot in page.get("/Annots") or []:
            if _field_name(annot) == FIELD_NAME and annot not in field_refs:
                field_refs.append(annot)
    acro[NameObject("/Fields")] = field_refs
    acro[NameObject("/NeedAppearances")] = BooleanObject(True)

    meta_title = None
    if reader.metadata:
        meta_title = reader.metadata.get("/Title")
    writer.add_metadata(
        {
            "/Producer": legal,
            "/Creator": legal,
            "/Copyright": text,
            "/Title": meta_title or src.stem,
        }
    )

    output = BytesIO()
    writer.write(output)
    verify_single_notice(output.getvalue())
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(output.getvalue())

    return {
        "input": str(src),
        "output": str(dest),
        "pages": len(writer.pages),
        "start": start,
        "year": year,
        "notice": text,
        "field": FIELD_NAME,
    }


def default_out(src: Path) -> Path:
    artifacts = Path("./artifacts")
    name = src.stem
    if not name.endswith("-copyright"):
        name = f"{name}-copyright"
    target_dir = artifacts if artifacts.exists() else src.parent
    return target_dir / f"{name}{src.suffix}"


def main() -> int:
    args = parse_args()
    src = args.input.expanduser().resolve()
    if not src.is_file():
        print(f"missing input: {src}", file=sys.stderr)
        return 1
    dest = src if args.overwrite else (args.out.expanduser().resolve() if args.out else default_out(src))
    info = stamp(src, dest, args.start, args.owner, args.legal)
    print(info["output"])
    print(f"pages={info['pages']} start={info['start']} year={info['year']}")
    print(info["notice"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
