#!/usr/bin/env python3
"""Stamp a living centered copyright footer onto every page of a PDF."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from io import BytesIO
from pathlib import Path

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


def en_dash_range(start: int, year: int) -> str:
    if year > start:
        return f"{start}\u2013{year}"
    return str(start)


def notice_text(start: int, year: int, owner: str) -> str:
    return f"Copyright \u00a9 {en_dash_range(start, year)} {owner}. All rights reserved."


def open_js(start: int, owner: str) -> str:
    owner_js = owner.replace("\\", "\\\\").replace('"', '\\"')
    return (
        f"var start = {int(start)};"
        "var y = (new Date()).getFullYear();"
        'var range = (y > start) ? (String(start) + "\\u2013" + String(y)) : String(start);'
        "try {"
        f" var f = this.getField('{FIELD_NAME}');"
        f' if (f) f.value = "Copyright \\u00a9 " + range + " {owner_js}. All rights reserved.";'
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
    c.setFont("Helvetica", FOOTER_PT)
    c.drawCentredString(width / 2.0, TEXT_Y, text)
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
    year = date.today().year
    text = notice_text(start, year, owner)
    reader = PdfReader(str(src))
    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception as exc:
            raise SystemExit(f"Encrypted PDF cannot be stamped: {exc}") from exc
    writer = PdfWriter()
    writer.append(reader)
    strip_old_copyright_widgets(writer)

    for page in writer.pages:
        box = page.mediabox
        width = float(box.width)
        height = float(box.height)
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

    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("wb") as fh:
        writer.write(fh)

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
    artifacts = Path("/home/workdir/artifacts")
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
