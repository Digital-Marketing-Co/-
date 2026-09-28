# Research protocol for /global

## Source tiers (prefer in this order)

1. National statistical office, central bank, sector regulator, customs, or line ministry PDF tables
2. UN family and specialized agencies, IMF, World Bank, OECD, Eurostat, regional development banks
3. University-press and Ivy / peer-reviewed series that reprint official microdata
4. Reputable industry yearbooks that cite the official series they remix
5. Secondary news only for breaks, revisions, and dated events — never as the sole national total

Record every keeper in `sources.jsonl` with publisher, title, date, URL, page or table id, and what cell it supports.

## Units and FX

- Lock one report unit in `scope.md`.
- Money becomes USD. Keep the source currency next to the USD cell.
- Date the FX series. Do not silently mix year-average and end-of-period rates in one table.
- Physical units stay physical. Do not dollarize tonnes unless the user topic is value.

## Rounds

Round 1 — lock topic, ranking variable, category list, country universe.
Round 2 — fill league-table cells from tier-1 and tier-2 sources.
Round 3 — fill 12-period series and category splits for the top of the table and any country the user named.
Later rounds — remaining countries, revision notes, dual-recognition cases.

Close a country after two consecutive targeted rounds that add no new cell. Write the miss in `insufficient-data.md`.

## Integrity

- Do not invent a national total.
- Do not allocate a bloc total by population or GDP unless the source publishes that allocation.
- Do not treat a city figure as a national figure.
- Label provisional, estimated, and modeled cells.
- When two official series disagree, print both and rank on the series named in `ranking.md`.
- Taiwan, Kosovo, Palestine, and similar recognition cases follow the user's named universe; default is a footnote plus appendix rather than a silent drop.

## Stop gate

The ranked table may print before every UN member has a cell. It may not print a number that no source supports. Two empty rounds on a country is a miss, not a zero.
