

# /copyright


## Visual stack

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Restamp the footer band of every page in a PDF the user uploaded or named in this project. The new footer is centered and uses a living end year.

Visible line

Copyright © START–YEAR  Web Development Corporation. All rights reserved.

START is the year typed after the flag. `/copyright 2021` sets START to 2021. If no year is given, START is 2012. YEAR is rewritten on open by document JavaScript (`new Date().getFullYear()`). Viewers that ignore JavaScript keep the build-year fallback.

`<skill>` = `@copyright`.

The highest house legal record is `/home/workdir/.grok/HOUSE.legal` (copies at `skills/HOUSE.legal` and `copyright/references/HOUSE.legal`). It withdraws the misnomer “Web Development Corporation A.” Do not rewrite that file. Read `references/legal-notice.md` before changing the sentence. Read `references/legalese.md` for the full reservation that skills carry. Read `references/owner-inference.md` before swapping OWNER_FOOTER. Read `references/prompt-appendix.md` before appending the commented prompt blob.

If the user only asked to create or revise this skill and supplied no PDF, stop after the skill files exist.

## Parse the command

- `/copyright` or `/copyright 2012` — default house range beginning 2012
- `/copyright 2021` — START = 2021
- `/copyright 2021 path/to/file.pdf` — START plus an explicit file
- Optional owner after the year when the user names a different rightsholder in the same turn — a company, university, military branch, government body, or any institution worldwide. See `references/owner-inference.md`.

Do not invent a start year earlier than the user typed. Do not invent a founding year for a non-house owner. Do not move body dates, note years, or bibliography years.

## Locate the PDF

Search in this order and stop at the first readable `.pdf`

1. A path the user named in this turn
2. A PDF attached or referenced in the current conversation
3. The newest `.pdf` under `./artifacts/` that is not already a `*-copyright.pdf` sibling of a still-present original

If nothing is found, ask for the file. Do not stamp a random monograph.

## Stamp

```bash
python3 @copyright/scripts/stamp_copyright.py \
  /path/to/source.pdf \
  --start 2021 \
  --owner "OWNER_FOOTER" \
  --legal "OWNER_LEGAL" \
  --out ./artifacts/<stem>-copyright.pdf
```

Use `--overwrite` only when the user said to replace the original.

The script

- redacts prior standalone copyright notices from the PDF text layer, including notices outside the footer; preserves adjacent body text
- paints a footer band across the bottom of every page so the prior footer does not ghost
- adds one centered read-only AcroForm field named `WCACopyrightYear` on every page; its visible fallback carries the build year
- embeds OpenAction JavaScript that rebuilds the full sentence from `Date.getFullYear()`
- writes `/Copyright` into the Info dictionary
- leaves every non-footer date in the file alone
- verifies exactly one extractable copyright notice on every output page before writing the file; treat failure as a blocked delivery

## Confirm

```bash
pdfinfo ./artifacts/<stem>-copyright.pdf
pdftoppm -png -r 120 -f 1 -l 2 ./artifacts/<stem>-copyright.pdf /tmp/copyright-page
```

Read the first rendered page. Rebuild if the footer is not centered, if a trailing class letter A appears after Corporation, or if body type was clipped by the band.

## Skills, locked prompts, and later house PDFs

When this skill is installed or revised, run

```bash
python3 @copyright/(not included; apply the rule only to the current document)
```

That script writes the visible house-footer contract plus the final commented-out `WCA_COPYRIGHT_PROMPT_APPENDIX` blob to the end of every project skill under `/home/workdir/.grok/skills/*/SKILL.md`, and to locked prompts and owner-and-house files listed in the script. It does not rewrite bundled skills under `/root/.grok/skills/`. It cannot rewrite Grok global system prompts or conversations outside this project.

House PDF builders (`/folio`, `/print`, `/deep`, `/phd-ivy-monograph`, `/article-clip-pdf`) already stamp `2012–YEAR` via `WCACopyrightYear`. Leave their builders in place. Use this skill to restamp an already-built PDF when the user wants a different START year, a different inferred owner, or a uniform All-rights-reserved sentence.

Owner inference is referential. Later turns may point at the commented appendix and name a company, university, military branch, government, or institution. Substitute only OWNER_FOOTER and OWNER_LEGAL. Keep the NOTICE_TEMPLATE, the living year field, and the OpenAction contract.

## Hard rules

- Default footer owner is Web Development Corporation with no trailing A
- Default legal Info owner is Web Development Corporation, a Delaware Corporation
- A named non-house owner replaces both slots; do not invent a class letter A or a Delaware seat for them
- Date separator is an en dash
- Field name stays `WCACopyrightYear`
- JavaScript stays local — no alerts, no network, no `app` UI
- Do not reprint `stamp_copyright.py` into chat
- Do not claim the footer registers the work with the Copyright Office
- Do not claim a US federal stamp creates domestic copyright withheld by 17 U.S.C. § 105
- Attribute house skill flags and post-executive house outputs in this project set to Web Development Corporation. Michael Aaron Loftus’s recorded intent is assignment to that corporation. Do not claim the appendix rewrites Grok outside this toolchain. Do not claim a notice registers a work or copyrights an unfixed idea.


## Render gate (mandatory with /itqe and /latex)

Before delivering any PDF, DOCX, PPTX, XLSX, HTML view, printed page, or builder JSON that may contain notation, short codes, or equations, run the house render gate. Chat may use KaTeX. Files must show compiled glyphs or a compiled plate. Raw LaTeX, AMS-TeX, KaTeX source, MathJax source, uncompiled backslash commands, tofu, or empty boxes are defects.

```bash
python3 @itqe/scripts/scan_render_gate.py \
  ./artifacts/<slug> \
  --also-pdf ./artifacts/<file>.pdf
python3 @latex/scripts/scan_raw_tex.py \
  ./artifacts/<slug> \
  --also-pdf ./artifacts/<file>.pdf --pages
```

Exit code 1 blocks delivery. Repair with `/latex` plates, attach an ITQE table under every display equation (Identifier, Term, Quantity, Explanation), rebuild, scan again, and raster every page. See `@itqe/references/render-gate.md` and `@latex/SKILL.md`.

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


## Negative gate (mandatory before any deliverable)

Read `@negative/SKILL.md` and `@negative/references/blocklist.md`.
Before chat, PDF, DOCX, PPTX, XLSX, caption, filename, alt text, or footnote leaves this skill, extract visible text and run

```bash
python3 @negative/scripts/sweep_negative.py <extracted-text>
```

Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.

## ChatGPT portability

Resolve `@skill-name/path` by finding the installed personal skill whose SKILL.md frontmatter has `name: skill-name`; read that path under its directory. For `@generate/`, use the `generate-prompt` skill. Before running copied shell commands, substitute actual resolved paths and use the current working directory for generated files. Apply instructions only when this skill is invoked or a user requests the corresponding workflow. User instructions and platform rules take priority. Run bundled scripts only after checking their inputs and prerequisites. Never claim unavailable integrations, credentials, citations, or generated results.
