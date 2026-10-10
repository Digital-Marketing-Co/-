

# /iterate — exhaustive expansion until saturation


## Visual stack

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Turn one topic or a closed set of topics into a living research ledger that grows by discrete iterations. Each iteration adds new claims, new primary sources, and new note events. After every insertion, citation numbers, page footnotes, and the bibliography are remapped so they stay contiguous in first-appearance reading order. When the saturation gate closes, emit a WCA compact Ivy Folio (default) or a /deep Georgia monograph. Finish on the latest /itqe contract and the /latex render gate.

This skill does not invent omniscience. Above-genius here is an operational posture — more rounds, rival-school pressure, quantitative figures on every relation the topic supports, and a written stop rule. It is not a claim that the model is the smartest person or computer.

Work in `./artifacts/iterate-<slug>/`.

`<folio>` = `@folio`
`<deep>` = `@deep`
`<ivy>` = `@wca-ivy-biblio`
`<itqe>` = `@itqe`
`<latex>` = `@latex`

Read on demand

- `references/iteration-protocol.md` — rounds, expansion operators, stop gate
- `references/source-tiers.md` — PDF-first Ivy, government, military, healthcare
- `references/citation-restamp.md` — insert-then-remap after every pass
- `references/emit-handoff.md` — folio / deep / ITQE / latex / copyright
- `scripts/new_iteration.py` — stamp a ledger row and a round file
- `<ivy>/scripts/reorder_citations.py`
- `<ivy>/scripts/qa_ivy_document.py`
- `<itqe>/SKILL.md` and `<itqe>/scripts/scan_render_gate.py`

If the user only asked to create or revise this skill and supplied no topic, stop after the skill files exist. Do not invent a monograph.

## When this skill runs

- User typed `/iterate`
- User asked to expand and expound a topic until an exhaustive higher-than-PhD document exists
- User asked to keep iterating an existing folio.json, monograph.json, or deep.json
- A stacked run (`/iterate /folio`, `/iterate /deep`, `/iterate /phd`) needs a multi-round research ledger before the builder

Do not use this skill for a one-shot clip, a corpus harvest of one author, or a non-research rewrite. Those are `/print`, `/corpus`, and `/summarize`.

## Workflow

### 1. Lock scope

Extract the topic or topic set, period, geography, exclusions, and emit target (`folio` default, `deep` when the user typed `/deep` or asked for Georgia banners).

Write `scope.md`

- working title
- topic set (one line per root)
- 6–12 research questions (more than a single-pass folio)
- inclusion and exclusion rules
- emit target and stacked flags
- starting iteration count (0 if new)

Slug the folder `iterate-<short-topic>`.

### 2. Open or resume the ledger

If `ledger.json` exists, resume from the last closed iteration. If not, seed

```bash
python3 @iterate/scripts/new_iteration.py \
  ./artifacts/iterate-<slug> \
  --topic "<working title>" \
  --init
```

Keepers live in `sources.jsonl`. Graph nodes live in `nodes.jsonl`. Each pass writes `rounds/round-NN.md` and appends `iterations/iter-NN.json`.

### 3. Run iterations

Follow `references/iteration-protocol.md`. One iteration is one closed research pass, not one search query.

Each iteration must

1. State the hole it is filling (from `open_questions` or a new branch the last pass opened).
2. Search with a preference for canonical PDF primary sources. Walk `references/source-tiers.md`.
3. Add only keepers that can be cited. Never fabricate a title, URL, page, or year.
4. Draft new or revised paragraphs into the working JSON (`folio.json` preferred). Place new notes with a high temporary n (9001+) or omit n and set `work_id`.
5. Add every new quantitative relation as a `type=equation` object with a compiled figure plan and a four-column ITQE stub (Identifier, Term, Quantity, Explanation).
6. Run the restamp (step 4) before starting the next iteration.
7. Write what remains open. A pass that adds no keeper and no new claim is an empty pass.

Default caps (raise only when the user names a harder stop)

- 8 iterations or 12 when `/deep` is stacked
- depth 5 from each root topic
- 120 keeper sources
- a branch closes after two consecutive empty targeted passes
- stop early if the saturation gate in `references/iteration-protocol.md` is met

### 4. Restamp citations after every iteration

Inserting a source in the middle of page one must renumber every later note, every page footnote, and the ending bibliography.

```bash
python3 @wca-ivy-biblio/scripts/reorder_citations.py \
  ./artifacts/iterate-<slug>/folio.json \
  --in-place
python3 @wca-ivy-biblio/scripts/qa_ivy_document.py \
  ./artifacts/iterate-<slug>/folio.json
```

Use `deep.json` or `monograph.json` when that is the working file. Never hand-renumber a file that already has more than a handful of `{{n}}` markers. Details are in `references/citation-restamp.md`.

Chicago form stays notes-bibliography. Numbers follow first appearance in reading order and stay contiguous `1..N`. The bibliography lists each unique work once in that same order. Do not alphabetize as the sort key. Do not use author-date parentheticals.

### 5. Adversarial pass inside each iteration

Before closing an iteration, write a short dissent block in `rounds/round-NN.md`

- the strongest published objection to the new claims
- a rival school, agency, or later revision
- any quantity that is still a point estimate without a variance or a stated gap

If the dissent names a reachable primary PDF, that PDF becomes the first search of the next iteration.

### 6. Saturation then emit

When the stop gate closes, follow `references/emit-handoff.md`.

Required stack order

1. Finish the working JSON body (intro, historiography, method, one chapter per surviving research question, synthesis, open problems, bibliography).
2. `/itqe` — fill every equation object and every ranked inventory. Maximize relevant formulas from any academic class the topic supports. Latest ITQE version is the skill at `@itqe`. Re-read that SKILL.md at emit time so a newer patch wins.
3. `/latex` — compile figures. No raw TeX on a delivered page.
4. `/ivy-biblio` — remap once more and QA.
5. `/banner` only when emit target is `/deep` or the user typed `/banner`.
6. `/copyright` living footer.
7. Build with the folio or deep builder.
8. Render gate, then raster every page.

```bash
python3 @itqe/scripts/scan_render_gate.py \
  ./artifacts/iterate-<slug> \
  --also-pdf ./artifacts/<file>.pdf
python3 @latex/scripts/scan_raw_tex.py \
  ./artifacts/iterate-<slug> \
  --also-pdf ./artifacts/<file>.pdf --pages
pdftoppm -png -r 140 ./artifacts/<file>.pdf /tmp/iterate-page
```

Exit code 1 blocks delivery. Repair, rebuild, scan again.

### 7. Deliver

Give the user the PDF. State iteration count, page count, note count, bibliography count, keeper count, remaining open questions, and the emit target. Do not dump the JSON or the ledger into chat.

If the user asked only for another iteration on an existing ledger and not a rebuild, deliver the updated PDF when the pass closed a material hole; otherwise state what the pass added and wait.

## Hard rules

- No invented sources, page numbers, or quotations.
- Prefer the issuing body's canonical PDF over an HTML reprint or a secondary blog.
- Prefer Ivy League, university-press, `.gov`, `.mil`, and named healthcare bodies (NIH, FDA, CMS, WHO, CDC, VA) when they own the fact.
- Citation numbers stay in first-appearance order after every insertion. Restamp is mandatory, not optional.
- ITQE four columns under every display equation. Identifier is the glyph, not the English spelling of a Greek letter.
- Chat may use KaTeX. Files may not show LaTeX, AMS-TeX, KaTeX, or MathJax source.
- Visible house anchor is Digital Marketing Company linking to https://DigitalMarketingCo.org. Plain-text domain is DigitalMarketingCo.org.
- No emoji. No tofu. No black boxes. No checkerboard baked into RGB as fake transparency.
- Do not reprint builder source into chat.
- Do not claim a clinical license, a military clearance, or that the model is literally the smartest agent in the world.


## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write figure, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.


## Negative gate (mandatory before any deliverable)

Read `@negative/SKILL.md` and `@negative/references/blocklist.md`.
Before chat, PDF, DOCX, PPTX, XLSX, caption, filename, alt text, or footnote leaves this skill, extract visible text and run

```bash
python3 @negative/scripts/sweep_negative.py <extracted-text>
```

Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.

## ChatGPT portability

Resolve `@skill-name/path` by finding the installed personal skill whose SKILL.md frontmatter has `name: skill-name`; read that path under its directory. For `@generate/`, use the `generate-prompt` skill. Before running copied shell commands, substitute actual resolved paths and use the current working directory for generated files. Apply instructions only when this skill is invoked or a user requests the corresponding workflow. User instructions and platform rules take priority. Run bundled scripts only after checking their inputs and prerequisites. Never claim unavailable integrations, credentials, citations, or generated results.
