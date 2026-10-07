---
name: article-clip-pdf
description: Extract a web article from a URL and reprint it as a clean Computer Modern PDF with only the article text plus in-article images. Use when the user pastes a news or blog link and wants a PDF, clip, reprint, reader view, Computer Modern export, or text-and-images only with ads, sidebars, related stories, and comments stripped. Images stay in source reading order, never duplicate, print at 100 percent page width with zero left or right margin or padding, keep source aspect ratio, and LANCZOS-upscale when the source bitmap is narrower than print.
metadata:
  type: workflow
  version: "1.3"
  visual_stack: visual-system
  flag: /clip
---

# Article Clip PDF


## Visual stack

Documents this skill emits follow `/home/workdir/.grok/skills/visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Reprint one web article as a letter-size PDF set in Latin Modern Roman (Computer Modern). No site chrome.

## Workflow

Work in `/home/workdir/artifacts/<slug>/`.

1. Extract

```bash
python3 <skill>/scripts/extract_article.py "URL" --out /home/workdir/artifacts/<slug>
```

`<skill>` is this skill directory (`/home/workdir/.grok/skills/article-clip-pdf`).

2. Review `article.json`

- Title, author, date, source name must match the page
- `paragraphs` must be the article only — delete share crumbs, related-story blurbs, newsletter CTAs
- `blocks` is the reading-order stream (headings, paragraphs, images). Prefer it over dumping images after paragraph two
- `images` must be the hero plus in-body media, each figure once. Delete card thumbs from Keep Reading / Trending
- Drop duplicates even when the CMS emits both an og:image and the same hero, or the same file as jpg and webp. Match on normalized URL, SHA-256, and perceptual hash
- Keep a caption only when it belongs to that image. Leave caption empty rather than inventing one
- YouTube iframes should already be a thumbnail plus iframe title
- Do not invent a second copy of an image to fill a layout slot. If the source used one figure, the clip uses one figure

If extraction is messy, read `references/extraction.md` and edit the JSON.

3. Build

```bash
python3 <skill>/scripts/build_cm_pdf.py /home/workdir/artifacts/<slug>/article.json \
  --out /home/workdir/artifacts/<Title_Slug>.pdf
```

Fonts are bundled at `assets/fonts/lmroman10-*.ttf`. Do not point reportlab at the TeX `.otf` files (CFF outlines fail).

4. Visual QA (mandatory)

```bash
pdftoppm -png -r 150 /home/workdir/artifacts/<Title_Slug>.pdf /tmp/clip-page
```

Inspect every page. Rebuild if text is clipped, images overflow, glyphs are missing, or leftover chrome snuck in.

5. Deliver the PDF. One-line source note is already in the footer/source line — do not append extra branding.

## Layout rules

- Letter, ~0.85 in side margins for type, justified body, CM bold title, CM italic byline
- Images follow the source corpus. A figure that sat between two paragraphs in the HTML sits between those same paragraphs in the PDF. Never bunch leftover figures after paragraph two or at the end unless that is where they were in the source
- Each distinct figure prints exactly once. Hash-collapse og/hero/srcset variants
- Every image is 100 percent of the page / viewport width. Zero left margin, zero right margin, zero left padding, zero right padding. The bitmap starts at x = 0 and ends at page width. Type keeps the 0.85 in inset; figures ignore it and do not letterbox
- Preserve the source aspect ratio exactly (height = page_width * source_h / source_w). Never squash or stretch to a fixed band height
- LANCZOS-upscale any bitmap narrower than page-width at 150 dpi before embedding. Do not bake a checkerboard into RGB
- A portrait taller than the sheet stays 100 percent wide and is height-clipped to the printable sheet rather than inset
- Any AI figure later inserted into a clip follows the same 100-percent-width, zero-side-gutter, aspect-locked rule and must be context-locked to the surrounding paragraph at the highest available generate resolution
- Footer — site name left, page number right, living copyright centered underneath
- Unicode apostrophes and quotes are fine in the bundled TTFs. Never substitute boxes.
- Strip emoji and other glyphs Latin Modern lacks (the scripts already drop common emoji). If a page PNG shows tofu, delete that character from article.json and rebuild.

## Scope

This skill is for a single article URL. It is not a multi-page site scrape, not a research report, and not a generic save-webpage-as-PDF printout of the live layout.


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
