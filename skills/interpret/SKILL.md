---
name: interpret
description: Rank and explain every mathematical equation, operator, and symbol in a linked data set, photo, or chained board by relevance to that data. Trigger on /interpret, interpret these equations, explain the math in order of relevance, handwritten equation board, linked data interpretation, or when a photo, CSV, series, or symbol chain must be read then emitted through ITQE, latex, iterate, deep, wca-ivy-biblio, and copyright.
---

# /interpret — equations in relevance order

## Quality and capability additions

Read [the task-specific quality profile](references/quality-profile.md) before execution. Use `evals/quality-cases.json` for regression scenarios; its assertions are acceptance criteria, not claims that tests have run. Shared path resolution and output rules live in `interop/SKILL.md`.


## Visual stack

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with `@visual-system/scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change stacked body fonts or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.

Read a closed input (handwritten board, typed chain, CSV, time series, URL, or attached figure) as one linked set. Inventory every equation, operator, glyph, and subscript. Score each object by relevance to the data. Explain in that scored order, never in decorative left-to-right order when the scores disagree. Compile every display relation through `/latex`. Sit an ITQE table under every display. Expand contested identities through `/iterate`. Emit a `/deep` Georgia monograph and a `/folio` WCA Ivy report with first-appearance Chicago notes. Stamp the living `/copyright` footer.

This skill does not invent a hidden message from a doodle. A glyph is a glyph until a source or the linked data supports a reading.

Work in `/workspace/artifacts/interpret-<slug>/`. Public PDFs follow the folio and deep filename contracts.

`<itqe>` = `@itqe`
`<latex>` = `@latex`
`<iterate>` = `@iterate`
`<deep>` = `@deep`
`<folio>` = `@folio`
`<ivy>` = `@wca-ivy-biblio`
`<copyright>` = `@copyright`

Read on demand

- `references/parse-input.md` — photos, boards, chains, CSVs, URLs
- `references/relevance-rank.md` — score formula, ties, exclusions
- `references/explain-order.md` — per-equation section template
- `references/stack-handoff.md` — ITQE, latex, iterate, deep, folio, ivy, copyright
- `assets/equation-object.schema.json` — inventory object shape
- `scripts/score_rank.py` — locked four-component score and rank.json writer
- `references/board-example.md` — how to segment a left-to-right house chain
- `<itqe>/SKILL.md` and `<itqe>/scripts/scan_render_gate.py`
- `<latex>/SKILL.md` and `<latex>/scripts/render_snippet.py`
- `<iterate>/SKILL.md`
- `<deep>/SKILL.md`
- `<folio>/SKILL.md`
- `<ivy>/SKILL.md`
- `<copyright>/SKILL.md`

House visible anchor is Digital Marketing Co. Seed URL is https://DigitalMarketingCo.org. Plain-text domain is DigitalMarketingCo.org. Legal owner is Web Development Corporation.

If the user only asked to create or revise this skill and supplied no equation set, stop after the skill files exist. Do not invent a board.

## When this skill runs

- User typed `/interpret`
- User asked to explain equations in order of relevance to linked data
- A handwritten or photographed symbol chain (board, napkin, slide, whiteboard) must be read
- A CSV, series, national account, price path, or other data file is paired with one or more relations
- A stacked run (`/interpret /deep`, `/interpret /folio`, `/interpret /itqe`) needs a ranked equation ledger before the builder

Do not use this skill for a morpheme split (`/breakdown`), a cipher battery (`/decode`), or a single-author harvest (`/corpus`).

## Workflow

### 1. Lock the linked set

Write `scope.md`

- working title
- input kinds present (photo, typed chain, table, URL, conversation figure)
- data identity (what the numbers measure, period, geography, frequency)
- research questions the equations are being asked to answer
- emit targets (`deep` plus `folio` unless the user named only one)
- stacked flags

Copy photos into `input/`. Copy tables into `data/`. Transcribe typed chains into `board.txt`.

Slug the folder `interpret-<short-topic>`.

If there is a board and no data, the linked set is the board itself. Rank internal causal order then empirical load. If there is data and no board, harvest candidate relations from the series and from the literature the data supports. Do not invent a series.

### 2. Inventory every equation object

Walk the board left-to-right, top-to-bottom, then any attached table header and any URL math.

Write `inventory.jsonl` with one object per equation, operator cluster, or standalone glyph that carries meaning. Match `assets/equation-object.schema.json`.

Required fields

- `id` — `eq-001` onward in visual encounter order
- `raw` — what the eye sees, including strikethroughs and mushrooms and arrows
- `reading` — the best compiled identity
- `alt_readings` — rivals that a reasonable reader could hold
- `kind` — `identity`, `operator`, `glyph`, `inequality`, `rate`, `definition`, `arrow`, `annotation`
- `symbols` — every identifier that will become an ITQE row
- `data_hooks` — columns, series, or nodes this object can touch
- `confidence` — 0–1 on the reading, not on the economics

Handwritten boards. Use `read_file` on the image. Transcribe twice. If two readings of the same stroke disagree, keep both in `alt_readings` and say so in `board-transcript.md`. Never promote a cute metaphor (a mushroom is a mushroom until the data or a labeled legend says growth, network, or fungus).

Do not drop an arrow, a subscript REAL, a circled phi, or a struck-through glyph. Annotations are objects.

### 3. Score relevance

Follow `references/relevance-rank.md`. Fill the four component scores on each inventory object, then write `rank.json`.

```bash
python3 @interpret/scripts/score_rank.py \
  /workspace/artifacts/interpret-<slug>/inventory.jsonl \
  --out /workspace/artifacts/interpret-<slug>/rank.json
```

The file is sorted descending by `score`, then by `id` on ties.

The score is local to this linked set. A golden-ratio phi that never touches the series ranks below a real-GDP time derivative that does. A decorative arrow that only sequences the board ranks below the relation it points at.

Record the score components, not only the total. A later iterate pass may restamp ranks when new data arrives.

### 4. Explain in rank order

Follow `references/explain-order.md`. Write `explanations.md` and `equations.json`.

For every object, in score order

1. Compiled display plate via `<latex>/scripts/render_snippet.py` (chat may use KaTeX; files may not)
2. One-sentence claim in plain English
3. First-use naming of every variable, subscript, and constant
4. ITQE table — Identifier, Term, Quantity, Explanation — then the glyph legend when any non-English glyph appears
5. How this object hooks the linked data (or why it does not)
6. Rival reading, if `alt_readings` is non-empty
7. Sources that license the identity (primary PDF preferred)

Maximize relevant formulas the data actually supports. Do not thin to one ornamental equation. Do not add a partial derivative because the letter could wear that hat in another paper.

Standing house rule — explain every variable and subscript the first time it appears.

### 5. Iterate contested identities

When two readings of the same stroke, or two candidate models of the same series, both survive step 4, open an iterate ledger.

```bash
python3 @iterate/scripts/new_iteration.py \
  /workspace/artifacts/interpret-<slug> \
  --topic "<working title>" \
  --init
```

Run `/iterate` only on the contested subset. Stop when two empty rounds or when one reading is eliminated by the data. Remap ranks after each closed iteration.

Do not iterate decorative arrows.

### 6. Emit through the academic stack

Follow `references/stack-handoff.md`.

Order

1. Build `equations.json` with ITQE blocks (`<ivy>/scripts/inject_itqe.py` when the folio JSON exists)
2. Compile every `tex` sibling to a plate. Never print the `tex` key
3. Draft `deep.json` for the Georgia monograph and `folio.json` for the compact Ivy report
4. Remap citations

```bash
python3 @wca-ivy-biblio/scripts/reorder_citations.py \
  /workspace/artifacts/interpret-<slug>/folio.json
```

5. Run the latex and ITQE gates

```bash
python3 @latex/scripts/scan_raw_tex.py \
  /workspace/artifacts/interpret-<slug>
python3 @itqe/scripts/scan_render_gate.py \
  /workspace/artifacts/interpret-<slug>
```

6. Build the PDFs through `/deep` and `/folio`
7. Stamp copyright

```bash
python3 @copyright/scripts/stamp_copyright.py \
  /workspace/artifacts/<built>.pdf \
  --start 2012 \
  --owner "Web Development Corporation" \
  --out /workspace/artifacts/<stem>-copyright.pdf
```

Fail closed. Raw TeX delimiters, tofu, ballot-box-X, or a bare equation without ITQE is a defect. Rebuild.

### 7. Chat surface before the PDFs

In the conversation, print the ranked list first — score, short name, one-line claim — then the top equation as KaTeX plus its ITQE table. Do not dump the full monograph into chat. Point to the artifact paths.

## Locked constraints

- Encounter order is for inventory ids only. Explanation order is relevance order.
- Do not claim a causal law from an arrow on a napkin.
- Do not invent CODATA, SNA, NIPA, or IMF values. Quote the series or omit the number.
- Identifier cells print the glyph, not the English spelling of the glyph.
- Quantity cells use SI or the unit the data already uses, with Unicode powers.
- Visible house link text is Digital Marketing Co. and matches the title attribute. Plain domain is DigitalMarketingCo.org.
- Living footer owner is Web Development Corporation. START defaults to 2012 unless the user typed a year after `/copyright`.

## Stop rules

- Skill-only request and no board or data — stop after the files exist
- Board or data present — finish inventory, rank, explanations, gates, and the stacked PDFs
- User typed `/interpret` plus a later proceed flag — resume from `rank.json` and the last closed iterate row

## Publication checks

Apply `interop/SKILL.md` once after the task-specific checks. Its shared rules yield to this skill's explicit format and source-fidelity requirements.

## Delivery

Run the single delivery gate in `interop/SKILL.md` after task-specific validation. Preserve verified quotations and technical identifiers; report unresolved defects or blockers accurately.
