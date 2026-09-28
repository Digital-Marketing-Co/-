---
name: ispy
description: Exhaustive I-Spy object inventory of an attached or referenced image. Trigger on /ispy, /I-Spy, ispy this, identify every object, window inventory, hidden-object catalog, or a request to name placement color and meaning of every object in a photo. Enhance or crop only when a label or figurine is unreadable at source resolution. Output a pane-by-pane catalog plus a fail-closed hidden-message section that does not assert a code unless a second plaintext reconstructs.
metadata:
  type: workflow
  version: "1.0"
  flag: /ispy
  owner: Web Development Corporation
---

# /ispy

Treat one attached or referenced raster as a closed visual corpus. Name every distinguishable object. Record pane or grid cell, relative placement inside the cell, dominant color, material guess, and readable text. Then test whether the arrangement could encode a second message. Do not invent objects the pixels do not support. Do not claim a hidden code unless a concrete reconstruction exists.

Work in `/home/workdir/artifacts/ispy-<slug>/`.

`<skill>` = `/home/workdir/.grok/skills/ispy`

Read on demand

- `references/inventory-schema.md` — required fields per object
- `references/hypotheses.md` — H0 vs H1 rules for meaning and codes
- `scripts/crop_grid.py` — optional pane crops from a labeled window or grid

## When this runs

- User typed `/ispy` or `ispy this`
- User asked to identify every object, figurine, vase, sign, or detail in a photo
- User asked what a crowded window, shrine, shelf, or still-life could mean if it were a hidden message
- User stacked `/ispy` with `/upscale`, `/decode`, `/Q`, `/folio`, or `/deep`

If no image is present, stop and ask for one. Do not invent a scene.

## Workflow

### 1. Lock the source

Copy the original file into the work directory as `source` plus its real extension. Record width, height, colorspace, and file size. Do not overwrite the attachment.

### 2. Decide whether enhancement is needed

Read the full frame first with `read_file` or `view_image`.

Enhance or crop only when a specific failure is present

- text on a sign or plaque is smaller than about 12 source pixels
- two adjacent figurines merge at display resolution
- glare, screen, or glass reflection hides a face or label

Allowed steps, in order

1. Crop the display region (window sash, shelf, table) so the catalog is not diluted by siding, roof, or shrubs.
2. Split a regular grid (3x3 window, bookcase bays, etc.) with `scripts/crop_grid.py` or ImageMagick.
3. Lanczos-upscale a crop at 1.5x or 2x only when the crop is under 1200 px on the long edge and a label is still unread. Cap destination at 80 MP and 12000 px. Prefer the `/upscale` skill when the whole frame must grow.
4. Never bake a checkerboard into RGB. Never claim new detail that interpolation invented.

Do not run a generative inpaint or an image-edit that adds objects.

### 3. Build the spatial frame

Name the container before the objects.

- building or room context (siding color, house number, roof edge, plants)
- the display itself (window of N columns by M rows, glass, muntins)
- reading order — left to right, top to bottom, pane A1..C3 or equivalent
- any readable exterior text (address plaque, yard sign)

House numbers, street context, and neighbor identity are scene facts. Do not turn a nearby address into a biography of the occupant.

### 4. Inventory every object

Walk the grid in reading order. For each distinguishable item write one record that matches `references/inventory-schema.md`.

Minimum fields

- `id` — stable slug (`B2-cowboy-hat`)
- `pane` — grid cell
- `placement` — left / center / right and front / mid / back inside the pane
- `name` — common English name
- `category` — figurine, vessel, textile, text-plaque, animal, religious, patriotic, plant, fixture, unknown
- `colors` — two to four dominant colors in ordinary words
- `material_guess` — glass, glazed ceramic, painted plaster, metal, paper, fabric, unknown
- `size_rel` — tiny / small / medium / large relative to the pane
- `readable_text` — exact letters if any, else empty
- `confidence` — high / medium / low
- `notes` — pose, facing direction, grouped companions, glare caveats

Count multiples. A row of six identical choir figures is six objects plus one group note. Reflections in the glass are not extra objects unless a second physical item is visible.

If an item cannot be named, keep it as `unknown-<pane>-<n>` and describe shape, color, and pose. Low confidence is allowed. Fabricated brand names are not.

### 5. Group and tally

After the flat list, emit

- count by category
- count by color family
- readable text corpus (every lettered object, in reading order)
- repeated motifs (pairs of amber discs, paired purple vases, angel clusters, hats, flags)
- empty or near-empty cells

### 6. Meaning section — two hypotheses

Follow `references/hypotheses.md`.

H0 — ordinary display. Collector window, religious home shrine, seasonal tableau, yard-sale glass, or I-Spy decoration for passers-by.

H1 — intentional second message. Acrostic of labels, mapped grid cipher, heraldic color code, or planted arrangement that reconstructs a second plaintext.

Write both. Accept H1 only when at least two independent observations reconstruct the same second text that is not a restatement of the surface scene (for example a sign that already says GOD DID IT). Color rhyme, religious density, and a house number are not a cipher.

Always include a short list of plausible ordinary readings

- folk-religious window shrine
- glass-and-figurine collection shown to the street
- patriotic or commemorative corner
- playful I-Spy for neighborhood walkers

Do not diagnose the occupant. Do not claim military, assassination, or intelligence meaning from figurines alone.

### 7. Optional stacks

- `/upscale` — only when a crop is still unread
- `/decode` — only on the extracted readable-text corpus, never on imagined labels
- `/Q` — only on integers actually printed in the frame (address, dates on plaques)
- `/folio` or `/deep` — only when the user asked for a monograph PDF of the inventory

Default chat deliverable is the catalog plus the H0/H1 section. Do not build a PDF unless asked.

### 8. Chat mathematics

If a count, ratio, or grid index is written as a formula, render it with KaTeX and name every symbol once. Example — pane index \(p = 3(r-1)+c\) for row \(r\) and column \(c\) in a 3-column sash.

## Anti-patterns

- Do not list the shrubs and siding as display objects unless the user asked for the whole photograph.
- Do not treat JPEG artifacts, muntin bars, or window locks as figurines.
- Do not use a generative edit to "clarify" a face.
- Do not assert a hidden political or religious code from motif density.
- Do not paste copyrighted product manuals. Name the object class instead.


## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write figure, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.
