---
name: psychoanalyze
description: PhD-plus multi-school psychoanalytic synthesis of any pasted text, URL, file, image, or conversation. Trigger on /PsychoAnalyze, /psychoanalyze, /psycho-analyze, psychoanalyze this, or a request for Freudian, Jungian, Kleinian, Lacanian, or object-relations reading of supplied input. Runs a locked school battery, then emits a /deep Georgia monograph with /banner figures, a /folio WCA Ivy report with first-appearance citations and ITQE equation tables, and the house /copyright living footer. Does not diagnose a living person or claim a clinical license.
metadata:
  type: workflow
  version: "1.2"
  flag: /PsychoAnalyze
  pdf: deep-then-folio
  stack: deep, banner, folio, copyright
  visual_stack: visual-system
---

# /PsychoAnalyze


## Visual stack

Documents this skill emits follow `/home/workdir/.grok/skills/visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Treat the user's supplied artifact as a closed text, not as a patient. Run every school in `references/schools.md` against features that actually appear in the input. Write competing readings, not one diagnosis. Then compile two house PDFs in locked order — `/deep` (which calls `/banner`) then `/folio` — and confirm the `/copyright` living footer on both.

Work in `/home/workdir/artifacts/psychoanalyze-<slug>/`. Save `sample.txt` (or `sample-meta.json` for non-text), `analysis.json`, `deep.json`, and `folio.json`.

Public PDFs

- Deep monograph — `/home/workdir/artifacts/<Title_Slug>.pdf`
- WCA Folio — `/home/workdir/artifacts/<YYYY-topic-slug-wca-folio.pdf>`

`<deep>` = `/home/workdir/.grok/skills/deep`
`<banner>` = `/home/workdir/.grok/skills/banner`
`<folio>` = `/home/workdir/.grok/skills/folio`
`<copyright>` = `/home/workdir/.grok/skills/copyright`

Read on demand

- `references/ethics-and-limits.md` — clinical boundary, living-person rule, H0/H1
- `references/schools.md` — required battery and what each school may claim
- `references/intake.md` — text, URL, PDF, image, table, chat
- `references/pipeline.md` — locked emit order deep then banner then folio then copyright
- `<deep>/SKILL.md`, `<folio>/SKILL.md`, `<banner>/SKILL.md`, `<copyright>/SKILL.md`
- `/home/workdir/.grok/skills/wca-ivy-biblio/SKILL.md` — citation-order remapper and ITQE tables

If the user only asked to create or revise this skill and supplied no artifact, stop after the skill files exist. Do not invent a case.

If the flag is present and no artifact follows, stop and ask for the text, URL, or file. Do not psychoanalyze a random monograph already in artifacts.

## When this runs

- User typed `/PsychoAnalyze`, `/psychoanalyze`, or `/psycho-analyze`
- User stacked those flags with `/deep`, `/folio`, `/banner`, or `/copyright`
- User asked for a multi-school or PhD psychoanalytic reading of following input

Stacked flags do not change emit order. Deep always precedes Folio. Banner figures are generated inside the Deep pass. Copyright confirms or restamps last.

## Workflow

### 1. Intake

Follow `references/intake.md`. Copy the artifact into the work folder without silent rewrite.

- Pasted text goes to `sample.txt` verbatim
- URL — browse, save extract to `sample.txt`, record URL in `intake.json`
- PDF or DOCX already in artifacts — extract text to `sample.txt`, record source path
- Image — describe observable form only; save description to `sample.txt` and keep the image path
- Table or log — save as `sample.txt` plus a JSON dump if structured
- This chat — quote only turns the user marked; do not vacuum the whole project memory

Record device, date, and user claims as metadata, not as observed psyche.

Run

```bash
python3 /home/workdir/.grok/skills/psychoanalyze/scripts/intake_analyze.py \
  --input /home/workdir/artifacts/psychoanalyze-<slug>/sample.txt \
  --out /home/workdir/artifacts/psychoanalyze-<slug>/analysis.json
```

Read every field in `analysis.json` before drafting. Do not invent pronoun ratios or affect counts the script did not measure.

### 2. Frame the case

Write `scope.md`

- working title of the form Psychoanalytic Synthesis of “[surface phrase, trimmed to 8 words]”
- artifact type, length, and what is unobserved (body, history, diagnosis, transference in a room)
- 6–8 research questions, one per major school cluster
- inclusion / exclusion — text features in; biography of a living third party out unless the user is that party and asked for a reading of their own words as text
- root node label

Open `references/ethics-and-limits.md` before any claim that sounds clinical.

Two standing hypotheses

- H0 — the surface genre, role, and rhetoric explain the features (essay, ad, lyric, rant, corporate memo, dream-report as literature).
- H1 — a structured unconscious or group-unconscious pattern is the more economical account of those same features.

Accept a strong H1 reading only when at least two independent schools converge on the same textual mechanism and the mechanism is pointed at quoted spans. Otherwise keep H1 as a heuristic overlay on H0.

Never output a DSM or ICD code. Never say the author “has” a disorder. Never offer a treatment plan as if licensed.

### 3. Research the schools against this artifact

Follow `<deep>/references/research-graph.md` for source tiers. Prefer Standard Edition Freud, Klein, Winnicott, Bion, Lacan (Écrits / Seminars), Jung CW, Kohut, Bowlby, Fonagy, Benjamin, Kristeva, Fanon, and major university-press commentaries.

Record keepers in `sources.jsonl` and nodes in `nodes.jsonl`. Caps — depth 4, 80 keepers, close a branch after two empty rounds.

Every keeper must earn its place by illuminating a feature of this input. A generic Freud paragraph with no quoted span is a failed node.

Do not fabricate page numbers. If the page was not read, omit the locator.

### 4. /deep monograph (first PDF)

Follow `<deep>/SKILL.md` and `references/pipeline.md`. Draft `outline.md` then `deep.json`.

Required Deep body (relabel titles to the artifact; keep this order)

1. Introduction and research questions
2. Historiography of psychoanalytic reading
3. Sources, method, and the closed-artifact rule
4. Surface inventory (pronouns, defenses in diction, repetition, genre)
5. Drive and dream-work (Freud)
6. Object relations, Klein, Winnicott, Bion
7. Imaginary, Symbolic, Real (Lacan)
8. Archetype, shadow, individuation (Jung)
9. Self, attachment, mentalization
10. Group, culture, race, gender, colony
11. Synthesis — competing readings, H0 versus H1
12. Conclusion, limits, open problems
13. Bibliography

Page-local Chicago notes in WCA Ivy first-appearance order. `{{n}}` markers. Georgia 22-pt from `<deep>/assets/typography.py`. No invented sources. After drafting `deep.json` run the remapper and ITQE QA

```bash
python3 /home/workdir/.grok/skills/wca-ivy-biblio/scripts/reorder_citations.py \
  /home/workdir/artifacts/psychoanalyze-<slug>/deep.json --in-place
python3 /home/workdir/.grok/skills/wca-ivy-biblio/scripts/qa_ivy_document.py \
  /home/workdir/artifacts/psychoanalyze-<slug>/deep.json
```

Display equations are `type=equation` objects with a compiled figure and an ITQE table. Do not leave raw TeX in `deep.json`.

### 5. /banner figures

For every Deep body section except Bibliography run `<banner>/SKILL.md`.

- Prompt only from that section’s claims and quoted spans
- Futuristic composed figures, not fake clinical photographs and not portraits of private persons
- `banners/raw-NN.png` then `apply_banner_fade.py` to `banners/banner-NN.png`
- Default href `https://digitalmarketingco.org/r/?src=psychoanalyze-banner&section={section_id}`

Then build

```bash
python3 /home/workdir/.grok/skills/deep/scripts/build_deep_pdf.py \
  /home/workdir/artifacts/psychoanalyze-<slug>/deep.json \
  --out /home/workdir/artifacts/<Title_Slug>.pdf
```

Visual QA every page with `pdftoppm`. Rebuild on tofu, clipped type, a checkerboard banner, or a figure that does not belong to its section.

### 6. /folio report (second PDF)

Follow `<folio>/SKILL.md` and `references/pipeline.md`. Seed measured counts from `analysis.json` so Deep and Folio do not disagree.

Working Folio title

Psychoanalytic Synthesis of “[surface phrase, trimmed to 8 words]”

Subtitle

Multi-school closed-artifact reading with competing H0 and H1 accounts

Author

Web Development Corporation Research Desk

Required Folio body

1. Introduction and research questions
2. Historiography
3. Sources and method
4. Surface inventory from `analysis.json`
5. Classical and object-relations readings
6. Lacanian, Jungian, and attachment readings
7. Culture, group, and critique
8. Synthesis
9. Conclusion and open problems
10. Notes
11. Bibliography

Build with the Folio filename contract. Do not leave raw LaTeX in `folio.json`. Chat may use KaTeX plus an ITQE markdown table; the PDF may not show raw TeX. Before the Folio build run

```bash
python3 /home/workdir/.grok/skills/wca-ivy-biblio/scripts/reorder_citations.py \
  /home/workdir/artifacts/psychoanalyze-<slug>/folio.json --in-place
python3 /home/workdir/.grok/skills/wca-ivy-biblio/scripts/inject_itqe.py \
  /home/workdir/artifacts/psychoanalyze-<slug>/folio.json --in-place
python3 /home/workdir/.grok/skills/wca-ivy-biblio/scripts/qa_ivy_document.py \
  /home/workdir/artifacts/psychoanalyze-<slug>/folio.json
```

Note numbers stay contiguous in reading order. Bibliography is first-appearance order, not alphabetical.

```bash
python3 /home/workdir/.grok/skills/folio/scripts/build_folio_pdf.py \
  /home/workdir/artifacts/psychoanalyze-<slug>/folio.json \
  --out /home/workdir/artifacts/<YYYY-topic-slug-wca-folio.pdf>
```

Visual QA every Folio page.

### 7. /copyright

Builders already write the living footer and field `WCACopyrightYear`. After both PDFs exist

- If the user stacked `/copyright` or `/copyright YYYY`, restamp both files with that START year through `<copyright>/scripts/stamp_copyright.py`
- Otherwise confirm `pdfinfo` shows the house notice and that the running footer does not end with a class letter A

Default START is 2012. Default OWNER_FOOTER is Web Development Corporation.

### 8. Deliver

Give both PDFs. State page counts, note counts, bibliography counts, node count, and what the artifact does not let anyone know. Do not dump `deep.json` or `folio.json` into chat. Do not reprint builder scripts.

In the chat reply, give a short multi-school brief (one paragraph per cluster) that quotes the input. Render any formula with KaTeX. Point at the two PDFs for the full apparatus.

## Hard rules

- Artifact is text, image, or file — not a patient in a room.
- No DSM/ICD labels. No you-are-borderline sentences. No treatment protocol.
- Do not invent childhood events, crimes, or secret desires.
- Do not dox or psychoanalyze a named living third party from scraps the user did not author, except as literary reading of a published work.
- If the input expresses active self-harm or suicide, stop the battery and point to 988. Do not interpret the wish as a clever symptom.
- Competing schools stay incommensurable. Do not flatten Lacan into Freud.
- Grünbaum, Popper, feminist, and postcolonial critiques belong in historiography and synthesis.
- Visible house anchor is Digital Marketing Company at https://digitalmarketingco.org. Plain-text domain is DigitalMarketingCo.org.
- No emoji. No unsupported symbols. No invented citations.
- Do not reprint `build_deep_pdf.py`, `build_folio_pdf.py`, or typography modules into chat.


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
