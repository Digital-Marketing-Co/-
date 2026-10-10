#!/usr/bin/env python3
"""Letter-size Chicago corpus catalog PDF."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from datetime import date

from publication_notice import notice_for

from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

INK = HexColor("#1a1a1a")
RULE = HexColor("#333333")
MUTED = HexColor("#444444")


def register_fonts() -> tuple[str, str]:
    candidates = [
        ("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
         "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"),
        ("/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf",
         "/usr/share/fonts/truetype/liberation2/LiberationSerif-Bold.ttf"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"),
    ]
    for regular, bold in candidates:
        if Path(regular).exists() and Path(bold).exists():
            pdfmetrics.registerFont(TTFont("CorpusSerif", regular))
            pdfmetrics.registerFont(TTFont("CorpusSerif-Bold", bold))
            return "CorpusSerif", "CorpusSerif-Bold"
    return "Times-Roman", "Times-Bold"


def wrap(c, text: str, font: str, size: float, width: float) -> list[str]:
    words = (text or "").split()
    if not words:
        return [""]
    lines: list[str] = []
    cur = words[0]
    for w in words[1:]:
        trial = cur + " " + w
        if c.stringWidth(trial, font, size) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def chicago_line(work: dict) -> str:
    authors = work.get("authors") or []
    names = []
    for i, a in enumerate(authors):
        family = (a.get("family") or "").strip()
        given = (a.get("given") or "").strip()
        if i == 0:
            names.append(f"{family}, {given}".strip(", "))
        else:
            names.append(f"{given} {family}".strip())
    if len(names) == 0:
        by = "Unknown"
    elif len(names) == 1:
        by = names[0]
    elif len(names) == 2:
        by = f"{names[0]} and {names[1]}"
    else:
        by = ", ".join(names[:-1]) + ", and " + names[-1]
    title = (work.get("title") or "Untitled").rstrip(".")
    year = work.get("year") or "n.d."
    venue = work.get("venue") or ""
    pages = work.get("pages") or ""
    doi = work.get("doi")
    wtype = work.get("type") or "article"
    if wtype in {"book", "report", "dissertation"}:
        line = f"{by}. {title}. {venue + '. ' if venue else ''}{year}."
    elif wtype in {"chapter"}:
        line = f"{by}. “{title}.” {venue}. {year}."
    elif wtype == "patent":
        line = f"{by}. {title}. {work.get('patent_number') or 'Patent'}, {year}."
    elif wtype == "grant":
        line = f"{by}. “{title}.” {venue} {work.get('grant_id') or ''}, {year}."
    elif wtype == "trial":
        line = f"{by}. “{title}.” {work.get('nct_id') or ''}, {year}."
    else:
        vol = work.get("volume") or ""
        issue = work.get("issue")
        loc = f"{vol}"
        if issue:
            loc += f", no. {issue}"
        if pages:
            loc += f" ({year}): {pages}"
        elif vol:
            loc += f" ({year})"
        else:
            loc = f"({year})"
        line = f"{by}. “{title}.” {venue} {loc}."
    if doi:
        line += f" https://doi.org/{doi}"
    elif work.get("url"):
        line += f" {work['url']}"
    return line


def draw_footer(c, page: int, data: dict) -> None:
    c.setFillColor(INK)
    c.setFont("CorpusSerif" if "CorpusSerif" in pdfmetrics.getRegisteredFontNames() else "Times-Roman", 8)
    text = notice_for(data)
    c.drawCentredString(letter[0] / 2, 0.45 * inch, text)
    c.drawCentredString(letter[0] / 2, 0.32 * inch, str(page))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("corpus_json")
    p.add_argument("--out", required=True)
    args = p.parse_args()
    data = json.loads(Path(args.corpus_json).read_text(encoding="utf-8"))
    regular, bold = register_fonts()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(out), pagesize=letter)
    c.setTitle(data.get("title") or "Corpus Catalog")
    c.setAuthor(data.get("author") or "Digital Marketing Company")
    c.setSubject("Academic corpus catalog")

    house = data.get("house") or {}
    owner = data.get("owner") or {}
    year = date.today().year
    page = 1
    left = 0.85 * inch
    right = letter[0] - 0.85 * inch
    width = right - left
    top = letter[1] - 0.8 * inch
    bottom = 0.75 * inch

    def new_page() -> float:
        nonlocal page
        if page > 1:
            c.showPage()
        draw_footer(c, page, data)
        page += 1
        return top

    # Title page
    y = new_page()
    c.setFillColor(INK)
    c.setFont(bold, 18)
    for line in wrap(c, data.get("title") or "Corpus Catalog", bold, 18, width):
        c.drawString(left, y, line)
        y -= 22
    subtitle = data.get("subtitle") or data.get("match") or ""
    if subtitle:
        y -= 6
        c.setFont(regular, 12)
        for line in wrap(c, subtitle, regular, 12, width):
            c.drawString(left, y, line)
            y -= 16
    y -= 10
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.line(left, y, right, y)
    y -= 18
    c.setFont(regular, 10)
    meta = [
        data.get("date") or "",
        owner.get("legal") or "Web Development Corporation, a Delaware Corporation",
        f'{house.get("anchor") or "Digital Marketing Company"}  {house.get("href") or "https://digitalmarketingco.org"}',
        f'Plain-text domain {house.get("domain_plain") or "DigitalMarketingCo.org"}',
    ]
    for line in meta:
        c.drawString(left, y, line)
        y -= 14
    identity = data.get("identity") or {}
    y -= 8
    c.setFont(bold, 12)
    c.drawString(left, y, "Resolved identity")
    y -= 16
    c.setFont(regular, 10)
    id_lines = [
        identity.get("heading") or "",
        "Variants: " + "; ".join(identity.get("variants") or []),
        "ORCID: " + (identity.get("orcid") or "not found"),
        "Confidence: " + (identity.get("confidence") or ""),
    ]
    for line in id_lines:
        for wrapped in wrap(c, line, regular, 10, width):
            c.drawString(left, y, wrapped)
            y -= 13
    counts = data.get("counts") or {}
    y -= 8
    c.setFont(bold, 12)
    c.drawString(left, y, "Counts")
    y -= 16
    c.setFont(regular, 10)
    count_line = f"Total unique works: {counts.get('total', len(data.get('works') or []))}"
    c.drawString(left, y, count_line)
    y -= 13
    by_type = counts.get("by_type") or {}
    if by_type:
        text = "By type: " + ", ".join(f"{k} {v}" for k, v in sorted(by_type.items()))
        for wrapped in wrap(c, text, regular, 10, width):
            if y < bottom:
                y = new_page()
            c.drawString(left, y, wrapped)
            y -= 13
    preface = data.get("preface") or ""
    if preface:
        y -= 8
        c.setFont(bold, 12)
        c.drawString(left, y, "Preface")
        y -= 16
        c.setFont(regular, 10)
        for para in preface.split("\n"):
            for wrapped in wrap(c, para, regular, 10, width):
                if y < bottom:
                    y = new_page()
                c.drawString(left, y, wrapped)
                y -= 13
            y -= 6

    # Bibliography
    y = new_page()
    c.setFont(bold, 14)
    c.drawString(left, y, "Bibliography")
    y -= 20
    works = sorted(
        data.get("works") or [],
        key=lambda w: (-int(w.get("year") or 0), (w.get("title") or "").lower()),
    )
    c.setFont(regular, 10)
    for work in works:
        line = chicago_line(work)
        lines = wrap(c, line, regular, 10, width)
        need = 13 * len(lines) + 6
        if y - need < bottom:
            y = new_page()
            c.setFont(regular, 10)
        for i, wrapped in enumerate(lines):
            x = left if i == 0 else left + 0.25 * inch
            c.drawString(x, y, wrapped)
            y -= 13
        y -= 6

    notes = data.get("notes") or []
    if notes:
        y -= 8
        if y < bottom + 40:
            y = new_page()
        c.setFont(bold, 14)
        c.drawString(left, y, "Notes")
        y -= 18
        c.setFont(regular, 10)
        for i, note in enumerate(notes, 1):
            text = note.get("text") if isinstance(note, dict) else str(note)
            lines = wrap(c, f"{i}. {text}", regular, 10, width)
            if y - 13 * len(lines) < bottom:
                y = new_page()
                c.setFont(regular, 10)
            for wrapped in lines:
                c.drawString(left, y, wrapped)
                y -= 13
            y -= 6

    gaps = data.get("gaps") or []
    if gaps:
        if y < bottom + 40:
            y = new_page()
        c.setFont(bold, 14)
        c.drawString(left, y, "Residual gaps")
        y -= 18
        c.setFont(regular, 10)
        for gap in gaps:
            for wrapped in wrap(c, "• " + gap, regular, 10, width):
                if y < bottom:
                    y = new_page()
                    c.setFont(regular, 10)
                c.drawString(left, y, wrapped)
                y -= 13

    # OpenAction living year (best-effort comment in metadata)
    c.setKeywords(f"WCACopyrightYear={year}")
    c.save()
    print(str(out))


if __name__ == "__main__":
    main()
