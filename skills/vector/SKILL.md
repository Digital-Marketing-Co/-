---
name: vector
description: Turn an attached or referenced raster or document page into an SVG vector graphic whose letterforms stay sharp at any zoom. Use when the user types /vector, asks to vectorize an image, wants live or outlined text from a poster, or needs an SVG/PDF of a chart so every label stays legible. Stacks after /upscale when a larger baseline exists.
---

# /vector

## Quality and capability additions

Read [the task-specific quality profile](references/quality-profile.md) before execution. Use `evals/quality-cases.json` for regression scenarios; its assertions are acceptance criteria, not claims that tests have run. Shared path resolution and output rules live in `interop/SKILL.md`.


Convert one image or one document page into an SVG whose shapes and letterforms are real vector paths, plus live text nodes when OCR is confident. Do not overwrite the source.

`<skill>` resolves with `interop/scripts/resolve_root.py vector` (live host: `@vector`).
`<upscale>` = `@upscale`.

## When this skill runs

- User typed /vector and pointed at an image, a PDF page, or a path.
- User asked for a vector graphic so on-image text stays crystal clear when the file is resized or printed.
- Extra type tokens after the flag (svg, pdf, png) are all written. SVG is always written.

If there is no file, stop and ask for one.

## What vector text means here

A dense poster cannot be trusted to Tesseract for every micro-label. Wrong live text is worse than a traced glyph.

Default path is visioncortex VTracer color spline. Every glyph becomes an outline. Outlines scale without blur. They are not editable type, but they keep the original spelling.

Live-text path — Tesseract words with confidence at or above 85 and box height at or above 14 source pixels become real SVG text on top of a cleaned patch. Large titles and sidebar paragraphs usually qualify. Tiny frequency ticks usually do not.

Always run both. Never replace a source glyph with a low-confidence OCR string.

## Source choice

Prefer an existing /upscale baseline when it is the same stem and RAM allows a long edge at or under 5400. Otherwise use the attached file. If the long edge is under 2000 px, run /upscale first, then vectorize that PNG.

PDF input — rasterize the requested page with pdftoppm at 300 dpi.

## Dependencies

If missing

```bash
pip install vtracer cairosvg -i https://pypi.org/simple
```

Tesseract `eng` is required for the live-text pass.

## Method

```bash
python3 @vector/scripts/vectorize.py \
  --input "/path/to/source.png" \
  --outdir /workspace/artifacts \
  --formats svg,png,pdf
```

Do not call ImageMagick convert to create the SVG. IM will only embed the bitmap. Rasterize with cairosvg. Do not send an SVG taller than 8000 px through IM convert.

## Output names

```
<stem>-vector.svg
<stem>-vector-preview.png
<stem>-vector.pdf
```

## After the script

1. Confirm the SVG contains path elements and, when OCR hit, text elements.
2. Rasterize a title crop and a small-label crop with cairosvg. Reject melted title letterforms.
3. Render the SVG, PDF, and preview PNG to the user.
4. State source size, SVG bytes, path count, live-text count, and extra formats.

## Honesty

Do not claim the file is a hand-redraw or that every micro-label is editable type. Say outlined letterforms plus live text where confidence cleared the gate.


## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write plate, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

## Delivery

Run the single delivery gate in `interop/SKILL.md` after task-specific validation. Preserve verified quotations and technical identifiers; report unresolved defects or blockers accurately.
