# Type research for WCA Folio

Locked after comparing long-form scholarly faces available under SIL OFL 1.1 that ReportLab can embed as static TTF.

## What "academic script" means here

A calligraphic *script* face (Snell Roundhand, Edwardian, Pinyon) fails sustained reading, screen zoom, and PDF text extraction. The scholarly meaning of script in this house is the Renaissance humanist construction that Claude Garamond cut for learned books — letterforms derived from chancery writing, not a wedding invitation.

## Faces considered

1. Liberation Serif (prior phd-ivy-monograph). Times metrics. Dense, institutional, tired on cream stock.
2. Gelasio-as-Georgia (prior /deep). Excellent on screens. Already used. Not a revision.
3. EB Garamond. Direct revival of the 1592 Berner specimen. Highest historical authority. Small x-height; weak below 11 pt on screens.
4. Crimson Pro / Crimson Text. Garamond-like faces designed for papers. Good, slightly less optical discipline than Literata.
5. Libre Baskerville. Baskerville carries a published credibility effect. Wide, tall, a little loud for notes.
6. Literata (TypeTogether, Google Play Books). Optical sizes. Cut for hours of reading. Open counters. Strong italic.
7. Cormorant Garamond. Beautiful display, too thin and sharp for body.
8. TeX Gyre Pagella / Schola. Palatino and Century Schoolbook metrics. Strong pedagogy case for Schola, but OFL packaging here is messier than the Google statics.

## Decision

- **Display / title / part heads — EB Garamond.** This is the authoritative academic script face. Use Regular or Medium for titles, Italic for subtitles. Never set body in it below 16 pt.
- **Body, abstract, notes, bibliography — Literata 18pt optical set at 10 / 14.2.** This is the reading face on a compact university-press measure (about 6.55 in, 68–74 characters). v1 Folio 11.5 / 17 is retired. Do not set body in EB Garamond.
- **Chrome — Libre Franklin.** American gothic, high x-height, reserved for kickers, running heads, footers, and the living copyright year so those elements never compete with the text face.

Do not swap families at runtime. Do not introduce a fourth family.
