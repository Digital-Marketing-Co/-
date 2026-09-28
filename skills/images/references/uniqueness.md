# Uniqueness and full-bleed QA

Every published raster in a `/images` run must be a unique file and a unique picture. Full-bleed left and right is mandatory. Quality is not traded for either rule.

## Unique means two checks

1. **Byte unique.** MD5 (or SHA-256) of the published file is not shared with any other banner, mid-section figure, or raw source used in the same document.
2. **Source unique.** A mid-section figure may not be a copy, crop, fade, or resize of that document's section banner, and a banner may not reuse another section's raw generate. One generate call, one published figure.

Do not attach `raw-NN` of section A as `fig-B-k`. Do not point two `banner.path` fields at the same PNG. Do not regenerate the same prompt for two sections.

## Fail closed on reuse

Before rebuild run

```bash
python3 /home/workdir/.grok/skills/images/scripts/audit_unique_images.py \
  /home/workdir/artifacts/<slug>/atlas.json
```

(or `deep.json` / `folio.json`). Exit code 1 blocks delivery. Replace each colliding figure with a new generate locked to that section's named objects, then audit again.

## Full bleed, max sharp size, no quality loss

Maximize print size without losing quality and without introducing aliasing, blur, or aspect distortion.

- Page-width pixel floor on letter is 2550 px wide (prefer 3300 px / 300 dpi). Generate at or above that floor.
- Full bleed left and right (x = 0 to page width, zero left margin, zero right margin, zero left padding, zero right padding) is allowed only when the published bitmap already meets that floor.
- If the file is narrower than the floor, regenerate at the floor. Do not LANCZOS-upscale a small preview across the page. Do not bicubic-stretch. Do not nearest-neighbor enlarge.
- Height follows the source aspect ratio. Do not letterbox. Do not squash into the type measure. Do not change aspect to buy width.
- Resize only with LANCZOS, and only downward or to the locked banner geometry (8.5 in at 150 dpi) when the source is already at or above the floor.
- Reject a figure that looks soft, stair-stepped, ringing, or stretched when rastered at print size.
- Banners keep full opacity on every edge; do not fade. Do not fade left or right. Mid-section figures stay at full opacity and still edge-to-edge left and right when the floor is met.
- RGB must not contain a checkerboard. Transparency is real alpha, never a baked preview pattern.

## Final QA engineering pass

After rebuild, raster every page and reject when any of these hold

- two pages show the same picture
- a figure sits inside the text column with left or right gutter
- a banner or figure is soft, aliased, stretched, letterboxed, or checkerboarded
- a figure was upscaled from a narrower bitmap to force bleed
- a subsection reused the parent section figure
- a figure is reused across sections
- a figure does not match the surrounding section claims

Write `figures/qa-uniqueness.md` with the hash table and the pass or fail line.
