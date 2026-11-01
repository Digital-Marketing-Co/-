# WCA Ivy citation-order remapping

Base remains CMOS notes-bibliography. WCA Ivy adds a reading-order contract.

## Two objects

- **Note** — one numbered citation event. Full form the first time a work is named; short form later. `notes[].n` is the superscript the reader sees.
- **Work** — one bibliographic object. One line in `bibliography[]`. Identified by `notes[].work_id` when present, else by `notes[].biblio` (0-based index into `bibliography[]` before remap), else by a normalized key taken from italic title words in the note text.

Several notes may point at one work. The work appears once in the bibliography, at the locus of its first note.

## Reading order

Walk in this sequence

1. `abstract`
2. each `sections[]` in array order, skipping sections whose `kind` is `notes` or `bibliography`
3. inside a section, each `paragraphs[]` item
4. string paragraphs first; then captions on `figure`; then `caption` on any `type=equation` object
5. `sections[].equations[]` when that extra list exists

Collect every integer inside `{{...}}` markers, left to right. Adjacent `{{1}}{{4}}` collapses to one run before collection. First-seen order of those integers is the old sequence.

## Remap

Let `old_order` be the first-seen note numbers. Assign `new = index + 1`. Every later mention of an old number uses the same new number.

After remap

- markers in every walked string use the new integers
- `notes[].n` uses the new integers
- `notes` is sorted by `n` ascending
- unused notes (never cited) are kept at the end only if `keep_unused` is true; default is to drop them and report the drop
- numbers are exactly `1..N` with no gaps

## Bibliography order

Build `work_first[work_id] = smallest new n` among notes that belong to that work.

Sort unique works by `work_first` ascending. Rewrite `bibliography[]` in that order. Update `notes[].biblio` to the new index.

Do not alphabetize. Family-name order is not the house sort key.

Do not print a second number series on bibliography lines. The citation number the reader already has is the note number.

## Insertions

When the agent adds a source in the middle of the argument

1. draft the new note with a temporary n that does not collide (for example 9001) or with `n` omitted and a `work_id`
2. place `{{9001}}` at the locus
3. run `reorder_citations.py --in-place`
4. never hand-renumber a file that already has more than a handful of markers

Deletions run the same script. Gaps close.

## What the script will not do

- invent a note text
- merge two works that do not share `work_id` / biblio index / title key
- turn Chicago event notes into IEEE reused numbers (the same book cited twice still consumes two note numbers)
- write author-date parentheticals
