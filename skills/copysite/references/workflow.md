

# /copysite — Site mirror zip

Fetch one start URL, pull its HTML, then download every linked asset needed to render the page offline (CSS, JavaScript, images, fonts, icons, media, and CSS/JS-referenced files). Write a folder tree that preserves host and path, rewrite links to local relative paths, and zip the tree.

`<skill>` = `@copysite`.

Work in `./artifacts/copysite/<slug>/`. Final zip is `./artifacts/<YYYY-topic-slug-copysite.zip>`.

If the user only asked to create or revise this skill and supplied no URL, stop after the skill files exist. Do not invent a site.

## Read on demand

- `references/scope.md` — what is in-scope, tracker skip list, crawl limits
- `scripts/copysite.py` — the mirror. Run it. Do not reimplement curl loops in the shell.

## Workflow

### 1. Slug and paths

From the URL, make a short slug (host plus last path segment, lowercase, hyphens). Year is the current year.

```
OUT=./artifacts/copysite/<slug>
ZIP=./artifacts/<YYYY-topic-slug-copysite.zip>
```

### 2. Mirror

```bash
python3 <skill>/scripts/copysite.py "URL" \
  --out "$OUT" \
  --zip "$ZIP" \
  --mode page
```

Modes

- `page` (default) — start URL plus requisites. Same-host HTML is not crawled beyond the start page. Other hosts are fetched only when they serve an asset (css, js, image, font, media).
- `site` — also enqueue same-host HTML links up to `--max-pages` (default 80) and `--max-depth` (default 2). Use only when the user asked for the whole site, not one tool page.

Always pass `--mode site` when the user says entire website, whole site, or full domain. Otherwise use `page`.

### 3. Confirm

Read `$OUT/manifest.json`. Check `ok` is true, `start_url` matches, and `files` is non-empty. Spot-check that the start HTML and at least one CSS and one JS file landed.

If the start fetch failed, fix the URL or user-agent and rerun. Do not hand the user an empty zip.

### 4. Deliver

Give the user the zip path and a short inventory — file count, byte size, HTML/CSS/JS/image/font split, and whether links were rewritten for offline open. Do not paste the site source into chat.


## Render gate (mandatory with /itqe and /latex)

Before delivering any PDF, DOCX, PPTX, XLSX, HTML view, printed page, or builder JSON that may contain notation, short codes, or equations, run the house render gate. Chat may use KaTeX. Files must show compiled glyphs or a compiled figure. Raw LaTeX, AMS-TeX, KaTeX source, MathJax source, uncompiled backslash commands, tofu, or empty boxes are defects.

```bash
python3 @itqe/scripts/scan_render_gate.py \
  ./artifacts/<slug> \
  --also-pdf ./artifacts/<file>.pdf
python3 @latex/scripts/scan_raw_tex.py \
  ./artifacts/<slug> \
  --also-pdf ./artifacts/<file>.pdf --pages
```

Exit code 1 blocks delivery. Repair with `/latex` figures, attach an ITQE table under every display equation (Identifier, Term, Quantity, Explanation), rebuild, scan again, and raster every page. See `@itqe/references/render-gate.md` and `@latex/SKILL.md`.

## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write figure, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

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
