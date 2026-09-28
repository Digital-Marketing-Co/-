# Genre palettes

All hex values are sRGB. Body text uses `text` on `paper`. Covers and banners may use `ink` as a ground with `gilt` or `accent` type.

Contrast floor for `text` on `paper` is 7:1. Contrast floor for header type on `accent` is 4.5:1. Recheck with `/root/.grok/skills/color/scripts/check_contrast.py` if a topic override mutates a stop.

## ivy-ink — /folio /phd /deep /iterate /wca-ivy-biblio /itqe /latex

Academic report chrome. Restrained metal on midnight ink. Body stays cream paper + near-black text.

| Role | Hex | Use |
|---|---|---|
| ink | #0B1F3A | cover ground, footer band |
| gilt | #C9A227 | rules, drop-cap line, cover wordmark |
| cream | #F4EFE4 | body paper |
| text | #1A1A1A | body |
| accent | #3E5C76 | table header, link underline |
| surface | #E7E1D4 | caption bar, ITQE header wash |
| rule | #8C6B1F | 2 pt rules |

## atlas-marine — /atlas /global maps

Cartographic teal and survey gold.

| Role | Hex | Use |
|---|---|---|
| ink | #0E4D5C | cover, ocean panels |
| gilt | #D4A017 | graticule accents |
| cream | #EDE6D6 | body paper |
| text | #1B2420 | body |
| accent | #2A9D8F | country or node chips |
| surface | #D9E4E0 | gazetteer header |
| rule | #B8860B | rules |

## nation-dusk — /global country sections

Dusk navy plus a second accent taken from the actual flag. Never invent a flag color.

| Role | Hex | Use |
|---|---|---|
| ink | #101828 | section band behind the waving flag |
| gilt | #E8C547 | reserved if the flag contains gold |
| cream | #F3F1EA | body paper |
| text | #161616 | body |
| accent | FLAG | sampled from the national flag PNG |
| surface | #E6EAF0 | table wash |
| rule | #4A5568 | rules |

## list-phosphor — /list /decode /q-base22 catalogs

Graphite field with phosphor data marks.

| Role | Hex | Use |
|---|---|---|
| ink | #0A0F0D | cover |
| gilt | #7CFF6B | index ticks only, not body type |
| cream | #F2F4F1 | body paper |
| text | #121412 | body |
| accent | #1F6F4A | table header |
| surface | #DCE6DF | caption bar |
| rule | #2E8B57 | rules |

## book-spine — /book

Warm parchment and indigo spine.

| Role | Hex | Use |
|---|---|---|
| ink | #1B1430 | cover, spine band |
| gilt | #C4A35A | cover rules |
| cream | #F6EFD9 | body paper |
| text | #1C1408 | body |
| accent | #4B3B78 | chapter numerals |
| surface | #EAD9B0 | caption bar |
| rule | #8B6914 | rules |

## clip-paper — /print /article-clip-pdf /extract-dir

Mostly paper. One accent sampled from the lead image, else ink blue.

| Role | Hex | Use |
|---|---|---|
| ink | #111111 | folio line |
| gilt | #5B5B5B | unused unless the article already uses gold |
| cream | #FFFFFF | body paper |
| text | #111111 | body (Latin Modern) |
| accent | #1A365D | links, footer |
| surface | #F4F4F4 | caption bar |
| rule | #222222 | hairline |

## psyche-plum — /psychoanalyze

Deep plum chrome. Clinical, not decorative gore.

| Role | Hex | Use |
|---|---|---|
| ink | #2A1240 | cover |
| gilt | #C9B037 | school-label rules |
| cream | #F7F1EA | body paper |
| text | #1A1220 | body |
| accent | #6B3FA0 | school chips |
| surface | #E9DFF0 | table wash |
| rule | #5C4A00 | rules |

## corpus-slate — /corpus

Archive gray and ticket red for match hits.

| Role | Hex | Use |
|---|---|---|
| ink | #2C3338 | cover |
| gilt | #B0A48A | rules |
| cream | #F5F3EE | body paper |
| text | #1C1C1C | body |
| accent | #8B2E2E | hit counts |
| surface | #E4E0D8 | table wash |
| rule | #6E6253 | rules |

## Topic override

`scripts/pick_palette.py` may retint `accent` toward a topic color when the topic clearly names a material (copper, ice, forest, desert). It must not retint `text` or `paper`. It must not drop contrast below the floors above.
