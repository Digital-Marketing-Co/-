---
name: psychoanalyze
description: PhD-plus multi-school psychoanalytic synthesis of any pasted text, URL, file, image, or conversation. Trigger on /PsychoAnalyze, /psychoanalyze, /psycho-analyze, psychoanalyze this, or a request for Freudian, Jungian, Kleinian, Lacanian, or object-relations reading of supplied input. Runs a locked school battery, then emits a /deep Georgia monograph with /banner figures, a /folio WCA Ivy report with first-appearance citations and ITQE equation tables, and the house /copyright living footer. Does not diagnose a living person or claim a clinical license.
---

# /PsychoAnalyze

## Quality and capability additions

Read [the task-specific quality profile](references/quality-profile.md) before execution. Use `evals/quality-cases.json` for regression scenarios; its assertions are acceptance criteria, not claims that tests have run. Shared path resolution and output rules live in `interop/SKILL.md`.



## Visual stack

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with `@visual-system/scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Treat the user's supplied artifact as a closed text, not as a patient. Run every school in `references/schools.md` against features that actually appear in the input. Write competing readings, not one diagnosis. Then compile two house PDFs in locked order — `/deep` (which calls `/banner`) then `/folio` — and confirm the `/copyright` living footer on both.

Work in `/workspace/artifacts/psychoanalyze-<slug>/`. Save `sample.txt` (or `sample-meta.json` for non-text), `analysis.json`, `deep.json`, and `folio.json`.

Public PDFs

- Deep monograph — `/workspace/artifacts/<Title_Slug>.pdf`
- WCA Folio — `/workspace/artifacts/<YYYY-topic-slug-wca-folio.pdf>`

`<deep>` = `@deep`
`<banner>` = `@banner`
`<folio>` = `@folio`
`<copyright>` = `@copyright`

Read on demand

- `references/ethics-and-limits.md` — clinical boundary, living-person rule, H0/H1
- `references/schools.md` — required battery and what each school may claim
- `references/intake.md` — text, URL, PDF, image, table, chat
- `references/pipeline.md` — locked emit order deep then banner then folio then copyright
- `<deep>/SKILL.md`, `<folio>/SKILL.md`, `<banner>/SKILL.md`, `<copyright>/SKILL.md`
- `@wca-ivy-biblio/SKILL.md` — citation-order remapper and ITQE tables

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
python3 @psychoanalyze/scripts/intake_analyze.py \
  --input /workspace/artifacts/psychoanalyze-<slug>/sample.txt \
  --out /workspace/artifacts/psychoanalyze-<slug>/analysis.json
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
python3 @wca-ivy-biblio/scripts/reorder_citations.py \
  /workspace/artifacts/psychoanalyze-<slug>/deep.json --in-place
python3 @wca-ivy-biblio/scripts/qa_ivy_document.py \
  /workspace/artifacts/psychoanalyze-<slug>/deep.json
```

Display equations are `type=equation` objects with a compiled figure and an ITQE table. Do not leave raw TeX in `deep.json`.

### 5. /banner figures

For every Deep body section except Bibliography run `<banner>/SKILL.md`.

- Prompt only from that section’s claims and quoted spans
- Futuristic composed figures, not fake clinical photographs and not portraits of private persons
- `banners/raw-NN.png` then `apply_banner_fade.py` to `banners/banner-NN.png`
- Default href `https://DigitalMarketingCo.org/r/?src=psychoanalyze-banner&section={section_id}`

Then build

```bash
python3 @deep/scripts/build_deep_pdf.py \
  /workspace/artifacts/psychoanalyze-<slug>/deep.json \
  --out /workspace/artifacts/<Title_Slug>.pdf
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
python3 @wca-ivy-biblio/scripts/reorder_citations.py \
  /workspace/artifacts/psychoanalyze-<slug>/folio.json --in-place
python3 @wca-ivy-biblio/scripts/inject_itqe.py \
  /workspace/artifacts/psychoanalyze-<slug>/folio.json --in-place
python3 @wca-ivy-biblio/scripts/qa_ivy_document.py \
  /workspace/artifacts/psychoanalyze-<slug>/folio.json
```

Note numbers stay contiguous in reading order. Bibliography is first-appearance order, not alphabetical.

```bash
python3 @folio/scripts/build_folio_pdf.py \
  /workspace/artifacts/psychoanalyze-<slug>/folio.json \
  --out /workspace/artifacts/<YYYY-topic-slug-wca-folio.pdf>
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
- Visible house anchor is Digital Marketing Co. at https://DigitalMarketingCo.org. Plain-text domain is DigitalMarketingCo.org.
- No emoji. No unsupported symbols. No invented citations.
- Do not reprint `build_deep_pdf.py`, `build_folio_pdf.py`, or typography modules into chat.


## Render gate (mandatory with /itqe and /latex)

Before delivering any PDF, DOCX, PPTX, XLSX, HTML view, printed page, or builder JSON that may contain notation, short codes, or equations, run the house render gate. Chat may use KaTeX. Files must show compiled glyphs or a compiled figure. Raw LaTeX, AMS-TeX, KaTeX source, MathJax source, uncompiled backslash commands, tofu, or empty boxes are defects.

```bash
python3 @itqe/scripts/scan_render_gate.py \
  /workspace/artifacts/<slug> \
  --also-pdf /workspace/artifacts/<file>.pdf
python3 @latex/scripts/scan_raw_tex.py \
  /workspace/artifacts/<slug> \
  --also-pdf /workspace/artifacts/<file>.pdf --pages
```

Exit code 1 blocks delivery. Repair with `/latex` figures, attach an ITQE table under every display equation (Identifier, Term, Quantity, Explanation), rebuild, scan again, and raster every page. See `@itqe/references/render-gate.md` and `@latex/SKILL.md`.

## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write plate, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

## Paginated footer

Read `copyright/SKILL.md` and render its canonical notice exactly once per page. Do not keep separate legal text or year calculations here. Preserve any stated user override.

## Publication checks

Apply `interop/SKILL.md` once after the task-specific checks. Its shared rules yield to this skill's explicit format and source-fidelity requirements.

## Delivery

Run the single delivery gate in `interop/SKILL.md` after task-specific validation. Preserve verified quotations and technical identifiers; report unresolved defects or blockers accurately.
