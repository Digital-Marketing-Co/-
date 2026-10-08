---
name: corpus
description: Compile a deduplicated academic corpus for one match string such as an author name, ORCID, or agency token. Use when the user types /corpus, asks to find all citations authored or co-authored by a named person, harvest a personal bibliography, or inventory documents by a researcher. Do not use for a topic monograph — that is /deep, /folio, or phd-ivy-monograph.
metadata:
  type: workflow
  version: "1.1"
  flag: /corpus
  visual_stack: visual-system
---

# /corpus


## Visual stack

Documents this skill emits follow `/home/workdir/.grok/skills/visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Compile every reachable work that matches one person, organization, or identifier. The unit of analysis is the **creator**, not a topic. Output is an inventory plus a Chicago bibliography catalog. Do not write a literature-review monograph unless the user also stacked `/folio` or `/deep`.

Work in `/home/workdir/artifacts/<slug>/`. Default printed catalog is `/home/workdir/artifacts/<YYYY>-<slug>-corpus.pdf`.

`<skill>` = `/home/workdir/.grok/skills/corpus`.

If the user only asked to create or edit this skill and did not invoke `/corpus` on a match, stop after the skill files exist. Do not invent a subject and do not harvest.

## Read on demand

- `references/identity.md` — parse the match, name variants, affiliation tokens
- `references/harvest.md` — source order, APIs, search rounds
- `references/dedup.md` — DOI / PMID / title keys, merge rules
- `references/chicago-corpus.md` — bibliography and note forms
- `references/handoff.md` — what this skill is not, and how to pass keepers to `/folio` or `/deep`
- `assets/schema/corpus.schema.json` — `corpus.json` shape
- `scripts/harvest_apis.py` — OpenAlex, Crossref, PubMed, Semantic Scholar
- `scripts/dedup_works.py` — merge `works.jsonl` lines
- `scripts/build_corpus_pdf.py` — letter-size catalog PDF

## Workflow

### 1. Parse the match

Treat the remainder of the user message after `/corpus` as the **match string**. Example seed supplied with this skill

Find all citations and documents that have been authored or co-authored by Dr. Andrew Yeager, MD DIA ARMY

Extract

- display name
- surname + given + initials
- degrees and credentials (`MD`, `PhD`, `DIA`)
- agency / service / employer tokens (`ARMY`, `DIA`, university, hospital)
- hard identifiers if present (`ORCID`, `PMID`, email)

Write `scope.md` with the parsed fields, inclusion rules, and exclusion rules. Affiliation tokens are **disambiguators**, not extra authors. They never become a second harvest subject.

Do not harvest a homonym. If two living researchers share the surname, stop and write the collision in `identity.md` before merging works.

### 2. Resolve identity

Follow `references/identity.md`. Build `identity.md` and `identity.json` with

- preferred heading
- name variants (with and without middle initial, hyphen, maiden name)
- ORCID if found
- OpenAlex / Semantic Scholar author IDs
- confirmed affiliations and years
- rejected homonyms and why

Confirmed identity is required before round 2 of harvest. A faculty page, ORCID record, or PubMed affiliation string that matches a disambiguator is enough. A lone surname hit is not.

### 3. Harvest

Follow `references/harvest.md`. Run the API helper first, then fill holes with `web_search` and `browse_page`.

```bash
python3 <skill>/scripts/harvest_apis.py \
  --name "Andrew M. Yeager" \
  --variants "Andrew Yeager" "A. M. Yeager" "Yeager AM" \
  --out /home/workdir/artifacts/<slug>/raw
```

Search kinds that count as documents in this corpus (include all; do not invent extras)

- journal articles, reviews, editorials, letters, errata, retractions
- book chapters, monographs, textbooks, published abstracts
- conference papers and published posters when a citable record exists
- NIH / DoD / other funded grants where the match is PI or named co-investigator
- patents and published applications
- clinical-trial registrations where the match is a listed investigator
- official `.gov` / `.mil` technical reports
- dissertations if the match is the author

Do not pull citing papers, news profiles, or related-article sidebars into the corpus. Those are context, not works **by** the match.

Each raw record goes to `raw/<source>.jsonl`. Keepers after identity filter go to `works.jsonl` (one object per line). Near-misses go to `rejected.jsonl` with a reason.

Caps that stop infinite harvest

- 8 search rounds
- a source class closes after two consecutive empty targeted rounds
- 400 keeper works unless the user raised the cap
- depth 1 only — do not recurse into co-author bibliographies unless the user said lab corpus or group corpus

Record every round in `rounds/round-N.md`.

Never fabricate a citation, page, DOI, PMID, or grant number.

### 4. Deduplicate

```bash
python3 <skill>/scripts/dedup_works.py \
  /home/workdir/artifacts/<slug>/works.jsonl \
  --out /home/workdir/artifacts/<slug>/works.dedup.jsonl \
  --report /home/workdir/artifacts/<slug>/dedup-report.md
```

Follow `references/dedup.md`. One work, one keeper. Reprints, PMC mirrors, author-manuscript copies, and Google Scholar HTML of the same DOI collapse to the best bibliographic record (DOI then PMID then ISBN then normalized title+year+first-author).

### 5. Classify and count

Write `corpus.json` matching `assets/schema/corpus.schema.json`.

Required tallies

- total unique works
- by type (article, chapter, book, abstract, grant, patent, trial, report, other)
- by year
- first-author vs co-author counts
- open vs closed full text
- works still unverified (catalog hit only)

Sort the bibliography by year descending, then title. Do not number bibliography entries.

### 6. Chicago catalog

Write `bibliography.md` using `references/chicago-corpus.md`. Every keeper gets one bibliography line. Notes are used only for identity collisions, uncertain attributions, and retracted or corrected items.

### 7. Print

```bash
python3 <skill>/scripts/build_corpus_pdf.py \
  /home/workdir/artifacts/<slug>/corpus.json \
  --out /home/workdir/artifacts/<YYYY>-<slug>-corpus.pdf
```

House marks on the catalog

- visible link anchor Digital Marketing Company → https://digitalmarketingco.org
- plain-text domain DigitalMarketingCo.org
- owner line Web Development Corporation, a Delaware Corporation, on the title page only
- running footer Web Development Corporation with living © 2012–YEAR field
- Times / Liberation Serif only; no tofu, no black boxes, no raw LaTeX

Verify the PDF pages visually before delivery. Render the file to the user.

### 8. Optional handoff

If the user also typed `/folio` or `/deep`, pass `works.dedup.jsonl` as the source list and follow `references/handoff.md`. Do not copy those skills’ chapter templates into this catalog.

## House rules that still apply

Explain every variable or subscript if an equation appears in a quoted abstract. Prefer primary PDFs. Do not write unsupported glyphs.


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
