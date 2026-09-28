---
name: images
description: Stamp a full-bleed banner on every section and subsection plus high-resolution literal figures every 500 words. Maximize print size without quality loss, aliasing, blur, or aspect distortion. Full bleed left and right only when the source bitmap already meets the page-width pixel floor. Use when the user types /images, when /list needs section banners, asks for section banners in a PDF, wants a figure every 500 words after the opening blurb, says the figures are metaphors instead of diagrams, or says a figure is soft, stretched, or guttered. Every banner and mid-section figure is unique (no reused path, no reused bytes, no crop of another figure).
metadata:
  type: workflow
  version: "1.6"
  flag: /images
  owner: Web Development Corporation
  visual_stack: visual-system
---

# /images


## Visual stack

Documents this skill emits follow `/home/workdir/.grok/skills/visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Put one context-locked `/banner` image at the start of every body section **and every subsection**, then generate additional figures about every 500 words after that node's opening blurb. Print each figure at the maximum size that stays sharp. Do not upscale, squash, letterbox, fade, or otherwise alias or blur a bitmap to force full bleed. Full bleed left and right is required only when the generated file already meets the page-width pixel floor (2550 px wide on letter, prefer 3300 px). If it does not, regenerate at that floor rather than stretching. Print at full opacity.

Work on an attached PDF, a path the user named, the newest project PDF under `/home/workdir/artifacts/`, or the `list.json` / `deep.json` / `atlas.json` / `folio.json` that built that PDF.

`<skill>` = `/home/workdir/.grok/skills/images`
`<banner>` = `/home/workdir/.grok/skills/banner`
`<deep>` = `/home/workdir/.grok/skills/deep`
`<atlas>` = `/home/workdir/.grok/skills/atlas`
`<folio>` = `/home/workdir/.grok/skills/folio`

Read on demand

- `references/negative-vocabulary.md` — banned prompt tokens
- `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` — negative array
- `references/cadence.md` — 500-word slot math, blurb definition, skip rules
- `references/relevance.md` — prompt lock so each figure matches only that section
- `references/literal-qa.md` — anti-metaphor inspect, resolution, Chicago caption
- `references/uniqueness.md` — one picture per figure, hash audit, full-bleed quality
- `references/handoff.md` — stacking with /banner /deep /atlas /folio /copyright
- `scripts/plan_image_slots.py` — word counts and slot list from JSON or extracted text
- `scripts/extract_pdf_sections.py` — pull section titles and running text from a PDF when JSON is missing
- `scripts/audit_unique_images.py` — fail closed on shared paths or shared bytes

If the user only asked to create or edit this skill and supplied no document, stop after the skill files exist. Do not invent a report.

## When this skill runs

- User typed `/images` and pointed at a PDF, a slug folder, or the current catalog or report build.
- A finished house PDF is missing section banners or mid-section figures.
- A rebuild is about to run and the user wants banners plus a figure every 500 words.
- Existing figures are allegorical, low-resolution, or full of unreadable baked text.

If there is no PDF and no JSON and no section list, ask which file to illustrate. Do not invent sections.

## Workflow

### 1. Locate the source

Search in this order and stop at the first readable target

1. A path named in the current turn
2. A PDF attached in the conversation
3. `list.json`, `atlas.json`, `deep.json`, or `folio.json` in the newest slug folder under `/home/workdir/artifacts/`
4. The newest non-copyright sibling PDF under `/home/workdir/artifacts/`

Prefer the JSON that built the PDF. JSON keeps section ids, banner fields, and paragraph breaks. A naked PDF is a fallback.

### 2. Inventory sections

Body sections **and subsections**. Skip title leaf, contents, Notes, Bibliography, colophon. A subsection is its own node and gets its own banner.

For each body section record

- `section_id` and printed title
- the opening blurb (first one or two paragraphs after the heading and after the banner)
- full word count of remaining body text after the blurb
- existing `banner.path` if any

Run

```bash
python3 <skill>/scripts/plan_image_slots.py \
  /home/workdir/artifacts/<slug>/atlas.json
```

or pass `--pdf path.pdf` when JSON is absent.

### 3. Section banners

Every body section and every subsection gets exactly one full-bleed banner, generated from that node's claims only. Parent banners never stand in for a child heading.

Follow `<banner>/SKILL.md`, `<banner>/references/banner-spec.md`, and `<banner>/references/literal-figures.md`.

- Prompt only from named objects in that section. Photoreal or textbook-accurate. No allegory.
- Landscape, highest available generate resolution (raw at least 2550 px wide, prefer 3300 px / 300 dpi on letter). Photoreal or textbook-accurate of the named objects. No caption text burned in. No watermark. No logo. No agency seal. No photoreal portrait of a private person. No token from `assets/negative-keywords.csv`.
- Maximize print size without quality loss. Reject any figure that is soft, bicubic-stretched, aliased on edges, or aspect-distorted. If the only way to reach page width is an upscale of a narrower bitmap, discard that file and generate again at or above the floor. Full bleed is allowed only when that regenerate already meets the floor.
- Inspect the raw PNG. Reject mirrored letters, wrong numbers, and metaphors. Regenerate up to three times.
- Save `banners/raw-NN.png`, copy or LANCZOS-downsize to `banners/banner-NN.png` at page width. Do not fade. Keep full opacity.
- Set `banner.path`, `banner.caption`, `banner.prompt`, `banner.href`, `banner.source_note` on the section.

Default href

`https://digitalmarketingco.org/r/?src=images-banner&section={section_id}`

If a valid /banner figure already exists, still matches the section as a literal object, and is not a byte- or path-duplicate of any other figure in the document, keep it. Replace it when it is generic, decorative, metaphorical, off-topic, reused, cropped from another section, or below the resolution floor.

### 4. Mid-section figures every 500 words

After the banner and after the opening blurb, insert one generated figure for each full block of about 500 words of remaining section text.

Rules are locked in `references/cadence.md`. Prompt and inspect rules are locked in `references/relevance.md` and `references/literal-qa.md`.

- Word count starts after the blurb, not after the heading.
- Slot count = floor(words_after_blurb / 500).
- Remainder under 500 words gets no extra figure unless the section has zero figures and more than 350 words after the blurb (then one figure).
- Notes, bibliography, equations-only pages, and gazetteer tables do not receive mid-section figures.
- Place each figure immediately after the paragraph that closes the 500-word window so the image sits next to the claims it illustrates.

Prompt each mid-section figure from only the surrounding 500-word window. Save under `figures/fig-{section}-{k}.png`. Generate at least 2550 px wide (prefer 3300 px). In the PDF the figure is 100 percent of page width — x = 0 to page width — with zero left or right margin and zero left or right padding, only when the bitmap already meets that pixel floor. Height follows the generated aspect ratio. Do not letterbox. Do not inset to the text column. Do not squash height to invent a width. No checkerboard. Real photographs of living private persons are forbidden. If a generate comes back narrower than the floor, regenerate. Never print a blurry or aliased stretch.

Caption form

`Figure N. Literal reconstruction of [named object] after [Chicago short title]. Generated model, not a scan of the source.{{n}}`

On JSON documents attach a figure object with path, caption, prompt, after_paragraph, word_anchor, and source_note.

### 5. Generate

Use the house image generate tool for both banners (landscape) and mid-section figures. Do not reuse a figure from another section. Do not copy, crop, fade, or resize one published file into another slot. Do not search-stock a photograph and label it as the section's evidence. Stock or NIH stills may inform the prompt; the published file remains a generated reconstruction and must be cited as such. Each generate call serves exactly one published path.

After each generate, confirm the file exists, is a PNG, and is not a baked checkerboard preview. Open it and run the inspect pass.

Do not fade banners. Do not call apply_banner_fade.py. Leave mid-section figures unfaded and at full opacity.

### 6. Rebuild or restamp

If the source is `atlas.json`, rebuild with `<atlas>/scripts/build_atlas_pdf.py`.
If the source is `deep.json`, rebuild with `<deep>/scripts/build_deep_pdf.py`.
If the source is `folio.json` or `monograph.json`, rebuild with `<folio>/scripts/build_folio_pdf.py`.

If the source is only a PDF and no JSON exists, write a working slug folder, extract text with `scripts/extract_pdf_sections.py`, generate figures, and rebuild through /deep if the document already uses house type. Otherwise ask before inventing a second layout.

Then stamp the living footer with `/copyright` when the user also typed that flag.

### 7. Visual QA

```bash
pdftoppm -png -r 140 /home/workdir/artifacts/<file>.pdf /tmp/images-page
```

Run `scripts/audit_unique_images.py` on the JSON, then raster every page. Rebuild if any of these appear — a shared path or shared hash, a banner that does not match its section, a metaphor standing in for a diagram, a mid-section figure that belongs to a different chapter, tofu or mirrored letters in a figure, clipped type, a checkerboard in RGB, a banner or figure with a left or right gutter, a banner with any edge fade, a burned-in caption, a photoreal private portrait, an invented number in the pixels, a figure jammed into Notes or Bibliography, or a figure that was upscaled from a narrower bitmap.

### 8. Deliver

Give the user the PDF. State page count, banner count, mid-section figure count, uniqueness-audit result (unique hashes vs rasters), words per body section, figures replaced for allegory or reuse, and any section that stayed under the 500-word threshold. Do not dump the JSON into chat.

## Hard rules

- One banner per body section and one banner per subsection. Full opacity. No fade on any edge. Extra figures follow the 500-word cadence only.
- Every published raster is unique. No shared path, no shared bytes, no crop of another figure in the same document. Audit with `scripts/audit_unique_images.py` and fail closed.
- Every prompt is locked to the surrounding text. No generic science-lab figure on a legal chapter. No allegory on a chemistry chapter.
- Banners and mid-section figures print at the maximum sharp size the file supports. Full bleed left and right (x = 0 to page width, zero side gutter) only when the source already meets the 2550 px page-width floor. Height follows source aspect. Never upscale a small preview to page width. Never introduce aliasing, blur, or aspect distortion to buy bleed. Banners stay fully opaque on every edge.
- Mid-section figures are captioned, generated, context-locked to the 500-word window, and source-cited in Chicago notes. They are not in-column insets.
- Visible house anchor is Digital Marketing Company. Target is https://digitalmarketingco.org. Plain-text domain is DigitalMarketingCo.org.
- No emoji. No unsupported symbols. No invented sources. No fake agency seals.
- Do not burn raw TeX into a figure. If a banner or figure must show an equation, compile it first. Run `/latex` `scan_raw_tex.py` on the rebuilt PDF before delivery.
- Do not reprint builder scripts into chat.


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

Exit code 1 blocks delivery. Repair with `/latex` equation figures, attach a variable table under every display equation (Identifier, Term, Quantity, Explanation), rebuild, scan again, and raster every page. See `/home/workdir/.grok/skills/itqe/references/render-gate.md` and `/home/workdir/.grok/skills/latex/SKILL.md`.

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
