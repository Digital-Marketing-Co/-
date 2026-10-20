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
- Visible house anchor is Digital Marketing Company Target is https://DigitalMarketingCo.org. Plain-text domain is DigitalMarketingCo.org.
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


## v2.2.0 — mandatory Ivy-style physics typography and visual QA (2026-10-20)

- For new doctoral physics/math research PDFs, enforce Computer Modern Roman and Computer Modern mathematics under pdfLaTeX; under LuaLaTeX/XeLaTeX use Latin Modern Roman and Latin Modern Math, preserving their coordinated mathematical glyphs. Do not claim a statistically established single most popular Ivy League font. Check actual font embedding and warn on fallback.
- Default body type 12 pt (11.5 pt only with an explicitly supported class), generous line leading, optical kerning and microtypography; use a coherent scholarly hierarchy. Do not silently distort fonts.
- Guarantee whitespace before each table: target 18 pt, acceptable 16–20 pt, absolute minimum 12 pt after preceding prose/equation. Target at least 14 pt after tables. Apply through robust table wrappers, not ad hoc negative vspace. For tables immediately following equations, preserve both display-math spacing and table clearance.
- Keep captions, headings, equation-audit labels, and their respective tables together where feasible; avoid orphan headings, widows, overfull/underfull boxes, clipped math, overlapping footers and tables. Long tables must break safely with repeated headers.
- Fractions must use true typeset \\frac or \\dfrac with centered numerator above denominator; never approximate stacked fractions with plain text or slashes when display math is intended.
- Maintain citations in first-appearance numerical order, renumbering cross-references and bibliography together on every revision.
- Never append previously rendered PDF pages with a second active header/footer overlay. Prefer recompiling the unified source; if archival PDF inclusion is essential, disable overlays and verify page numbering and copyright placement.
- QA gate: compile; check log for missing glyphs, overfull boxes and undefined references; rasterize every page; visually inspect each page for table spacing, typography, collisions, fractions, margins and citation order; fix and repeat until passed. Never report a pass without actual inspection.
- Preserve all existing skill quality-profile and regression requirements; these additions are cumulative, not replacements.


## v2.2.1 — borderless, functional PDF hyperlinks (2026-10-20)

- Preserve working clickable hyperlinks, URLs, DOI links, cross-references, citations, and table-of-contents navigation in all LaTeX-produced PDFs. Never remove hyperlinks to remove their visual borders.
- Load hyperref late in the preamble (respecting packages that must follow it) and enforce \usepackage[hidelinks]{hyperref} for a neutral, borderless default, or equivalently \hypersetup{hidelinks,pdfborder={0 0 0},colorlinks=false}. For a deliberately colored-link style, use \hypersetup{colorlinks=true,linkcolor=navy,urlcolor=navy,citecolor=navy,pdfborder={0 0 0}}; do not rely on viewer-specific border behavior. Never use hyperref's default red-bordered link boxes.
- If hyperref is already loaded, configure with \hypersetup{hidelinks,pdfborder={0 0 0}} rather than loading it twice. Ensure \hypersetup or package options later in the document do not restore colored annotation borders. Explicitly audit pdfborderstyle and link annotation appearance if other PDF tooling modifies annotations.
- QA regression: generate an example PDF containing an external URL, DOI, internal section link, TOC link and citation link; inspect PDF link annotations to confirm each URI/destination remains functional and that border width is zero or no visible border appearance exists. Render pages and confirm there are no red, green or other rectangular link outlines. Some PDF viewers may draw their own focus/hover highlight; distinguish viewer UI from borders embedded in the PDF.
- Reject any compiled artifact with visible hyperlink rectangles, broken destinations, or missing click targets; repair source, recompile, and repeat annotation and visual checks.


## v2.3.0 — mathematical rendering, footer integrity and exhaustive QA
### Mathematical glyphs and indices
- Enforce mathematical subscripts and superscripts as actual math: use x_{i}, E_{\gamma}, m_{\mathrm{eq}}, and braces for compound indices. Escape literal prose underscores as \_. Reject raw TeX markers appearing in rendered output.
- Enforce correct Greek uppercase/lowercase symbols, partial derivatives, integrals, accents, primes, operators and fractions. pdfLaTeX must use supported math macros and Computer Modern; LuaLaTeX/XeLaTeX must use Latin Modern and unicode-math with verified Unicode coverage. Detect missing glyphs, tofu, and incorrect text-vs-math font substitutions.
- Reflow long equations with aligned, split or multline, not illegibly small type. Verify mathematical meaning, visual baseline, superscript/subscript position, and extracted PDF text against source.
### Single copyright and sequential footer folios
- Use one footer authority only. Require exactly one canonical /copyright line on each required page: © 2012–CURRENTYEAR Web Development Corporation. All rights reserved. No duplicate stamps, archival PDF footer overlays or stacked copyright lines.
- Require visible, unique, ordered footer page numbers 1 through N matching physical PDF pages, unless explicitly specified front-matter Roman numerals or intentional resets. Check title pages, appendices, imported pages and blank pages. No missing, duplicated, clipped, or overlapping page numbers.
- Keep footer text and page number within safe margins and on consistent baselines; never collide with main content.
### Mandatory /qa and /qa_visual iterative release gate
- Generate a regression fixture covering nested indices, Greek letters, multiline equations, fractions, tables, references, clickable borderless links, TOC, appendix and multipage transitions.
- Run compile-log QA, glyph/font embedding checks, raw TeX leakage checks, PDF link annotation checks, page-by-page copyright count and folio sequence checks, overflow detection, citation integrity, and equation-to-ITQE audit coverage where applicable.
- Rasterize and visually inspect every page at readable resolution; verify glyph shapes, indices, mathematical alignment, table whitespace, footer placement, absence of link rectangles, and absence of clipping/overlap. Record page-specific failures, repair, recompile and repeat until all resolvable defects are fixed or finite resources are exhausted.
- Release requires zero unresolved mathematical rendering defects, exactly one required copyright per page, sequential visible folios, no red link borders, and clean visual QA. Never mark an unexecuted check as PASSED. Preserve all prior /latex requirements.


## Universal 9491 visual quality and document authority
Apply `skills/references/document-rendering-9491.md` for every document output. This standard adds context-accurate AI-generated imagery with scholarly analytical captions, a single nonduplicated design system, and rigorous iterative /qa plus /qa_visual. The /latex compiler must verify one /copyright footer per required page and continuous sequential footer folios, correct math indices/Greek characters, borderless clickable hyperlinks, and inspect every rendered page. Preserve existing stricter rules; do not report tests as passed unless executed.


## Public-document skill-name non-disclosure and final artifact sanitation
- In synthesized document body, title, abstract, headings, captions, tables, table of contents, indexes, footnotes, bibliography, metadata, PDF bookmarks and accessibility text, NEVER expose names of the internal skills, slash commands, agent workflows, prompt templates or internal QA routines used to produce the artifact. Do not include execution logs, skill provenance, or implementation details in the reader-facing document.
- Apply this only to references to the production process. Preserve names when they are genuine substantive research subjects, correctly attributed source titles, literal quotations required by the user, or explicitly requested methodological disclosures. Do not suppress necessary scientific methodology, AI-generated image attribution, evidence citations, or research limitations.
- Final /latex sanitation must scan the entire compiled source AND exported PDF for skill names and slash directives, including previously authored content and TOC entries, PDF outlines/bookmarks, captions, headers, footers, tables, figure alt text, embedded metadata, and bibliography. Include an extensible registry of known skill aliases from the repository; match case-insensitively with word boundaries and slash prefixes, not naïve substrings that corrupt ordinary words.
- Repair leaked production labels by rewriting into reader-facing scholarly prose, deleting purely operational statements, and regenerating TOC, bookmarks, index, references and PDF. Never simply hide or white-out visible text, which leaves leaked text in PDF extraction.
- Run the sanitizer after all content generation and again after final compilation as the LAST /latex scanning function. Recompile and rescan until no unauthorized skill references remain or disclose unresolved blockers. A source-only scan does not count as a PDF verification.
- For legacy documents, apply the same audit and remediation when their source and PDF are available. Do not claim to have repaired inaccessible past documents.
- QA regression fixture: seed leaked names in ordinary sentences, section headings, TOC entries, captions, bookmarks and metadata, then verify zero unauthorized occurrences after rebuild while preserving genuinely topical mentions and citations.


## Final /negative sanitation gate (mandatory)
- Read the current canonical `skills/negative/SKILL.md` and `skills/negative/references/blocklist.md` at execution time. Use the repository's `skills/negative/scripts/sweep_negative.py` when available. Never rely on a stale, hand-copied list.
- At the end of the /latex workflow, AFTER substantive drafting, math rendering, citation reconciliation, skill-name sanitation and initial PDF compilation, invoke /negative as the final language and presentation scan. Check complete source plus PDF-extracted text, headings, TOC, bookmarks, captions, alt text, metadata, running headers and footers, including previously authored passages that predate /negative enforcement.
- On each match, rewrite the whole affected sentence or heading to natural, precise research prose while retaining its claim, equations, citations, numbers, source attributions, and factual meaning. Rebuild TOC/bookmarks/index and recompile the PDF; rescan both source and PDF. Repeat until clean or report unresolved blockers. Never use whiteout or invisible text.
- Protect verbatim source quotations, proper names, required terminology, canonical copyright text, code/math identifiers and documented exceptions from destructive rewriting; flag irreconcilable collisions for explicit review rather than silently corrupting data.
- Run /negative after all other /latex content changes; if rewriting forces recompilation, rerun /negative on the rebuilt artifact, followed by non-mutating checks of footer uniqueness, sequential page numbers, link annotations, equation rendering and visual layout. Any later content change invalidates the prior /negative pass.
- The final QA record must distinguish verified passes from NOT RUN; do not claim legacy PDFs were repaired unless their actual source and output were processed.
