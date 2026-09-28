# Citation restamp after every iteration

House contract is WCA Ivy Chicago notes-bibliography. Full algorithm lives in `/home/workdir/.grok/skills/wca-ivy-biblio/references/citation-order.md`. This file is only the iterate insertion rule.

## The user-facing example

If page one already has three citation events and the document has twenty notes, and the next iteration adds a new source as the second event on page one, that new source must not stay numbered 21 in the middle of 1, 2, 3. After remap the new event is 2, the old 2 becomes 3, and every later number, every page footnote, and the bibliography order shift by one.

## How to insert

1. Give the new work a `work_id` (short slug from author-year-title).
2. Append a note object with a temporary `n` in 9001–9999, or omit `n`.
3. Place `{{9001}}` (or the chosen temporary) at the exact locus in reading order.
4. Append a bibliography line for a new work only. A later short-form note to an existing work does not add a bibliography line.
5. Run the remapper on the working JSON.
6. Run `qa_ivy_document.py`. Fail closed on gaps, unused colliding numbers, or an alphabetized bibliography that ignores first appearance.

```bash
python3 /home/workdir/.grok/skills/wca-ivy-biblio/scripts/reorder_citations.py \
  /home/workdir/artifacts/iterate-<slug>/folio.json \
  --in-place
python3 /home/workdir/.grok/skills/wca-ivy-biblio/scripts/qa_ivy_document.py \
  /home/workdir/artifacts/iterate-<slug>/folio.json
```

The remapper writes `citation-map.json` beside the source (old-to-new). Keep that file. Do not edit superscripts by hand across a long file.

## What must move together

- inline `{{n}}` and `{{n, m, p}}` markers
- `notes[].n`
- page-local footnote bands the builder will reprint
- `bibliography[]` order (first appearance of each unique work)
- any concordance in a collected Notes section

Numbers after remap are exactly `1..N` with no gaps.

## Deletions

Withdrawing a claim deletes its unique note events if nothing else cites that locus. Run the same remapper. Gaps close.

## Forbidden

- leaving a new source numbered as last-plus-one when it appears early in reading order
- author-date parentheticals as the citation mechanism
- alphabetized bibliography as the house sort
- inventing a page number so a note looks complete
