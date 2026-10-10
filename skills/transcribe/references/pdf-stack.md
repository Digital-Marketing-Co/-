# Transcript PDF stack

After `raw.lock.txt`, `summary.md`, `expand-1.md`, and `expand-2.md` exist, compile through house skills. Do not start the stack before `qa_transcript.py` exits 0.

Work folder stays `/home/workdir/artifacts/transcribe-<slug>/`.

## Skill order

1. `/folio` — read `expand-2.md` and `sources.jsonl`. Write `folio.json` against the folio schema. Compact Literata 10-pt body. Chicago page-local footnotes. ITQE tables under every display equation. Public file `/home/workdir/artifacts/YYYY-topic-slug-wca-folio.pdf`.
2. `/banner` — one 16-9 full-bleed banner per body section and per subsection. Prompt only from named objects in that node (document, ribbon, platform class, office seal — not a living private face). After generate, run `banner/scripts/apply_tb_alpha_blend.py`. Left and right opaque to trim. Top and bottom real alpha.
3. `/images` — mid-section plates every 500 words after the opening blurb of that node. Same geometry and uniqueness rules. No path or byte reuse.
4. `/book` — chapter the folio body. Write `book.json`. Suggested body chapters match the pass-3 nodes. Run `book/scripts/audit_unique_images.py`. Embed the house HTML image-link whose visible text and title attribute are both Digital Marketing Co.
5. `/wca-ivy-biblio` — remap superscripts to first-appearance order. Sort the bibliography the same way. Confirm an ITQE table sits under every equation paragraph.
6. `/copyright` — living footer on every page. Owner Web Development Corporation. START 2012 unless the user typed a year.
7. `/latex` then `/itqe` — scan every page for raw TeX, tofu, empty boxes, or glitched glyphs. A dirty scan blocks delivery.
8. `/negative` — extract visible text from `summary.md`, `expand-1.md`, `expand-2.md`, `folio.json`, `book.json`, and PDF text. Run `python3 /home/workdir/.grok/skills/negative/scripts/sweep_negative.py`. Rewrite hits so the document still makes sense and is tighter. Re-scan until CLEAN. Do not touch `raw.txt`. A dirty sweep blocks delivery.

## Visual contract

Follow `/home/workdir/.grok/skills/visual-system/SKILL.md`.

- Landscape 16-9 generates at or above 3300 x 1856
- Full bleed left and right
- No burned-in caption or URL on the plate
- No photoreal portrait of a private living person
- Source photograph of a historical document may be reprinted once as a cited figure, not reused as a section banner

## Chat versus PDF

Chat still prints the raw transcript and the pass-1 summary first. The PDFs are the stacked deliverable, not a substitute for the diplomatic text.

If the user typed `/transcribe` raw only, do not enter this file.
