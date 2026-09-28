# Fail-closed compile gate

No visual document ships while raw TeX, KaTeX source, or missing glyphs remain on a page the reader can see.

## Must-run order

1. Harvest the draft (`harvest_raw_tex.py`).
2. Compile every display hit and every stubborn inline hit (`render_snippet.py` or the target native renderer).
3. Embed plates or proven Unicode. Attach ITQE under every display plate.
4. Build the file.
5. Scan every page (`scan_raw_tex.py --also-pdf <file> --pages`). Exit code 1 blocks delivery.
6. Raster every page (`pdftoppm`). Open every page. Tofu, empty boxes, or a visible backslash command blocks delivery.
7. Only then deliver.

A stacked flag (`/folio`, `/phd`, `/deep`, `/print`, `/images`, `/banner`, `/itqe`, `/ivy-biblio`, docx, pptx, xlsx) does not skip steps 5–6.

## What counts as unrendered source

- `$...$`, `$$...$$`, `\(...\)`, `\[...\]`
- A backslash command the reader would see (`\frac`, `\sum`, `\int`, `\mathrm`, `\times`, `\alpha`, `\text`, `\left`, `\begin`, and the rest of the scanner list)
- KaTeX or MathJax delimiters left in HTML as visible text instead of compiled spans
- U+FFFD, empty rectangles, black boxes, white boxes over glyphs
- A Unicode line that the document face cannot draw (proof-line failure)
- ASCII-TeX identifiers on a visible page (`I_tot`, `B_k`, `p_t^GEM`, `Λ_int`). Compile them to Unicode subscripts/superscripts or to a snippet figure
- White empty boxes, black boxes, or .notdef tofu standing in for the intended scalar, operator, or Greek letter. Identify the intended glyph, compile it, and replace the box

After `scan_raw_tex.py` exits 0, raster **every** page (`pdftoppm -png -r 140`) and walk the rasters. A clean source scan that still shows □_int or B□ on a page is a failed intended-render sweep. Do not deliver.

## Allowed source that must stay off the page

- `equations/*.tex` siblings
- JSON keys `tex`, `latex`, `source`, `preamble`
- Fenced listings whose job is to teach TeX

## Chat versus file

Chat still uses KaTeX. Files do not print the KaTeX source. They print glyphs or a compiled plate.
