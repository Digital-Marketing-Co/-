---
name: ispy
description: Exhaustive I-Spy object inventory of an attached or referenced image, then one stacked book-iterate-deep PDF with per-element breakdown, corpus decode, 16-9 full-bleed banners and figures, WCA Ivy notes, and a living copyright footer. Trigger on /ispy, /I-Spy, ispy this, identify every object, window inventory, hidden-object catalog, or a request to name placement color and meaning of every object in a photo.
metadata:
  type: workflow
  version: "1.1"
  flag: /ispy
  owner: Web Development Corporation
  stacks: book, iterate, deep, breakdown, decode, banner, images, wca-ivy-biblio, copyright
  visual_stack: visual-system
---

# /ispy

Treat one attached or referenced raster as a closed visual corpus. Name every distinguishable object. Record pane or grid cell, relative placement inside the cell, dominant color, material guess, and readable text. Then test whether the arrangement could encode a second message. After the catalog exists, compile one letter-size PDF by running the stack in `references/pdf-stack.md`. Do not invent objects the pixels do not support. Do not claim a hidden code unless a concrete reconstruction exists.

Work in `/home/workdir/artifacts/ispy-<slug>/`.

Skill root is `/home/workdir/.grok/skills/ispy`.

Read on demand

- `references/inventory-schema.md` — required fields per object
- `references/hypotheses.md` — H0 vs H1 rules for meaning and codes
- `references/pdf-stack.md` — book, iterate, deep, breakdown, decode, banner, images, ivy, copyright
- `references/negative-vocabulary.md` — banned generate tokens
- `scripts/crop_grid.py` — optional pane crops from a labeled window or grid

If the user only asked to edit this skill and supplied no image, stop after the skill files exist. Do not invent a scene or a book.

## When this runs

- User typed `/ispy` or `ispy this`
- User asked to identify every object, figurine, vase, sign, or detail in a photo
- User asked what a crowded window, shrine, shelf, or still-life could mean if it were a hidden message
- User stacked `/ispy` with `/upscale`, `/decode`, `/Q`, `/book`, `/iterate`, `/folio`, or `/deep`

If no image is present and this is not a skill-edit turn, stop and ask for one.

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
2. Split a regular grid with `scripts/crop_grid.py` or ImageMagick.
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

Walk the grid in reading order. For each distinguishable item write one record that matches `references/inventory-schema.md`. Save `inventory.json`.

Minimum fields — id, pane, placement, name, category, colors, material_guess, size_rel, readable_text, confidence, notes.

Count multiples. Reflections in the glass are not extra objects unless a second physical item is visible. If an item cannot be named, keep it as `unknown-<pane>-<n>`. Fabricated brand names are not allowed.

### 5. Group and tally

After the flat list, emit count by category, count by color family, readable text corpus in reading order, repeated motifs, and empty cells.

### 6. Meaning section — two hypotheses

Follow `references/hypotheses.md`.

H0 — ordinary display. Write it first.

H1 — intentional second message. Accept only when at least two independent observations reconstruct the same second text that is not already printed on a card.

Do not diagnose the occupant. Do not claim military, assassination, or intelligence meaning from figurines alone.

### 7. Chat catalog

Print the pane catalog and the H0/H1 section in chat so the inventory is readable before the book build finishes.

### 8. Stacked PDF

Follow `references/pdf-stack.md` in this order

1. `/breakdown` on every inventory name token and every readable_text word
2. `/decode` on the readable-text corpus only
3. `/iterate` on the catalog plus those two products
4. `/book` chapter plan
5. `/deep` Georgia body emit
6. `/banner` on every body section and subsection
7. `/images` on the 500-word cadence
8. `/wca-ivy-biblio` first-appearance notes and ITQE tables
9. `/copyright` living footer

One public PDF. Unique rasters. 16-9 full bleed left and right. Real alpha ramps on the top and bottom only after generate. No private-person portrait in a generated banner.

### 9. Chat mathematics

If a count, ratio, or grid index is written as a formula, render it with KaTeX and name every symbol once.

## Anti-patterns

- Do not list shrubs and siding as display objects unless the user asked for the whole photograph.
- Do not treat JPEG artifacts, muntins, or window locks as figurines.
- Do not use a generative edit to clarify a face.
- Do not assert a hidden political or religious code from motif density.
- Do not paste copyrighted product manuals.
- Do not skip the PDF stack on a live `/ispy` image run.
- Do not invent a monograph when the turn is only a skill edit.

## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Slash flags stay routing tokens only. Do not write fade phrases into generate prompts. Apply top-bottom alpha with `apply_tb_alpha_blend.py` after generate.


## Negative gate (mandatory before any deliverable)

Read `/home/workdir/.grok/skills/negative/SKILL.md` and `/home/workdir/.grok/skills/negative/references/blocklist.md`.
Before chat, PDF, DOCX, PPTX, XLSX, caption, filename, alt text, or footnote leaves this skill, extract visible text and run

```bash
python3 /home/workdir/.grok/skills/negative/scripts/sweep_negative.py <extracted-text>
```

Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.

## House interop

Read visual-system/references/house-output.md before any document, deck, or page. Visible link text is Digital Marketing Company. The title attribute matches that text. Plain domain text is DigitalMarketingCo.org. Legal owner is Web Development Corporation. Do not nest an anchor inside an instruction sentence. Stack visual-system, negative, latex, and itqe before delivery when the file contains prose or math. Banners and plates stay unique, full-bleed, and context-locked.


## Final gate

Run /negative as the last step of this skill, after every other section, before chat, a file, a caption, a filename, or alt text is delivered.

1. Read the blocklist at skills/negative/references/blocklist.md.
2. Extract the visible text of the deliverable.
3. Run `python3 /root/.grok/server-skills/negative/scripts/sweep_negative.py` on that text. If that path is missing, use `/home/workdir/.grok/skills/negative/scripts/sweep_negative.py`.
4. Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN.
5. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.
