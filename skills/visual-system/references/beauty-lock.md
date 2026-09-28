# Beauty and uniqueness lock (book / banner / images)

Every published banner and every mid-text still is a fresh house generate. Never search-stock a photograph and drop it into a slot. Never reuse a path, a byte hash, a crop, a fade, a recolor, or a near-duplicate perceptual hash.

Read `prompt-engineering.md` before writing any generate prompt.

## Quality bar

Each generate must read as an awe-inspiring, publication-grade still — editorial stock-photo sharpness, cinematic color, physically based materials, visible air and depth, futuristic without costume sci-fi. Reject soft, muddy, toy-like, collage, clip-art, or generic-lab output. Regenerate up to three times. A fourth failure blocks the slot.

## Style clause (append after named objects)

```
futuristic cinematic still of the named objects only, awe-inspiring, stunningly perfected, absolutely beautiful, publication-grade editorial still, photoreal volumetric lighting, physically based materials, visible depth in air and surfaces, gold and violet rim light, shallow depth of field, razor-sharp focus on the named objects, 3300 by 1856 landscape, same lighting family across this document but a unique composition per node, no caption text, no watermark, no logo, no allegory, no metaphor architecture
```

Do not write figure, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into the generate prompt. The still is produced with the house generate tool; the prompt describes the scene, not the tool.

Neon grids, hologram UI, and floating chrome appear only when those objects already exist in the section or window text.

## Context lock

- Banner — named objects and setting from that section or subsection title plus its opening claims only. A parent banner never covers a child heading.
- Mid-text still — named objects from the surrounding 500-word window only. Cover the caption. If the picture could sit on any other chapter, it fails.

## Uniqueness

One generate call, one published path. Audit SHA-256 and average-hash before delivery. A colliding still is replaced, not cropped. Two prompts in one document must differ on at least three axes in `prompt-engineering.md`.
