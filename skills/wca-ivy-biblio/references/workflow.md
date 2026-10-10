

# /ivy-biblio — WCA Ivy citation order and ITQE figures


## Visual stack

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
This skill is the house remapper and equation-table gate for every WCA compact Ivy report. CMOS 17/18 notes-bibliography remains the sentence form. Two locked house revisions replace alpha bibliography and bare equations.

1. Citation numbers and unique works follow **first appearance in reading order**. Inserting a note remaps every later number. The bibliography lists each work once, in that same first-appearance order. No author-date parentheticals.
2. **Primary project mandate (ITQE).** The document must prefer the maximum number of relevant mathematically represented formulas, identities, rates, estimators, constraints, mappings, and quantitative descriptions that the topic actually supports, from any class of academia (mathematics, physics, chemistry, engineering, economics, finance, statistics, epidemiology, computer science, operations research, linguistics, music theory, or any other field that has a written relation). Each display figure is followed immediately by an **ITQE table** — Identifier, Term, Quantity or unit, Explanation. Do not thin the math to a single ornamental equation. Do not skip a relation because the surrounding prose is historical, legal, clinical, or qualitative. If a claim is quantitative, write it as a figure plus ITQE. Inline first-use sentences still name every symbol.

Skill root is `@wca-ivy-biblio`.

Read on demand

- `references/citation-order.md` — remap algorithm, work identity, QA gates
- `references/wca-ivy-forms.md` — note form and bibliographic form
- `references/itqe.md` — ITQE columns, placement, symbol-first-use rule
- `scripts/reorder_citations.py` — rewrite folio.json / monograph.json / deep.json
- `scripts/inject_itqe.py` — attach ITQE blocks to equation objects
- `scripts/qa_ivy_document.py` — fail the document if numbers or tables are wrong
- `assets/itqe.schema.json` — equation object shape

`<folio>` = `@folio`
`<phd>` = `@phd-ivy-monograph`
`<psycho>` = `@psychoanalyze`
`<latex>` = `@latex`

If the user only asked to create or revise this skill and supplied no document, stop after the skill files exist. Do not invent a monograph.

## When this skill runs

- User typed `/ivy-biblio` or `/wca-ivy`
- User asked to reorder citations, restamp note numbers, or put the bibliography in citation order
- `/folio`, `/phd`, or `/PsychoAnalyze` is drafting or rebuilding a JSON document that has `{{n}}` markers
- User typed `/itqe` or asked to maximize formulas, equations, or Interactive Tables of Quantitative Elements
- A document contains display math and must grow an ITQE table under each figure; drafting must prefer the maximum number of relevant figures the topic supports, from any academic class
- Visual or script QA finds a gap in note numbers, an alpha-sorted bibliography that ignores first appearance, or a bare equation

Stacked flags do not change emit order of Deep then Folio. This skill runs on each JSON **before** the matching builder.

## Workflow

### 1. Inventory

Copy or locate the working JSON (`folio.json`, `monograph.json`, or `deep.json`) under `./artifacts/<slug>/`.

Walk sections in file order. Record every `{{n}}` / `{{n, m}}` marker, every `notes[].n`, every `notes[].work_id` (optional), every bibliography string, and every equation object or figure.

Write `ivy-inventory.md` in the work folder only when the document is large enough that a human must see the map. Do not dump the inventory into chat.

### 2. Identity of works

A **note** is one numbered citation event. A **work** is one bibliographic object.

- If `notes[].work_id` is present, group notes that share it into one work.
- Else derive a work key from the bibliography line the note points at (`notes[].biblio` index) or from a normalized short title inside the note text.
- Full form and later short form of the same book are one work. They keep separate note numbers (Chicago event notes) and one bibliography line.

Never invent a source. Never invent a page locator.

### 3. Remap citation numbers

```bash
python3 @wca-ivy-biblio/scripts/reorder_citations.py \
  ./artifacts/<slug>/folio.json \
  --in-place
```

The script

- walks `sections[].paragraphs`, abstracts, captions, and equation captions in document order
- collects first-seen note numbers
- assigns new integers 1..N with no gaps
- rewrites every `{{old}}` marker and every `notes[].n`
- sorts `notes` by the new n
- orders `bibliography` by first appearance of each unique work
- writes `citation-map.json` beside the source (old-to-new map)

Run it again after any later insertion. Do not edit superscripts by hand across a long file.

### 4. Attach ITQE tables

Every display equation must be a paragraph object, not raw TeX. Shape is in `assets/itqe.schema.json`. Compile missing figures with `<latex>/scripts/render_snippet.py`. Then

```bash
python3 @wca-ivy-biblio/scripts/inject_itqe.py \
  ./artifacts/<slug>/folio.json \
  --in-place
```

The injector refuses to invent identifiers. If `itqe` is empty it writes a stub row list from `symbols[]` only when that field already exists. Otherwise it fails and the agent must fill the four columns from the surrounding sentence.

Chat replies still render math with KaTeX. Directly under that KaTeX block, print a compact markdown ITQE table. The PDF builder draws the same table under the figure.

### 5. QA

```bash
python3 @wca-ivy-biblio/scripts/qa_ivy_document.py \
  ./artifacts/<slug>/folio.json
```

Fail the document when any of these hold

- a `{{n}}` has no `notes[].n`
- note numbers are not exactly 1..N after remap
- a later note number first appears before an earlier one
- bibliography order disagrees with first-appearance order of works
- a display `type=equation` object lacks a non-empty `itqe` array
- an ITQE row is missing identifier, term, quantity, or explanation
- raw TeX delimiters remain in a visible paragraph string
- author-date parentheticals of the form (Smith 2019) appear as the citation mechanism

Then build through `<folio>/scripts/build_folio_pdf.py` or the Deep twin. Visual-QA every equation page with `pdftoppm`. Rebuild on tofu, a missing ITQE header, a clipped table, or a trailing comma in a superscript run.

### 6. Deliver

State note count, unique-work count, whether the bibliography was reordered, and how many ITQE tables were attached. Do not dump JSON or the remapper source into chat.

## Hard rules

- Chicago note form for `notes[].text`. Bibliographic form for `bibliography[]`.
- Bibliography is first-appearance order. Do not alphabetize as the sort key. Do not invent a second number series on bibliography lines.
- Note numbers are the only citation numbers. They stay contiguous and in reading order.
- No author-date parentheticals.
- ITQE under every display equation. The ITQE flag is a primary drafting mandate, not a late QA sticker. Maximize relevant figures across every academic class the topic touches. Inline quantities still get a first-use sentence that names every symbol.
- Visible house anchor is Digital Marketing Co. Target is https://DigitalMarketingCo.org. Plain-text domain is DigitalMarketingCo.org.
- No emoji. No tofu. No invented sources.
- After remapping notes, run `/latex` `scan_raw_tex.py` on the JSON and on the built PDF. Uncompiled TeX left in a note, caption, or equation unicode line is a defect.
- Do not reprint builder or remapper source into chat unless a new helper was written in this run.


## Render gate (mandatory with /itqe and /latex)

Before delivering any PDF, DOCX, PPTX, XLSX, HTML view, printed page, or builder JSON that may contain notation, short codes, or equations, run the house render gate. Chat may use KaTeX. Files must show compiled glyphs or a compiled figure. Raw LaTeX, AMS-TeX, KaTeX source, MathJax source, uncompiled backslash commands, tofu, or empty boxes are defects.

```bash
python3 @itqe/scripts/scan_render_gate.py \
  ./artifacts/<slug> \
  --also-pdf ./artifacts/<file>.pdf
python3 @latex/scripts/scan_raw_tex.py \
  ./artifacts/<slug> \
  --also-pdf ./artifacts/<file>.pdf --pages
```

Exit code 1 blocks delivery. Repair with `/latex` figures, attach an ITQE table under every display equation (Identifier, Term, Quantity, Explanation), rebuild, scan again, and raster every page. See `@itqe/references/render-gate.md` and `@latex/SKILL.md`.

## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write plate, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

## Canonical footer

Render `copyright/SKILL.md` and its canonical notice helper once per page. Do not reproduce independent legal text or calculate years here.

## Negative gate (mandatory before any deliverable)

Read `@negative/SKILL.md` and `@negative/references/blocklist.md`.
Before chat, PDF, DOCX, PPTX, XLSX, caption, filename, alt text, or footnote leaves this skill, extract visible text and run

```bash
python3 @negative/scripts/sweep_negative.py <extracted-text>
```

Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.

## ChatGPT portability

Resolve `@skill-name/path` by finding the installed personal skill whose SKILL.md frontmatter has `name: skill-name`; read that path under its directory. For `@generate/`, use the `generate-prompt` skill. Before running copied shell commands, substitute actual resolved paths and use the current working directory for generated files. Apply instructions only when this skill is invoked or a user requests the corresponding workflow. User instructions and platform rules take priority. Run bundled scripts only after checking their inputs and prerequisites. Never claim unavailable integrations, credentials, citations, or generated results.
