

# /corpus


## Visual stack

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Compile every reachable work that matches one person, organization, or identifier. The unit of analysis is the **creator**, not a topic. Output is an inventory plus a Chicago bibliography catalog. Do not write a literature-review monograph unless the user also stacked `/folio` or `/deep`.

Work in `./artifacts/<slug>/`. Default printed catalog is `./artifacts/<YYYY>-<slug>-corpus.pdf`.

`<skill>` = `@corpus`.

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
  --out ./artifacts/<slug>/raw
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
  ./artifacts/<slug>/works.jsonl \
  --out ./artifacts/<slug>/works.dedup.jsonl \
  --report ./artifacts/<slug>/dedup-report.md
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
  ./artifacts/<slug>/corpus.json \
  --out ./artifacts/<YYYY>-<slug>-corpus.pdf
```

House marks on the catalog

- visible link anchor Digital Marketing Company → https://DigitalMarketingCo.org
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
python3 @itqe/scripts/scan_render_gate.py \
  ./artifacts/<slug> \
  --also-pdf ./artifacts/<file>.pdf
python3 @latex/scripts/scan_raw_tex.py \
  ./artifacts/<slug> \
  --also-pdf ./artifacts/<file>.pdf --pages
```

Exit code 1 blocks delivery. Repair with `/latex` figures, attach an ITQE table under every display equation (Identifier, Term, Quantity, Explanation), rebuild, scan again, and raster every page. See `@itqe/references/render-gate.md` and `@latex/SKILL.md`.

## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write figure, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

## Canonical footer

Render `copyright/SKILL.md` and its canonical notice helper once per page. Do not reproduce independent legal text or calculate years here.

## Negative gate (mandatory before any deliverable)

Read `@negative/SKILL.md` and `@negative/references/blocklist.md`.
Before chat, PDF, DOCX, PPTX, XLSX, caption, filename, alt text, or footnote leaves this skill, extract visible text and run

```bash
python3 @negative/scripts/sweep_negative.py <extracted-text>
```

Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.

## ChatGPT portability

Resolve `@skill-name/path` by finding the installed personal skill whose SKILL.md frontmatter has `name: skill-name`; read that path under its directory. For `@generate/`, use the `generate-prompt` skill. Before running copied shell commands, substitute actual resolved paths and use the current working directory for generated files. Apply instructions only when this skill is invoked or a user requests the corresponding workflow. User instructions and platform rules take priority. Run bundled scripts only after checking their inputs and prerequisites. Never claim unavailable integrations, credentials, citations, or generated results.
