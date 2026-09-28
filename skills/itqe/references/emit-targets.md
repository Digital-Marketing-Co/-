# Emit targets

## Chat

1. One-line caption
2. KaTeX display block for equations
3. Markdown table with headers Identifier | Term | Quantity | Explanation
4. Secondary table ITQE — glyphs with headers Glyph | Name and case | Role in this equation | Operators on this plate
5. Source line with named dataset

Do not wrap the table in a code fence. Do wrap KaTeX in `$$`. Chat may use KaTeX. File ITQE cells and body strings must already be compiled Unicode or a plate — never dump KaTeX source into JSON that a PDF builder will print.

## Folio / Deep JSON

Set `type` to `equation`. Fill `unicode` or `plate`. Fill `itqe` as an array of four-key objects. Optional `legend` array. Then run `inject_itqe.py` and `qa_ivy_document.py`.

## HTML white paper

```html
<figure class="itqe">
  <div class="plate"><!-- rendered KaTeX --></div>
  <figcaption>Equation N. Caption.</figcaption>
  <details open>
    <summary>ITQE — quantitative elements</summary>
    <table>
      <caption>ITQE</caption>
      <thead><tr><th>Identifier</th><th>Term</th><th>Quantity</th><th>Explanation</th></tr></thead>
      <tbody><!-- rows --></tbody>
    </table>
    <p class="legend"></p>
  </details>
</figure>
```

Collapsible is the white-paper look. Default state is open so print and a11y still see the rows.

## DOCX / PPTX / XLSX

Native table. Four columns. Header row. No screenshot.

## Inventory without an equation

A ranked factor list is still an ITQE table. Caption names the inventory (`Causal factors of national longevity, GBD Level 3 plus distal determinants`). Identifier may be a short code (`SBP`, `PM25`, `GDP`, `U5MR`).
