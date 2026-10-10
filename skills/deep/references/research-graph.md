# Recursive node research

## Graph

`nodes.jsonl` — one object per node.

```
{"id":"n000","parent":null,"label":"root topic","kind":"topic","queries":[],"keepers":[],"children":[],"status":"open"}
```

Kinds: topic, person, institution, statute, instrument, dataset, school, controversy, place, period.

## Recursion

1. Round-map the current node (survey + library guides + official chronologies).
2. Open primary and Ivy PDFs. Record exact titles, authors, years, page or section locators, stable URLs, access date YYYY-MM-DD.
3. Extract new child labels. Add only nodes that change an explanation of the root or of the parent.
4. Recurse. Use depth 4 and 80 keepers as review checkpoints; continue material branches in documented batches. Apply doctoral-protocol.md.
5. Close a node only when two consecutive targeted rounds add neither material evidence nor explanatory branches; log resource-limited nodes as open.

Write `rounds/round-N.md` and `graph.md` (Mermaid or outline of the node tree).

## Source tiers

Same rank as phd-ivy-monograph `research-protocol.md`:

1. Primary documents (statutes, hearings, archival objects, official statistics, patents, manuals).
2. Ivy League and peer university-press monographs and articles.
3. U.S. government and military (.gov, .mil).
4. Other peer-reviewed journals.
5. Learned-society reference works.
6. Journalism only to reach an underlying document.

Do not cite content-farm pages. Do not pad the bibliography with unread items.

## Honesty

Conflicts stay in the text. Thin literature is named as thin. Paywalled books may be cited from a catalog or preview; say so and do not invent page numbers.
