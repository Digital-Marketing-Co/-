---
name: summarize
description: Summarize, rewrite, and humanize source text on a locked 0-5 scale. Trigger on /summarize, summarize this, rewrite this, humanize this, make this less AI, or a stacked flag such as /summarize /deep /folio /banner. Default pipeline is summarize then rewrite then humanize. Does not invent facts, citations, or locked house numbers.
metadata:
  type: workflow
  version: "3.0"
  flag: /summarize
  visual_stack: visual-system
---

# /summarize


## Visual stack

Documents this skill emits follow `/root/.grok/server-skills/visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Take one source and walk it through a locked scale. The default walk is summarize, then rewrite, then humanize (levels 2 then 3 then 4). The output must keep every proper name, date, measurement, path, URL, and house rule that the source actually contains.

`<skill>` resolves with `interop/scripts/resolve_root.py summarize` (live host: `/root/.grok/server-skills/summarize`)

Read on demand

- `references/scale.md` — the 0-5 scale, tells, and bans
- `references/handoff.md` — how this skill talks to /deep, /folio, and /banner
- `references/humanize.md` — voice rules that stop stock LLM cadence

Work in `/workspace/artifacts/summarize-<slug>/` when the pass is more than a short chat reply.

If the user only asked to create or revise this skill and supplied no source, stop after the skill files exist. Do not invent a source.

## When this runs

- User typed `/summarize`
- User asked to summarize, rewrite, humanize, destock, or make this sound like a person
- User stacked `/summarize` with `/deep`, `/folio`, and/or `/banner`
- User pointed at a skill file, a PDF, a URL, a prior folio, or pasted text

If there is no source, stop and ask for it.

## Source lock

Copy the source into `source.md` or `source.txt` before touching it. Do not edit the lock file.

Acceptable sources

- pasted text
- a URL (clip the article first with article-clip-pdf extract, then summarize the article body)
- a project skill path (`deep/SKILL.md`, `folio/SKILL.md`, `banner/SKILL.md`)
- a prior `deep.json`, `folio.json`, or finished PDF text extract
- the current user prompt when they say "this prompt"

Never treat a skill rewrite as a license to change locked type sizes, fade inches, owner strings, OpenAction field names, or filename patterns.

## The scale

Full definitions live in `references/scale.md`. Use these names in chat and in `pass.json`.

- 0 Verbatim — return the source. No compression.
- 1 Compress — cut filler. Keep original sentences where they already work.
- 2 Summarize — keep the argument, drop the tour. Facts stay.
- 3 Rewrite — new sentences, same claims. Clean syntax. Still institutional.
- 4 Humanize — spoken cadence. Concrete verbs. No fake warmth. No invented color.
- 5 Teach — humanize plus why it matters, still inside the source's facts.

Default when the user types `/summarize` with no level — run 2, then 3, then 4, and deliver the level-4 text with a short level-2 abstract on top.

If they name a single verb, map it.

- summarize → 2
- rewrite → 3
- humanize → 4
- rewrite then humanize → 3 then 4
- teach / explain like a person → 5

## Workflow

### 1. Scope

Write `scope.md`

- source kind and path
- requested level or the default 2-3-4 walk
- keep list (names, numbers, paths, flags, owner lines)
- drop list (ads, chrome, repeated throat-clearing)
- stacked skills, if any (`/deep`, `/folio`, `/banner`)

### 2. Passes

Write `passes/L2.md`, `passes/L3.md`, `passes/L4.md` as needed. Each pass reads only the previous pass plus the source lock. A later pass may not add a fact the source lock does not contain.

Record the walk in `pass.json` with keys source, walk, kept, dropped, handoff.

### 3. Voice check

Read `references/humanize.md`. Reject the draft and rerun level 4 if any of these appear

- In today's rapidly evolving landscape
- It is important to note that
- delve, tapestry, underscore, leverage, robust, seamless, cutting-edge used as decoration
- a claim the source lock does not support
- a locked house number that drifted (22 pt, 18 pt, 4.35 in, 2012, WCACopyrightYear)

### 4. Optional handoff

If the user also typed `/folio` or `/deep`, follow `references/handoff.md`. The humanized text becomes the working abstract and section prose. It does not become a license to skip research or to invent notes.

If they also typed `/banner`, banners still come from section claims after the draft exists. Do not generate figures from the summary alone.

### 5. Deliver

Give the user the final level they asked for. If the walk was 2-3-4, lead with a 6-12 line abstract, then the humanized rewrite.

When the pass is a skill rewrite, write the new `SKILL.md` in place only after a keep-list diff. Locked tokens listed in `references/handoff.md` must survive as the same words or the same numeral.

Do not dump `pass.json` into chat unless they ask.

## Hard rules

- No new facts. No new citations. No new page numbers.
- No change to locked typography, fade geometry, owner legal lines, or OpenAction field names when the source is a house skill or house PDF.
- Visible house name stays Digital Marketing Company. Legal owner line stays Web Development Corporation when that line is already in the source.
- Running footers never print a trailing class letter A on the house name.
- No emoji in skill files or in PDFs this skill hands off.
- This skill does not compile a PDF by itself. PDF output goes through /folio, /deep, /print, or article-clip-pdf.


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

## Delivery

Run this once, last, after every other section. Full contract: `interop/SKILL.md`.

1. Resolve the negative skill as the first existing directory among `/root/.grok/server-skills/negative` and `/home/workdir/.grok/skills/negative`.
2. Extract visible text from chat, the file, captions, filenames, and alt text.
3. Run `python3 <negative-root>/scripts/sweep_negative.py` on that text.
4. Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN.
5. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.
