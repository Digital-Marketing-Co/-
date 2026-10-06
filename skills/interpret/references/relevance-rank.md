# Relevance rank

Score is local to this linked set. Do not reuse a score from another interpret run.

## Components

Each equation object receives four components in `[0, 1]`. Write them on the object before the weighted sum.

1. `data_fit` — how directly the object names or transforms a column or series that exists in the linked set. A time derivative of real GDP against a real-GDP quarterly series is high. A golden-ratio constant with no series is low.
2. `structural_load` — how much of the board's claimed mechanism sits on this object. A rate that the arrows point at is high. A sequencing arrow is low.
3. `identifiability` — whether the object can be estimated, tested, or falsified with the data that is actually present. An inequality against zero on a growth rate is identifiable. An unlabeled pictogram is not.
4. `source_warrant` — whether a primary methodology or identity licenses this reading (SNA 2008, BEA NIPA handbook, a named paper). Doodles score zero here until a source attaches.

## Weight

```
score = 0.40 * data_fit
      + 0.25 * structural_load
      + 0.20 * identifiability
      + 0.15 * source_warrant
```

Keep the weights locked unless the user names a different mandate (for example, source-first). Record the weight vector in `rank.json`.

## Sort

Descending `score`. Ties break on visual `id` ascending so the ledger is stable.

## What does not get a high score by default

- Decorative arrows that only say "next"
- Unlabeled pictograms (mushroom, tree, star) until a legend or the data names them
- Constants that never enter the series (φ as golden ratio on a GDP board with no Fibonacci claim)
- House labels (ITQE, GLOBAL as a caption) unless they are themselves the object of study
- Struck-through glyphs, except as evidence of a rejected identity, in which case they rank as annotations

## What does

- The left-hand or right-hand side of the board's main inequality or implication
- Any transform the data already carries (REAL, log, YoY, SA)
- Operators that change dimension (∂/∂t on a stock)
- Thresholds the data can cross (≫ 0, ≫ φ when φ is defined)

## Restamp

After an iterate round that adds a series or kills a reading, recompute components and rewrite `rank.json`. Explanation order follows the new file. Inventory `id` values stay frozen.
