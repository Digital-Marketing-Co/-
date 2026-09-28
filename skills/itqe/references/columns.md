# ITQE columns and Greek legend

## Columns

| Letter | Header printed | Allowed content |
|---|---|---|
| I | Identifier | Exact compiled glyph on the plate (Unicode or mini-plate, never raw TeX) |
| T | Term | English name |
| Q | Quantity | Unit, dimension, coded domain, or `dimensionless` |
| E | Explanation | One clause, local to this plate |

Header kicker is the four letters `ITQE` in muted small caps or Libre Franklin 8 pt.

## First-use sentence

The sentence that introduces a plate names every identifier in reading order before or with the plate. The table does not replace that sentence. The table is the durable key.

## Greek, Hebrew, and variant Latin

Build the legend from identifiers that are not plain ASCII Latin.

| Glyph | Name to print |
|---|---|
| α | alpha (lowercase) |
| β | beta (lowercase) |
| γ | gamma (lowercase) |
| δ | delta (lowercase) |
| Δ | delta (capital) |
| ε | epsilon (lowercase) |
| θ | theta (lowercase) |
| λ | lambda (lowercase) |
| μ | mu (lowercase) |
| π | pi (lowercase) |
| σ | sigma (lowercase) |
| Σ | sigma (capital) |
| τ | tau (lowercase) |
| φ | phi (lowercase) |
| ω | omega (lowercase) |
| ℓ | script l |
| ħ | h-bar |

Spoken form states the role on this plate, not a dictionary gloss of the letter.

Print the compiled glyph in the Identifier cell. Print the English name and case after the glyph, and again in the secondary ITQE — glyphs table. Never leave theta, lambda, or sigma as Latin stand-ins for θ, λ, or σ.

Secondary table columns (required when any non-English glyph is on the plate)

| Column | Holds |
|---|---|
| Glyph | Compiled character |
| Name and case | alpha (lowercase), Delta (capital), varphi (variant) |
| Role in this equation | Local function of the glyph on this plate |
| Operators on this plate | Only operators that actually bind this glyph here; otherwise none on this plate |

## Quantity cell conventions

- Time as human age or duration — `years`
- Powers and units — Unicode only (`m⁻¹`, `kg·m²`, `yr⁻¹`). Never `m^-1` or `kg m^2`
- Rate — `deaths per 1,000` or `yr⁻¹` when a force of mortality
- Money — ISO currency code then unit (`USD per person`)
- Mass concentration — `µg m⁻³`
- Pressure — `mmHg` when that is the clinical unit already in the prose
- Percent of DALYs — `% of DALYs`
- Rank — `rank (1 = longest e0)`
- Unknown unit — do not guess; write `not reported`

## Empty cells

An empty cell is a defect. If a quantity is truly unknown, the Quantity cell is `not reported` and the Explanation cell states why.
