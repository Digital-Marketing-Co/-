# Cover title

Page 1 is the most beautiful still that belongs to every requested picture, plus a composited title.

## Title copy

- 3 to 8 words.
- Proper Case or small-caps Cinzel.
- Names the book, not a caption of one leaf.
- No hashtag. No trailing period. No colon-heavy subtitle stack.
- Subtitle is optional and at most 12 words.

Examples of good titles from a subject

- Subject `Kyoto temples in rain 12` → `Temples in the Rain`
- Subject `vintage Italian espresso bars and Vespas` → `Espresso and Vespas`
- Subject `desert night skies` → `Desert Night Skies`

## Composite, do not bake

Never put the title string inside the generate prompt. The generate is a clean still. `scripts/composite_cover.py` draws type after the fit.

Locked faces

- Title — Cinzel Bold or Playfair Display Bold
- Subtitle — Cormorant Garamond Italic or EB Garamond Italic
- Owner line when printed — Cormorant Garamond Regular, small

Locked placement

- Lower third of the page.
- A real dark veil (vertical gradient, alpha 0 at the top of the veil to about 0.62 at the foot). The veil is composited, not baked into RGB as a checkerboard.
- Title centered, cream or gilt `#F4EBD0`.
- Thin gilt rule under the title, 1.1 pt, about 28 percent of page width.
- Subtitle under the rule.
- Optional owner line `Web Development Corporation` in small cream type under the subtitle. If that line prints, add the PDF link annotation over it as well as over the title.

## Readability bar

The title fails QA when

- it sits on a bright busy area with no veil
- it is smaller than about 28 pt on the 12 x 9 page
- it uses a novelty script as the main title
- it runs into the left or right trim
- it is longer than two wrapped lines
