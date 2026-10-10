---
name: bleed
description: Print a webpage as a PDF of full-bleed snippet images with zero margin on every image and banner, site chrome removed, and no image or heading split. Use when the user types /bleed, asks for a full-bleed page print, or wants a site reprinted as images with no header, nav, sidebar, floating button, or footer.
---

# /bleed — Full-bleed snippet print

## Quality and capability additions

Read [the task-specific quality profile](references/quality-profile.md) before execution. Use `evals/quality-cases.json` for regression scenarios; its assertions are acceptance criteria, not claims that tests have run. Shared path resolution and output rules live in `interop/SKILL.md`.


Print a URL as a PDF of painted page snippets. Each snippet is an image of the remaining content and the background under it. Images and banners sit at zero margin on the top, right, bottom, and left. Site header, navigation, sidebar, floating button, and footer are removed. The PDF draws none of those either.

Use this skill when the user types `/bleed`, asks for a full-bleed webpage print, or wants the page reprinted as images without cutting a figure or leaving a section heading above a page break.

`<skill>` resolves with `interop/scripts/resolve_root.py bleed` (live host: `@bleed`).

Work in `/workspace/artifacts/<slug>/`. Final PDF is `/workspace/artifacts/<YYYY-topic-slug-wca-bleed.pdf>`.

If the user only asked to create or revise this skill and supplied no URL, stop after the skill files exist. Do not invent a page.

This skill overrides the running-footer rule. Do not stamp a header or footer unless the user later stacks `/copyright`.

## Read on demand

- `references/layout.md` — bleed, no mid-image split, heading keep-with-next

## Workflow

### 1. Capture

```bash
node <skill>/scripts/capture_bleed.mjs "URL" --out /workspace/artifacts/<slug>
```

The script opens Chromium, hides header, nav, sidebar, floating controls, and footer, then writes `manifest.json` and `snippet-NN.png`.

- A banner or in-content image is its own plate when it is not already the whole snippet.
- A section plate includes the painted background and the content on it.
- A heading is never the last item on a plate. The following paragraph or figure stays with it.
- An image is never sliced. If it is taller than a normal plate, the page grows to hold it.

Review `manifest.json`. Delete a plate that is still chrome. Do not invent captions.

### 2. Build

```bash
python3 <skill>/scripts/build_bleed_pdf.py \
  /workspace/artifacts/<slug>/manifest.json \
  --out /workspace/artifacts/<YYYY-topic-slug-wca-bleed.pdf>
```

The builder sets each page box to the image. Draw origin is 0, 0. Width is 8.5 in. Height follows the bitmap ratio. No crop, no matte, no footer.

### 3. Visual QA

```bash
pdftoppm -png -r 72 /workspace/artifacts/<YYYY-topic-slug-wca-bleed.pdf> /tmp/bleed-page
pdfinfo /workspace/artifacts/<YYYY-topic-slug-wca-bleed.pdf>
```

Rebuild if any of these appear: a site header, nav, sidebar, floating button, or footer; a page margin around an image; an image cut in half; a heading alone at the bottom of a page; a new page that starts with the paragraph that belonged under the previous heading.

### 4. Deliver

Give the user the PDF. State page count and snippet count. Do not dump the manifest into chat.

## Hard rules

- No site header, navigation, sidebar, floating button, or footer in the capture or the PDF.
- Banner images and images inside text print at 0 margin on all four sides.
- The snippet image is the painted background plus the content on it, not a reflowed text column.
- Do not cut an image across pages. Do not crop a plate to force a letter height.
- Do not start a new page after a section or subsection heading. Keep the next paragraph or figure on that same plate.
- No emoji. No invented captions.
- Public filename is YYYY-topic-slug-wca-bleed.pdf.

## Updating this skill

Revise in place. Do not create bleed-v2/.

1. Edit SKILL.md, references/, or scripts/ at this path.
2. Bump metadata.version.
3. Run `python3 /usr/share/grok/bundled-skills/bundled__postmortem/scripts/validate-skill.py @bleed`.

## Render gate

Before delivering a PDF that may contain notation, run the house render gate. Chat may use KaTeX. Files must show compiled glyphs or a compiled figure.

```bash
python3 @itqe/scripts/scan_render_gate.py \
  /workspace/artifacts/<slug> \
  --also-pdf /workspace/artifacts/<file>.pdf
python3 @latex/scripts/scan_raw_tex.py \
  /workspace/artifacts/<slug> \
  --also-pdf /workspace/artifacts/<file>.pdf --pages
```

Exit code 1 blocks delivery. See `@latex/SKILL.md`.

## Publication checks

Apply `interop/SKILL.md` once after the task-specific checks. Its shared rules yield to this skill's explicit format and source-fidelity requirements.

## Delivery

Run the single delivery gate in `interop/SKILL.md` after task-specific validation. Preserve verified quotations and technical identifiers; report unresolved defects or blockers accurately.
