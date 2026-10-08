---
name: global
description: Produce a country-by-country global intelligence report on any topic, ranked by the most relevant variable descending, with a waving national flag and a full-bleed scenic country banner on every country section. Use when the user types /global, asks for a global intel report, country-by-country overview, world ranking, or comparative country sections on a topic. Stacks with /banner, /images, /copyright, /folio, /deep, /itqe, and /latex. Do not use for an author harvest (/corpus) or a single-place atlas (/atlas).
metadata:
  type: workflow
  version: "1.1"
  flag: /global
  stacks: banner, images, copyright, folio, deep, iterate, itqe, latex
  owner: Web Development Corporation
  visual_stack: visual-system
---

# /global — country-by-country intelligence report on {{input}}


## Visual stack

Documents this skill emits follow `/home/workdir/.grok/skills/visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Turn any topic into a ranked world intelligence report. One section per country. Default sort is the most relevant quantitative variable for that topic, descending. Every country section opens with a waving national flag and a full-bleed scenic banner of that country. The topic is never hardcoded. Real estate, currencies, and product classes from example prompts are not part of this skill.

Work in `/home/workdir/artifacts/global-<slug>/`. Default printed report is `/home/workdir/artifacts/<YYYY>-<slug>-global.pdf`.

`<skill>` = `/home/workdir/.grok/skills/global`
`<banner>` = `/home/workdir/.grok/skills/banner`
`<images>` = `/home/workdir/.grok/skills/images`
`<copyright>` = `/home/workdir/.grok/skills/copyright`
`<folio>` = `/home/workdir/.grok/skills/folio`
`<deep>` = `/home/workdir/.grok/skills/deep`
`<iterate>` = `/home/workdir/.grok/skills/iterate`

Read on demand

- `references/locked-prompt.md` — rewritten execution prompt
- `references/ranking.md` — how to pick and apply the ranking variable
- `references/country-section.md` — flag, banner, body, series, categories
- `references/research-protocol.md` — sources, units, coverage, stop gate
- `references/negative-vocabulary.md` — banned prompt tokens
- `assets/negative-keywords.csv` — portable negative array
- `assets/schema/global.schema.json` — `global.json` shape

If the user only asked to create or revise this skill and supplied no topic, stop after the skill files exist. Do not invent a topic.

## When this skill runs

- User typed `/global` followed by a topic (`{{input}}`)
- User asked for a country-by-country intelligence report, world ranking, or comparative national overview of a topic
- A stacked run (`/global /banner /images /copyright`, `/global /folio`, `/global /deep`) needs the ranked country dossier before figures and footer

Do not use this skill for an author-only harvest (`/corpus`), a single-place spatial atlas (`/atlas`), or a non-geographic inventory (`/list` unless the user also asked for country sections).

## Rewritten execution prompt

Place flags in this order. `{{input}}` is the remainder of the user message after `/global` and after any stacked flags.

```
/global {{input}} /banner /images /copyright

Compile a country-by-country intelligence report on {{input}}. Discover the natural categories, units, and time grain of the topic. Do not import leftover example taxonomies. Convert every monetary figure to United States dollars and state the FX date. Rank sovereign countries by the single most relevant aggregate variable for {{input}}, descending, unless the user named a different sort key.

For each ranked country write one section that contains
- a beautifully rendered waving national flag
- a full-bleed, full-width scenic banner of that country with zero left margin, zero right margin, and bleed on the top edge
- the ranking value, year, source, and coverage note
- every relevant subcategory of {{input}} that exists for that country
- a time series for the last available 12 periods at the natural grain (month when monthly data exist, else quarter or year)
- an electric-blue, semi-transparent, visually clean chart of that series when numbers exist

Prefer primary statistical agencies, central banks, UN and specialized-agency yearbooks, OECD, IMF, World Bank, Eurostat, .gov, .mil, and university-press work. Do not invent a national total. Mark estimates, gaps, and dual-recognition cases in plain language.

/banner — one full-bleed left-and-right banner on every body section and every subsection. Zero left margin, zero right margin, zero left padding, zero right padding. Height follows source aspect. Print at full opacity. Do not fade any edge.

/images — generate or print each figure at the maximum size that does not lose quality and does not introduce aliasing, blur, or aspect distortion.

/copyright — restamp every page with the living centered footer. START defaults to 2012 unless the user typed /copyright YYYY. YEAR is Date.getFullYear on open. Default owner is Web Development Corporation.
```

When the user also typed `/folio` or `/deep`, those builders run after `global.json` exists. `/iterate` may enlarge coverage before emit.

## Workflow

### 1. Lock the topic

Treat the remainder after `/global` and after stacked flags as `{{input}}`.

Write `scope.md`

- working title (`Global intelligence report — {{input}}`)
- topic in one sentence
- unit of analysis (what one observation is)
- ranking variable candidate list and the chosen default
- natural time grain (month, quarter, year)
- natural unit (USD, count, share, tonnes, TWh, index, rate)
- inclusion rules for countries and dependencies
- exclusion rules
- category discovery rule (include every relevant class that the sources actually use for this topic)
- coverage target (UN members plus widely recognized states unless the user narrowed the set)

Do not copy sample taxonomies from older prompts into `scope.md` unless the user topic is actually that market.

### 2. Discover categories and the ranking variable

Read `references/ranking.md`.

- List the classes the literature uses for `{{input}}`.
- Keep every class that is material. Do not drop a class because an example prompt used three classes.
- Choose one primary ranking variable. Default is the largest meaningful national aggregate for the topic over the latest complete year, converted to USD when the quantity is money.
- If the topic has no money quantity, rank on the largest meaningful physical or count aggregate, then on a published index, then on a documented rate.
- Record the choice, the year, the unit, and why rivals lost.

Write `ranking.md` in the run folder.

### 3. Research

Follow `references/research-protocol.md`.

Write `sources.jsonl` and `countries.jsonl`. One row per country. Never fabricate a national total. When only a regional bloc figure exists, do not split it by population unless the source itself publishes the split.

Convert currencies to USD with a dated FX source. State both the original-currency figure and the USD figure when the source was not already in USD.

Stop a coverage branch after two consecutive empty targeted rounds for that country. Move thin countries to `insufficient-data.md` rather than inventing ranks.

### 4. Draft the dossier

Write `outline.md`, then `global.json` matching `assets/schema/global.schema.json`.

Required front matter — title, subtitle, author, date, owner block, house block, abstract (150–250 words), keywords, ranking variable, ranking year, FX date, coverage count.

Required body

1. Scope and ranking rule
2. Global league table (every ranked country, compact)
3. Method, sources, and gaps
4. One section per ranked country, in descending rank order
5. Insufficient-data and non-sovereign appendix
6. Notes
7. Bibliography

Each country section follows `references/country-section.md`.

Paragraphs that will emit through `/folio` use `{{n}}` citation markers.

### 5. Flags and banners

For every country section produce two images before the PDF build.

Flag

- Beautifully rendered waving national flag of that country
- Correct current civil flag
- Cloth in motion, readable canton and field, no extra emblems
- Transparent or clean sky only behind the cloth
- Save as `flags/flag-<iso2>.png`
- Do not invent a flag. If the polity is disputed, use the flag the user named or the widely used civil flag and footnote the dispute.

Scenic banner

- Prefer a high-resolution, royalty-free or openly licensed photograph of a named real place in that country
- Subject is landscape, cityscape, or landmark that a traveler would recognize as that country
- Full bleed left and right. Bleed the top edge. Zero left margin, zero right margin, zero left padding, zero right padding
- Full opacity. No edge fade. No letterbox. No checkerboard baked into RGB
- Height follows source aspect after the page-width floor
- Caption names the real place and the license or generate note
- Save as `banners/banner-<iso2>.png`
- One unique bitmap per country. Do not reuse bytes or paths across countries

Then run `/banner` for any non-country body section and every subsection that still lacks a banner. Country scenic banners already satisfy the country-section banner slot. Do not crop one country banner into another country slot.

Read `<banner>/SKILL.md` and `<images>/SKILL.md` before generate. Load `assets/negative-keywords.csv` first. Never write figure, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into a concatenated generate prompt.

### 6. Charts

When a country has a usable series, emit one chart of the last 12 available periods of the ranking variable and, when categories exist, a stacked or small-multiple view of those categories.

Chart style

- Electric blue, semi-transparent fills, thin high-contrast strokes
- Clean axes, named units, dated source line
- No 3-D extrusion, no clip-art globes, no unreadably small labels
- Save as `charts/chart-<iso2>.png` (and `charts/chart-<iso2>-categories.png` when needed)

If no honest 12-period series exists, print a single-year bar or omit the chart and say why.

### 7. Emit

Default emit is the compact `/folio` builder unless the user typed `/deep`. Then stamp `/copyright`.

Work folder files that must exist before emit

- `scope.md`
- `ranking.md`
- `global.json`
- `sources.jsonl`
- `flags/flag-<iso2>.png` for every printed country
- `banners/banner-<iso2>.png` for every printed country
- chart files when series exist

Final PDF name form

`/home/workdir/artifacts/<YYYY>-<topic-slug>-global-wca-folio.pdf`

Visible house link text is Digital Marketing Company. Title attribute and visible text match. Plain-text domain is DigitalMarketingCo.org. Target may be `https://digitalmarketingco.org`.

### 8. Render gate

Before delivery run the house `/itqe` and `/latex` scans on the work folder and the PDF. Exit code 1 blocks delivery. Compile every formula. Attach an Interactive Table of Quantitative Elements under every display equation. Never leave raw TeX, tofu, or empty boxes on a page.

## Hard rules

- Topic-agnostic. Never inject leftover example taxonomies unless the user topic is that market.
- Rank descending on the chosen variable. State ties and year breaks.
- Convert money to USD. Date the FX source.
- Include every material subcategory the sources use for the topic.
- One waving flag and one unique full-bleed scenic banner per country section.
- Full-bleed banners touch both page edges and the top trim of the banner box. No side margin. No fade.
- Do not invent national totals, flags, or landmarks.
- Do not diagnose living persons. Do not print operational methods for weapons, crime, or exploitation.
- House link and living copyright footer on every PDF this skill emits.

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
