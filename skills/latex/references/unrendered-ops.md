# Unrendered operators and operands

A visible page fails if a reader can still see source markers where a compiled operator or operand should be. LaTeX, AMS-TeX, KaTeX, MathJax, ASCII-math, and Unicode-fallback leftovers are the same defect.

## Fail on sight

| Marker | What it usually is | Required render |
|---|---|---|
| `_` | subscript | Unicode subscript or a compiled plate (`x_i` → xᵢ) |
| `\` | command or escape | compiled glyph; no backslash on the page |
| `/` between operands | fraction, division, per-unit solidus | stacked fraction, ÷, or a plate (`a/b`, `m/s` in a formula) |
| `^` | superscript | Unicode superscript or a plate (`x^2`, `10^{-3}`) |
| `<=` `>=` `!=` `~=` | relations | ≤ ≥ ≠ ≈ |
| `->` `<->` | arrows | → ↔ |
| `*` between operands | multiplication | · or × |
| `+` `-` `=` inside a leaked token that also has `_`, `^`, or `/` | arithmetic | compiled expression |

Operands (variables, indices, Greek letters, units, numerals that belong to the expression) ship as glyphs in the same plate or Unicode run. Do not leave the operand in source form beside a compiled operator.

## Allowed solidus and underscore

Strip before judging:

- `http://` and `https://` URLs
- email addresses
- fenced code listings whose job is to show source
- JSON keys `tex`, `latex`, `source`, `preamble`
- prose solidus in `and/or`, `n/a`, `N/A`, `w/o`, `I/O`

Any other visible `_` fails. Any visible `\` fails. A solidus with an operand on both sides fails unless it is in the allowlist above.

## Scan

```bash
python3 /root/.grok/server-skills/latex/scripts/scan_unrendered_ops.py \
  /home/workdir/artifacts/<slug> \
  --also-pdf /home/workdir/artifacts/<file>.pdf
```

Exit code 1 blocks delivery. Compile the hit with `render_snippet.py` or proven Unicode, attach ITQE if the expression is display math, rebuild, scan again.
