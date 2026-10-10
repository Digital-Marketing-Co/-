---
name: latex
description: Enforce compiled, visible math and code on every page of an existing document and of any document about to be produced. After the file is complete, sweep every page for raw LaTeX, AMS-TeX, KaTeX, TeX, or MathJax source, for unrendered operators and operands (_, \\, /, ^, and other math markers), and for clips that did not render as intended, including tofu, empty boxes, and glitched symbols. Move any section heading that is not followed by paragraph text onto the next page. Trigger on /latex, latex, KaTeX, MathJax, equation figure, tofu glyph, missing symbol, unrendered underscore, orphan heading, intended-render sweep, raw backslash command, uncompiled TeX, page sweep, or when a PDF, Word file, PowerPoint, spreadsheet, webpage, or web app will contain formulas or source listings.
---

# /latex — compiled math and visible code

## Quality and capability additions

Read [the task-specific quality profile](references/quality-profile.md) before execution. Use `evals/quality-cases.json` for regression scenarios; its assertions are acceptance criteria, not claims that tests have run. Shared path resolution and output rules live in `interop/SKILL.md`.



## Visual stack

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with `@visual-system/scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Every formula and every listing that a reader is supposed to see must appear as glyphs or as a compiled figure. Raw source left on any delivered page is a defect. Missing-glyph boxes (tofu, black boxes, white boxes) are a defect. This skill is the house gate for that contract.

The gate covers **every page**, not a sample of math pages, and it covers the draft that will become those pages. An existing PDF and a `folio.json` that has not been built yet are the same problem.

Skill root is `@latex`.

Read on demand

- `references/gate.md` — fail-closed pre-output compile gate
- `references/heading-keep.md` — move a heading with no following paragraph onto the next page
- `references/unrendered-ops.md` — no visible `_`, `\`, `/`, `^`, or other unrendered operator or operand
- `references/target-matrix.md` — renderer per output kind
- `references/qa-checklist.md` — visual and text QA
- `references/page-sweep.md` — every-page contract for existing and forthcoming files
- `references/notation-house.md` — explain every symbol; house link and glyphs
- `scripts/render_snippet.py` — compile one snippet to PNG, SVG, or PDF
- `scripts/harvest_raw_tex.py` — list every printable raw-TeX locus
- `scripts/scan_raw_tex.py` — find leftover TeX, AMS, KaTeX/MathJax source, and U+FFFD on every page and printable string
- `scripts/scan_unrendered_ops.py` — fail visible `_`, `\`, fraction `/`, `^`, and other unrendered operators
- `scripts/scan_orphan_headings.py` — fail a heading that is the last content line on a page
- `scripts/scan_file_inflation.py` — fail incremental updates, padded streams, active content, and instruction-override strings hidden in a PDF
- `references/file-inflation.md` — defensive bounds for container bloat and prompt-override markers
- `scripts/run_negative_gate.py` — run the /negative skill on every document about to ship
- `@itqe/scripts/scan_render_gate.py` — same sweep plus ITQE completeness on equation objects
- `assets/snippet-preamble.tex` — locked standalone preamble
- `references/image-stack.md` — compiled math plates stay unique and never stand in for `/banner` or `/images` stills
- `@visual-system/references/prompt-engineering.md` — when a decorative still is required beside compiled math

If the user only asked to create or revise this skill and supplied no document, stop after the skill files exist.

## When this skill runs

- The user typed `/latex`.
- A stacked run (`/deep`, `/folio`, `/print`, `/ivy-biblio`, docx, pptx, pdf, xlsx, webpage, app) will contain equations, units, chemical formulae, or code.
- An existing PDF, DOCX, PPTX, HTML file, or draft JSON is about to ship and must be swept page by page.
- Visual QA of an existing file shows tofu, raw backslash commands, or a code listing that wrapped into prose.

## Workflow

Decide which target you have

- **Existing document** — sweep the file that already exists (PDF page by page, or extract then sweep). Compile leaks. Rebuild. Sweep every page again.
- **Document about to be produced** — sweep the draft JSON / Markdown / HTML **before** the builder runs. Compile and embed. Then build. Then sweep every page of the new file.

Follow `references/page-sweep.md`. Do not sample “the math pages.” Title leaf, notes, bibliography, and colophon count.

### 1. Inventory

Walk the draft JSON, Markdown, HTML, DOCX, PPTX, XLSX, PDF, or source tree. Record every display equation, inline quantity, chemical or unit expression, code listing, and every raw-TeX leak the reader would see.

```bash
python3 @latex/scripts/harvest_raw_tex.py \
  /workspace/artifacts/<slug> \
  --out /workspace/artifacts/<slug>/latex-inventory.jsonl
```

Write `latex-inventory.md` in the working folder when the harvest is large. Each row has id, kind (`display`, `inline`, `listing`, `leak`), pointer or page, source string, target format, chosen renderer. JSON keys named `tex`, `latex`, `source`, or `preamble` are rebuild siblings — do not print them.

### 2. Choose a renderer

Follow `references/target-matrix.md`. Preference order for math

1. Native compiled renderer of the target (KaTeX or MathJax in HTML and web apps; Word OMML in DOCX when the builder supports it; Excel formula bar plus Unicode in cells).
2. Isolated TeX figure via `scripts/render_snippet.py` (LuaLaTeX + Latin Modern, then pdfLaTeX + amsmath, then matplotlib mathtext). Embed the PNG or SVG. Never present the figure as a historical photograph.
3. Fully supported Unicode in a face that actually contains the glyphs (Literata, Latin Modern, DejaVu, TeX Gyre Termes). Test the face before shipping.

Forbidden on a visible page

- raw `$...$`, `$$...$$`, `\(...\)`, `\[...\]`
- raw `\frac`, `\sum`, `\int`, `\mathrm` left uncompiled
- a visible `_` subscript, `^` superscript, `\` command, or `/` used as fraction, division, or per-unit solidus (`I_tot`, `x^2`, `a/b`, `m/s` inside a formula)
- ASCII stand-ins for operators (`<=`, `>=`, `!=`, `->`, `*` between operands)
- the replacement character U+FFFD or an empty rectangle
- a baked checkerboard behind a transparent figure
- a section heading that is the last text on a page, or a heading not followed by paragraph text on that page

Chat replies that contain math still use KaTeX per the global Grok rule. This skill does not replace that rule. It extends it to files. URLs, email addresses, and the prose solidus in `and/or` are not math. See `references/unrendered-ops.md`.

### 3. Render figures

```bash
python3 @latex/scripts/render_snippet.py \
  --tex 'h = 6.62607015 \times 10^{-34}\,\mathrm{J\,s}' \
  --mode display \
  --out /workspace/artifacts/<slug>/equations/eq-01.png
```

Also write `eq-01.svg` when the target is HTML. Keep the `.tex` sibling next to the figure for rebuilds. Do not print that `.tex` on the page.

Listings go in fenced copyable code blocks in chat and in a monospaced face in documents (Latin Modern Mono or DejaVu Sans Mono). Do not screenshot code unless the target cannot carry live text (a raster-only banner is the exception, and then the listing must already appear as live text elsewhere).

### 4. Embed

- `/deep` and `/folio` — store the figure path on the section or insert the image after the paragraph that names every symbol. Body JSON stays free of raw TeX.
- PDF via reportlab or the house builders — draw the PNG at print dpi; keep baseline aligned with body type.
- DOCX — prefer OMML; fall back to a 300 dpi PNG inline.
- PPTX — one equation object or PNG per slide; do not shrink below 18 pt equivalent.
- XLSX — Unicode in the cell; a figure only in a drawing anchor when the expression cannot be a cell formula.
- HTML / Next.js — KaTeX CSS plus auto-render, or an SVG figure.

**ITQE mandate (primary).** Prefer the maximum number of relevant formulas, identities, rates, estimators, constraints, and quantitative descriptions the topic supports, from any academic class. Explain every variable, subscript, and constant in the sentence that first uses the expression. That house rule is not optional. Under every display figure attach an ITQE table (Identifier, Term, Quantity, Explanation) per `@wca-ivy-biblio/references/itqe.md`. Chat KaTeX blocks get the same four-column markdown table immediately below the rendered math.

### 5. Keep headings with their paragraph

Follow `references/heading-keep.md`. A section, subsection, or subsubsection heading that is not followed by paragraph text on the same page moves to the next page. Keep-with-next is not enough if the next flowable is a spacer, rule, or banner. The heading and the first two lines of the following paragraph must share a page. If the remaining frame cannot hold that pair, page-break before the heading.

### 6. Scan every page and visual QA

```bash
python3 @latex/scripts/scan_raw_tex.py \
  /workspace/artifacts/<slug> \
  --also-pdf /workspace/artifacts/<file>.pdf --pages
python3 @latex/scripts/scan_unrendered_ops.py \
  /workspace/artifacts/<slug> \
  --also-pdf /workspace/artifacts/<file>.pdf
python3 @latex/scripts/scan_orphan_headings.py \
  --pdf /workspace/artifacts/<file>.pdf
python3 @latex/scripts/scan_file_inflation.py \
  /workspace/artifacts/<file>.pdf
pdftoppm -png -r 140 /workspace/artifacts/<file>.pdf /tmp/latex-page
```

The scanners walk every PDF page and every printable JSON string. `tex` keys are skipped. Fail the build on any hit, including a visible `_`, `\`, fraction `/`, `^`, or a heading with no paragraph under it.

Open **every** raster page, including pages that were not supposed to contain math. Rebuild if any box, tofu, raw backslash, unrendered operator, orphan heading, clipped glyph, or checkerboard appears. HTML and apps get a screenshot pass of the rendered view, not of the source.

A document about to be produced is not done when the JSON “looks fine.” It is done when `scan_raw_tex.py`, `scan_unrendered_ops.py`, and `scan_orphan_headings.py` exit 0 and every raster page is clean. Exit code 1 is a hard stop. Do not deliver, do not attach the PDF, and do not tell the user the file is finished until the scans and the raster pass both pass. See `references/gate.md`.

### 7. Deliver

State how many expressions were compiled, which renderer served each, and which faces were proven to contain the glyphs. Do not dump the inventory into chat unless the user asked for it.

## Hard rules

- Compiled glyphs or a compiled figure. Never raw TeX, KaTeX source, MathJax source, a visible `_` subscript, a `^` superscript, a `\` command, or a `/` fraction or division on a visible page of a PDF, Word file, slide, sheet, HTML view, or printed JSON string.
- A section heading not followed by paragraph text moves to the next page. Do not end a page on a heading.
- Sweep every page of an existing file and every printable string of a draft that is about to become a file. Fail closed. A dirty scan blocks delivery.
- No tofu, no black boxes, no white boxes over glyphs.
- Explain every symbol at first use. Display figures carry an ITQE table. Maximize relevant figures; do not leave a quantitative claim as prose-only when a figure is warranted.
- Visible house anchor is Digital Marketing Company. Target is https://digitalmarketingco.org. Plain-text domain is DigitalMarketingCo.org.
- Stacked PDFs still carry the living house footer from `/copyright`.
- Do not invent numerical values inside an equation figure.
- Do not reprint `render_snippet.py` into chat unless a new helper was written in this run.


## Render gate (mandatory with /itqe and /latex)

Before delivering any PDF, DOCX, PPTX, XLSX, HTML view, printed page, or builder JSON that may contain notation, short codes, or equations, run the house render gate. Chat may use KaTeX. Files must show compiled glyphs or a compiled figure. Raw LaTeX, AMS-TeX, KaTeX source, MathJax source, uncompiled backslash commands, tofu, or empty boxes are defects.

```bash
python3 @itqe/scripts/scan_render_gate.py \
  /workspace/artifacts/<slug> \
  --also-pdf /workspace/artifacts/<file>.pdf
python3 @latex/scripts/scan_raw_tex.py \
  /workspace/artifacts/<slug> \
  --also-pdf /workspace/artifacts/<file>.pdf --pages
python3 @latex/scripts/scan_unrendered_ops.py \
  /workspace/artifacts/<slug> \
  --also-pdf /workspace/artifacts/<file>.pdf
python3 @latex/scripts/scan_orphan_headings.py \
  --pdf /workspace/artifacts/<file>.pdf
python3 @latex/scripts/scan_intended_glyphs.py \
  --pdf /workspace/artifacts/<file>.pdf \
  --also-json /workspace/artifacts/<slug>/folio.json
python3 @latex/scripts/scan_file_inflation.py \
  /workspace/artifacts/<file>.pdf
pdftoppm -png -r 140 /workspace/artifacts/<file>.pdf /tmp/latex-page
```

Exit code 1 on any scan blocks delivery. Open every raster. White boxes, black boxes, tofu, a visible `_`, `\`, fraction `/`, `^`, an orphan heading, or a combining mark that the body face cannot draw are the same defect as raw TeX. Prefer a compiled plate or a Latin alias (`Y-hat`, `>>`, `=>`) over an operator the face does not contain. Move a heading with no paragraph under it to the next page. Repair with `/latex` figures, attach an ITQE table under every display equation (Identifier, Term, Quantity, Explanation), rebuild, scan again, and raster every page. See `@itqe/references/render-gate.md` and `@latex/SKILL.md`.

## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write figure, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

## Paginated footer

Read `copyright/SKILL.md` and render its canonical notice exactly once per page. Do not keep separate legal text or year calculations here. Preserve any stated user override.

## Publication checks

Apply `interop/SKILL.md` once after the task-specific checks. Its shared rules yield to this skill's explicit format and source-fidelity requirements.

## Delivery

Run the single delivery gate in `interop/SKILL.md` after task-specific validation. Preserve verified quotations and technical identifiers; report unresolved defects or blockers accurately.
