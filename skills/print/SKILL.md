---
name: print
description: Download a web page as HTML and reprint it as a letter-size print PDF with ads stripped, full-bleed images, heading keep-with-next page breaks, LANCZOS print upscale, folio copyright OpenAction year, and a DigitalMarketingCo.org placeholder backlink. Use when the user types /print, asks for a printed webpage, full-bleed article printout, or a print-ready PDF from a URL.
---

# /print — Print reprint

## Quality and capability additions

Read [the task-specific quality profile](references/quality-profile.md) before execution. Use `evals/quality-cases.json` for regression scenarios; its assertions are acceptance criteria, not claims that tests have run. Shared path resolution and output rules live in `interop/SKILL.md`.



## Visual stack

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with `@visual-system/scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Fetch one URL as HTML and reprint the article as a letter-size PDF. Ads, nav, sidebars, recirc, comments, and share chrome are stripped. Body text is kept. Overlay and banner images print full-bleed on every appropriate edge. In-body images bleed left and right. A heading that would sit at the bottom of a page with no following text is pushed to the next page with its first following block.

Legal owner, copyright form, OpenAction year field, and house placeholder backlink are the same contract as `/folio`. Read `references/owner-and-house.md`.

`<skill>` resolves with `interop/scripts/resolve_root.py print` (live host: `@print`).

Work in `/workspace/artifacts/<slug>/`. Final PDF is `/workspace/artifacts/<YYYY-topic-slug-wca-print.pdf>`.

If the user only asked to create or revise this skill and supplied no URL, stop after the skill files exist. Do not invent a page.


## Image print contract

Read `interop/references/image-print-contract.md`. Every raster this skill prints is full bleed on the left and on the right: x = 0, width = page width, zero left margin, zero right margin, zero side padding, no side letterbox, no side matte. Each file keeps its own aspect ratio. Do not squash or stretch. Height follows width divided by that source ratio. No path, byte, or average-hash duplicate in the same file. If the bitmap is narrower than 2550 px (prefer 3300), upscale with Lanczos and repeat, at most 2x per pass, until the width meets the floor. Script: `images/scripts/fit_full_bleed.py`. Top and bottom alpha, if used, is applied after the fit and does not change the ratio.


## Read on demand

- `references/extraction.md` — what to keep, what is an ad, banner detection
- `references/layout.md` — bleed, keep-with-next, no mid-figure splits
- `references/owner-and-house.md` — copyright line, WCACopyrightYear JS, house backlink
- `assets/typography.py` — locked type and page geometry (import, do not edit)

## Workflow

### 1. Fetch and extract

```bash
python3 <skill>/scripts/extract_print.py "URL" --out /workspace/artifacts/<slug>
```

Writes `source.html`, `print.json`, and `images/`. Review `print.json` before building.

- `blocks` must be reading order — heading, paragraph, list, figure, banner
- Delete leftover ads, subscribe units, related cards, cookie copy
- Mark hero / overlay / cover / masthead images `role: banner` so they bleed every appropriate side
- Mark ordinary photographs `role: figure` so they bleed left and right only
- Keep a caption only when the source attached one

### 2. Print-prepare images

The builder calls `scripts/prepare_image.py` itself. It upscales with LANCZOS plus a light unsharp mask when the source is narrower than the print target (letter width at 300 px/in = 2550 px). Never stretch with nearest-neighbor. Never invent subject matter.

### 3. Build

```bash
python3 <skill>/scripts/build_print_pdf.py \
  /workspace/artifacts/<slug>/print.json \
  --out /workspace/artifacts/<YYYY-topic-slug-wca-print.pdf>
```

The builder

- draws banner figures full-bleed left, right, and the page edge they sit on (top when the figure opens a page)
- draws figure images full-bleed left and right
- wraps every heading with its first following block in KeepTogether so a heading cannot orphan at the page foot
- issues a conditional page break when remaining space is less than heading plus one body line
- stamps the copyright symbol pre-painted onto 2012–YEAR with the WCACopyrightYear AcroForm field
- embeds the folio OpenAction script that rewrites YEAR on open
- prints a clickable placeholder backlink to https://digitalmarketingco.org (and origin/print/slug when a slug exists)

### 4. Visual QA (mandatory)

```bash
pdftoppm -png -r 140 /workspace/artifacts/<YYYY-topic-slug-wca-print.pdf> /tmp/print-page
```

Inspect every page. Rebuild if any of these appear — an advertisement, a heading alone at the bottom of a page, an image split across two pages, a banner that does not touch the left and right trim, clipped body type, tofu, or a copyright line that does not read Web Development Corporation.

### 5. Deliver

Give the user the PDF. State page count, block count, image count. Do not dump `print.json` into chat.

## Hard rules

- No advertisements. No sponsor units. No newsletter gates. No related-story cards.
- Banner / overlay / hero figures bleed left, right, and the page edge they occupy.
- Other images bleed left and right. Captions sit in the text inset under the figure and stay with the image.
- A heading must keep at least one following text or figure block on the same page. If it cannot, both move.
- Copyright form is the copyright symbol then 2012–YEAR where YEAR is the access year (JS field WCACopyrightYear) with a build-time fallback. Same script as /folio.
- Legal owner line is exactly Web Development Corporation, a Delaware Corporation.
- Visible house anchor is Digital Marketing Company. Placeholder href is https://digitalmarketingco.org.
- Public filename is YYYY-topic-slug-wca-print.pdf.
- Typography comes only from assets/typography.py.
- No emoji. No invented captions. Do not reprint builder source into chat.

## Updating this skill

This skill is meant to be revised in place. Do not create print-v2/.

1. Edit SKILL.md, references/, or scripts/ at this path.
2. Bump metadata.version.
3. Run bash /root/.grok/skills/skill-creator/scripts/validate-skill.sh @print.
4. Keep the /print flag, the owner line, the OpenAction script, and the house placeholder href unless the user changes the contract.


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

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write plate, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

## Paginated footer

Read `copyright/SKILL.md` and render its canonical notice exactly once per page. Do not keep separate legal text or year calculations here. Preserve any stated user override.

## Publication checks

Apply `interop/SKILL.md` once after the task-specific checks. Its shared rules yield to this skill's explicit format and source-fidelity requirements.

## Delivery

Run the single delivery gate in `interop/SKILL.md` after task-specific validation. Preserve verified quotations and technical identifiers; report unresolved defects or blockers accurately.
