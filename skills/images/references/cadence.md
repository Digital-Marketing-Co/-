# Cadence — 500-word mid-section figures

## Blurb

The opening blurb is the first one or two body paragraphs after the section heading and after the banner figure. Those paragraphs introduce the section. They do not receive a mid-section figure of their own. The banner already covers them.

## Counting

Count words in the remaining body paragraphs of that section or subsection only. A subsection is its own counting window.

- Include ordinary paragraphs and list items.
- Exclude the heading, the banner caption, footnotes printed on the page, running headers, and the living copyright line.
- Exclude `type=equation` figures and ITQE tables from the 500-word tally (they already occupy visual space).
- Strip HTML/JSON tags before counting.

Slot count

```
slots = floor(words_after_blurb / 500)
```

If `slots == 0` and `words_after_blurb >= 350`, grant one figure so a short-but-real chapter is not bare under the banner.

If `words_after_blurb < 350`, banner only.

## Placement

For slot k in 1..slots, walk the remaining paragraphs in order until the cumulative word count first meets or exceeds `k * 500`. Insert the figure after that paragraph.

Never insert inside Notes or Bibliography. Never insert between a display equation and its ITQE table. Never insert on the title leaf.

The inserted figure is a full-bleed figure, not a column inset, when the source already meets the 2550 px page-width floor. Width equals the page only in that case. Aspect is unchanged. Never stretch a narrower file to invent bleed. Caption sits under the figure inside the type measure.

## Captions

One sentence. Drawn from the window, not from another chapter. No URL text on the image. The caption lives under the figure in the PDF, not burned into pixels.
