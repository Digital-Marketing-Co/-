---
name: extract-dir
description: Extract every published document in a website directory or sitemap into one PDF per URL, using article-clip-pdf and optional copysite plus one banner figure, without rewriting or reprinting the same text twice. Trigger on /extract_dir, extract directory, sitemap white papers to PDF, reprint a site section, or QA-optimize extracted web documents into per-slug folders.
metadata:
  type: workflow
  version: "1.1"
  flag: /extract_dir
  visual_stack: visual-system
---

# /extract_dir


## Visual stack

Documents this skill emits follow `/home/workdir/.grok/skills/visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Reprint each unique published document under a site directory or sitemap path as one letter PDF. Source text is extracted once. Do not run a second writer over the same body.

Skill root is /home/workdir/.grok/skills/extract-dir.
Clip skill is /home/workdir/.grok/skills/article-clip-pdf.
Copysite skill is /home/workdir/.grok/skills/copysite.
Banner skill is /home/workdir/.grok/skills/banner.
Monograph skill is /home/workdir/.grok/skills/phd-ivy-monograph.

Read references/qa-protocol.md before a multi-URL run. Read references/pipeline.md for the locked order.

## When this skill runs

- User typed /extract_dir.
- User asked to turn every white paper, report, or directory listing on a live site into PDFs.
- User stacked article-clip, copysite, banner, and monograph and forbade duplicated steps or duplicated body text.

If no start URL or sitemap is given, stop and ask for one.

## Locked order (do not reorder, do not double-run)

1. Discover unique document URLs from the sitemap or directory index.
2. Deduplicate. Canonical English loc wins. Drop hreflang mirrors, trailing-slash twins, and query variants.
3. Extract article JSON plus in-body images with article-clip-pdf/scripts/extract_article.py. Use copysite --mode page only when the clip extract is empty or the page is an app shell that needs local assets to recover images. Never copysite --mode site for this skill.
4. Attach at most one faded banner figure per document (hero figure, not one figure per heading). Compose the raw figure, then run banner/scripts/apply_banner_fade.py.
5. Build exactly one PDF per URL with article-clip-pdf/scripts/build_cm_pdf.py. Write it into that document folder.
6. Invoke phd-ivy-monograph only when the user explicitly asked for a new research monograph and the source page is not already a complete published white paper. A live white paper is a primary source, not a prompt to rewrite. Skipping the monograph rewrite is the correct anti-duplication action.
7. Run the QA battery in references/qa-protocol.md. Rebuild a single document if it fails. Do not reprint siblings.

## Work paths

ROOT=/home/workdir/artifacts/extract_dir
ROOT/slug/article.json
ROOT/slug/images/
ROOT/slug/banners/banner-00.png
ROOT/slug/Title_Slug.pdf
ROOT/manifest.json

slug is the last path segment of the canonical URL, lowercase, hyphens kept.

## Hard rules

- One PDF per canonical URL. No English plus Spanish pair. No clip PDF plus monograph PDF of the same body.
- Do not invent sections, citations, or equations that the source page does not contain.
- Do not paste site chrome, nav, CTAs, related-story cards, or comments into article.json.
- Visible house link text is exactly Digital Marketing Company. Target is https://digitalmarketingco.org. Plain-text domain is DigitalMarketingCo.org.
- Living footer owner is Web Development Corporation, start year 2012, living year on open.
- Real-alpha banners only. No baked checkerboard.
- Copyable Python goes in a fenced block only when a new helper is written in the conversation.
- Times or Latin Modern only. No tofu, no emoji, no black boxes.


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
