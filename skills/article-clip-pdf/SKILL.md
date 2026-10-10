---
name: article-clip-pdf
description: Extract a web article from a URL and reprint it as a clean Computer Modern PDF with only the article text plus in-article images. Use when the user pastes a news or blog link and wants a PDF, clip, reprint, reader view, Computer Modern export, or text-and-images only with ads, sidebars, related stories, and comments stripped. Images stay in source reading order, never duplicate, print at 100 percent page width with zero left or right margin or padding, keep source aspect ratio, and LANCZOS-upscale when the source bitmap is narrower than print.
---

# Article Clip PDF

## Quality and capability additions

Read [the task-specific quality profile](references/quality-profile.md) before execution. Use `evals/quality-cases.json` for regression scenarios; its assertions are acceptance criteria, not claims that tests have run. Shared path resolution and output rules live in `interop/SKILL.md`.



## Visual stack

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with `@visual-system/scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Reprint one web article as a letter-size PDF set in Latin Modern Roman (Computer Modern). No site chrome.


## Image print contract

Read `interop/references/image-print-contract.md`. Every raster this skill prints is full bleed on the left and on the right: x = 0, width = page width, zero left margin, zero right margin, zero side padding, no side letterbox, no side matte. Each file keeps its own aspect ratio. Do not squash or stretch. Height follows width divided by that source ratio. No path, byte, or average-hash duplicate in the same file. If the bitmap is narrower than 2550 px (prefer 3300), upscale with Lanczos and repeat, at most 2x per pass, until the width meets the floor. Script: `images/scripts/fit_full_bleed.py`. Top and bottom alpha, if used, is applied after the fit and does not change the ratio.


## Workflow

Work in `/workspace/artifacts/<slug>/`.

1. Extract

```bash
python3 <skill>/scripts/extract_article.py "URL" --out /workspace/artifacts/<slug>
```

`<skill>` is this skill directory (`@article-clip-pdf`).

2. Review `article.json`

- Title, author, date, source name must match the page
- `paragraphs` must be the article only — delete share crumbs, related-story blurbs, newsletter CTAs
- `blocks` is the reading-order stream (headings, paragraphs, images). Prefer it over dumping images after paragraph two
- `images` must be the hero plus in-body media, each figure once. Delete card thumbs from Keep Reading / Trending
- Drop duplicates even when the CMS emits both an og:image and the same hero, or the same file as jpg and webp. Match on normalized URL, SHA-256, and perceptual hash
- Keep a caption only when it belongs to that image. Leave caption empty rather than inventing one
- YouTube iframes should already be a thumbnail plus iframe title
- Do not invent a second copy of an image to fill a layout slot. If the source used one figure, the clip uses one figure

If extraction is messy, read `references/extraction.md` and edit the JSON.

3. Build

```bash
python3 <skill>/scripts/build_cm_pdf.py /workspace/artifacts/<slug>/article.json \
  --out /workspace/artifacts/<Title_Slug>.pdf
```

Fonts are bundled at `assets/fonts/lmroman10-*.ttf`. Do not point reportlab at the TeX `.otf` files (CFF outlines fail).

4. Visual QA (mandatory)

```bash
pdftoppm -png -r 150 /workspace/artifacts/<Title_Slug>.pdf /tmp/clip-page
```

Inspect every page. Rebuild if text is clipped, images overflow, glyphs are missing, or leftover chrome snuck in.

5. Deliver the PDF. One-line source note is already in the footer/source line — do not append extra branding.

## Layout rules

- Letter, ~0.85 in side margins for type, justified body, CM bold title, CM italic byline
- Images follow the source corpus. A figure that sat between two paragraphs in the HTML sits between those same paragraphs in the PDF. Never bunch leftover figures after paragraph two or at the end unless that is where they were in the source
- Each distinct figure prints exactly once. Hash-collapse og/hero/srcset variants
- Every image is 100 percent of the page / viewport width. Zero left margin, zero right margin, zero left padding, zero right padding. The bitmap starts at x = 0 and ends at page width. Type keeps the 0.85 in inset; figures ignore it and do not letterbox
- Preserve the source aspect ratio exactly (height = page_width * source_h / source_w). Never squash or stretch to a fixed band height
- LANCZOS-upscale any bitmap narrower than page-width at 150 dpi before embedding. Do not bake a checkerboard into RGB
- A portrait taller than the sheet stays 100 percent wide and is height-clipped to the printable sheet rather than inset
- Any AI figure later inserted into a clip follows the same 100-percent-width, zero-side-gutter, aspect-locked rule and must be context-locked to the surrounding paragraph at the highest available generate resolution
- Footer — site name left, page number right, living copyright centered underneath
- Unicode apostrophes and quotes are fine in the bundled TTFs. Never substitute boxes.
- Strip emoji and other glyphs Latin Modern lacks (the scripts already drop common emoji). If a page PNG shows tofu, delete that character from article.json and rebuild.

## Scope

This skill is for a single article URL. It is not a multi-page site scrape, not a research report, and not a generic save-webpage-as-PDF printout of the live layout.


## Render gate (mandatory with /itqe and /latex)

Before delivering any PDF, DOCX, PPTX, XLSX, HTML view, printed page, or builder JSON that may contain notation, short codes, or equations, run the house render gate. Chat may use KaTeX. Files must show compiled glyphs or a compiled figure. Raw LaTeX, AMS-TeX, KaTeX source, MathJax source, uncompiled backslash commands, tofu, or empty boxes are defects.

```bash
python3 @itqe/scripts/scan_render_gate.py \
  /workspace/artifacts/<slug> \
  --also-pdf /workspace/artifacts/<file>.pdf
python3 @latex/scripts/scan_raw_tex.py \
  /workspace/artifacts/<slug> \
  --also-pdf /workspace/artifacts/<file>.pdf --pages
```

Exit code 1 blocks delivery. Repair with `/latex` figures, attach an ITQE table under every display equation (Identifier, Term, Quantity, Explanation), rebuild, scan again, and raster every page. See `@itqe/references/render-gate.md` and `@latex/SKILL.md`.

## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write figure, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

## Paginated footer

Read `copyright/SKILL.md` and render its canonical notice exactly once per page. Do not keep separate legal text or year calculations here. Preserve any stated user override.

## Publication checks

Apply `interop/SKILL.md` once after the task-specific checks. Its shared rules yield to this skill's explicit format and source-fidelity requirements.

## Delivery

Run the single delivery gate in `interop/SKILL.md` after task-specific validation. Preserve verified quotations and technical identifiers; report unresolved defects or blockers accurately.
