# Print layout contract

Letter 8.5 x 11 in. Cream ground. Text lives in the inset. Images do not.

## Bleed

- Page frame is full-bleed (x = 0, width = page). Text styles carry the inset.
- Figure images draw at x = 0 and width = page. They bleed left and right. They never split across a page break. Caption stays in the inset and is KeepTogether with the plate.
- Banner / overlay / hero plates also bleed left and right. When the plate is the first flowable on a page it also bleeds the top trim. A banner that lands at the foot of a page is moved to the next page so it is not sliced.
- Do not letterbox a banner inside the text column.

## Headings must not orphan

- Every heading is packed with its first following block (paragraph, list, quote, or figure) inside KeepTogether.
- Before a heading the builder issues a conditional page break equal to heading height plus one body line plus a small gutter. If that much room is not left, the heading starts the next page.
- A heading with no following text is still not allowed to sit in the last 1.4 in of a page. Move it.
- Do not leave a heading as the last visible item on a page.

## Body splits

- Paragraphs may break across pages after at least two lines have printed.
- Lists, captions, and the copyright colophon stay together.
- Never split an image. Never split a heading from its first following block.

## Image quality (the upscale move)

Target width is letter width at 300 px/in (2550 px).

- If the source is narrower, `prepare_image.py` upscales with LANCZOS and a light UnsharpMask. That is the locked quality move. It recovers edge contrast after upsample. It does not invent faces or type.
- If the source is already at or above target, keep native pixels and only downsample with LANCZOS when the file is enormous.
- Never use nearest-neighbor or bilinear stretch.

## Chrome

Footer on every page after the first plate — short owner left, page number right, copyright field plus house placeholder link on the last page colophon.
