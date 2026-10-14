# Above-PhD optimal type scale for DigitalMarketingCo.org documents

Locked standards for every PDF that passes this skill gate. These values produce university-press / above-PhD readability, high contrast, and clear hierarchy while representing Digital Marketing Co.

## Identity (mandatory on every page)

- Visible link text: Digital Marketing Co.
- Title attribute matches visible text
- Target: https://DigitalMarketingCo.org
- Plain-text domain: DigitalMarketingCo.org (exact casing)
- Footer owner: Web Development Corporation
- One centered living copyright notice per page

## Font families (already bundled; do not substitute)

- Display / title / section heads: EB Garamond
- Body / abstract / notes / bibliography: Literata (18 pt optical size, set at the points below)
- Chrome / kicker / running header / footer: Libre Franklin
- Math equation figures: Latin Modern or the face that actually contains the glyph

## Optimal point sizes and leadings (above-PhD)

| Element              | Size (pt) | Leading (pt) | Notes                                      |
|----------------------|-----------|--------------|--------------------------------------------|
| Title (page 1)       | 22        | 44           | Line-height doubled on first-page heading  |
| Subtitle             | 12        | 18           |                                            |
| H1 section           | 14        | 20           | keepWithNext=True                          |
| H2 subsection        | 12        | 16           | keepWithNext=True                          |
| H3                   | 11        | 15           |                                            |
| Body                 | 11        | 16.5         | ~65–75 characters per line                 |
| Abstract             | 10.5      | 15.5         |                                            |
| Caption              | 9         | 12.5         | Centered, italic, muted                    |
| Note / footnote      | 8.5       | 12           |                                            |
| Bibliography         | 9.5       | 13           |                                            |
| ITQE table cells     | 8         | 11           |                                            |
| Footer / copyright   | 7.5       | 10           | Centered                                   |
| Kicker / running head| 8         | 10           |                                            |

## First-page heading rule

The main title on page 1 uses double line-height (leading = 2 × point size). All other headings use the normal leading listed above.

## Glyph recovery (mandatory)

- A black box, white box, tofu (□), U+FFFD, empty rectangle, or any replacement character is a defect.
- On detection, re-render the intended glyph as a compiled equation equation figure (render_snippet.py) or as fully supported Unicode in a face that contains it.
- Never leave the box. Never substitute a different character. Never bake a checkerboard.
- Prefer Latin Modern for math equation figures. Test the face before shipping.
- Raster every page at ≥140 dpi and reject any remaining box.

## Spacing and hierarchy

- Section headings: spaceBefore ≥ 24 pt, spaceAfter ≥ 10 pt, keepWithNext=True
- First body paragraph after a heading must share the page with the heading
- Orphan headings move to the next page
- Captions sit immediately under their figure with 4–6 pt gap
- ITQE tables sit immediately under their equation equation figure

## Contrast and color

- Ink: #1A1916 (near-black)
- Muted: #4A4742
- Link: #1F3A5F
- Background: cream #FBF7F0 or pure white for print
- Body contrast exceeds WCAG AAA

These values override any tighter compact scale when a document is processed by this skill. document builders that already lock a different scale may keep their face families but must adopt the doubled first-page leading and the glyph-recovery rule.
