

# /banner


## Visual stack

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md` and the beauty lock in `references/beauty-lock.md`. Each banner is a fresh house generate — awe-inspiring, stunningly perfected, futuristic cinematic still — locked to objects named in that section or subsection. Read `visual-system/references/prompt-engineering.md` before every generate. Never reuse a parent banner, a prior chapter banner, a stock download, a shared prompt, or a near-duplicate perceptual hash.
Make one RGBA banner PNG per body section **and per subsection** and put a hidden click-through URL over the banner. `/list`, `/deep`, `/folio`, `/images`, `/book`, and `/ispy` call this after the draft exists. It can also run alone on an existing `deep.json`, `list.json`, `folio.json`, `book.json`, or report folder. Subsections are not covered by the parent section banner. Each heading level that prints as a body node gets its own generate. Generate opaque 16-9 rasters. After generate, run `scripts/apply_tb_alpha_blend.py` so only the top and bottom blend into the page. Left and right stay opaque to trim.

`<banner>` = `@banner`.
`<deep>` = `@deep`.

Read on demand

- `references/section-inventory.md` — one banner per section and per subsection
- `references/negative-vocabulary.md` — banned prompt tokens
- `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` — negative array
- `references/banner-spec.md` — locked 16-9 geometry and top-bottom alpha
- `references/beauty-lock.md` — awe-inspiring unique banner per node
- `@visual-system/references/prompt-engineering.md` — PhD prompt order, three-axis differentiation, beauty rejection
- `@images/scripts/audit_unique_images.py` — SHA-256 and average-hash fail-closed audit
- `references/literal-figures.md` — anti-metaphor, source cite, glyph QA, resolution (when present)
- `scripts/apply_tb_alpha_blend.py` — real alpha ramps on the top and bottom only
- `references/emit-file.md` — restamp the parent file before delivery
- `@images/scripts/rebuild_document.py` — parent builder or stamp-manifest fallback
- `@images/scripts/stamp_images_into_pdf.py` — insert plates into a naked PDF

## When this skill runs

- User typed /banner and pointed at a document folder or a list of section and subsection titles.
- /list, /deep, /folio, or /images reached the banner step.
- A finished PDF is missing banners on new sections or new subsections.
- A prior banner is allegorical, low-resolution, or full of unreadable baked text.

If there is no section list and no topic, stop and ask which sections and subsections need banners. Do not invent headings.

If the user only asked to create or edit this skill and supplied no document, stop after the skill files exist. Do not invent a report.

## Emit the file (mandatory)

A banner run is unfinished until the document file contains those stills. Read `references/emit-file.md`. Generate with the house `generate_image` tool so each PNG exists on disk. Write `banners/raw-NN.png`, run `apply_tb_alpha_blend.py` to `banners/banner-NN.png`, set `banner.path` on every body node, then rebuild

```bash
python3 @images/scripts/rebuild_document.py \
  ./artifacts/<slug>
```

Naked PDF with no JSON — write `stamp-manifest.json` and pass `--manifest`. Render the output file to the user. Chat-only stills are a defect.

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

One landscape generate per section **and per subsection**. Read `visual-system/references/prompt-engineering.md` and `references/literal-figures.md` first when that file exists. Prompt only from named objects in that node, not from the parent chapter at large. Do not put any token from `assets/negative-keywords.csv` into the generate prompt. Differ this prompt from every earlier prompt in the document on at least three axes (object, camera scale, material, setting, key light).

The prompt must

- name the real objects in that section (residues, devices, documents, landforms), not stand-ins
- demand a photoreal or textbook-accurate rendering of those objects
- include an equation or numeral only when that exact string is already in the section text
- add `no caption text, no watermark, no logo, no agency seal, no photoreal portrait of a private person, no allegory, no metaphor architecture`
- stay free of false quantities and invented proper names
- request 3300 x 1856 (floor 2550 x 1434). Ask for an awe-inspiring, stunningly perfected, futuristic cinematic still of the named objects. Never invent a skyline or building that does not appear in the section.
- append the beauty-lock clause from `references/beauty-lock.md` after the named objects
- use the house generate tool. Do not drop a downloaded stock file into the slot. Do not write AI, xAI, or ChatGPT into the prompt.
- refuse to attach a compiled `/latex` equation plate as a banner

Orientation is landscape 16-9. Request 3300 x 1856 px (floor 2550 x 1434). Do not put fade or transparency words in the prompt.

Save the raw file as `banners/raw-NN.png`.

### 3. Inspect

Open `banners/raw-NN.png` with the image reader. Follow the rejection list in `references/literal-figures.md` when present. Regenerate up to three times. Write `banners/qa-NN.md`.

### 4. Size and bleed

Copy `banners/raw-NN.png` through `scripts/apply_tb_alpha_blend.py` to `banners/banner-NN.png`. If a resize is required, LANCZOS-downsize only to 8.5 in wide at 150 px/in or keep 3300 px wide, force 16-9 height, x = 0, no side inset. Do not fade the left or right. Do not call any fade script other than `apply_tb_alpha_blend.py`. Pictorial interior and the left and right columns stay opaque. Top and bottom receive the scripted alpha ramp so the page paper shows through. No left or right margin, padding, letterbox, or crop bar. RGB must not contain a checkerboard. Alpha 0 rows keep real picture RGB.

### 5. Attach

On the section object set banner.path, banner.href, banner.caption, banner.prompt, and banner.source_note.

Caption form

`Section banner. Literal reconstruction of [named object] after [Chicago short title]. Generated model, not a scan of the source.{{n}}`

Default href

`https://digitalmarketingco.org/r/?src=deep-banner&section={section_id}`

Never print the URL on the banner.

### 6. QA

Open the published PNG and confirm

- left and right columns are fully opaque and touch trim
- top and bottom are real alpha ramps, not a baked checkerboard
- no baked checkerboard in RGB
- no burned-in caption
- no allegory passed the inspect step

Rebuild through `rebuild_document.py` (or the parent builder named in `references/emit-file.md`) before delivery. Confirm every body section and every subsection has its own banner in the output file and that each banner touches both page edges.

Coverage fail — a printed subsection heading with no `banner.path` of its own is a defect. Regenerate. Do not crop the parent banner into the child slot.

## Hard rules

- 16-9 landscape. Full bleed left and right at 100 percent page width. Zero left margin, zero right margin, zero left padding, zero right padding. The builder places the banner at x = 0. Left and right columns stay opaque and touch trim. Top and bottom only receive `apply_tb_alpha_blend.py`. No side letterbox. No side crop bar.
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
