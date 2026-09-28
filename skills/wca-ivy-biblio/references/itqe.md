# ITQE tables under rendered equations

ITQE is the Interactive Table of Quantitative Elements. It is the house plate that sits immediately under every display equation. The four columns are locked.

## Primary project mandate

When `/itqe`, `/ivy-biblio`, `/folio`, `/phd`, `/latex`, or a stacked rebuild runs, the **primary and mostly important** drafting rule for the working document is this

- Include the **maximum number of relevant** mathematically represented formulas, equations, identities, inequalities, rates, estimators, constraints, mappings, recurrences, and quantitative descriptions that the topic actually supports.
- Field of origin does not matter. Pull relations from any class of academia if they are on-topic and can be written without inventing a constant or a source.
- Every such display relation is a compiled plate plus its matching ITQE table. A prose-only treatment of a quantitative claim is a defect, not a style choice.
- Do not invent equations the literature does not support. Do not pad with decorative identities that never appear in the argument. Maximize *relevant* plates, not ornamental ones.
- Historical, legal, clinical, or qualitative chapters still carry plates wherever a rate, score, threshold, ratio, or formal relation is discussed.

This mandate outranks “keep the chapter short” and “save the math for an appendix.” It does not outrank source honesty or the no-invented-values rule.

| Column | Name | What it holds |
|---|---|---|
| I | Identifier | The symbol, operator, or named quantity as printed (`E`, `m`, `c`, `ħ`, `Δt`) |
| T | Term | English name of that identifier (`energy`, `rest mass`) |
| Q | Quantity | Unit, dimension, or domain (`J`, `kg`, `m s⁻¹`, dimensionless, set of states) |
| E | Explanation | Role of the identifier in this equation, in one short clause |

The header row prints the four letters expanded — Identifier, Term, Quantity, Explanation — with a muted kicker `ITQE` above the rule.

## Placement

- PDF / Folio / Deep — the compiled plate (or a Unicode line the face can draw), then the caption, then the ITQE table, kept together so a page break does not orphan the table.
- Chat — KaTeX display block, then a markdown table with those four headers.
- HTML / app — the rendered KaTeX node, then a semantic table with caption `ITQE`.
- DOCX / PPTX — plate or OMML, then a 4-column table. Do not screenshot the table.

Do not put ITQE above the plate. Do not bury it in a footnote. Do not skip it because the equation “looks obvious.”

Inline math inside a sentence does not get a table. It still gets the house first-use sentence that names every symbol.

## How to fill a row

- Identifier matches the glyph on the plate. Do not invent a new symbol in the table.
- Term is the ordinary name a dissertation committee would accept.
- Quantity prefers SI or the unit already in the surrounding prose. Write `dimensionless` when that is the fact.
- Explanation is local to this equation, not a Wikipedia gloss of the whole field.

Constants quote BIPM, NIST, or CODATA when a number is claimed. Do not invent a value.

Every variable, subscript, and constant that appears on the plate has a row. Operators that are not quantities (`=`, `+`) do not.

## Source fields

On a paragraph object

```json
{
  "type": "equation",
  "id": "eq-1",
  "plate": "equations/eq-01.png",
  "unicode": "E = mc²",
  "caption": "Equation 1. Mass–energy equivalence.",
  "itqe": [
    {"identifier": "E", "term": "energy", "quantity": "J", "explanation": "total energy of the isolated system"}
  ]
}
```

`tex` may exist as a sibling rebuild file. It is never printed on the page.

`inject_itqe.py` will copy `symbols[]` into empty `itqe` rows when those symbols already carry term and quantity. It will not guess explanations.

## QA

Reject the page when

- a display equation has no ITQE table
- a plate symbol is missing from the identifier column
- any of the four cells is blank
- raw TeX delimiters are visible in the plate, the caption, any ITQE cell, or surrounding prose
- ASCII-TeX shorthands (`^{}`, `_{}`, `m^-2`) appear in a cell
- the table is a baked screenshot of a checkerboard
- tofu or missing-glyph boxes appear in identifier, term, quantity, or explanation cells

Stack `/latex` for compilation. This skill owns the table that follows the plate.
