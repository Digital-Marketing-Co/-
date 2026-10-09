# /bleed layout contract

Letter width is 8.5 in. Page height follows the snippet ratio. There is no text inset on a snippet page.

## Bleed

- Every snippet, banner, and in-content image is a page image.
- The media box equals the image: x = 0, y = 0, width = page width, height = page height.
- Top, right, bottom, and left margin are 0. No matte. No letterbox. No crop.
- Do not stretch a bitmap off its own ratio. Height follows width divided by the source ratio.
- Do not fade the edges. The snippet must match the painted page.

## Do not cut an image

- A figure, banner, picture, or svg is one plate. Never slice it across two pages.
- If a section is taller than one comfortable plate, split only between whole blocks.
- A split is illegal inside an image, a figure, or a paragraph that contains an image.

## Headings stay with the next paragraph

- A section or subsection heading is packed with its first following paragraph or figure.
- Do not start a new page immediately after a heading.
- Do not end a page on a heading. That leaves the paragraph awkwardly on the next page.
- If the pair does not fit in the current plate, move both.

## Chrome

- Strip site header, navigation, sidebar, floating button, and footer before capture.
- Do not draw a PDF header, page number, or footer.
- Capture the painted background under the remaining content. The plate is that paint, not a reflow.
