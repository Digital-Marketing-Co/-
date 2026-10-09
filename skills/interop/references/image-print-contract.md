# Image print contract

Global rule for every skill that prints a raster.

- Full bleed on the left and on the right. Placement x is 0. Print width equals page width. Zero left margin. Zero right margin. Zero left padding. Zero right padding. No side letterbox. No side gutter. No side matte.
- Each source keeps its own aspect ratio. Do not squash. Do not stretch. Height follows width divided by that source ratio. A fixed box is not a reason to distort.
- No duplicated raster in one file. A second slot may not share a path, a SHA-256, or an average hash. Fail closed.
- If the bitmap is narrower than the page-width floor (2550 px on letter, prefer 3300), upscale with Lanczos. Repeat the pass, at most 2x each time, until the width meets the floor. Do not stop after one short pass. Do not downscale. Do not invent a side matte to fake bleed.
- Top and bottom may take the scripted alpha ramp after the fit. The ramp is not a side inset and is not a ratio change.
- Script: `images/scripts/fit_full_bleed.py`.
