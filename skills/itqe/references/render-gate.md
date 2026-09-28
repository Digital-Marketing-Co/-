# Render gate — compiled math only, intended glyphs only

No delivered page may show uncompiled LaTeX, AMS-TeX, KaTeX source, TeX source, MathJax source, or a clip that is not the intended symbol. Missing-glyph boxes, ballot-box-X stand-ins, tofu, and glitched operators fail the same gate. Chat still uses KaTeX. Files use compiled glyphs or a compiled plate plus an ITQE table.

After the builder finishes, scan the entire document. Do not stop at the first clean source scan. See `intended-render.md`.

## Commands

```bash
python3 /home/workdir/.grok/skills/itqe/scripts/scan_render_gate.py \
  /home/workdir/artifacts/<slug> \
  --also-pdf /home/workdir/artifacts/<file>.pdf

python3 /home/workdir/.grok/skills/latex/scripts/scan_raw_tex.py \
  /home/workdir/artifacts/<slug> \
  --also-pdf /home/workdir/artifacts/<file>.pdf --pages
```

Exit code 1 blocks delivery. Raster every PDF page after a clean scan.

## Defects

- `$...$`, `$$...$$`, `\(...\)`, `\[...\]`
- `\begin{equation}`, `\begin{align}`, `\frac`, `\sum`, `\mathrm`, Greek commands left as source
- Caret-brace or underscore-brace in any printable string, including Identifier, Term, Quantity, Explanation
- ASCII-TeX exponents in cells or prose (`m^-2`, `uu^T`, `R^{I×J×K}`)
- Visible `katex.render` or MathJax source
- U+FFFD, ☒ ☐ □ ■ ◻ ▣ ⬜ ▢, or runs of empty boxes
- A printed clip that is not the intended mathematical symbol (ρ as ☒, × as a boxed X)
- A `type=equation` object with no plate/unicode and no ITQE rows
- An ITQE cell that still holds a backslash command or a missing-glyph stand-in

## Repair

Compile with `/latex` `render_snippet.py`, store the PNG on the equation object, keep `tex` as a hidden rebuild sibling, fill Identifier-Term-Quantity-Explanation, rebuild, scan again.
