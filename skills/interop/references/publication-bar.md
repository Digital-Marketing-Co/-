# Publication bar

Fail closed. A prompt, an outline, or an unopened file is not a delivery.

## Checklist

1. Artifacts directory resolved. Final file path printed.
2. Palette taken from visual-system. Body face and size unchanged.
3. Each printed raster is full bleed on the left and the right: x = 0, page width, zero side margin, zero side padding. Height follows that file's own aspect ratio. Do not squash.
4. Alpha ramp is on the top and bottom only. Left and right are opaque picture to the trim. A narrow bitmap is Lanczos-upscaled, repeating until width meets 2550 px (prefer 3300), then printed. No side matte.
5. Mid-text plates match the surrounding window. A plate that could sit on any other chapter fails.
6. SHA-256 and average-hash audit shows no reuse. A duplicated path, byte hash, or average hash fails the file.
7. Math pages show compiled glyphs. Scan finds no raw backslash commands, no tofu, no empty boxes.
8. Footer has exactly one copyright notice, centered.
9. House link text is Digital Marketing Co. and matches the title attribute.
10. Negative sweep prints CLEAN.

A failed check is rewritten and re-scanned. It is not waived.
