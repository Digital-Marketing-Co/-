---
name: banner
description: Generate full-bleed banners for every body section and every subsection. Literal high-resolution context-locked figures at full opacity with a hidden tracking link. Use when the user types /banner, when /list /deep /folio /images need section banners, when a subsection is missing its own banner, when figures came out as metaphors instead of diagrams, or when an existing report is missing bleed banners. Every banner prints at 100 percent page width with zero left or right margin or padding, keeps the source aspect ratio, and is not faded on any edge.
metadata:
  type: workflow
  version: "1.5"
  flag: /banner
  owner: Web Development Corporation
  visual_stack: visual-system
---

# /banner


## Visual stack

Documents this skill emits follow `/home/workdir/.grok/skills/visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Make one RGBA banner PNG per body section **and per subsection** and put a hidden click-through URL over the banner. `/list`, `/deep`, `/folio`, and `/images` call this after the draft exists. It can also run alone on an existing `deep.json`, `list.json`, `folio.json`, or report folder. Subsections are not covered by the parent section banner. Each heading level that prints as a body node gets its own generate. Print at full opacity. Do not fade any edge.

`<banner>` = `/home/workdir/.grok/skills/banner`.
`<deep>` = `/home/workdir/.grok/skills/deep`.

Read on demand

- `references/section-inventory.md` — one banner per section and per subsection
- `references/negative-vocabulary.md` — banned prompt tokens
- `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` — negative array
- `references/banner-spec.md` — locked geometry (when present)
- `references/literal-figures.md` — anti-metaphor, source cite, glyph QA, resolution (when present)

## When this skill runs

- User typed /banner and pointed at a document folder or a list of section and subsection titles.
- /list, /deep, /folio, or /images reached the banner step.
- A finished PDF is missing banners on new sections or new subsections.
- A prior banner is allegorical, low-resolution, or full of unreadable baked text.

If there is no section list and no topic, stop and ask which sections and subsections need banners. Do not invent headings.

## Workflow

### 1. Inventory sections

From `list.json`, `deep.json`, `folio.json`, `atlas.json`, or the user list collect every body node. A body node is any section **or subsection** with `kind` equal to `body`, or with `level` 1 or 2 that is not front matter. One banner per node. A subsection does not inherit the parent banner.

Skip title leaf, contents, Notes, Bibliography, and colophon. New sections or subsections added after a first pass still need their own banner.

Inventory rule

- `level` 1 section → `banners/banner-NN.png`
- `level` 2+ subsection → `banners/banner-NN-SS.png` (NN is the parent, SS is the subsection order)
- Record `parent_id` on the subsection banner object so QA can prove coverage

If a parent has three printed subsections, the document must contain four unique banners for that family (one parent + three children), each from its own generate.

### 2. Prompt

One landscape generate per section **and per subsection**. Read `references/literal-figures.md` first when that file exists. Prompt only from named objects in that node, not from the parent chapter at large. Do not put any token from `assets/negative-keywords.csv` into the generate prompt.

The prompt must

- name the real objects in that section (residues, devices, documents, landforms), not stand-ins
- demand a photoreal or textbook-accurate rendering of those objects
- include an equation or numeral only when that exact string is already in the section text
- add `no caption text, no watermark, no logo, no agency seal, no photoreal portrait of a private person, no allegory, no metaphor architecture`
- stay free of false quantities and invented proper names
- request at least 2550 px on the long edge (prefer 3300 px). Ask for razor-sharp, high-dynamic-range, publication-grade imaging of the named objects. Name the objects that appear in the section text. Never invent a skyline or building that does not appear in the section.

Orientation is landscape.

Save the raw file as `banners/raw-NN.png`.

### 3. Inspect

Open `banners/raw-NN.png` with the image reader. Follow the rejection list in `references/literal-figures.md` when present. Regenerate up to three times. Write `banners/qa-NN.md`.

### 4. Size and bleed

Copy `banners/raw-NN.png` to `banners/banner-NN.png`. If a resize is required, LANCZOS-downsize only to 8.5 in wide at 150 px/in (page width, x = 0, no side inset) and set height from the source aspect ratio. Do not fade the top. Do not fade the bottom. Do not fade the left or right. Do not call `apply_banner_fade.py`. Keep full opacity on every edge. No left or right margin, padding, letterbox, or crop bar. RGB must not contain a checkerboard. If the file uses an alpha channel, every pixel that is part of the picture stays fully opaque.

### 5. Attach

On the section object set banner.path, banner.href, banner.caption, banner.prompt, and banner.source_note.

Caption form

`Section banner. Literal reconstruction of [named object] after [Chicago short title]. Generated model, not a scan of the source.{{n}}`

Default href

`https://digitalmarketingco.org/r/?src=deep-banner&section={section_id}`

Never print the URL on the banner.

### 6. QA

Open the published PNG and confirm

- every picture pixel is fully opaque
- no top fade and no bottom fade
- no baked checkerboard
- no burned-in caption
- no allegory passed the inspect step

If /deep, /list, /folio, or /images then builds the PDF, confirm every body section and every subsection has its own banner and that each banner touches both page edges.

Coverage fail — a printed subsection heading with no `banner.path` of its own is a defect. Regenerate. Do not crop the parent banner into the child slot.

## Hard rules

- Full opacity. No fade on any edge.
- Full bleed left and right at 100 percent page width. Zero left margin, zero right margin, zero left padding, zero right padding. The builder places the banner at x = 0. Left edge pixel column and right edge pixel column touch the page trim. No side letterbox. No side crop bar.
- One banner per section and one banner per subsection. Parent banners never stand in for a child heading.
- Literal to that node. No metaphor. No false equations.
- No raw TeX, KaTeX, or MathJax source in the banner pixels. Compile an equation figure first or omit numerals.
- No token from `assets/negative-keywords.csv` in a concatenated generate prompt.
- Chicago cite the reconstruction source in the caption.
- Hidden link, not visible URL text.
- Do not generate violent, sexual-exploitation, or hate imagery.


## Render gate (mandatory with /itqe and /latex)

Before delivering any PDF, DOCX, PPTX, XLSX, HTML view, printed page, or builder JSON that may contain notation, short codes, or equations, run the house render gate. Chat may use KaTeX. Files must show compiled glyphs or a compiled equation figure. Raw LaTeX, AMS-TeX, KaTeX source, MathJax source, uncompiled backslash commands, tofu, or empty boxes are defects.

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
