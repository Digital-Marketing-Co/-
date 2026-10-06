# Coffee-table geometry

Locked default is landscape coffee-table.

| Mode | Page (in) | Source (px at 300 dpi) | PDF points |
| --- | --- | --- | --- |
| landscape (default) | 12 wide x 9 tall | 3600 x 2700 | 864 x 648 |
| square (user said square) | 11 x 11 | 3300 x 3300 | 792 x 792 |
| portrait (user said portrait) | 9 wide x 12 tall | 2700 x 3600 | 648 x 864 |

## Bleed

- Image origin is (0, 0).
- Image width equals page width.
- Image height equals page height.
- No left, right, top, or bottom margin.
- No crop-box inset.
- No printer marks.
- No letterbox and no pillarbox.
- No top-bottom alpha ramp. Every edge is opaque.

## Fit rule

Cover-crop the generate to the page aspect. Scale with LANCZOS so the shorter overflow axis is trimmed equally. Then apply a light UnsharpMask (radius 1.2, percent 80, threshold 3) only after an upsample.

If the generate is already larger than the target on both axes, downsample with LANCZOS. Never use nearest-neighbor or bilinear.

## Reject

- Any visible paper band
- A generate that was padded instead of cropped
- A still whose long edge is under 2550 px
- Mixed page sizes in one book
