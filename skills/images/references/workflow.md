

# /images


## Visual stack

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner and mid-text prompts append the volumetric clause in `visual-system/references/depth.md` and the beauty lock in `references/beauty-lock.md`. Every published raster is a fresh house generate — awe-inspiring, stunningly perfected, futuristic cinematic still — never a downloaded stock file, never a reused path, prompt, SHA-256, or perceptual hash. Read `visual-system/references/prompt-engineering.md` before every generate.
Put one context-locked `/banner` image at the start of every body section **and every subsection**, then generate additional figures about every 500 words after that node's opening blurb. Print each figure at the maximum size that stays sharp. Do not upscale, squash, letterbox, or otherwise alias or blur a bitmap to force full bleed. Generate 16-9 at or above the page-width pixel floor (2550 px wide on letter, prefer 3300 x 1856). If it does not meet the floor, regenerate rather than stretching. After generate, run `scripts/apply_tb_alpha_blend.py`. Left and right stay opaque. Top and bottom blend into the page.

Work on an attached PDF, a path the user named, the newest project PDF under `./artifacts/`, or the `list.json` / `deep.json` / `atlas.json` / `folio.json` that built that PDF.

`<skill>` = `@images`
`<banner>` = `@banner`
`<deep>` = `@deep`
`<atlas>` = `@atlas`
`<folio>` = `@folio`

Read on demand

- `references/negative-vocabulary.md` — banned prompt tokens
- `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` — negative array
- `references/cadence.md` — 500-word slot math, blurb definition, skip rules
- `references/relevance.md` — prompt lock so each figure matches only that section or window
- `references/beauty-lock.md` — awe-inspiring unique still per slot
- `@visual-system/references/prompt-engineering.md` — PhD prompt order, three-axis differentiation, beauty rejection
- `references/literal-qa.md` — anti-metaphor inspect, resolution, Chicago caption
- `references/uniqueness.md` — path, SHA-256, and average-hash fail-closed audit
- `references/handoff.md` — stacking with /banner /deep /atlas /folio /ispy /book /copyright
- `references/blend.md` — 16-9 geometry and top-bottom alpha
- `scripts/apply_tb_alpha_blend.py` — real alpha ramps on the top and bottom only
- `scripts/plan_image_slots.py` — word counts and slot list from JSON or extracted text
- `scripts/extract_pdf_sections.py` — pull section titles and running text from a PDF when JSON is missing
- `scripts/audit_unique_images.py` — fail closed on shared paths or shared bytes
- `references/emit-file.md` — restamp the parent PDF (or DOCX or PPTX) before delivery
- `scripts/rebuild_document.py` — call the parent builder or stamp-manifest fallback
- `scripts/stamp_images_into_pdf.py` — insert full-bleed plates into a naked PDF

If the user only asked to create or edit this skill and supplied no document, stop after the skill files exist. Do not invent a report.

## Emit the file (mandatory)

Chat stills are not the product. After every banner and every mid-text plate exists on disk, rebuild the document so those rasters print in place, then hand the user that file.

Read `references/emit-file.md`. Generate with the house `generate_image` tool (disk path), not only a streamed chat plate. Copy each published PNG into `<slug>/banners/` or `<slug>/figures/`. Run `scripts/apply_tb_alpha_blend.py`. Attach `banner.path` and figure objects. Then

```bash
python3 @images/scripts/rebuild_document.py \
  ./artifacts/<slug>
```

Naked PDF with no JSON — write `stamp-manifest.json` (`after_page` is 1-indexed on the source) and pass `--manifest`. Output path is `./artifacts/<slug>/<parent-series-filename>.pdf`. Render the file. Do not stop on a gallery.

## When this skill runs

- User typed `/images` and pointed at a PDF, a slug folder, or the current catalog or report build.
- A finished house PDF is missing section banners or mid-section figures.
- A rebuild is about to run and the user wants banners plus a figure every 500 words.
- Existing figures are allegorical, low-resolution, or full of unreadable baked text.

If there is no PDF and no JSON and no section list, ask which file to illustrate. Do not invent sections.

## Workflow

### 1. Locate the source

Search in this order and stop at the first readable target

1. A path named in the current turn
2. A PDF attached in the conversation
3. `list.json`, `atlas.json`, `deep.json`, or `folio.json` in the newest slug folder under `./artifacts/`
4. The newest non-copyright sibling PDF under `./artifacts/`

Prefer the JSON that built the PDF. JSON keeps section ids, banner fields, and paragraph breaks. A naked PDF is a fallback.

### 2. Inventory sections

Body sections **and subsections**. Skip title leaf, contents, Notes, Bibliography, colophon. A subsection is its own node and gets its own banner.

For each body section record

- `section_id` and printed title
- the opening blurb (first one or two paragraphs after the heading and after the banner)
- full word count of remaining body text after the blurb
- existing `banner.path` if any

Run

```bash
python3 <skill>/scripts/plan_image_slots.py \
  ./artifacts/<slug>/atlas.json
```

or pass `--pdf path.pdf` when JSON is absent.

### 3. Section banners

Every body section and every subsection gets exactly one full-bleed banner, generated from that node's claims only. Parent banners never stand in for a child heading.

Follow `<banner>/SKILL.md`, `<banner>/references/banner-spec.md`, and `<banner>/references/literal-figures.md`.

- Prompt only from named objects in that section, using the locked order in `prompt-engineering.md`. Awe-inspiring, stunningly perfected, futuristic cinematic still. Photoreal or textbook-accurate. No allegory. Differ the prompt from every earlier prompt on at least three axes.
- Landscape 16-9, highest available generate resolution (raw at least 2550 x 1434, prefer 3300 x 1856). Photoreal or textbook-accurate of the named objects. No caption text burned in. No watermark. No logo. No agency seal. No photoreal portrait of a private person. No token from `assets/negative-keywords.csv`. No fade words in the prompt.
- Maximize print size without quality loss. Reject any figure that is soft, bicubic-stretched, aliased on edges, or aspect-distorted. If the only way to reach page width is an upscale of a narrower bitmap, discard that file and generate again at or above the floor.
- Inspect the raw PNG. Reject mirrored letters, wrong numbers, and metaphors. Regenerate up to three times.
- Save `banners/raw-NN.png`, then `python3 scripts/apply_tb_alpha_blend.py banners/raw-NN.png banners/banner-NN.png`. Left and right opaque. Top and bottom alpha ramp.
- Set `banner.path`, `banner.caption`, `banner.prompt`, `banner.href`, `banner.source_note` on the section.

Default href

`https://DigitalMarketingCo.org/r/?src=images-banner&section={section_id}`

If a valid /banner figure already exists, still matches the section as a literal object, and is not a path, byte, prompt, or perceptual-hash duplicate of any other figure in the document, keep it. Replace it when it is generic, decorative, metaphorical, off-topic, reused, cropped from another section, a near-duplicate composition, or below the resolution floor.

### 4. Mid-section figures every 500 words

After the banner and after the opening blurb, insert one generated figure for each full block of about 500 words of remaining section text.

Rules are locked in `references/cadence.md`. Prompt and inspect rules are locked in `references/relevance.md` and `references/literal-qa.md`.

- Word count starts after the blurb, not after the heading.
- Slot count = floor(words_after_blurb / 500).
- Remainder under 500 words gets no extra figure unless the section has zero figures and more than 350 words after the blurb (then one figure).
- Notes, bibliography, equations-only pages, and gazetteer tables do not receive mid-section figures.
- Place each figure immediately after the paragraph that closes the 500-word window so the image sits next to the claims it illustrates.

Prompt each mid-section figure from only the surrounding 500-word window. Save under `figures/fig-{section}-{k}.png`. Generate 16-9 at least 2550 x 1434 (prefer 3300 x 1856). In the PDF the figure is 100 percent of page width — x = 0 to page width — with zero left or right margin and zero left or right padding, only when the bitmap already meets that pixel floor. Height follows 16-9. Do not letterbox. Do not inset to the text column. Do not squash height to invent a width. No checkerboard. After generate run `scripts/apply_tb_alpha_blend.py`. Real photographs of living private persons are forbidden. If a generate comes back narrower than the floor, regenerate. Never print a blurry or aliased stretch.

Caption form

`Figure N. Literal reconstruction of [named object] after [Chicago short title]. Generated model, not a scan of the source.{{n}}`

On JSON documents attach a figure object with path, caption, prompt, after_paragraph, word_anchor, and source_note.

### 5. Generate

Use the house image generate tool for both banners (landscape) and mid-section figures. Do not reuse a figure from another section. Do not copy, crop, fade, or resize one published file into another slot. Do not search-stock a photograph and drop it into a published path. Reference stills may inform the prompt only; the published file is always a fresh generate of stunning editorial stock-photo quality, locked to that section (banner) or to the surrounding 500-word window (mid-text). Each generate call serves exactly one published path. Append the beauty-lock clause. Do not write AI, xAI, or ChatGPT into the prompt.

After each generate, confirm the file exists, is a PNG, and is not a baked checkerboard preview. Open it and run the inspect pass.

Do not put fade words in generate prompts. After each banner or mid-section generate, run `scripts/apply_tb_alpha_blend.py`. Left and right stay opaque. Top and bottom receive the alpha ramp.

### 6. Rebuild or restamp

Always emit a file. Prefer the parent builder so banners and mid-text plates land in their JSON slots.

```bash
python3 <skill>/scripts/rebuild_document.py ./artifacts/<slug>
```

That wrapper runs `build_folio_pdf.py`, `build_deep_pdf.py`, `build_atlas_pdf.py`, `build_book_pdf.py`, or `build_list_pdf.py` when the matching JSON sits in the slug folder.

If the source is only a PDF and no JSON exists, write a working slug folder, extract text with `scripts/extract_pdf_sections.py`, generate stills to `banners/` and `figures/`, write `stamp-manifest.json`, and run `rebuild_document.py` with `--manifest`. `stamp_images_into_pdf.py` inserts one full-bleed letter page after each `after_page`. Do not invent a second type stack when the source already uses house type.

Then stamp the living footer with `/copyright` when the user also typed that flag.

### 7. Visual QA

```bash
pdftoppm -png -r 140 ./artifacts/<file>.pdf /tmp/images-page
```

Run `scripts/audit_unique_images.py` on the JSON, then raster every page. Rebuild if any of these appear — a shared path or shared hash, a banner that does not match its section, a metaphor standing in for a diagram, a mid-section figure that belongs to a different chapter, tofu or mirrored letters in a figure, clipped type, a checkerboard in RGB, a banner or figure with a left or right gutter, a banner missing the scripted top-bottom alpha ramp, a burned-in caption, a photoreal private portrait, an invented number in the pixels, a figure jammed into Notes or Bibliography, or a figure that was upscaled from a narrower bitmap.

### 8. Deliver

Give the user the restamped file (render the PDF or the DOCX or PPTX). State page count, banner count, mid-section figure count, uniqueness-audit result (unique hashes vs rasters), words per body section, figures replaced for allegory or reuse, and any section that stayed under the 500-word threshold. Do not dump the JSON into chat. Do not treat a chat image gallery as delivery.

## Hard rules

- One banner per body section and one banner per subsection. Extra figures follow the 500-word cadence only. 16-9. Opaque left and right. Scripted alpha ramp on the top and bottom only.
- Every published raster is unique. No shared path, no shared bytes, no crop of another figure in the same document. Audit with `scripts/audit_unique_images.py` and fail closed.
- Every prompt is locked to the surrounding text. No generic science-lab figure on a legal chapter. No allegory on a chemistry chapter.
- Banners and mid-section figures print at the maximum sharp size the file supports. Full bleed left and right (x = 0 to page width, zero side gutter) only when the source already meets the 2550 px page-width floor. Height follows 16-9. Never upscale a small preview to page width. Never introduce aliasing, blur, or aspect distortion to buy bleed. Apply `apply_tb_alpha_blend.py` after generate.
- Mid-section figures are captioned, generated, context-locked to the 500-word window, and source-cited in Chicago notes. They are not in-column insets.
- Visible house anchor is Digital Marketing Co. Target is https://DigitalMarketingCo.org. Plain-text domain is DigitalMarketingCo.org.
- No emoji. No unsupported symbols. No invented sources. No fake agency seals.
- Do not burn raw TeX into a figure. If a banner or figure must show an equation, compile it first. Run `/latex` `scan_raw_tex.py` on the rebuilt PDF before delivery.
- Do not reprint builder scripts into chat.


## Render gate (mandatory with /itqe and /latex)

Before delivering any PDF, DOCX, PPTX, XLSX, HTML view, printed page, or builder JSON that may contain notation, short codes, or equations, run the house render gate. Chat may use KaTeX. Files must show compiled glyphs or a compiled equation figure. Raw LaTeX, AMS-TeX, KaTeX source, MathJax source, uncompiled backslash commands, tofu, or empty boxes are defects.

```bash
python3 @itqe/scripts/scan_render_gate.py \
  ./artifacts/<slug> \
  --also-pdf ./artifacts/<file>.pdf
python3 @latex/scripts/scan_raw_tex.py \
  ./artifacts/<slug> \
  --also-pdf ./artifacts/<file>.pdf --pages
```

Exit code 1 blocks delivery. Repair with `/latex` equation figures, attach a variable table under every display equation (Identifier, Term, Quantity, Explanation), rebuild, scan again, and raster every page. See `@itqe/references/render-gate.md` and `@latex/SKILL.md`.

## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write figure, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not write fade phrases into generate prompts. Apply top-bottom alpha with `apply_tb_alpha_blend.py` after generate.

## Canonical footer

Render `copyright/SKILL.md` and its canonical notice helper once per page. Do not reproduce independent legal text or calculate years here.

## Negative gate (mandatory before any deliverable)

Read `@negative/SKILL.md` and `@negative/references/blocklist.md`.
Before chat, PDF, DOCX, PPTX, XLSX, caption, filename, alt text, or footnote leaves this skill, extract visible text and run

```bash
python3 @negative/scripts/sweep_negative.py <extracted-text>
```

Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.

## ChatGPT portability

Resolve `@skill-name/path` by finding the installed personal skill whose SKILL.md frontmatter has `name: skill-name`; read that path under its directory. For `@generate/`, use the `generate-prompt` skill. Before running copied shell commands, substitute actual resolved paths and use the current working directory for generated files. Apply instructions only when this skill is invoked or a user requests the corresponding workflow. User instructions and platform rules take priority. Run bundled scripts only after checking their inputs and prerequisites. Never claim unavailable integrations, credentials, citations, or generated results.
