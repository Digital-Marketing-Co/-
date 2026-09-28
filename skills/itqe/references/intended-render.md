# Intended-render sweep — after the document is complete

`/itqe` plus `/latex` do not end when the builder writes a file. After completion, scan the **entire** document for two classes of defect

1. Uncompiled source — LaTeX, AMS-TeX, KaTeX, TeX, MathJax still visible as source
2. Failed clips — a region that was meant to be a mathematical symbol but printed a box, a replacement character, a boxed X, tofu, a truncated plate, or any other glyph that is not what the author intended

The second class is why `R = ☒L/A` is a fail even when no backslash remains. The intended output is ρ. The printed clip is a ballot box with X. That is not the mathematics.

## When this pass runs

- After `/folio`, `/phd`, `/deep`, `/print`, `/atlas`, `/images`, `/banner`, `/copyright`, or any other stacked builder writes a PDF, DOCX, PPTX, XLSX, HTML view, or printable JSON
- After a user pastes a screenshot or page crop that already shows a box, tofu, or glitched symbol
- Whenever `/itqe` or `/latex` is invoked on an existing file

Do not sample “the math pages.” Title leaf, notes, bibliography, colophon, banners, figure captions, and ITQE cells count.

## What to identify

Treat all of the following as the same family — source that never became the intended glyph

- `$...$`, `$$...$$`, `\(...\)`, `\[...\]`
- Command source left on the page (`\rho`, `\times`, `\frac`, `\sum`, `\mathrm`, `\begin`)
- Visible KaTeX or MathJax source (`katex.render`, `[tex]`, MathJax delimiters)
- U+FFFD replacement character
- Ballot box with X (U+2612 ☒) used as a math stand-in
- Empty or filled squares used as missing glyphs (☐ □ ■ ◻ ▣ ⬜ ▢ ▤)
- Runs of empty rectangles
- A plate whose visible character does not match the hidden `tex` sibling
- An Identifier cell that prints “rho”, “theta”, or a box instead of ρ, θ, or the plate glyph
- ASCII-TeX identifiers left on a visible page or in an ITQE cell (`I_tot`, `B_k`, `p^bi`, `Λ_int`, `P_30`). Print compiled Unicode (`Iₜₒₜ`, `Bₖ`, `P₃₀`, `Λᵢₙₜ`) or a compiled snippet figure
- A body face that cannot draw the identifier (Λ or ₀ printing as an empty box). Switch that span to a proven face (DejaVu Serif / Latin Modern) and raster the page again
- Clipped or overlapping operators so ×, ·, or a fraction bar is unreadable

## Commands

```bash
python3 /home/workdir/.grok/skills/latex/scripts/harvest_raw_tex.py \
  /home/workdir/artifacts/<slug> \
  --out /home/workdir/artifacts/<slug>/latex-inventory.jsonl

python3 /home/workdir/.grok/skills/itqe/scripts/scan_render_gate.py \
  /home/workdir/artifacts/<slug> \
  --also-pdf /home/workdir/artifacts/<file>.pdf

python3 /home/workdir/.grok/skills/latex/scripts/scan_raw_tex.py \
  /home/workdir/artifacts/<slug> \
  --also-pdf /home/workdir/artifacts/<file>.pdf --pages

pdftoppm -png -r 140 /home/workdir/artifacts/<file>.pdf /tmp/itqe-page
```

Exit code 1 from either scan is a hard stop. A raster page that shows ☒, □, tofu, or a symbol that is not the intended one is also a hard stop even if the text extract missed it.

## Repair order

1. Name the intended glyph from the `tex` sibling, the surrounding sentence, or the ITQE Identifier that should have been printed
2. Compile that snippet with `/latex` `render_snippet.py` using Latin Modern (or another face proven to contain the glyph)
3. Embed the plate or proven Unicode. Never screenshot a checkerboard
4. Fill Identifier-Term-Quantity-Explanation with compiled glyphs, not Latin spellings and not boxes
5. Rebuild
6. Sweep every page again
7. Deliver only when the printed clip is the intended mathematics

## Chat vs files

Chat may still use KaTeX. Files may not show KaTeX source. Files must show the intended compiled symbol.
