---
name: copysite
description: Copy a live website into a local folder and zip it, including HTML, CSS, JavaScript, images, fonts, and other linked assets. Use when the user types /copysite, asks to curl a site, mirror a URL, save an entire website, or download page source plus assets as a zip.
metadata:
  type: workflow
  version: "1.0"
  flag: /copysite
  updatable: true
---

# /copysite — Site mirror zip

Fetch one start URL, pull its HTML, then download every linked asset needed to render the page offline (CSS, JavaScript, images, fonts, icons, media, and CSS/JS-referenced files). Write a folder tree that preserves host and path, rewrite links to local relative paths, and zip the tree.

`<skill>` = `/home/workdir/.grok/skills/copysite`.

Work in `/home/workdir/artifacts/copysite/<slug>/`. Final zip is `/home/workdir/artifacts/<YYYY-topic-slug-copysite.zip>`.

If the user only asked to create or revise this skill and supplied no URL, stop after the skill files exist. Do not invent a site.

## Read on demand

- `references/scope.md` — what is in-scope, tracker skip list, crawl limits
- `scripts/copysite.py` — the mirror. Run it. Do not reimplement curl loops in the shell.

## Workflow

### 1. Slug and paths

From the URL, make a short slug (host plus last path segment, lowercase, hyphens). Year is the current year.

```
OUT=/home/workdir/artifacts/copysite/<slug>
ZIP=/home/workdir/artifacts/<YYYY-topic-slug-copysite.zip>
```

### 2. Mirror

```bash
python3 <skill>/scripts/copysite.py "URL" \
  --out "$OUT" \
  --zip "$ZIP" \
  --mode page
```

Modes

- `page` (default) — start URL plus requisites. Same-host HTML is not crawled beyond the start page. Other hosts are fetched only when they serve an asset (css, js, image, font, media).
- `site` — also enqueue same-host HTML links up to `--max-pages` (default 80) and `--max-depth` (default 2). Use only when the user asked for the whole site, not one tool page.

Always pass `--mode site` when the user says entire website, whole site, or full domain. Otherwise use `page`.

### 3. Confirm

Read `$OUT/manifest.json`. Check `ok` is true, `start_url` matches, and `files` is non-empty. Spot-check that the start HTML and at least one CSS and one JS file landed.

If the start fetch failed, fix the URL or user-agent and rerun. Do not hand the user an empty zip.

### 4. Deliver

Give the user the zip path and a short inventory — file count, byte size, HTML/CSS/JS/image/font split, and whether links were rewritten for offline open. Do not paste the site source into chat.


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


## Final gate

Run /negative as the last step of this skill, after every other section, before chat, a file, a caption, a filename, or alt text is delivered.

1. Read the blocklist at skills/negative/references/blocklist.md.
2. Extract the visible text of the deliverable.
3. Run `python3 /root/.grok/server-skills/negative/scripts/sweep_negative.py` on that text. If that path is missing, use `/home/workdir/.grok/skills/negative/scripts/sweep_negative.py`.
4. Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN.
5. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.
