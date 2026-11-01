# I-Spy PDF stack

After `inventory.json` and the H0/H1 catalog exist, compile one public letter-size PDF. Do not emit four separate public books. One work folder. One deliverable PDF.

Work folder stays `./artifacts/ispy-<slug>/`.
Public PDF is `./artifacts/ispy-<slug>/<Title_Slug>.pdf`.

## Seed

The closed corpus is

- `source` plus extension
- `inventory.json`
- the pane catalog
- the readable-text list in reading order
- H0 and the fail-closed H1 test

Do not add objects the pixels do not support. Do not diagnose the occupant.

## Skill order

1. `/breakdown` — every inventory `name` token and every exact `readable_text` token that is a word. Write `breakdown.json`. One morphology section per token. Do not invent words that are not in the inventory.
2. `/decode` — only the concatenated readable-text corpus plus object-id slugs as a closed string. Write `decode/analysis.json`. Keep the ispy H1 rule. A Zipf or n-gram outlier is not a second plaintext.
3. `/iterate` — treat the catalog plus breakdown plus decode as the topic set. Expand object classes, materials, and printed brands with primary sources. Stop when two empty rounds occur or when new claims would require invented objects.
4. `/book` — chapter the iterated corpus. Suggested body chapters — Container and grid. Pane catalog. Object classes. Readable text. Morphology of names. Decode battery. H0 ordinary display. H1 fail-closed test. Do not reprint the same paragraph in two chapters.
5. `/deep` — emit the long Georgia research body from that chapter plan into `deep.json`. Lock Georgia type from the deep skill. Do not invent a second title.
6. `/banner` — one 16-9 full-bleed banner per body section and per subsection. Prompt only from named objects in that node. After generate, run `banner/scripts/apply_tb_alpha_blend.py`.
7. `/images` — mid-section figures on the 500-word cadence. Same 16-9 geometry and top-bottom alpha blend. Unique path and unique bytes.
8. `/wca-ivy-biblio` — first-appearance Chicago notes, remapped bibliography, ITQE table under every display equation.
9. `/copyright` — living footer on every page. Default owner Web Development Corporation. START 2012 unless the user typed a year.

Then rebuild through the book or deep builder that owns `book.json` / `deep.json`. Scan with `/latex` and `/itqe` render gates before delivery.

## Banners and figures

Follow the upgraded `/banner` and `/images` contracts.

- Landscape 16-9.
- Full bleed left and right. x = 0. Zero side gutter.
- Pictorial interior stays opaque.
- Top and bottom only receive a real alpha gradient that lets the page paper show through.
- Never bake a checkerboard into RGB.
- No photoreal portrait of a private person. If the source photo contains a living person, banners reconstruct objects and architecture, not the sitter's face.

## Chat versus PDF

Chat still prints the pane catalog and H0/H1 first so the user can read the inventory without waiting on the book. The PDF is the stacked deliverable, not a substitute for the catalog.

If the user only asked to edit this skill and supplied no image, stop after the skill files exist.
