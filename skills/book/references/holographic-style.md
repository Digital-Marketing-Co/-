# Locked plate size and holographic style

Every banner and every mid-chapter plate in a `/book` run uses one canvas and one look.

## Canvas

- Width 3300 px
- Height 1856 px
- Aspect 16:9
- Color RGBA
- Left and right columns opaque
- Top and bottom receive a real alpha ramp after generate
- Print at 100 percent page width, x = 0, zero side gutter

If a generate returns a different pixel size, LANCZOS-resample onto this exact canvas before the alpha ramp. Do not letterbox. Do not change aspect. Do not ship a second size in the same book.

## Style lock

Append this clause to every generate prompt after the named objects of that 500-word window:

```
futuristic cinematic still of the named objects, absolutely beautiful, stunning editorial stock-photo quality, photoreal volumetric lighting, physically based materials, gold and violet rim light, shallow depth of field, razor-sharp focus on the named objects, same lighting family, no caption text, no watermark, no logo, no allegory
```

Do not write figure, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into the prompt.

## Cadence

After the section banner and after the opening blurb (first one or two paragraphs), insert one new plate for each full 500 words of remaining body text in that chapter.

```
slots = floor(words_after_blurb / 500)
```

If a chapter would have zero slots, expand the chapter from source claims until `words_after_blurb >= 500`, then generate the plate. Do not skip the cadence by leaving a chapter thin. Notes and Bibliography never receive plates.

Each plate is locked to the objects named in that 500-word window. A banner and a mid-chapter plate in the same chapter still use different prompts and different bytes.
