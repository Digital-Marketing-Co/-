---
name: deep
description: Produce a doctoral research monograph from a topic or text blob using recursive, iterative evidence synthesis, verified academic PDF citations, mandatory WCA bibliography, ITQE, LaTeX, and unique images and banners for every section type. Use for /deep, /iterate /deep, recursive research, or advanced scholarly synthesis.
---

# /deep


## Visual stack

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Turn one topic into a letter-size Chicago notes-bibliography PDF. Research walks a source graph, not a flat reading list. Type is frozen Georgia at the locked double scale. Every printed section and subsection of every type gets its own unique banner.

Work in `./artifacts/<slug>/`. Final PDF is `./artifacts/<Title_Slug>.pdf`.

`<skill>` = `@deep`.
`<banner>` = `@banner`.

Read on demand

- `references/locked-prompt.md` — the execution prompt with frozen numbers
- `references/research-graph.md` — node recursion and source tiers
- `references/chicago-and-marks.md` — notes, page locators, superscript runs, page-local footnotes
- `references/house-style.md` — Digital Marketing Company link and glyphs
- `assets/typography.py` — locked point sizes (import, do not edit)
- `assets/schema/deep.schema.json` — JSON shape
- `<banner>/SKILL.md` and `<banner>/references/banner-spec.md`

If the user only asked to create or edit this skill and supplied no research topic, stop after the skill files exist. Do not invent a topic.

## Mandatory composition and precedence

On every research invocation read and apply `@wca-ivy-biblio/SKILL.md`, `@itqe/SKILL.md`, `@latex/SKILL.md`, `@images/SKILL.md`, and `@banner/SKILL.md`, including their required workflow references. Read `@iterate/SKILL.md` and its workflow for stacked `/iterate /deep`; use iterative research passes on ordinary `/deep` too. Resolve aliases by installed frontmatter name. Missing dependencies must be reported, never silently skipped.

Read `references/doctoral-protocol.md` before scoping and each revision. Its research, evidence, and coverage gates replace conflicting legacy defaults. WCA controls citation ordering; LaTeX controls math compilation; ITQE controls symbol tables; images controls uniqueness. This skill's all-section banner coverage and full-opacity requirements supersede narrower banner exclusions and fades. Keep the locked typography unchanged. Apply user instructions first.

Treat the subject or blob immediately after `/deep` as input. Distinguish quotations, propositions, and assumptions; investigate them rather than endorsing them. If the request only updates the skill, do not invent or execute a research topic.

## Workflow

### 1. Lock the prompt

Copy `references/locked-prompt.md` into `scope.md`. Do not change TITLE_PT, BODY_PT, NOTE_PT, banner inch values, or the Georgia family name.

Extract the topic, period, geography, and exclusions from the user message. Write

- working title
- 4–8 research questions
- inclusion / exclusion rules
- the root node label

### 2. Recursive research

Follow `references/research-graph.md`. Use `web_search` and `browse_page`. Prefer primary PDFs, Ivy / university-press work, `.gov`, and `.mil`.

Record keepers in `sources.jsonl`. Record the graph in `nodes.jsonl`. Write `rounds/round-N.md`.

Caps that stop infinite recursion

- Start with depth 4 and 80 keeper sources as review checkpoints, not completeness claims. Expand in documented batches while material questions remain and resources permit.
- Close a branch only after two consecutive targeted rounds add neither material evidence nor a new explanatory branch.
- Report resource-limited branches as open, never saturated.

Connected nodes needed to explain the root stay in scope. Decorative tangents do not. Never fabricate a citation or a page number.

### 3. Draft

Write `outline.md`, then `deep.json` matching the schema.

Required front matter — title, subtitle, author, date, house block, abstract (150–250 words), keywords.

Required body (relabel to the topic)

1. Introduction and research questions
2. Historiography or literature review
3. Sources and method
4. One chapter per major research question (or per major graph branch)
5. Synthesis
6. Conclusion and open problems
7. Bibliography

A collected Notes chapter is optional concordance only. Every citation used on a page must already appear in that page’s footer band.

Paragraphs use `{{n}}` or `{{n, m, p}}` markers. Multiple marks at one locus become one superscript run with comma-space (`12, 15`). Every note lists every page actually used from that source for that claim.

Explain every variable, subscript, and constant the first time an equation appears.

Allowed inline tags in JSON text — `i`, `em`, `b`, `sup`, `a`.

### 4. Banners and images

Run `/images` and `/banner` (accept `/banners` as an alias). Assign exactly one unique banner to every printed section and subsection at every heading level, including abstract, methods, appendices, glossary, Notes, and Bibliography. A title-only cover, automatic contents, and running headers are layout furniture and exempt. Parent banners never satisfy child slots. Add separate inline explanatory images when useful; never reuse a banner as an inline image or equation plate.

- Prompt only from that section’s claims.
- Save the raw generate to `banners/raw-NN.png`.
- Render at 16:9 and full width. Use full opacity without top or bottom fades; this rule resolves conflicting legacy fade instructions in dependencies.
- Write `banners/banner-NN.png` (RGBA, real alpha).
- Set `banner.path`, `banner.caption`, `banner.prompt`, and `banner.href` on the section.

Default href

`https://digitalmarketingco.org/r/?src=deep-banner&section={section_id}`

Replace that placeholder later only when a real SEO title URL for that node exists. Do not print the URL on the figure.

### 5. Build

Before building, run WCA citation remapping and its document QA, both math render scans, and the images uniqueness audit. Read each script's current interface before invoking it. Flatten nested heading nodes in reading order when the legacy builder cannot traverse them; preserve `level`, `parent_id`, and a banner on each. The canonical builder supports equation objects and ITQE tables; inspect remaining capability gaps, especially nested headings, inline images, and banners on Notes/Bibliography. Inspect its capabilities. Extend it or use a compatible verified renderer before delivery; do not silently drop unsupported fields. Require output-level coverage proof, not JSON presence alone.


```bash
python3 <skill>/scripts/build_deep_pdf.py \
  ./artifacts/<slug>/deep.json \
  --out ./artifacts/<Title_Slug>.pdf
```

### 6. Visual QA (mandatory)

```bash
pdftoppm -png -r 140 ./artifacts/<Title_Slug>.pdf /tmp/deep-page
```

Inspect every page. Rebuild if any of these appear — tofu, black or white boxes over glyphs, clipped type, a checkerboard in a banner, a banner that is not full-bleed left and right, a missing caption, a broken house link, or a figure that does not belong to its section.

### 7. Deliver

Give the user the PDF. State page count, note count, bibliography count, node count, and remaining research gaps. Do not dump `deep.json` into chat.

Output a copyable Python fence only when a new helper script is written during the run. Do not reprint `build_deep_pdf.py` or `typography.py`.

## Hard rules

- Chicago notes plus bibliography. Notes that appear on a page print in that page’s footer band (Chicago note form, above the living copyright line). No author-date parentheticals. Do not rely on a collected endnote chapter as the only citation display.
- Typography comes only from `assets/typography.py`. BODY_PT is 22. Face is Georgia (bundled Gelasio registered as Georgia).
- Visible house anchor is exactly Digital Marketing Company. Target is https://digitalmarketingco.org. Plain-text domain is DigitalMarketingCo.org.
- No emoji. No unsupported symbols. No invented sources.
- Math is compiled glyphs or a compiled figure. Run `/latex` `scan_raw_tex.py` on the draft and on the built PDF before delivery. A dirty scan blocks the file. Georgia/Gelasio often lacks Greek. Prefer a Latin Modern figure over a tofu line.
- Banners are generated illustrations, never presented as historical photographs.


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

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write figure, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

## Canonical copyright

Invoke `@copyright/SKILL.md` as the sole authority for copyright wording, year logic, ownership, and footer links. Never independently calculate or hard-code competing legal language in this skill or its execution prompt. Preserve citation footnotes above that footer.

## Negative gate (mandatory before any deliverable)

Read `@negative/SKILL.md` and `@negative/references/blocklist.md`.
Before chat, PDF, DOCX, PPTX, XLSX, caption, filename, alt text, or footnote leaves this skill, extract visible text and run

```bash
python3 @negative/scripts/sweep_negative.py <extracted-text>
```

Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN. Do not delete a claim to hide a token. Do not leave a hole. Preserve verbatim user source, exact source titles, author names, quotations, established technical terminology, mathematical identifiers, and required citation metadata. Scholarly fidelity takes precedence over stylistic substitutions; log these protected occurrences separately and apply the negative gate to editable prose and image prompts. Never alter scientific meaning or bibliographic identity to clear a vocabulary scan.

## ChatGPT portability

Resolve `@skill-name/path` by finding the installed personal skill whose SKILL.md frontmatter has `name: skill-name`; read that path under its directory. For `@generate/`, use the `generate-prompt` skill. Before running copied shell commands, substitute actual resolved paths and use the current working directory for generated files. Apply instructions only when this skill is invoked or a user requests the corresponding workflow. User instructions and platform rules take priority. Run bundled scripts only after checking their inputs and prerequisites. Never claim unavailable integrations, credentials, citations, or generated results.

## Canonical repository and portability

Before future use, read the current Digital-Marketing-Co/- main revision and its sync contract, policy, and ledger. Merge verified improvements without discarding repository-only assets or newer renderer code. Preserve the image print contract: native source aspect ratio, page-width placement, zero side inset, no stretching. Generate banners at 16:9; do not distort non-banner figures into that ratio. Use interop publication checks when installed, resolving paths for the actual host rather than assuming Grok paths. Deliverables follow this skill's stricter citation, compiled-math, all-section coverage, and canonical copyright gates.
