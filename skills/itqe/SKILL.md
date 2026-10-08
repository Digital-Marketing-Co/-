---
name: itqe
description: Emit Interactive Tables of Quantitative Elements under every display equation or ranked quantitative inventory, and run the fail-closed render gate so no raw LaTeX, AMS-TeX, KaTeX, TeX, or MathJax source reaches a delivered page. After the document is complete, scan every page and every printable string for uncompiled source and for clips that did not render as intended, including missing symbols, tofu, ballot-box-X stand-ins, empty boxes, and glitched glyphs that are not the symbol the author meant. Trigger on /itqe, ITQE table, render gate, scan_render_gate, intended-render sweep, missing symbol, tofu glyph, quantitative elements table, collapsible variable table, Greek-letter legend, or when folio, phd, deep, banner, copyright, latex, ivy-biblio, print, atlas, images, or psychoanalyze must attach Identifier-Term-Quantity-Explanation figures and sweep uncompiled math. Distinct from the fiscal Imputed Tax Quantitative Easing white paper of the same acronym.
metadata:
  type: workflow
  version: "1.7"
  flag: /itqe
  stacks: folio, phd-ivy-monograph, deep, banner, copyright, latex, wca-ivy-biblio, atlas, images, print, psychoanalyze, decode, article-clip-pdf, extract-dir
  owner: Web Development Corporation
  house_acronym: Interactive Table of Quantitative Elements
  fiscal_homonym: Imputed Tax Quantitative Easing
  visual_stack: visual-system
---

# /itqe — Interactive Table of Quantitative Elements


## Visual stack

Documents this skill emits follow `/home/workdir/.grok/skills/visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
ITQE in this skill is the house **Interactive Table of Quantitative Elements**. Four locked columns sit under every display equation and under every ranked quantitative inventory. The look matches the figures on DigitalMarketingCo.org white papers (collapsible variable table, automatic Greek-letter legend, Identifier-Term-Quantity-Explanation body) and the PDF figures drawn by `/folio`, `/phd-ivy-monograph`, `/deep`, and `/ivy-biblio`.

This skill does **not** draft the fiscal monograph *Imputed Tax Quantitative Easing*. That work lives at the house white-paper index and in the blog node on zero-tax America. If the user asked for the fiscal framework, load `/folio` or `/deep` on that topic. If they typed `/itqe` they want the table contract.

Skill root is `/home/workdir/.grok/skills/itqe`.

Read on demand

- `references/columns.md` — locked four columns, Greek legend, first-use rule
- `references/emit-targets.md` — chat, PDF, HTML, DOCX, PPTX, XLSX
- `references/stack.md` — how this skill sits under banner, copyright, deep, folio
- `references/render-gate.md` — fail-closed scan before delivery
- `references/intended-render.md` — post-completion full-document intended-render sweep
- `scripts/scan_render_gate.py` — ITQE completeness plus `/latex` raw-TeX and missing-glyph sweep
- `/home/workdir/.grok/skills/latex/scripts/scan_raw_tex.py` — mandatory sibling gate (latex skill v1.7+)
- `/home/workdir/.grok/skills/latex/scripts/scan_intended_glyphs.py` — mandatory sibling gate for white-box operators and combining marks
- `assets/itqe.schema.json` — equation and inventory object shape
- `/home/workdir/.grok/skills/wca-ivy-biblio/references/itqe.md` — twin column contract
- `/home/workdir/.grok/skills/wca-ivy-biblio/scripts/inject_itqe.py` — attach rows to folio JSON

House visible anchor is Digital Marketing Company. Seed URL is https://digitalmarketingco.org. Plain-text domain is DigitalMarketingCo.org.

If the user only asked to create or revise this skill and supplied no inventory topic, stop after the skill files exist.

## When this skill runs

- User typed `/itqe`
- User asked for an interactive table of quantitative elements, a collapsible variable table, or a Greek-letter legend under math
- A stacked run (`/folio`, `/phd`, `/deep`, `/banner`, `/copyright`, `/latex`, `/ivy-biblio`) will print a display equation or a ranked metric table
- Chat must show KaTeX plus the four-column figure
- A longevity, ranking, factor, or KPI inventory must be emitted as ITQE rows rather than a bare list

## Locked columns

Print the expanded headers Identifier, Term, Quantity, Explanation. Print a muted kicker ITQE above the rule. Never rename the four columns. Never drop a column because the figure looks obvious.

Identifier holds the glyph or code as printed. Term holds the ordinary English name. Quantity holds the SI unit, dimension, domain, or rank scale. Explanation holds the role in this figure, one short clause, local not encyclopedic.

## Cell and corpus render contract (v1.2)

Every printable string in the corpus is a delivered page. That includes Identifier, Term, Quantity, and Explanation cells, captions, legends, body paragraphs, headings, footnotes, bibliography lines, banners, and figure captions. Chat may use KaTeX. Files may not.

Hard rule for ITQE cells and for running text

- Write compiled glyphs or a compiled mini-figure. Use Unicode subscripts and superscripts (`h₁₆`, `m⁻²`, `uuᵀ`, `ℝ`, `‖·‖_F`) or house markup the builder actually compiles (`<i>`, `<b>`, `<sup>`).
- Never put LaTeX, AMS-TeX, KaTeX, or MathJax source in a cell or in prose. Forbidden on a visible page or in a printable JSON string: `$...$`, `$$...$$`, `\(...\)`, `\[...\]`, `\frac`, `\sum`, `\mathbf`, `\mathrm`, `\begin`, caret-brace `^{}`, underscore-brace `_{}`, and ASCII-TeX exponents such as `m^-2` or `R^{I×J×K}`.
- The `tex` key is a rebuild sibling only. It is never printed.
- Identifier must match the figure glyph, not a smashed ASCII alias, unless the figure itself uses that Latin code.
- Quantity uses SI with Unicode powers (`kg·m²`, `m⁻¹`, `rad·s⁻¹`), never `m^-1` or `kg m^2`.
- Deep Georgia runs that cannot draw Greek must embed a Latin Modern figure for the cell cluster rather than print tofu.

If a cell needs a stacked fraction or a large operator, compile that cell with `/latex` `render_snippet.py` and store a small PNG on the row as `identifier_plate` / `quantity_plate`. Do not screenshot a checkerboard.

## Greek-letter legend

When any identifier is a Greek, Hebrew, or variant Latin glyph, emit a legend immediately under the table.

Format — glyph — name (case). Spoken form.

Example — sigma (lowercase). Population standard deviation of age at death.

Do not invent a glyph that is not on the figure. Latin-only figures still get the four columns. They skip the legend.

## Glyph-first identifiers and secondary glyph table (v1.3)

Identifier cells print the compiled glyph first, never the English spelling as a stand-in. Write θ, not the six letters t-h-e-t-a. Write λ, not lambda. Write Σ, not Sigma. Compile through `/latex` or store Unicode that the target face can draw. The English name and the case label (lowercase, capital, or variant) come after the glyph, never in place of it.

After the primary four-column ITQE table, if the figure uses any non-English glyph (Greek, Hebrew, variant Latin, nabla, partial, script-ell, h-bar), emit a second table titled ITQE — glyphs. One row per distinct glyph on that figure. Locked columns

- Glyph — the compiled character as printed on the figure
- Name and case — spoken English name plus lowercase, capital, or variant
- Role in this equation — how that glyph functions on this figure only
- Operators on this figure — only the calculus or algebra that actually appears with this glyph here (a time derivative, a line integral, a sum, a contraction). Write none on this figure when the glyph is a static label. Do not invent a partial derivative, a multiple integral, or a summation because the letter could wear that hat in another paper.

Do not duplicate a Latin-only identifier into the glyph table. Do not pad rows with decorative analysis. Relevance is local to the figure.

## Placement

- Chat — KaTeX display (or a titled inventory), then the markdown ITQE table, then the legend if needed
- Folio / Deep PDF — compiled figure or Unicode line the face can draw, caption, ITQE table, keep-together so a page break does not orphan the table
- HTML white paper — rendered KaTeX node, then a semantic table with caption ITQE, wrapped in an open details block titled Quantitative elements so the table is collapsible
- DOCX / PPTX — figure or OMML, then a native 4-column table
- XLSX — one sheet named ITQE with the four headers in row 1

Do not put the table above the figure. Do not bury it in a footnote. Do not screenshot a checkerboard.

## How to fill a row

- Identifier matches the glyph or code on the figure
- Term is the dissertation name, not slang
- Quantity prefers SI or the unit already in the prose. Write dimensionless when that is the fact. Write years not yrs in the Quantity cell
- Explanation is local to this figure
- Constants quote BIPM, NIST, CODATA, UN WPP, WHO, or IHME GBD when a number is claimed. Do not invent a value
- Every variable, subscript, and constant on the figure gets a row
- Operators that are not quantities do not get rows
- Ranked inventories (nations, factors, KPIs) use the same four columns. Identifier may be an ISO code, a GBD risk id, or a rank index

## Ranked inventories

When the user asks for nations, factors, or causal lists, emit

1. A definition figure for the headline statistic (mean, median, variance) as KaTeX plus ITQE
2. A factor taxonomy as ITQE rows (one row per factor)
3. A ranking table in ordinary columns (rank, name, mean, median if known, spread if known)
4. A source line naming UN WPP, WHO GHE, IHME GBD, HMD, or the paper actually used
5. A gap line for any statistic that was not published at country grain (do not fabricate median age at death or variance for a country that has no life table in the session)

Never claim a country-level median or variance you did not compute from a life table or cite from a named dataset.

## Stack order

When flags are combined, run in this order

1. `/deep` or `/folio` drafts the JSON
2. `/itqe` fills every equation object and every ranked inventory
3. `/latex` compiles figures so no raw TeX reaches a page
4. `/ivy-biblio` remaps notes and re-checks ITQE completeness
5. `/banner` stamps section figures
6. `/copyright` stamps the living footer
7. Builder writes the PDF
8. Visual QA of every page

Chat-only `/itqe` stops after step 2 and prints the tables here.

## JSON shape

An equation object has type equation, an id, unicode or figure, caption, an itqe array of four-key objects, and a legend array whenever a non-English glyph is on the figure. Each legend row has glyph, name, case, role, and operators. The key tex may exist as a rebuild sibling. It is never printed. Full schema is assets/itqe.schema.json.

To attach rows on a folio JSON run inject_itqe.py from wca-ivy-biblio against the working JSON.

## Post-completion intended-render sweep (mandatory, v1.4)

The flag `/itqe` identifies **all** LaTeX, AMS-TeX, KaTeX, TeX, and MathJax on the job. After the document is built, do not stop at “the scan found no backslash.” Walk the **entire** finished file — every page, every caption, every ITQE cell, every footnote, every banner, every figure — and ask whether each clip printed the symbol the author intended.

A clip that is not the intended glyph is a defect even when no `$...$` remains. The house example is `R = ☒L/A` where the ballot-box-X is a missing-glyph stand-in for ρ. That page fails the gate.

Identify

- raw source still visible (`$...$`, `$$...$$`, `\(...\)`, `\[...\]`, `\frac`, `\rho`, `\times`, KaTeX or MathJax source)
- missing symbols of any sort (U+FFFD, ☒ ☐ □ ■ ◻ ▣ ⬜ ▢, empty rectangles, .notdef boxes)
- a compiled figure whose visible glyph is the wrong character (rho drawn as a box, times drawn as a letter x inside a square, mu drawn as u)
- clipped, truncated, or overlapping math that no longer matches the `tex` rebuild sibling
- Identifier cells that print a Latin spelling or a box instead of the figure glyph

Repair

1. Read `references/intended-render.md`
2. Harvest every math locus with `/latex` `harvest_raw_tex.py`
3. Recompile the intended snippet with `/latex` `render_snippet.py` in a face that contains the glyph (Latin Modern first)
4. Store the figure; keep `tex` hidden; fill Identifier-Term-Quantity-Explanation with compiled glyphs
5. Rebuild
6. Run `scan_render_gate.py`, `scan_raw_tex.py --pages`, and latex v1.7 `scan_intended_glyphs.py`
7. Raster **every** page at 140 dpi or higher and reject any clip that is not the intended symbol
8. Prefer Latin aliases (`Y-hat`, `>>`, `=>`) or a compiled plate when the body face cannot draw ≫, ⇒, or combining circumflex. Do not leave those operators in an ITQE Identifier cell.

Do not attach the file and do not tell the user it is finished while any clip is a box, a tofu square, or a glitch that does not match the intended mathematics.

## Render gate (mandatory)

Every document skill that can print notation ends on this gate. Chat may render KaTeX. A PDF, Word file, slide, sheet, printed HTML view, or builder JSON printable string may not show the source of that KaTeX, of LaTeX, of AMS-TeX, of TeX, or of MathJax. After that source sweep, the same gate walks every page for clips that failed to render as intended.

```bash
python3 /home/workdir/.grok/skills/itqe/scripts/scan_render_gate.py \
  /home/workdir/artifacts/<slug> \
  --also-pdf /home/workdir/artifacts/<file>.pdf
python3 /home/workdir/.grok/skills/latex/scripts/scan_raw_tex.py \
  /home/workdir/artifacts/<slug> \
  --also-pdf /home/workdir/artifacts/<file>.pdf --pages
python3 /home/workdir/.grok/skills/latex/scripts/scan_intended_glyphs.py \
  --pdf /home/workdir/artifacts/<file>.pdf \
  --also-json /home/workdir/artifacts/<slug>/folio.json
pdftoppm -png -r 140 /home/workdir/artifacts/<file>.pdf /tmp/itqe-page
```

Exit code 1 is a hard stop. Do not attach the file. Do not tell the user it is finished. Compile the leak with `/latex` `render_snippet.py`, store a figure, fill the four ITQE columns, rebuild, and scan again. Raster every page and reject tofu, empty boxes, clipped glyphs, or a visible backslash command.

## QA — reject the figure when

- a display equation has no ITQE table
- a figure symbol is missing from the identifier column
- a Greek or other non-English figure glyph is spelled in Latin letters in the Identifier cell (theta for θ)
- a non-English figure glyph has no secondary glyph-table row
- the secondary glyph table lists an operator that does not appear on this figure
- any of the four primary cells is blank
- raw TeX, AMS, KaTeX, or MathJax delimiters are visible on a delivered page, including inside any ITQE cell
- ASCII-TeX shorthands (`^{}`, `_{}`, `m^-2`, `uu^T`, `I_tot`, `B_k`, `Λ_int`, `p^bi`) appear in a cell or in body copy
- A raster page shows a white empty box, a black box, or tofu where a scalar, operator, subscript, or Greek letter belongs. Identify the intended glyph and recompile it before delivery
- the table is a baked screenshot
- tofu, U+FFFD, ☒, ☐, □, empty boxes, or any other missing-glyph stand-in appears in an identifier, term, quantity, explanation, figure, caption, or body line
- a compiled clip is not the symbol the `tex` sibling or the surrounding prose intended (ρ printed as ☒, × printed as a boxed X)
- a Greek or other non-English figure glyph is spelled in Latin letters in the Identifier cell
- a non-English figure glyph has no secondary ITQE — glyphs row
- the secondary glyph table lists an operator that does not appear on this figure
- a country median or variance is stated with no source
- the fiscal ITQE framework is mixed into the table contract without the user asking for that monograph
- `scan_render_gate.py` or `scan_raw_tex.py` exits 1

## Hard rules

- Four columns only. Identifier, Term, Quantity, Explanation
- Explain every variable and constant the first time it appears
- Visible house anchor is Digital Marketing Company linking to https://digitalmarketingco.org
- Plain-text domain is DigitalMarketingCo.org
- No emoji. No invented sources. No black boxes
- Display math is compiled glyphs or a compiled figure before the ITQE table. Raw `$...$`, a backslash command, a missing symbol, or a glitched stand-in on the page is a defect. Stack `/latex` and fail closed on a dirty scan or a failed intended-render sweep.
- Do not reprint builder source into chat


## Render gate (mandatory with /itqe and /latex)

Before delivering any PDF, DOCX, PPTX, XLSX, HTML view, printed page, or builder JSON that may contain notation, short codes, or equations, run the house render gate. Chat may use KaTeX. Files must show compiled glyphs or a compiled figure. Raw LaTeX, AMS-TeX, KaTeX source, MathJax source, uncompiled backslash commands, tofu, or empty boxes are defects.

```bash
python3 /home/workdir/.grok/skills/itqe/scripts/scan_render_gate.py \
  /home/workdir/artifacts/<slug> \
  --also-pdf /home/workdir/artifacts/<file>.pdf
python3 /home/workdir/.grok/skills/latex/scripts/scan_raw_tex.py \
  /home/workdir/artifacts/<slug> \
  --also-pdf /home/workdir/artifacts/<file>.pdf --pages
```

Exit code 1 blocks delivery. Repair with `/latex` figures, attach an ITQE table under every display equation (Identifier, Term, Quantity, Explanation), rebuild, scan again, and raster every page. See `/home/workdir/.grok/skills/itqe/references/render-gate.md` and `/home/workdir/.grok/skills/latex/SKILL.md`.

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

Read `/home/workdir/.grok/skills/negative/SKILL.md` and `/home/workdir/.grok/skills/negative/references/blocklist.md`.
Before chat, PDF, DOCX, PPTX, XLSX, caption, filename, alt text, or footnote leaves this skill, extract visible text and run

```bash
python3 /home/workdir/.grok/skills/negative/scripts/sweep_negative.py <extracted-text>
```

Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.

## House interop

Read visual-system/references/house-output.md before any document, deck, or page. Visible link text is Digital Marketing Company. The title attribute matches that text. Plain domain text is DigitalMarketingCo.org. Legal owner is Web Development Corporation. Do not nest an anchor inside an instruction sentence. Stack visual-system, negative, latex, and itqe before delivery when the file contains prose or math. Banners and plates stay unique, full-bleed, and context-locked.
