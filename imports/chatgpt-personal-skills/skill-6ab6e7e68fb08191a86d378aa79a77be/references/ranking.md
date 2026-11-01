# Ranking rule for /global

Pick one primary sort key per run. Print countries in descending order of that key. Never keep a leftover sort key from an older topic.

## How to choose the variable

Ask, in order

1. Did the user name a sort key? Use it.
2. Is there a latest-year national aggregate in money? Use that aggregate in USD.
3. Is there a latest-year national aggregate in physical units or counts? Use that.
4. Is there a published official index or composite? Use that.
5. Is there a documented rate (per capita, per TWh, per 100,000)? Use that only when an aggregate would mislead.

Write the choice in the run folder as `ranking.md` with

- variable name
- unit
- year or period
- FX date if money
- why two rival variables lost
- treatment of ties
- treatment of year-mismatched countries (rank on the latest common year; footnote newer vintages)

## Money

Convert every national-currency total to USD. Record

- original amount and ISO currency
- USD amount
- FX source and date
- whether the source already published a USD series

Do not mix nominal and real series in the same league table without a label. Prefer the series the primary source treats as the headline total.

## Categories

Discover classes from the sources for this topic. Keep every class that is material to `{{input}}`. Sum-to-total checks

- if published classes are a partition of the ranking total, print them as a partition
- if they overlap, say so and do not add them into the ranking total
- if a class exists in some countries and not others, print it where it exists and mark it absent elsewhere

Do not force a three-class schema.

## Coverage and order

Default universe is UN member states plus other widely recognized states. Dependencies, constituent countries, and special administrative regions go in the appendix unless the user asked to rank them with sovereigns.

Order

1. Countries with a comparable ranking value, descending
2. Tied countries, alphabetical by English short name
3. Countries in the universe with no usable value, in `insufficient-data.md`, not in the ranked table

A country with only a modeled estimate may enter the ranked table if the source is named and the cell is labeled estimate. Ungrounded guesses do not enter the table.
