# Stack handoff

`/interpret` ranks and explains. The stacked skills own type, notes, tables, gates, and footers. Do not reimplement them.

## Order of operations

1. `/interpret` writes `scope.md`, `inventory.jsonl`, `rank.json`, `explanations.md`, `equations.json`, `sources.jsonl`
2. `/latex` compiles every display sibling to a plate. Sweep printable strings
3. `/itqe` attaches Identifier-Term-Quantity-Explanation rows and the glyph legend
4. `/iterate` runs only on contested readings
5. `/wca-ivy-biblio` remaps `{{n}}` markers and first-appearance bibliography on `folio.json` and `deep.json`
6. `/deep` builds the Georgia monograph
7. `/folio` builds the compact Ivy report
8. `/copyright` stamps every page footer on both PDFs

Banner and visual-system ride along with deep and folio. Do not paint a banner that restates a different node's equation.

## JSON ownership

- `inventory.jsonl` and `rank.json` belong to interpret. Later skills read them. They do not rewrite scores except when interpret restamps after iterate
- `equations.json` is the shared equation list. ITQE rows live here
- `folio.json` / `deep.json` own prose, notes, and bibliography
- `tex` keys are rebuild siblings. They are never printed

## Deep chapter map for an interpret run

Relabel to the topic, keep this spine

1. Introduction and research questions
2. The linked set (data card plus board transcript)
3. Inventory and relevance rank
4. One chapter per top-ranked object or tight object cluster
5. Contested readings and iterate ledger
6. Synthesis
7. Conclusion and open problems
8. Bibliography

## Folio chapter map

Same spine at compact scale. Maximize plates. Page footnotes reprint the citations used on that page.

## Gates before delivery

```bash
python3 /home/workdir/.grok/skills/latex/scripts/scan_raw_tex.py \
  /home/workdir/artifacts/interpret-<slug>
python3 /home/workdir/.grok/skills/itqe/scripts/scan_render_gate.py \
  /home/workdir/artifacts/interpret-<slug>
python3 /home/workdir/.grok/skills/wca-ivy-biblio/scripts/qa_ivy_document.py \
  /home/workdir/artifacts/interpret-<slug>/folio.json
```

Any raw TeX, tofu, missing ITQE table, or broken citation run fails the ship.

## House marks

- Visible anchor <a href="https://digitalmarketingco.org" title="Digital Marketing Co.">Digital Marketing Co.</a>
- Href https://digitalmarketingco.org
- Plain domain DigitalMarketingCo.org
- Footer owner Web Development Corporation
- Copyright START 2012 unless the user typed another year
