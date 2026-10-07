# Uniqueness and full-bleed QA

Every published raster in a `/images` or `/banner` run must be a unique file and a unique picture. Full-bleed left and right is mandatory. Quality is not traded for either rule.

## Unique means three checks

1. **Byte unique.** SHA-256 of the published file is not shared with any other banner, mid-section still, raw source, or compiled `/latex` snippet used as decoration in the same document.
2. **Source unique.** A mid-section still may not be a copy, crop, fade, recolor, or resize of that document's section banner, and a banner may not reuse another section's raw generate. One generate call, one published figure.
3. **Perceptually unique.** Average-hash Hamming distance of published RGB (ignoring alpha) must be greater than 10 against every other published still in the document. Near-duplicates fail even when bytes differ.

Do not attach `raw-NN` of section A as `fig-B-k`. Do not point two `banner.path` fields at the same PNG. Do not regenerate the same prompt for two sections. Two prompts must differ on at least three axes in `visual-system/references/prompt-engineering.md`.

## Fail closed on reuse

Before rebuild run

```bash
python3 /home/workdir/.grok/skills/images/scripts/audit_unique_images.py \
  /home/workdir/artifacts/<slug>/folio.json
```

(or `deep.json` / `atlas.json` / `book.json`). Exit code 1 blocks delivery. Replace each colliding still with a new generate locked to that node's named objects, then audit again.

## Full bleed, max sharp size, no quality loss

Maximize print size without losing quality and without introducing aliasing, blur, or aspect distortion.

- Page-width pixel floor on letter is 2550 px wide (prefer 3300 px / 300 dpi). Generate at or above that floor.
- Full bleed left and right (x = 0 to page width, zero left margin, zero right margin, zero left padding, zero right padding) is allowed only when the published bitmap already meets that floor.
- If the file is narrower than the floor, regenerate at the floor. Do not LANCZOS-upscale a small preview across the page.
- Height follows 16-9 for banners. Do not letterbox. Do not squash into the type measure.
- Reject a still that looks soft, stair-stepped, ringing, or stretched when rastered at print size.
- After generate, run `apply_tb_alpha_blend.py`. Left and right stay opaque. Top and bottom receive a real alpha ramp. RGB must not contain a checkerboard.

## Final QA engineering pass

After rebuild, raster every page and reject when any of these hold

- two pages show the same picture or a near-duplicate composition
- a still sits inside the text column with left or right gutter
- a banner or still is soft, aliased, stretched, letterboxed, or checkerboarded
- a still was upscaled from a narrower bitmap to force bleed
- a subsection reused the parent section still
- a still does not match the surrounding section claims
- a `/latex` equation plate was copied into a banner slot

Write `figures/qa-uniqueness.md` with the hash table and the pass or fail line.
