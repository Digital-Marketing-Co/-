# All-pages TeX sweep

Raw TeX is a defect on every visible page of a finished file and on every string that a builder will print. Source siblings (`.tex` plates, `tex` keys, fenced listings that teach TeX) are the only exceptions.

## Two targets

1. **Existing document** — a PDF, DOCX, PPTX, HTML file, or already-written `folio.json` / `deep.json` in artifacts. Sweep every page or every printable string. Compile what leaked. Rebuild. Sweep again.
2. **Document about to be produced** — the draft JSON, Markdown, or HTML that a stacked skill will turn into pages. Sweep that draft **before** the builder runs. Do not wait for `pdftoppm` to discover `\frac` on page 14.

## What counts as a visible page

- Each PDF page, including title leaf, notes, bibliography, colophon
- Each Word page after pagination
- Each PowerPoint slide
- Each spreadsheet print area the reader is meant to see
- Each HTML view the reader loads, not the source pane
- Each Folio / Deep / Print JSON string that the builder will draw (`title`, `abstract`, `paragraphs[]` strings, captions, note text, bibliography text)

A page with no intended math still gets scanned. Leaked source often sits in a footer, a caption, or a notes band.

## Allowed raw TeX (not visible)

- `assets/*.tex` and `equations/*.tex` siblings kept for rebuilds
- JSON keys named `tex`, `latex`, `source`, `preamble`
- Fenced `tex` / `latex` code listings whose purpose is to teach source
- This skill’s own scripts

Those files must never be copied onto the page as body type.

## Required order

1. `harvest_raw_tex.py` on the draft or the extracted PDF text
2. `render_snippet.py` for every display or stubborn inline hit
3. Embed the plate or proven Unicode; attach ITQE under every display plate
4. `scan_raw_tex.py --pages` on the built PDF (or the draft JSON if the PDF does not exist yet)
5. `pdftoppm` every page, not a sample of math pages
6. Rebuild until the scan is clean and no page shows tofu, a backslash command, a ballot-box-X stand-in, or any clip that is not the intended symbol
7. Do not deliver, attach, or declare the document finished while step 4 or step 5 still fails, or while a rastered page shows a glitched stand-in instead of the intended mathematics
8. After the document is complete, walk every page again under the `/itqe` intended-render contract (`/home/workdir/.grok/skills/itqe/references/intended-render.md`)

This order is the house compile gate. `/folio`, `/phd`, `/deep`, `/print`, `/images`, `/banner`, `/itqe`, and `/ivy-biblio` inherit it. See `gate.md`.
