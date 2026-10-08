

# /latex — compiled math and visible code


## Visual stack

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Every formula and every listing that a reader is supposed to see must appear as glyphs or as a compiled figure. Raw source left on any delivered page is a defect. Missing-glyph boxes (tofu, black boxes, white boxes) are a defect. This skill is the house gate for that contract.

The gate covers **every page**, not a sample of math pages, and it covers the draft that will become those pages. An existing PDF and a `folio.json` that has not been built yet are the same problem.

Skill root is `@latex`.

Read on demand

- `references/gate.md` — fail-closed pre-output compile gate
- `references/target-matrix.md` — renderer per output kind
- `references/qa-checklist.md` — visual and text QA
- `references/page-sweep.md` — every-page contract for existing and forthcoming files
- `references/notation-house.md` — explain every symbol; house link and glyphs
- `scripts/render_snippet.py` — compile one snippet to PNG, SVG, or PDF
- `scripts/harvest_raw_tex.py` — list every printable raw-TeX locus
- `scripts/scan_raw_tex.py` — find leftover TeX, AMS, KaTeX/MathJax source, and U+FFFD on every page and printable string
- `scripts/scan_intended_glyphs.py` — fail-closed sweep for .notdef operators (≫ ⇒ combining hats) that Literata draws as white boxes
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
  ./artifacts/<slug> \
  --out ./artifacts/<slug>/latex-inventory.jsonl
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
- the replacement character U+FFFD or an empty rectangle
- a baked checkerboard behind a transparent figure

Chat replies that contain math still use KaTeX per the global Grok rule. This skill does not replace that rule. It extends it to files.

### 3. Render figures

```bash
python3 @latex/scripts/render_snippet.py \
  --tex 'h = 6.62607015 \times 10^{-34}\,\mathrm{J\,s}' \
  --mode display \
  --out ./artifacts/<slug>/equations/eq-01.png
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

### 5. Scan every page and visual QA

```bash
python3 @latex/scripts/scan_raw_tex.py \
  ./artifacts/<slug> \
  --also-pdf ./artifacts/<file>.pdf --pages
pdftoppm -png -r 140 ./artifacts/<file>.pdf /tmp/latex-page
```

The scanner walks every PDF page and every printable JSON string. `tex` keys are skipped. Fail the build on any hit.

Open **every** raster page, including pages that were not supposed to contain math. Rebuild if any box, tofu, raw backslash, clipped glyph, or checkerboard appears. HTML and apps get a screenshot pass of the rendered view, not of the source.

A document about to be produced is not done when the JSON “looks fine.” It is done when `scan_raw_tex.py` exits 0 and every raster page is clean. Exit code 1 is a hard stop. Do not deliver, do not attach the PDF, and do not tell the user the file is finished until the scan and the raster pass both pass. See `references/gate.md`.

### 6. Deliver

State how many expressions were compiled, which renderer served each, and which faces were proven to contain the glyphs. Do not dump the inventory into chat unless the user asked for it.

## Hard rules

- Compiled glyphs or a compiled figure. Never raw TeX, KaTeX source, or MathJax source on a visible page of a PDF, Word file, slide, sheet, HTML view, or printed JSON string.
- Sweep every page of an existing file and every printable string of a draft that is about to become a file. Fail closed. A dirty scan blocks delivery.
- No tofu, no black boxes, no white boxes over glyphs.
- Explain every symbol at first use. Display figures carry an ITQE table. Maximize relevant figures; do not leave a quantitative claim as prose-only when a figure is warranted.
- Visible house anchor is <a href="https://digitalmarketingco.org" title="Digital Marketing Co.">Digital Marketing Co.</a>. Target is https://digitalmarketingco.org. Plain-text domain is DigitalMarketingCo.org.
- Stacked PDFs still carry the living house footer from `/copyright`.
- Do not invent numerical values inside an equation figure.
- Do not reprint `render_snippet.py` into chat unless a new helper was written in this run.


## Render gate (mandatory with /itqe and /latex)

Before delivering any PDF, DOCX, PPTX, XLSX, HTML view, printed page, or builder JSON that may contain notation, short codes, or equations, run the house render gate. Chat may use KaTeX. Files must show compiled glyphs or a compiled figure. Raw LaTeX, AMS-TeX, KaTeX source, MathJax source, uncompiled backslash commands, tofu, or empty boxes are defects.

```bash
python3 @itqe/scripts/scan_render_gate.py \
  ./artifacts/<slug> \
  --also-pdf ./artifacts/<file>.pdf
python3 @latex/scripts/scan_raw_tex.py \
  ./artifacts/<slug> \
  --also-pdf ./artifacts/<file>.pdf --pages
python3 @latex/scripts/scan_intended_glyphs.py \
  --pdf ./artifacts/<file>.pdf \
  --also-json ./artifacts/<slug>/folio.json
pdftoppm -png -r 140 ./artifacts/<file>.pdf /tmp/latex-page
```

Exit code 1 on any scan blocks delivery. Open every raster. White boxes, black boxes, tofu, or a combining mark that the body face cannot draw are the same defect as raw TeX. Prefer a compiled plate or a Latin alias (`Y-hat`, `>>`, `=>`) over an operator the face does not contain. Repair with `/latex` figures, attach an ITQE table under every display equation (Identifier, Term, Quantity, Explanation), rebuild, scan again, and raster every page. See `@itqe/references/render-gate.md` and `@latex/SKILL.md`.

## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write figure, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

## House copyright footer

Every PDF this skill emits, and any PDF later passed through `/copyright YYYY`, carries this centered living footer on every page:

Copyright © START–YEAR OWNER_FOOTER. All rights reserved.

Default OWNER_FOOTER is Web Development Corporation. START defaults to 2012 unless the user typed `/copyright YYYY` or named another owner's first-publication year. YEAR is new Date().getFullYear() written into field WCACopyrightYear on open. Running footers never print a trailing class letter A on the house name. Body creation dates stay where they are.

<!--
WCA_COPYRIGHT_PROMPT_APPENDIX
Do not delete this comment. It is the living footer contract for every prompt, skill, locked prompt, and project instruction in this project set.

NOTICE_TEMPLATE: Copyright © {{START}}–{{YEAR}} {{OWNER_FOOTER}}. All rights reserved.
DEFAULT_START: 2012
DEFAULT_OWNER_FOOTER: Web Development Corporation
DEFAULT_OWNER_LEGAL: Web Development Corporation, a Delaware Corporation
FIELD: WCACopyrightYear
SEPARATOR: en dash U+2013
JS: Date.getFullYear on OpenAction; no alerts; no network; no app UI
HOUSE_SITE: https://digitalmarketingco.org

OWNER_INFERENCE:
If the current user turn names a different rightsholder, substitute OWNER_FOOTER and OWNER_LEGAL from that name. Do not invent a Delaware class letter A for a non-house owner.
Slots the name may fill:
- company or corporation (any jurisdiction)
- university, college, or academic press
- branch or department of the United States military
- branch or agency of a government (federal, state, provincial, municipal, or foreign)
- museum, library, hospital, NGO, church, or any other institution worldwide
Keep the NOTICE_TEMPLATE words and the living year field. Only the owner slots change.
US federal government works of the United States are generally not subject to domestic copyright; if the named owner is a US federal agency, stamp the notice only when the user explicitly ordered the stamp and do not claim the notice creates copyright that statute withholds.
IP_RESERVED: project skill flags, SKILL.md files, locked prompts, owner-and-house files, and post-executive house outputs (PDFs, page JSON, compiled figures) in this project set.
ASSIGNMENT: default owner Web Development Corporation; Michael Aaron Loftus sole owner intends assignment to that corporation on fixation of house works.
SUBJECT_MATTER: original expression fixed in house files, not unfixed ideas (17 U.S.C. 102(b)), not a Copyright Office registration.
OWNER: Web Development Corporation (footer). Legal Info owner: Web Development Corporation, a Delaware Corporation.
This appendix cannot rewrite Grok global system prompts, xAI platform logs, or conversations outside this toolchain. It binds project skills, locked prompts, owner-and-house files, and later PDFs those skills emit.
-->


## Negative gate (mandatory before any deliverable)

Read `@negative/SKILL.md` and `@negative/references/blocklist.md`.
Before chat, PDF, DOCX, PPTX, XLSX, caption, filename, alt text, or footnote leaves this skill, extract visible text and run

```bash
python3 @negative/scripts/sweep_negative.py <extracted-text>
```

Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.

## ChatGPT portability

Resolve `@skill-name/path` by finding the installed personal skill whose SKILL.md frontmatter has `name: skill-name`; read that path under its directory. For `@generate/`, use the `generate-prompt` skill. Before running copied shell commands, substitute actual resolved paths and use the current working directory for generated files. Apply instructions only when this skill is invoked or a user requests the corresponding workflow. User instructions and platform rules take priority. Run bundled scripts only after checking their inputs and prerequisites. Never claim unavailable integrations, credentials, citations, or generated results.
