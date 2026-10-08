---
name: list
description: Compile a complete, deduplicated inventory of every single instance of a user predicate by iterative multi-round research until two empty rounds, then emit a structured list catalog with full-bleed section and subsection banners, max-sharp images, and a living copyright footer. Trigger on /list, complete list of every, list every single, inventory every, enumerate all instances, or when the user pastes a predicate after /list. Stacks with /banner, /images, and /copyright by default. Do not use for an author harvest (that is /corpus) or a non-list report alone (that is /deep, /folio, or /iterate).
metadata:
  type: workflow
  version: "1.2"
  flag: /list
  stacks: banner, images, copyright, folio, deep, iterate, itqe, latex
  owner: Web Development Corporation
  visual_stack: visual-system
---

# /list — complete inventory of every single {{input}}


## Visual stack

Documents this skill emits follow `/home/workdir/.grok/skills/visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Turn one predicate into a closed, deduplicated catalog of every reachable instance. Research is iterative and multi-round. A first search page is never the list. Stop only when the saturation gate closes. Then print a structured inventory. Default stacked flags are `/banner`, `/images`, and `/copyright`.

Work in `/home/workdir/artifacts/list-<slug>/`. Default printed catalog is `/home/workdir/artifacts/<YYYY>-<slug>-list.pdf`.

`<skill>` = `/home/workdir/.grok/skills/list`
`<banner>` = `/home/workdir/.grok/skills/banner`
`<images>` = `/home/workdir/.grok/skills/images`
`<copyright>` = `/home/workdir/.grok/skills/copyright`
`<folio>` = `/home/workdir/.grok/skills/folio`
`<deep>` = `/home/workdir/.grok/skills/deep`
`<iterate>` = `/home/workdir/.grok/skills/iterate`

Read on demand

- `references/locked-prompt.md` — rewritten execution prompt with flag placement
- `references/negative-vocabulary.md` — banned prompt tokens
- `assets/negative-keywords.csv` — portable negative array
- `assets/negative-keywords.xlsx` — preserved workbook
- `references/research-protocol.md` — rounds, operators, stop gate
- `references/dedup.md` — identity keys and merge rules
- `references/emit-handoff.md` — catalog PDF and stacked flags
- `assets/schema/list.schema.json` — `list.json` shape
- `scripts/new_round.py` — stamp a round file and saturation counters

If the user only asked to create or revise this skill and supplied no predicate, stop after the skill files exist. Do not invent a list.

## When this skill runs

- User typed `/list` followed by a predicate (`{{input}}`)
- User asked for a complete list of every single X, every instance of X, or an inventory of all X
- A stacked run (`/list /banner /images /copyright`, `/list /folio`, `/list /deep`) needs the inventory before figures and footer

Do not use this skill for an author-only harvest (`/corpus`), a spatial catalog (`/atlas`), or a narrative report that is not an inventory.

## Rewritten execution prompt

Place flags in this order. `{{input}}` is the remainder of the user message after `/list` and after any stacked flags.

```
/list {{input}} /banner /images /copyright

Iterate targeted search, primary-source reads, and rival-list crosswalks until you compile a deduplicated inventory of every single instance of {{input}}. Close a branch only after two consecutive empty targeted rounds. Do not stop at the first results page. Do not invent instances. Prefer primary PDFs, university-press work, .gov, and .mil.

Then emit the structured catalog.

/banner — one full-bleed left-and-right banner on every body section and every subsection. Zero left margin, zero right margin, zero left padding, zero right padding. Height follows source aspect. Print at full opacity. Do not fade the top edge. Do not fade the bottom edge. Do not fade the left or right edges.

/images — generate each figure at the maximum print size that does not lose quality and does not introduce aliasing, blur, or aspect distortion. Full bleed left and right only when the source bitmap already meets the page-width pixel floor so the print does not upscale, squash, or letterbox.

/copyright — restamp every page with the living centered footer. START defaults to 2012 unless the user typed /copyright YYYY. YEAR is Date.getFullYear on open. Default owner is Web Development Corporation.
```

When the user also typed `/folio` or `/deep`, those builders run after the inventory exists. `/iterate` may enlarge the catalog before emit.

## Workflow

### 1. Lock the predicate

Treat the remainder after `/list` and after stacked flags as `{{input}}`.

Write `scope.md`

- working title (`Complete list of every single {{input}}`)
- predicate in one sentence
- unit of analysis (what counts as one instance)
- inclusion rules
- exclusion rules
- geography, period, language limits if the user set them
- stacked flags actually present (banner, images, copyright are on by default)
- emit target (`list` catalog default; `folio` or `deep` when those flags appear)

Slug the folder `list-<short-predicate>`.

If `{{input}}` is empty, stop and ask what to list. Do not invent a predicate.

### 2. Open the ledger

```bash
python3 /home/workdir/.grok/skills/list/scripts/new_round.py \
  /home/workdir/artifacts/list-<slug> \
  --predicate "{{input}}" \
  --init
```

Keepers live in `items.jsonl`. Sources live in `sources.jsonl`. Each pass writes `rounds/round-NN.md` and updates `ledger.json`.

### 3. Iterate until saturation

Follow `references/research-protocol.md`. One iteration is one closed research pass, not one query.

Each pass must

1. Run several targeted searches (exact phrase, official registries, scholarly indexes, government and military catalogs, rival published lists)
2. Open primary pages or PDFs for candidate instances
3. Record every keeper with a stable identity key (see `references/dedup.md`)
4. Record why rejected candidates failed the unit-of-analysis test
5. Write new research questions that the current list still cannot answer
6. Close the round in `ledger.json`

Caps that stop infinite recursion

- 12 research rounds or two consecutive empty targeted rounds, whichever comes first after at least four rounds
- 400 keeper items unless the user raised the cap
- depth 4 from the predicate root

A round is empty when it adds zero new keepers after dedup. Two consecutive empty rounds close the gate. Do not claim completeness if a named official register was never opened.

Never fabricate an instance, an identifier, a count, or a page number.

### 4. Deduplicate and classify

Merge `items.jsonl` on the identity keys in `references/dedup.md`. One real-world instance equals one row.

Write `taxonomy.md` and attach a `class` field on each item so the printed catalog can open a subsection per class. Classes are derived from the keepers, not invented in advance.

Write `gaps.md` for registers that were unreachable, paywalled, or unnamed.

### 5. Draft the catalog

Write `outline.md`, then `list.json` matching `assets/schema/list.schema.json`.

Required front matter — title, subtitle, date, house block, abstract (the predicate plus the keeper count plus the saturation rule), keywords.

Required body

1. Predicate and unit of analysis
2. Method, source tiers, and saturation log
3. Master inventory (the complete numbered list)
4. One subsection per taxonomy class
5. Residual gaps and open registers
6. Bibliography

Each section **and each subsection** is a body node. Notes and Bibliography do not receive banners.

Paragraphs that cite a source use `{{n}}` markers. Explain every variable, subscript, and constant the first time an equation appears.

Do not print a house-marks prose sentence. House presence on every page is two centered three-dimensional buttons stamped by `/copyright`: Digital Marketing Company → https://digitalmarketingco.org and Web Development Corporation → https://WebDevelopment.tv. Button title text equals the visible name. Buttons open in a new window.

### 6. Stacked figures and footer

Default stack runs in this order

1. Inventory and `list.json` exist
2. `/banner` — one banner per section **and** per subsection. Follow the current `<banner>/SKILL.md` (subsection contract is mandatory). Full bleed left and right. Zero side gutter. Full opacity. No fade on any edge.
3. `/images` — additional figures only when a section's remaining words after the blurb earn them. Maximize print size without quality loss, aliasing, blur, or aspect distortion. Full bleed left and right only when the bitmap already meets the page-width floor. Follow the current `<images>/SKILL.md`.
4. Build the catalog PDF (house list builder, or `/folio` / `/deep` when those flags are present)
5. `/copyright` — living footer on every page

Do not skip banners on subsections. Do not stretch a narrow preview to page width.

### 7. Render gate and deliver

```bash
python3 /home/workdir/.grok/skills/itqe/scripts/scan_render_gate.py \
  /home/workdir/artifacts/list-<slug> \
  --also-pdf /home/workdir/artifacts/<file>.pdf
python3 /home/workdir/.grok/skills/latex/scripts/scan_raw_tex.py \
  /home/workdir/artifacts/list-<slug> \
  --also-pdf /home/workdir/artifacts/<file>.pdf --pages
```

Exit code 1 blocks delivery.

Give the user the PDF. State keeper count, round count, empty-round pair that closed the gate, banner count (sections plus subsections), mid-section figure count, uniqueness-audit result, and residual gaps. Do not dump `list.json` into chat.

## Hard rules

- The list is the product. Narrative chapters exist only to define the predicate, the method, and the classes.
- Two consecutive empty targeted rounds close research. Do not stop earlier. Do not invent a third empty-round story to look complete.
- One real instance, one row. Dedup before print.
- Banner every section and every subsection. Full bleed left and right.
- Images print at the largest sharp size the bitmap supports. No upscale, no aliasing, no blur, no squash. Full bleed only when that rule still holds.
- No raw TeX on a visible page. No tofu. No checkerboard RGB. No reused figure bytes.
- No emoji. No invented sources. No fake agency seals.
- Do not print a house-marks prose sentence. House marks are two centered 3D buttons: Digital Marketing Company and Web Development Corporation.

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

Read `/home/workdir/.grok/skills/negative/SKILL.md` and `/home/workdir/.grok/skills/negative/references/blocklist.md`.
Before chat, PDF, DOCX, PPTX, XLSX, caption, filename, alt text, or footnote leaves this skill, extract visible text and run

```bash
python3 /home/workdir/.grok/skills/negative/scripts/sweep_negative.py <extracted-text>
```

Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.
