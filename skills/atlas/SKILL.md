---
name: atlas
description: Compile a figure-and-gazetteer academic atlas PDF for one place, network, or spatial topic. Use when the user types /atlas, asks for a gazetteer, map figures, knowledge atlas, institutional atlas, or place-node inventory. Stacks with /deep recursive graph research, /banner full-bleed figures, phd-ivy-monograph Chicago notes, and /folio WCA filename plus hidden metadata. Do not use for an author harvest (that is /corpus) or a non-spatial linear monograph alone.
metadata:
  type: workflow
  version: "1.1"
  flag: /atlas
  owner: Web Development Corporation
  visual_stack: visual-system
---

# /atlas


## Visual stack

Documents this skill emits follow `/home/workdir/.grok/skills/visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Turn one place, route, institution set, or spatial topic into a letter-size atlas PDF. The unit of analysis is the **node on a map or network**, not a creator and not a free-form essay. Each body figure is a /banner full-bleed illustration. Gazetteer entries carry Chicago notes. Packaging follows the WCA Folio filename and living footer contract.

Work in `/home/workdir/artifacts/<slug>/`. Default printed file is `/home/workdir/artifacts/<YYYY>-<topic-slug>-wca-atlas.pdf`.

`<skill>` = `/home/workdir/.grok/skills/atlas`.
`<deep>` = `/home/workdir/.grok/skills/deep`.
`<banner>` = `/home/workdir/.grok/skills/banner`.
`<folio>` = `/home/workdir/.grok/skills/folio`.
`<mono>` = `/home/workdir/.grok/skills/phd-ivy-monograph`.

If the user only asked to create or edit this skill and supplied no atlas subject, stop after the skill files exist. Do not invent a region, network, or title.

## Read on demand

- `references/locked-prompt.md` — frozen type, banner inches, house strings
- `references/research-atlas.md` — node graph for places, routes, institutions
- `references/figures.md` — one figure per body section, banner handoff
- `references/gazetteer.md` — entry fields, coordinates, name variants
- `references/handoff.md` — what this skill is not, stacking with /deep /folio /banner /corpus
- `assets/schema/atlas.schema.json` — `atlas.json` shape
- `scripts/atlas_to_deep.py` — compile atlas.json into deep.json
- `scripts/build_atlas_pdf.py` — filename, compile, invoke the /deep builder

Type, fade geometry, and owner strings are locked in `<deep>/assets/typography.py` and `<banner>/references/banner-spec.md`. Do not invent a second scale.

## Workflow

### 1. Scope

Treat the remainder of the user message after `/atlas` as the **subject**. Extract

- working title
- geography (place, region, corridor, campus, theater)
- period if any
- network kind (places, institutions, routes, holdings, knowledge nodes)
- exclusions

Write `scope.md` with 4–8 research questions, inclusion / exclusion rules, and the root node label. Do not invent a subject.

### 2. Recursive place-graph research

Follow `references/research-atlas.md`. Use `web_search` and `browse_page`. Prefer primary map sheets, gazetteers, Ivy / university-press cartography, `.gov`, and `.mil`.

Record keepers in `sources.jsonl`. Record the graph in `nodes.jsonl`. Write `rounds/round-N.md`.

Caps that stop infinite recursion

- depth 4 from the root
- 80 keeper sources
- 40 gazetteer entries unless the user raised the cap
- a branch closes after two consecutive empty targeted rounds

Connected nodes needed to locate the root stay in scope. Decorative travelogue does not. Never fabricate a citation, a page number, or a coordinate.

### 3. Draft

Write `outline.md`, then `atlas.json` matching the schema.

Required front matter — title, subtitle, author, date, house block, abstract (150–250 words), keywords, projection or base-map note if coordinates appear.

Required body (relabel to the subject)

1. How to read this atlas
2. Historiography of the maps and gazetteers
3. Sources and method
4. One figure-chapter per major node or cluster (gazetteer entry plus claims)
5. Routes, adjacencies, and synthesis
6. Conclusion and open problems
7. Notes
8. Bibliography

Paragraphs use `{{n}}` or `{{n, m, p}}` markers. Multiple marks at one locus become one superscript run with comma-space (`12, 15`). Every note lists every page actually used from that source for that claim.

Explain every variable, subscript, and constant the first time an equation or coordinate formula appears.

Allowed inline tags in JSON text — `i`, `em`, `b`, `sup`, `a`.

### 4. Figures

For each body section except Notes and Bibliography run the /banner skill. Follow `references/figures.md`.

- Prompt only from that section’s claims and named places.
- Save the raw generate to `banners/raw-NN.png`.
- Fade and size with `<banner>/scripts/apply_banner_fade.py`.
- Write `banners/banner-NN.png` (RGBA, real alpha).
- Set `banner.path`, `banner.caption`, `banner.prompt`, and `banner.href` on the section.

Default href

`https://digitalmarketingco.org/r/?src=atlas-banner&section={section_id}`

Do not print the URL on the figure. Banners are generated illustrations, never presented as historical photographs or official map reproductions.

Optional gazetteer figure (phd-ivy-monograph habit) may sit under the figure as `figure.path` when a second schematic is required. One banner per section is mandatory. A second figure is optional.

### 5. Build

```bash
python3 <skill>/scripts/build_atlas_pdf.py \
  /home/workdir/artifacts/<slug>/atlas.json \
  --out /home/workdir/artifacts/<YYYY>-<topic-slug>-wca-atlas.pdf
```

The builder

- writes `deep.json` beside `atlas.json` so /deep typography and bleed banners stay locked
- invokes `<deep>/scripts/build_deep_pdf.py`
- prints the public filename (`YYYY-topic-slug-wca-atlas.pdf`)
- stamps the living footer contract already compiled by the /deep builder

When the user also typed `/folio`, keep the atlas token in the filename (`wca-atlas`, not `wca-folio`) so the two series do not collide. Still use the Folio house origin and `/white-papers/{slug}` backlink pattern from `<folio>/references/discoverability.md`.

### 6. Visual QA (mandatory)

```bash
pdftoppm -png -r 140 /home/workdir/artifacts/<YYYY>-<topic-slug>-wca-atlas.pdf /tmp/atlas-page
```

Inspect every page. Rebuild if any of these appear — tofu, black or white boxes over glyphs, clipped type, a checkerboard in a banner, a banner that is not full-bleed left and right, a banner without a top and bottom fade, a missing caption, a broken house link, an invented coordinate, or a figure that does not belong to its section.

### 7. Deliver

Give the user the PDF. State page count, figure count, gazetteer entry count, note count, bibliography count, node count, and remaining research gaps. Do not dump `atlas.json` into chat.

Output a copyable Python fence only when a new helper script is written during a later run. Do not reprint `build_atlas_pdf.py`, `atlas_to_deep.py`, or `<deep>/assets/typography.py`.

## Hard rules

- Chicago notes plus bibliography. No author-date parentheticals.
- Typography comes only from `<deep>/assets/typography.py`. BODY_PT is 22. Face is Georgia (bundled Gelasio registered as Georgia).
- Banner geometry comes only from `<banner>/references/banner-spec.md` (8.5 in wide, 4.35 in tall, full-opacity edges).
- Visible house anchor is exactly <a href="https://digitalmarketingco.org" title="Digital Marketing Co.">Digital Marketing Co.</a>. Target is https://digitalmarketingco.org. Plain-text domain is DigitalMarketingCo.org.
- Public filename is `YYYY-topic-slug-wca-atlas.pdf`.
- No emoji. No unsupported symbols. No invented sources. No invented latitudes or longitudes.
- Coordinates, when printed, must cite the gazetteer or survey sheet they came from.


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
