

# /deep


## Visual stack

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Turn one topic into a letter-size Chicago notes-bibliography PDF. Research walks a source graph, not a flat reading list. Type is frozen Georgia at the locked double scale. Every body section gets a /banner figure.

Work in `./artifacts/<slug>/`. Final PDF is `./artifacts/<Title_Slug>.pdf`.

`<skill>` = `@deep`.
`<banner>` = `@banner`.

Read on demand

- `references/locked-prompt.md` — the execution prompt with frozen numbers
- `references/research-graph.md` — node recursion and source tiers
- `references/chicago-and-marks.md` — notes, page locators, superscript runs, page-local footnotes
- `references/house-style.md` — <a href="https://digitalmarketingco.org" title="Digital Marketing Co.">Digital Marketing Co.</a> link and glyphs
- `assets/typography.py` — locked point sizes (import, do not edit)
- `assets/schema/deep.schema.json` — JSON shape
- `<banner>/SKILL.md` and `<banner>/references/banner-spec.md`

If the user only asked to create or edit this skill and supplied no research topic, stop after the skill files exist. Do not invent a topic.

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

- depth 4 from the root
- 80 keeper sources
- a branch closes after two consecutive empty targeted rounds

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

### 4. Banners

For each body section (not Notes, not Bibliography) run the /banner skill.

- Prompt only from that section’s claims.
- Save the raw generate to `banners/raw-NN.png`.
- Fade and size with `<banner>/scripts/apply_banner_fade.py`.
- Write `banners/banner-NN.png` (RGBA, real alpha).
- Set `banner.path`, `banner.caption`, `banner.prompt`, and `banner.href` on the section.

Default href

`https://digitalmarketingco.org/r/?src=deep-banner&section={section_id}`

Replace that placeholder later only when a real SEO title URL for that node exists. Do not print the URL on the figure.

### 5. Build

```bash
python3 <skill>/scripts/build_deep_pdf.py \
  ./artifacts/<slug>/deep.json \
  --out ./artifacts/<Title_Slug>.pdf
```

### 6. Visual QA (mandatory)

```bash
pdftoppm -png -r 140 ./artifacts/<Title_Slug>.pdf /tmp/deep-page
```

Inspect every page. Rebuild if any of these appear — tofu, black or white boxes over glyphs, clipped type, a checkerboard in a banner, a banner that is not full-bleed left and right, a banner without a top and bottom fade, a missing caption, a broken house link, or a figure that does not belong to its section.

### 7. Deliver

Give the user the PDF. State page count, note count, bibliography count, node count, and remaining research gaps. Do not dump `deep.json` into chat.

Output a copyable Python fence only when a new helper script is written during the run. Do not reprint `build_deep_pdf.py` or `typography.py`.

## Hard rules

- Chicago notes plus bibliography. Notes that appear on a page print in that page’s footer band (Chicago note form, above the living copyright line). No author-date parentheticals. Do not rely on a collected endnote chapter as the only citation display.
- Typography comes only from `assets/typography.py`. BODY_PT is 22. Face is Georgia (bundled Gelasio registered as Georgia).
- Visible house anchor is exactly <a href="https://digitalmarketingco.org" title="Digital Marketing Co.">Digital Marketing Co.</a>. Target is https://digitalmarketingco.org. Plain-text domain is DigitalMarketingCo.org.
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
