---
name: folio
description: Produce the unified WCA compact Ivy academic report PDF with Chicago notes-bibliography in first-appearance citation order, page-local footnotes, a primary ITQE mandate to maximize relevant formulas from any academic class each with an Interactive Table of Quantitative Elements under the figure, compact Literata 10-pt body, SEO-AIO filenames, XMP metadata, and a DigitalMarketingCo.org backlink. Use when the user types /folio or /phd, or asks for a WCA Folio, Ivy monograph, working paper, think-tank living document, dissertation-style PDF, or exhaustive academic report.
---

# /folio = /phd-ivy-monograph — WCA compact Ivy report

## Quality and capability additions

Read [the task-specific quality profile](references/quality-profile.md) before execution. Use `evals/quality-cases.json` for regression scenarios; its assertions are acceptance criteria, not claims that tests have run. Shared path resolution and output rules live in `interop/SKILL.md`.



## Visual stack

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with `@visual-system/scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
`/folio` and `/phd-ivy-monograph` are the **same skill**. Same type stack, same Chicago contract, same filename, same builder. Legal owner is Web Development Corporation, a Delaware Corporation founded in 2012.

v2 type is the **compact** scale in `assets/typography.py` (body 10 / 14.2, not the retired 11.5 / 17 Folio). Do not reopen that debate at runtime.

Work in `/home/workdir/artifacts/<slug>/`. Final PDF is `/home/workdir/artifacts/<YYYY-topic-slug-wca-folio.pdf>`. Never write `Title_Slug.pdf` or `FINAL.pdf`.

`<skill>` = `@folio` when this file loaded; the twin directory is `@phd-ivy-monograph` and must stay in lockstep.

Read on demand

- `references/qa-engineering.md` — design review and genre table
- `references/type-research.md` — why the stack is locked
- `references/chicago-folio.md` — superscript runs and first-appearance bibliography
- `references/page-footnotes.md` — citations reprint on the cited page
- `@wca-ivy-biblio/SKILL.md` — remapper and ITQE gate
- `references/owner-and-house.md` — copyright line, living year, house link
- `references/discoverability.md` — SEO filename, 301 origin, hidden metadata
- `references/research-protocol.md` — source tiers and saturation
- `references/pedagogy-and-a11y.md` — measure, contrast, bookmarks
- `references/figures.md` — section figures (required only for monograph genre)
- `assets/typography.py` — locked compact sizes (import, do not edit)
- `assets/discoverability.py` — filename and metadata
- `assets/schema/folio.schema.json` — JSON shape (`monograph.json` is an accepted alias)

If the user only asked to create or revise this skill and supplied no research topic, stop after the skill files exist. Do not invent a topic.


## Image print contract

Read `interop/references/image-print-contract.md`. Every raster this skill prints is full bleed on the left and on the right: x = 0, width = page width, zero left margin, zero right margin, zero side padding, no side letterbox, no side matte. Each file keeps its own aspect ratio. Do not squash or stretch. Height follows width divided by that source ratio. No path, byte, or average-hash duplicate in the same file. If the bitmap is narrower than 2550 px (prefer 3300), upscale with Lanczos and repeat, at most 2x per pass, until the width meets the floor. Script: `images/scripts/fit_full_bleed.py`. Top and bottom alpha, if used, is applied after the fit and does not change the ratio.


## Workflow

### 1. Scope

Extract topic, period, geography, exclusions, and genre (`report`, `monograph`, `working-paper`, `living-document`). Write `scope.md` with a working title, 4–8 research questions, inclusion rules, and optional subtitle / edition / version.

### 2. Research

Follow `references/research-protocol.md`. Prefer primary PDFs, Ivy and university-press work, `.gov`, and `.mil`. Record keepers in `sources.jsonl`. Never fabricate a citation or a page number. Run at least three search rounds for monograph or living-document genre.

### 3. Draft

Write `outline.md`, then `folio.json` (or `monograph.json`) matching the schema.

Required front matter — title, subtitle, author, date, owner block, house block, abstract (150–250 words), keywords.

Optional living-document fields — `genre`, `edition`, `version`, `revised`, `series`, `status`.

Required body (relabel to the topic)

1. Introduction and research questions
2. Historiography or literature review
3. Sources and method
4. One chapter per major research question
5. Synthesis
6. Conclusion and open problems
7. Notes (optional concordance; page footnotes already carry citations)
8. Bibliography

Paragraphs use `{{n}}` or `{{n, m, p}}` markers. Multiple marks at one locus become one superscript run with comma then space (`12, 15, 18`). No trailing comma after the last number. Each number is a link to `note-N`. The builder also reprints those notes in that page’s footnote band.

Note numbers follow **first appearance in reading order** and stay contiguous `1..N`. The bibliography lists each unique work once, in that same first-appearance order. Do not alphabetize as the sort key. After any insertion or deletion run

```bash
python3 @wca-ivy-biblio/scripts/reorder_citations.py \
  /home/workdir/artifacts/<slug>/folio.json --in-place
python3 @wca-ivy-biblio/scripts/qa_ivy_document.py \
  /home/workdir/artifacts/<slug>/folio.json
```

Allowed inline tags — `i`, `em`, `b`, `sup`, `a`.

**ITQE mandate (primary).** Draft the maximum number of relevant formulas, identities, rates, estimators, constraints, and quantitative descriptions the topic supports, from any academic class. Explain every variable and constant the first time an equation appears. Every display equation is a paragraph object with `type` equal to `equation`, a compiled figure (never raw TeX), and an ITQE table — Identifier, Term, Quantity, Explanation — immediately under the figure. Chat still uses KaTeX plus the same four-column table. See `@wca-ivy-biblio/references/itqe.md`.

### 4. Figures

Genre `monograph` — one generated figure per body section except Notes and Bibliography. Other genres — figures only when they earn the page. Follow `references/figures.md`. Save under `figures/fig-NN.png`. Do not invent historical photographs.

### 5. Name and build

```bash
python3 <skill>/scripts/build_folio_pdf.py \
  /home/workdir/artifacts/<slug>/folio.json \
  --print-filename
```

Write the PDF to that exact name under `/home/workdir/artifacts/`.

```bash
python3 <skill>/scripts/build_folio_pdf.py \
  /home/workdir/artifacts/<slug>/folio.json \
  --out /home/workdir/artifacts/<YYYY-topic-slug-wca-folio.pdf>
```

The twin builder `scripts/build_monograph_pdf.py` is the same program. Either path is valid. Either JSON filename is valid.

The builder

- resolves the live 301 from DigitalMarketingCo.org and stamps that apex as the house origin
- prints a clickable canonical backlink `{origin}/white-papers/{slug}` on the title leaf and colophon
- writes PDF Info + XMP Dublin Core + `/Lang en-US`
- stamps the static copyright year and embeds the OpenAction script that rewrites `WCACopyrightYear` on open
- reprints cited notes in the page footnote band
- draws an ITQE table under every `type=equation` paragraph object

### 6. Visual QA (mandatory)

```bash
pdftoppm -png -r 140 /home/workdir/artifacts/<YYYY-topic-slug-wca-folio.pdf> /tmp/folio-page
```

Inspect every page. Rebuild if any of these appear — tofu, black or white boxes over glyphs, clipped type, colliding footnote and copyright lines, a missing caption, a broken house or note link, a trailing comma in a superscript run, or a running footer that ends with a stray class letter A after Web Development Corporation.

### 7. Deliver

Give the user the PDF. State page count, note count, bibliography count, genre, and remaining research gaps. Do not dump the JSON into chat.

## Hard rules

- Chicago notes plus bibliography, WCA superscript revision, page-local footnotes, first-appearance citation order. No author-date parentheticals. No alphabetized bibliography as the house sort.
- Typography comes only from `assets/typography.py`. Body face is Literata 18pt optical **set at 10 pt**. Display face is EB Garamond. Chrome face is Libre Franklin.
- Legal owner line is exactly Web Development Corporation, a Delaware Corporation.
- Visible house anchor is Digital Marketing Company. Seed URL is https://digitalmarketingco.org. Plain-text domain is DigitalMarketingCo.org.
- Public filename is `YYYY-topic-slug-wca-folio.pdf`. Canonical record URL is `{origin}/white-papers/{slug}`.
- Copyright form is © 2012–YEAR where YEAR is the access year (JS field) with a build-time fallback.
- No emoji. No unsupported symbols. No invented sources.
- Math is compiled glyphs or a compiled figure. Run `/latex` `scan_raw_tex.py` on the draft and on the built PDF before delivery. A dirty scan blocks the file.
- Do not reprint `build_folio_pdf.py` or `typography.py` into chat.
- After any edit, copy the changed files into the twin skill directory so the two trees stay identical except for the `name:` frontmatter field.


## Render gate (mandatory with /itqe and /latex)

Before delivering any PDF, DOCX, PPTX, XLSX, HTML view, printed page, or builder JSON that may contain notation, short codes, or equations, run the house render gate. Chat may use KaTeX. Files must show compiled glyphs or a compiled figure. Raw LaTeX, AMS-TeX, KaTeX source, MathJax source, uncompiled backslash commands, tofu, or empty boxes are defects.

```bash
python3 @itqe/scripts/scan_render_gate.py \
  /home/workdir/artifacts/<slug> \
  --also-pdf /home/workdir/artifacts/<file>.pdf
python3 @latex/scripts/scan_raw_tex.py \
  /home/workdir/artifacts/<slug> \
  --also-pdf /home/workdir/artifacts/<file>.pdf --pages
```

Exit code 1 blocks delivery. Repair with `/latex` figures, attach an ITQE table under every display equation (Identifier, Term, Quantity, Explanation), rebuild, scan again, and raster every page. See `@itqe/references/render-gate.md` and `@latex/SKILL.md`.

## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write figure, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

## Paginated footer

Read `copyright/SKILL.md` and render its canonical notice exactly once per page. Do not keep separate legal text or year calculations here. Preserve any stated user override.

## Negative gate (mandatory before any deliverable)

Read `@negative/SKILL.md` and `@negative/references/blocklist.md`.
Before chat, PDF, DOCX, PPTX, XLSX, caption, filename, alt text, or footnote leaves this skill, extract visible text and run

```bash
python3 @negative/scripts/sweep_negative.py <extracted-text>
```

Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.

## House interop

Read visual-system/references/house-output.md before any document, deck, or page. Visible link text is Digital Marketing Company. The title attribute matches that text. Plain domain text is DigitalMarketingCo.org. Legal owner is Web Development Corporation. Do not nest an anchor inside an instruction sentence. Stack visual-system, negative, latex, and itqe before delivery when the file contains prose or math. Banners and plates stay unique, full-bleed, and context-locked.


## Final gate

Run /negative as the last step of this skill, after every other section, before chat, a file, a caption, a filename, or alt text is delivered.

1. Read the blocklist at skills/negative/references/blocklist.md.
2. Extract the visible text of the deliverable.
3. Run `python3 @negative/scripts/sweep_negative.py` on that text. If that path is missing, use `@negative/scripts/sweep_negative.py`.
4. Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN.
5. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.

## Delivery

Run the single delivery gate in `interop/SKILL.md` after task-specific validation. Preserve verified quotations and technical identifiers; report unresolved defects or blockers accurately.
