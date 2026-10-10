---
name: extract-dir
description: Extract every published document in a website directory or sitemap into one PDF per URL, using article-clip-pdf and optional copysite plus one banner figure, without rewriting or reprinting the same text twice. Trigger on /extract_dir, extract directory, sitemap white papers to PDF, reprint a site section, or QA-optimize extracted web documents into per-slug folders.
---

# /extract_dir

## Quality and capability additions

Read [the task-specific quality profile](references/quality-profile.md) before execution. Use `evals/quality-cases.json` for regression scenarios; its assertions are acceptance criteria, not claims that tests have run. Shared path resolution and output rules live in `interop/SKILL.md`.



## Visual stack

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with `@visual-system/scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Reprint each unique published document under a site directory or sitemap path as one letter PDF. Source text is extracted once. Do not run a second writer over the same body.

Skill root is @extract-dir.
Clip skill is @article-clip-pdf.
Copysite skill is @copysite.
Banner skill is @banner.
Monograph skill is @phd-ivy-monograph.

Read references/qa-protocol.md before a multi-URL run. Read references/pipeline.md for the locked order.


## Image print contract

Read `interop/references/image-print-contract.md`. Every raster this skill prints is full bleed on the left and on the right: x = 0, width = page width, zero left margin, zero right margin, zero side padding, no side letterbox, no side matte. Each file keeps its own aspect ratio. Do not squash or stretch. Height follows width divided by that source ratio. No path, byte, or average-hash duplicate in the same file. If the bitmap is narrower than 2550 px (prefer 3300), upscale with Lanczos and repeat, at most 2x per pass, until the width meets the floor. Script: `images/scripts/fit_full_bleed.py`. Top and bottom alpha, if used, is applied after the fit and does not change the ratio.


## When this skill runs

- User typed /extract_dir.
- User asked to turn every white paper, report, or directory listing on a live site into PDFs.
- User stacked article-clip, copysite, banner, and monograph and forbade duplicated steps or duplicated body text.

If no start URL or sitemap is given, stop and ask for one.

## Locked order (do not reorder, do not double-run)

1. Discover unique document URLs from the sitemap or directory index.
2. Deduplicate. Canonical English loc wins. Drop hreflang mirrors, trailing-slash twins, and query variants.
3. Extract article JSON plus in-body images with article-clip-pdf/scripts/extract_article.py. Use copysite --mode page only when the clip extract is empty or the page is an app shell that needs local assets to recover images. Never copysite --mode site for this skill.
4. Attach at most one faded banner figure per document (hero figure, not one figure per heading). Compose the raw figure, then run banner/scripts/apply_banner_fade.py.
5. Build exactly one PDF per URL with article-clip-pdf/scripts/build_cm_pdf.py. Write it into that document folder.
6. Invoke phd-ivy-monograph only when the user explicitly asked for a new research monograph and the source page is not already a complete published white paper. A live white paper is a primary source, not a prompt to rewrite. Skipping the monograph rewrite is the correct anti-duplication action.
7. Run the QA battery in references/qa-protocol.md. Rebuild a single document if it fails. Do not reprint siblings.

## Work paths

ROOT=/workspace/artifacts/extract_dir
ROOT/slug/article.json
ROOT/slug/images/
ROOT/slug/banners/banner-00.png
ROOT/slug/Title_Slug.pdf
ROOT/manifest.json

slug is the last path segment of the canonical URL, lowercase, hyphens kept.

## Hard rules

- One PDF per canonical URL. No English plus Spanish pair. No clip PDF plus monograph PDF of the same body.
- Do not invent sections, citations, or equations that the source page does not contain.
- Do not paste site chrome, nav, CTAs, related-story cards, or comments into article.json.
- Visible house link text is exactly Digital Marketing Co. Target is https://DigitalMarketingCo.org. Plain-text domain is DigitalMarketingCo.org.
- Living footer owner is Web Development Corporation, start year 2012, living year on open.
- Real-alpha banners only. No baked checkerboard.
- Copyable Python goes in a fenced block only when a new helper is written in the conversation.
- Times or Latin Modern only. No tofu, no emoji, no black boxes.


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
