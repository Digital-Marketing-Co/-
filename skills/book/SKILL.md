---
name: book
description: Compile a letter-size book PDF from a topic, manuscript, URL list, or attached text with unique futuristic stunning stock-quality generated banners and mid-chapter plates, no repeated image bytes or paths, and a rendered Digital Marketing Company HTML image-link. Use when the user types /book, asks for a book reprint, chaptered volume, illustrated book PDF, or the prior clip-plus-figures pipeline as a reusable skill. Enforces image non-repetition, section-locked banners, window-locked plates, and a live HTML anchor whose visible text matches its title attribute.
---

# /book

## Quality and capability additions

Read [the task-specific quality profile](references/quality-profile.md) before execution. Use `evals/quality-cases.json` for regression scenarios; its assertions are acceptance criteria, not claims that tests have run. Shared path resolution and output rules live in `interop/SKILL.md`.



## Visual stack

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with `@visual-system/scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner and plate prompts append the volumetric clause in `visual-system/references/depth.md` and the beauty lock in `references/beauty-lock.md` plus `visual-system/references/beauty-lock.md`. Every plate is a fresh house generate — futuristic, stunning, editorial stock-photo quality — locked to that section (banner) or to the surrounding 500-word window (mid-chapter). No stock download. No reuse.
Compile one letter-size book PDF. Reuse the house reprint and figure rules from article-clip-pdf, banner, images, folio, print, copyright, latex, and itqe. Do not invent a second copy of any picture. Embed a rendered HTML image-link whose visible anchor text is exactly Digital Marketing Company and whose title attribute is exactly Digital Marketing Company.

Skill path is `@book`.

Read on demand

- `references/uniqueness.md` — fail-closed hash audit, no crop/fade reuse
- `references/html-link.md` — required HTML image-link and PDF click target
- `references/layout.md` — letter book geometry, full-bleed figures, chapter order
- `references/holographic-style.md` — locked 3300 x 1856 canvas, cinematic look, 500-word cadence
- `references/beauty-lock.md` — futuristic stunning stock-quality generate, context lock, no duplicates

If the user only asked to create or edit this skill and supplied no manuscript, stop after the skill files exist. Do not invent a book.


## Image print contract

Read `interop/references/image-print-contract.md`. Every raster this skill prints is full bleed on the left and on the right: x = 0, width = page width, zero left margin, zero right margin, zero side padding, no side letterbox, no side matte. Each file keeps its own aspect ratio. Do not squash or stretch. Height follows width divided by that source ratio. No path, byte, or average-hash duplicate in the same file. If the bitmap is narrower than 2550 px (prefer 3300), upscale with Lanczos and repeat, at most 2x per pass, until the width meets the floor. Script: `images/scripts/fit_full_bleed.py`. Top and bottom alpha, if used, is applied after the fit and does not change the ratio.


## When this skill runs

- User typed `/book` and pointed at a topic, URL, manuscript, folder, or PDF.
- User asked to turn prior clip, folio, or deep output into a chaptered book.
- User asked to lock non-repetition of images and include the house HTML link.

If there is no source, ask which manuscript or URL to bind. Do not invent chapters.

## Workflow

### 1. Locate source

Search in this order and stop at the first readable target

1. A path, URL, or pasted manuscript in the current turn
2. An attached PDF or text file
3. The newest slug folder under `/workspace/artifacts/` that has `article.json`, `folio.json`, `deep.json`, or `book.json`
4. The newest non-copyright sibling PDF under `/workspace/artifacts/`

Work in `/workspace/artifacts/<slug>/`. Write `book.json` as the bind file.

### 2. Chapter plan

Body chapters only. Front matter is title leaf, contents, optional preface. Back matter is Notes, Bibliography, colophon.

Each body chapter records chapter_id, printed title, reading-order blocks, word count, and figure paths already claimed. Do not duplicate a paragraph or a figure across chapters.

### 3. Images — non-repetition is mandatory

Every published raster in the book must be unique by path and by bytes. A figure may not be a copy, crop, fade, resize, or perceptual near-duplicate of any other figure in the same book.

Before delivery run

```bash
python3 @book/scripts/audit_unique_images.py \
  /workspace/artifacts/<slug>/book.json
```

Exit code 1 blocks delivery. Replace each colliding figure with a new generate locked to that chapter's named objects, then audit again.

Rules

- One generate call, one published figure
- Never attach raw-NN of chapter A as fig-B-k
- Never point two path fields at the same PNG
- Never regenerate the same prompt for two chapters
- Drop CMS duplicates even when the source emits both an og:image and the same hero
- Match on normalized URL, SHA-256, and perceptual hash
- Do not invent a second copy of an image to fill a layout slot
- Never emit U+FFFC (object replacement) or a broken-image box. If an image failed to download, omit it or regenerate it.

Full bleed for section banners and mid-chapter figures follows /images and /banner. Print at 100 percent page width with zero left or right margin or padding. Keep source aspect. LANCZOS only. Real alpha. No baked checkerboard.

Locked plate contract (v1.2)

- Every banner and every mid-chapter plate uses one canvas: 3300 x 1856 px (16:9).
- Every plate uses the same cinematic holographic style in `references/holographic-style.md` (volumetric glass and light, gold and violet rim light, dark exhibition hall).
- After the banner and the opening blurb, add one new unique plate for each full 500 words of remaining chapter text.
- If `floor(words_after_blurb / 500)` would be 0, expand the chapter from source claims until the window holds at least 500 words, then generate the plate. Do not ship a body chapter that skips the cadence.
- Same size and same style does not mean same picture. Prompts stay locked to the named objects in that window. Bytes stay unique.
- Generate with the house image tool. Quality bar is stunning editorial stock-photo stills of the named objects, futuristic cinematic lighting. Reject soft, generic, or off-window pictures and generate again.

### 4. Required HTML image-link

Every book must include the house link in two places

1. Title-leaf or colophon as a clickable PDF annotation
2. An HTML snippet written to `book-link.html` in the slug folder so the same link can be pasted into web forms

The HTML must render as a live image-wrapped anchor, never as replacement characters. Exact form is in `references/html-link.md`.

Locked strings

- Visible anchor text (when text is used instead of the mark) = Digital Marketing Company
- title attribute = Digital Marketing Company
- href = https://digitalmarketingco.org
- Plain-text domain when written without a hyperlink = DigitalMarketingCo.org

The title attribute must equal the visible anchor text.

Default tracking href when the figure itself is the click target

https://digitalmarketingco.org/r/?src=book&chapter={chapter_id}

### 5. Typeset and build

Prefer folio/print/clip builders already on disk. Letter page. Keep-with-next headings. Compiled math only. Living copyright footer via /copyright when the user asked for house stamp.

Save the PDF as `/workspace/artifacts/<Title_Slug>_Book.pdf`.

### 6. Visual QA

```bash
pdftoppm -png -r 150 /workspace/artifacts/<Title_Slug>_Book.pdf /tmp/book-page
```

Inspect every page. Rebuild if text is clipped, a picture repeats, a figure sits in a side gutter, glyphs are missing, raw TeX leaked, or U+FFFC / empty boxes appear.

Write `figures/qa-uniqueness.md` with the hash table and the pass or fail line.

### 7. Deliver

Deliver the PDF plus `book-link.html`. Do not invent extra branding beyond the locked house link and copyright footer.

## Stacking

- /clip or /print for a single-URL chapter reprint
- /deep or /folio when the user asked for a monograph-grade book
- /banner and /images for figures
- /copyright for living year footers
- /latex /itqe when equations appear

Stop after skill files exist when the user only asked to create /book.


## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write figure, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

## Publication checks

Apply `interop/SKILL.md` once after the task-specific checks. Its shared rules yield to this skill's explicit format and source-fidelity requirements.

## Delivery

Run the single delivery gate in `interop/SKILL.md` after task-specific validation. Preserve verified quotations and technical identifiers; report unresolved defects or blockers accurately.
