# Country section contract

Every ranked country is one body section. Rank number is the section order. ISO 3166-1 alpha-2 is the file key.

## Opening block (required)

1. Waving flag at readable print size. Path `flags/flag-<iso2>.png`. Caption is the English short name plus "civil flag."
2. Full-bleed scenic banner. Path `banners/banner-<iso2>.png`. Caption names a real place in that country and the license or generate note.
3. Rank line — rank, English short name, official short name if different, ISO2, ranking value, unit, year.
4. Source line — publisher, table or series name, retrieval date.
5. Coverage line — what the national total includes and excludes.

## Body

Write intelligence, not a travel blurb.

- What the ranking value means for this topic in this country
- Every material subcategory with the latest period value in the report unit (USD when money)
- Last 12 periods at the natural grain when the series exists
- Drivers, breaks, and definition changes
- Peer comparison to the two countries immediately above and below in rank
- Known gaps, revisions, and dual-counting risks

Do not pad with encyclopedia geography unless the geography changes the statistic.

## Flag rules

- Current civil flag. No historic flags unless the topic is historic flags.
- Cloth waving. Readable canton, stars, emblems, and stripes.
- No extra seals, no fake coats of arms, no text watermarks.
- Transparent background preferred. If opaque, use a clean sky that is not a baked checkerboard.
- Disputed polities — one flag, one footnote.

## Banner rules

- Named real place in that country. Not a globe, not a collage of many countries, not an allegory.
- Prefer a searched high-resolution photograph with a usable license. Generate only when no photograph meets the page-width pixel floor.
- Full bleed left and right. Bleed the top of the banner box. Zero side margin and padding.
- Full opacity. No fade on any edge.
- Unique bytes and unique path per country.
- Long edge at least 2550 px before print downsize. LANCZOS only. Keep source aspect.

## Chart rules

- Electric blue, semi-transparent fills, thin strokes, named units
- File `charts/chart-<iso2>.png`
- Category companion `charts/chart-<iso2>-categories.png` when classes exist
- Source and period printed under the chart, not burned into the plot area

## Subsection banners

If a country section has printed subsections (for example one subsection per discovered class), each subsection gets its own `/banner` image. The country scenic banner does not stand in for a child heading.
