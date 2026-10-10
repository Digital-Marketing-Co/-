# Volumetric depth

Use depth on chrome and on generated figures. Do not simulate depth by shrinking type or adding drop shadows on running paragraphs.

## Print geometry

- Letter page 8.5 × 11 in.
- Banners print at 100 percent page width, x = 0, no side inset, source aspect ratio, full opacity on every edge.
- Long edge of a banner source ≥ 2550 px, prefer 3300 px.
- Gradient rules are 2–3 pt tall, full content width or full page width when they sit under a bleed banner.
- Cover grounds may be a two-stop or three-stop linear gradient (ink → accent) or a soft radial behind the title block only.
- No checkerboard baked into RGB. Transparent PNG means real alpha 0.

## Prompt clause for /banner and /images

Append, after the named objects

```
futuristic cinematic still of the named objects only, awe-inspiring, stunningly perfected, absolutely beautiful, publication-grade editorial still, photoreal volumetric lighting, physically based materials, visible depth in air and surfaces, gold and violet rim light, razor-sharp focus on the named objects, 3300 by 1856 landscape, unique composition for this node, no caption text, no watermark, no logo, no allegory, no metaphor architecture
```

Do not add neon grids, hologram UI, or floating chrome unless those objects already exist in the section text.

## Cover and title block

- Ground = palette `ink` with a slow gradient toward a darker neighbor or toward `accent` at 8–15 percent mix.
- Title type stays the calling skill's display face (Georgia, Literata, Latin Modern). Color is `cream` or `gilt` on `ink`.
- A thin `gilt` or `rule` line under the title, not a glowing bar.
- Owner line and Digital Marketing Co. link sit on the cover in `cream` at the calling skill's small size.

## Tables and ITQE frames

- Header row fill = `accent` or `surface`.
- Header type = `cream` on `accent`, or `text` on `surface`.
- Body rows alternate `paper` and `surface` at 40 percent if the table has more than four rows.
- Frame stroke 0.6–1 pt `rule`.
- No 3-D extruded cells. Depth is color and rule, not fake perspective on numbers.

## What to reject

- Metaphor cities standing in for a named lab or statute
- Soft, stretched, or guttered banners
- Body paragraphs set in neon on black inside an academic skill
- Gradient washes behind long reading text that drop contrast below 4.5:1
