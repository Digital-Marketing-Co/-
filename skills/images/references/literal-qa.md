# Literal figure QA

Mid-section figures follow the same anti-metaphor contract as `/banner` `references/literal-figures.md`.

## Resolution

Mid-section figures print at 100 percent page width (x = 0 to page width) with zero left or right margin or padding. Height follows the generated aspect ratio. Generate at least 2550 px on the long edge, prefer 3300 px. Do not generate a small sketch and stretch it. Do not letterbox or inset to the text column.

## Caption

`Figure N. Literal reconstruction of [named object or process] after [Chicago short title]. Generated model, not a scan of the source.{{n}}`

Add the source to `notes` and `bibliography` if it is not already a first-appearance work.

## Inspect

Open every mid-section PNG before attach.

Reject when

- the figure is a metaphor for the window instead of the window's objects
- letters or digits in the pixels are wrong, mirrored, or tofu
- a constant, percentage, or atom count appears that the 500-word window does not state
- pairing, stereochemistry, or device geometry contradicts the cited source
- a private face is rendered as a photograph
- the file is a byte copy, crop, fade, or resize of another figure in the same document
- the file would print with a left or right gutter or was upscaled from a narrower bitmap

Regenerate up to three times. If labels will not render cleanly, ship an unlabeled structure and keep the names in the caption only.

Write `figures/qa-{section}-{k}.md` with pass or fail reason.
