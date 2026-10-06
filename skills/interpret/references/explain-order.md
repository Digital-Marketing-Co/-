# Explain order

Print objects in `rank.json` order. Inventory ids stay in encounter order inside the ledger so a reader can walk back to the board.

## Per-object section

Use this heading skeleton in `explanations.md` and in the folio / deep chapters that reprint it.

1. Rank line — rank number, score to two decimals, `id`, short name
2. Display plate — compiled glyphs. Chat may use KaTeX. Files use a `/latex` PNG or supported Unicode
3. Claim — one sentence, no jargon pile
4. First-use names — every variable, subscript, superscript, and constant in that sentence
5. ITQE table — Identifier, Term, Quantity, Explanation. Every symbol on the plate gets a row. Operators that are not quantities do not
6. Glyph legend — only when a Greek, Hebrew, nabla, partial, or variant Latin glyph is present
7. Data hook — column, period, unit, and whether the object is observed, derived, or missing
8. Rival reading — omit the subsection when `alt_readings` is empty
9. Warrant — Chicago note to the methodology or paper. Primary PDF preferred

## First-use rule

The first time `Y^{real}` appears, write that `Y` is output and the superscript `real` marks a constant-price measure. Do not repeat the lecture on later pages. Do repeat the ITQE row on every plate that still shows the glyph.

## Maximizing formulas

If the linked set supports a definition, an identity, a rate, an estimator, and a constraint, print all five as separate plates. Do not collapse them into one ornamental line.

Examples the GDP board often supports once the data is present

- Real output as a chained or constant-price aggregate
- Instantaneous growth as a time derivative
- Average growth as a log difference over a window
- An inequality against zero or against a threshold
- An SNA identity that decomposes the same aggregate

Do not add an IS-LM system because the letters look macro. Local relevance only.

## Language

- Identifier cells print the glyph
- Quantity cells print SI or the series unit with Unicode powers
- Explanation cells are local to this plate
- No raw TeX in a cell, caption, heading, footnote, or bibliography line
