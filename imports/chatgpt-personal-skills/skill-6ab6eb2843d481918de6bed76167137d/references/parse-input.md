# Parse input

The linked set is everything the user pointed at in the same turn plus any file already sitting in the interpret work folder. Do not fetch a random national-account table because the board says GDP.

## Input kinds

1. Photograph or scan of a board, napkin, slide, or notebook.
2. Typed symbol chain in the prompt.
3. Tabular data — CSV, TSV, XLSX, pasted markdown table.
4. Named series — a URL, FRED code, BEA NIPA table, World Bank indicator, or file path.
5. Conversation figure already rendered in this thread.

A run may mix kinds. Inventory them all.

## Photograph

- Copy the file into `input/` under the work folder.
- Read the image with `read_file`.
- Write `board-transcript.md` with two independent readings.
- Segment left-to-right clusters. A large V sitting on a small M with GLOBAL under it is one object, not three, unless the strokes are clearly separate claims.
- Keep raw marks. Arrows, mushrooms, circled letters, strikethroughs, and superscript REAL are objects.
- Confidence below 0.5 stays in `alt_readings`. Do not silently pick the prettier identity.

## Typed chain

Write `board.txt` verbatim. Do not normalize φ to phi in the raw field. Normalization lives in `reading`.

## Tables and series

Copy into `data/`. Write `data-card.md`

- source
- period
- frequency
- geography
- unit
- transformation already applied (real, seasonally adjusted, log, YoY)
- missingness

Do not rebase, deflate, or seasonally adjust unless the user asked or the identity on the board already names that transform. If the board says GDP REAL, look for a real series. If only a nominal series is present, say so and keep the identity as a claim about a missing transform.

## URLs

Browse the page for the series documentation and the latest methodology PDF. Prefer BEA, BLS, Census, IMF, OECD, World Bank, FRED, and university-press PDFs. Record keepers in `sources.jsonl`. Never invent a page locator.

## Empty sides

- Board only — the linked set is the board. Rank by internal dependence, then by how much empirical load the identity would need.
- Data only — harvest candidate relations from the series definition and from the literature that series supports. Each harvested identity is an equation object with `kind` identity or rate.
- Neither — stop and ask. Do not invent a board.
