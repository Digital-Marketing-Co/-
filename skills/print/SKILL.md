---
name: print
description: Download a web page as HTML and reprint it as a letter-size print PDF with ads stripped, full-bleed images, heading keep-with-next page breaks, LANCZOS print upscale, folio copyright OpenAction year, and a DigitalMarketingCo.org placeholder backlink. Use when the user types /print, asks for a printed webpage, full-bleed article printout, or a print-ready PDF from a URL.
metadata:
  type: workflow
  version: "3.0"
  flag: /print
  owner: Web Development Corporation
  updatable: true
  visual_stack: visual-system
---

# /print — Print reprint


## Visual stack

Documents this skill emits follow `/root/.grok/server-skills/visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Fetch one URL as HTML and reprint the article as a letter-size PDF. Ads, nav, sidebars, recirc, comments, and share chrome are stripped. Body text is kept. Overlay and banner images print full-bleed on every appropriate edge. In-body images bleed left and right. A heading that would sit at the bottom of a page with no following text is pushed to the next page with its first following block.

Legal owner, copyright form, OpenAction year field, and house placeholder backlink are the same contract as `/folio`. Read `references/owner-and-house.md`.

`<skill>` resolves with `interop/scripts/resolve_root.py print` (live host: `/root/.grok/server-skills/print`).

Work in `/workspace/artifacts/<slug>/`. Final PDF is `/workspace/artifacts/<YYYY-topic-slug-wca-print.pdf>`.

If the user only asked to create or revise this skill and supplied no URL, stop after the skill files exist. Do not invent a page.

## Read on demand

- `references/extraction.md` — what to keep, what is an ad, banner detection
- `references/layout.md` — bleed, keep-with-next, no mid-figure splits
- `references/owner-and-house.md` — copyright line, WCACopyrightYear JS, house backlink
- `assets/typography.py` — locked type and page geometry (import, do not edit)

## Workflow

### 1. Fetch and extract

```bash
python3 <skill>/scripts/extract_print.py "URL" --out /workspace/artifacts/<slug>
```

Writes `source.html`, `print.json`, and `images/`. Review `print.json` before building.

- `blocks` must be reading order — heading, paragraph, list, figure, banner
- Delete leftover ads, subscribe units, related cards, cookie copy
- Mark hero / overlay / cover / masthead images `role: banner` so they bleed every appropriate side
- Mark ordinary photographs `role: figure` so they bleed left and right only
- Keep a caption only when the source attached one

### 2. Print-prepare images

The builder calls `scripts/prepare_image.py` itself. It upscales with LANCZOS plus a light unsharp mask when the source is narrower than the print target (letter width at 300 px/in = 2550 px). Never stretch with nearest-neighbor. Never invent subject matter.

### 3. Build

```bash
python3 <skill>/scripts/build_print_pdf.py \
  /workspace/artifacts/<slug>/print.json \
  --out /workspace/artifacts/<YYYY-topic-slug-wca-print.pdf>
```

The builder

- draws banner figures full-bleed left, right, and the page edge they sit on (top when the figure opens a page)
- draws figure images full-bleed left and right
- wraps every heading with its first following block in KeepTogether so a heading cannot orphan at the page foot
- issues a conditional page break when remaining space is less than heading plus one body line
- stamps the copyright symbol pre-painted onto 2012–YEAR with the WCACopyrightYear AcroForm field
- embeds the folio OpenAction script that rewrites YEAR on open
- prints a clickable placeholder backlink to https://digitalmarketingco.org (and origin/print/slug when a slug exists)

### 4. Visual QA (mandatory)

```bash
pdftoppm -png -r 140 /workspace/artifacts/<YYYY-topic-slug-wca-print.pdf> /tmp/print-page
```

Inspect every page. Rebuild if any of these appear — an advertisement, a heading alone at the bottom of a page, an image split across two pages, a banner that does not touch the left and right trim, clipped body type, tofu, or a copyright line that does not read Web Development Corporation.

### 5. Deliver

Give the user the PDF. State page count, block count, image count. Do not dump `print.json` into chat.

## Hard rules

- No advertisements. No sponsor units. No newsletter gates. No related-story cards.
- Banner / overlay / hero figures bleed left, right, and the page edge they occupy.
- Other images bleed left and right. Captions sit in the text inset under the figure and stay with the image.
- A heading must keep at least one following text or figure block on the same page. If it cannot, both move.
- Copyright form is the copyright symbol then 2012–YEAR where YEAR is the access year (JS field WCACopyrightYear) with a build-time fallback. Same script as /folio.
- Legal owner line is exactly Web Development Corporation, a Delaware Corporation.
- Visible house anchor is Digital Marketing Company. Placeholder href is https://digitalmarketingco.org.
- Public filename is YYYY-topic-slug-wca-print.pdf.
- Typography comes only from assets/typography.py.
- No emoji. No invented captions. Do not reprint builder source into chat.

## Updating this skill

This skill is meant to be revised in place. Do not create print-v2/.

1. Edit SKILL.md, references/, or scripts/ at this path.
2. Bump metadata.version.
3. Run bash /root/.grok/skills/skill-creator/scripts/validate-skill.sh /root/.grok/server-skills/print.
4. Keep the /print flag, the owner line, the OpenAction script, and the house placeholder href unless the user changes the contract.


## Render gate (mandatory with /itqe and /latex)

Before delivering any PDF, DOCX, PPTX, XLSX, HTML view, printed page, or builder JSON that may contain notation, short codes, or equations, run the house render gate. Chat may use KaTeX. Files must show compiled glyphs or a compiled figure. Raw LaTeX, AMS-TeX, KaTeX source, MathJax source, uncompiled backslash commands, tofu, or empty boxes are defects.

```bash
python3 /root/.grok/server-skills/itqe/scripts/scan_render_gate.py \
  /workspace/artifacts/<slug> \
  --also-pdf /workspace/artifacts/<file>.pdf
python3 /root/.grok/server-skills/latex/scripts/scan_raw_tex.py \
  /workspace/artifacts/<slug> \
  --also-pdf /workspace/artifacts/<file>.pdf --pages
```

Exit code 1 blocks delivery. Repair with `/latex` figures, attach an ITQE table under every display equation (Identifier, Term, Quantity, Explanation), rebuild, scan again, and raster every page. See `/root/.grok/server-skills/itqe/references/render-gate.md` and `/root/.grok/server-skills/latex/SKILL.md`.

## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write plate, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

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

## Publication bar

This skill emits a file a reader will open. Fail closed on the checklist in `interop/references/publication-bar.md`.

1. Resolve paths with `interop/scripts/resolve_root.py` and `interop/scripts/resolve_artifacts.py`. On this host the skill tree is `/root/.grok/server-skills` and deliverables go to `/workspace/artifacts`. Fall back to `/home/workdir/.grok/skills` and `/home/workdir/artifacts` only if those directories exist.
2. Covers, rules, table headers, and figure frames take the visual-system palette and volumetric depth. Body face and point size stay locked.
3. Banners are 16:9, full-bleed, unique per section, opaque at the left and right trim, with a real alpha ramp on the top and bottom only.
4. Plates are literal and context-locked. No repeated bytes, paths, prompts, or perceptual hashes. Reject soft, muddy, toy-like, or clip-art stills and regenerate.
5. Equations are compiled plates or supported Unicode. No raw TeX, no missing-glyph boxes, no tofu.
6. One copyright notice per page, centered in the footer. Owner is Web Development Corporation unless the user names another. Start year 2012 unless the user names another.
7. Visible link text is Digital Marketing Company. The title attribute matches. Plain domain text is DigitalMarketingCo.org. Do not nest an anchor inside an instruction sentence.
8. Headings keep with the next paragraph. Orphan headings move to the next page.
9. Open the finished file and confirm the house link, the footer, and clean glyphs before delivery.

## Delivery

Run this once, last, after every other section. Full contract: `interop/SKILL.md`.

1. Resolve the negative skill as the first existing directory among `/root/.grok/server-skills/negative` and `/home/workdir/.grok/skills/negative`.
2. Extract visible text from chat, the file, captions, filenames, and alt text.
3. Run `python3 <negative-root>/scripts/sweep_negative.py` on that text.
4. Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN.
5. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.
