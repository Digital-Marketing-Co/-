---
name: transcribe
description: Transcribe attached or referenced data into a locked raw verbatim text, then write a summary that is expanded twice into a research-ready manuscript and compiled through folio, images, banner, and book. Trigger on /transcribe, raw transcript, plaque or citation OCR, letter dump, framed-document readout, or expand this source into a WCA Folio illustrated book.
---

# /transcribe

## Quality and capability additions

Read [the task-specific quality profile](references/quality-profile.md) before execution. Use `evals/quality-cases.json` for regression scenarios; its assertions are acceptance criteria, not claims that tests have run. Shared path resolution and output rules live in `interop/SKILL.md`.


Lock one source. Dump it as raw text. Summarize it. Expand that summary. Expand it again until it is a manuscript. Then compile one letter-size illustrated book through `/folio`, `/images`, `/banner`, and `/book`.

Do not rewrite the raw layer. Do not invent glyphs the source does not support. Do not skip the two expansion passes and jump straight to a PDF.

Work in `/workspace/artifacts/transcribe-<slug>/`.

Skill root is `@transcribe`.

Read on demand

- `references/source-types.md` — accepted inputs and ingest order
- `references/raw-lock.md` — verbatim rules, uncertainty marks, reading order
- `references/expand-ladder.md` — summary then expand then expand-again
- `references/pdf-stack.md` — folio, images, banner, book, ivy, copyright
- `assets/schema/transcript.schema.json` — required JSON shape
- `scripts/init_workdir.py` — folder, lock copy, empty transcript.json
- `scripts/qa_transcript.py` — fail closed if raw was edited after lock

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with the visual-system picker. Paint covers, banners, rules, table headers, and figure frames. Do not change folio or book locked body fonts or point sizes. Banner and plate prompts append the volumetric clause in `visual-system/references/depth.md`.

If the user only asked to create or revise this skill and supplied no source, stop after the skill files exist. Do not invent a document or a book.

## When this runs

- User typed `/transcribe`
- User asked for a raw transcript of a photo, scan, plaque, citation, letter, PDF, screenshot, or recording
- User asked to dump text then expand it into a folio or illustrated book
- User stacked `/transcribe` with `/folio`, `/images`, `/banner`, and/or `/book`

If no source is present and this is not a skill-edit turn, stop and ask for one.

Default stack when `/transcribe` is typed alone with a source — run the full ladder through book. If the user says raw only, stop after `raw.txt`. If they say summary only, stop after pass-1.

## Workflow

### 1. Lock the source

Copy the original into the work folder as `source` plus its real extension. Never overwrite the attachment.

Record in `source-meta.md`

- path, bytes, mime or extension
- width and height for rasters
- page count for PDFs
- language guess
- ingest method used

Acceptable sources and the ingest order live in `references/source-types.md`.

Framed wall documents (citations, commissions, diplomas) are first-class. Read the full frame with `read_file` or `view_image`. Crop only when glare or the frame hides a line. Do not inpaint missing paper.

### 2. Raw transcript (locked)

Write `raw.txt` and the `raw` object inside `transcript.json`.

Rules are in `references/raw-lock.md`. Short form

- Reading order is top to bottom, left to right, then attached devices (ribbon, seal, signature)
- Keep line breaks that mark a printed line
- Keep ALL CAPS, small-cap headings, and original spelling
- Mark unreadable runs as `[illegible]` or `[cut off]`
- Mark uncertain readings as `[word?]`
- Transcribe signatures as the written name plus `(signed)` when the printed office line is also present
- Do not correct, modernize, expand abbreviations, or fill clipped words from memory
- After `raw.txt` is written, copy it to `raw.lock.txt` and do not edit the lock

Chat must print the raw block in a fenced code block before any summary.

### 3. Pass-1 summary

Write `summary.md` (about 120–220 words). One paragraph or short bullets. Only claims that the raw text actually supports. No biography of a named person unless that biography is printed on the source. No campaign history unless the source states it.

### 4. Pass-2 expansion

Write `expand-1.md`. Target 800–1,600 words.

Allowed now

- Restate every raw claim in full sentences
- Identify printed offices, awards, platforms, and dates that appear in the raw
- Add a short public-record context paragraph only when a keeper PDF or `.mil` / `.gov` / university-press source confirms it
- Tag every sentence `raw` or `context`
- Keep a claims table in `claims.jsonl` (`id`, `text`, `origin`, `keeper`)

Forbidden

- Inventing a date the source does not print
- Inventing a second award
- Diagnosing the recipient
- Turning a family photo filename into a family narrative unless the user asked for that and the fact is already in the raw or a cited keeper

### 5. Pass-3 expansion

Write `expand-2.md`. Target 3,000–6,000 words or until the topic saturates.

This pass is the manuscript seed for `/folio` and `/book`.

- One section per major raw claim
- One section for the physical object (paper, frame, ribbon bar, signature block) when the source is a photograph
- One historiography or literature section from keepers
- One open-problems section
- Chicago `{{n}}` markers as soon as a keeper is used
- ITQE mandate — any rate, date-span, hull count, frequency band, medal class, or other quantitative description the topic supports becomes a compiled display equation plus a four-column Identifier-Term-Quantity-Explanation table
- Explain every variable and constant the first time an equation appears

Run at least two research rounds. Prefer primary PDFs, `.mil`, `.gov`, and university-press work. Record keepers in `sources.jsonl`. Never fabricate a page number.

### 6. Compile the stack

Follow `references/pdf-stack.md`. Order is fixed

1. `/folio` — compact Ivy report from `expand-2.md` into `folio.json`, then the folio builder
2. `/banner` — one 16-9 full-bleed banner per body section and per subsection
3. `/images` — mid-section plates on the 500-word cadence
4. `/book` — chapter the folio body into `book.json`, uniqueness audit, letter-size book PDF
5. `/wca-ivy-biblio` — first-appearance notes, remapped bibliography, ITQE tables
6. `/copyright` — living footer, owner Web Development Corporation, START 2012 unless the user typed a year
7. `/latex` and `/itqe` render gates — fail closed on raw TeX or tofu
8. `/negative` — extract visible text from every pass file and every PDF page. Sweep with `negative/scripts/sweep_negative.py`. Rewrite hits so the prose still holds and reads tighter. Re-scan until CLEAN. Block delivery on leftover hits. Do not rewrite `raw.txt` or `raw.lock.txt`.

One work folder. Two public PDFs are allowed — the folio file named `YYYY-topic-slug-wca-folio.pdf` and the book file the book skill names. Do not emit four untitled drafts.

Visible house anchor is Digital Marketing Company Seed URL is https://DigitalMarketingCo.org. Plain-text domain is DigitalMarketingCo.org. Anchor text must match the title attribute.

### 7. Visual QA and deliver

Raster every PDF page at 140 dpi. Rebuild if tofu, clipped type, reused banner bytes, a metaphor plate, or a broken house link appears.

Chat deliverable order

1. Raw fenced transcript
2. Pass-1 summary
3. Paths to `expand-1.md`, `expand-2.md`, `transcript.json`
4. The folio PDF and the book PDF when the stack ran
5. Page count, note count, bibliography count, remaining gaps

Do not dump builder JSON into chat.

## Publication checks

Apply `interop/SKILL.md` once after the task-specific checks. Its shared rules yield to this skill's explicit format and source-fidelity requirements.

## Delivery

Run the single delivery gate in `interop/SKILL.md` after task-specific validation. Preserve verified quotations and technical identifiers; report unresolved defects or blockers accurately.
