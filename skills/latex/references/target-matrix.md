# Target matrix

Choose one renderer per expression. Do not mix raw TeX into a target that will not compile it.

## Chat reply

Use KaTeX (global Grok rule). Fenced code blocks for listings. Do not emit a PDF plate into chat unless the user asked for a file.

## /folio and /phd compact PDF

Literata 10 pt body does contain Greek and most math operators used in SI text. Prefer Unicode in the JSON for simple quantities (`c = 299 792 458 m s^-1`) after confirming the face. Display derivations become PNG plates from `render_snippet.py` at 300 dpi, captioned, placed after the naming paragraph.

## /deep Georgia 22 pt PDF

Bundled Gelasio-as-Georgia is missing common Greek (nu, Delta often tofu). Do not put Greek or minus-U+2212 into `/deep` JSON. Spell `delta-nu_Cs` or embed a Latin Modern plate. This is the most common house failure mode.

## /print and generic PDF

Same as folio if the builder face is Literata or Times-class with a math fallback. Otherwise plate.

## /banner plates

Banners may show an equation only when that exact equation is in the section. Render the equation as a plate first, then composite, or omit numbers entirely. No false quantities.

## HTML page and Next.js app

KaTeX CSS + `renderToString` or auto-render. Self-host or pin the KaTeX version. Fallback SVG from `render_snippet.py --format svg`. Code listings use a real `<pre><code>` with a monospaced face, never an image of code.

## DOCX / Word

First try Office Math (OMML) via the docx skill. If the builder cannot emit OMML, insert a 300 dpi PNG with alt text equal to the TeX source. Keep the `.tex` sibling in the project folder.

## PPTX / slides

One compiled plate or OMML object per slide. Minimum rendered height 18 pt equivalent. Caption on the slide names every symbol.

## XLSX / spreadsheet

Put values and simple Unicode in cells. Use a cell formula when the expression is computable. A drawing-anchor PNG only when the expression is not a spreadsheet formula (for example a definition identity that must look typeset in a print layout).

## Markdown source

Allowed to contain TeX inside fenced `tex` / `latex` listings because that is source. Unfenced `$...$` and `\[...\]` in Markdown that will be printed as body type must be compiled first.

## Draft JSON about to become a page

`folio.json`, `monograph.json`, and `deep.json` body strings are visible pages. Harvest and compile them before the builder runs. Only keys named `tex`, `latex`, `source`, or `preamble` may keep raw source.
