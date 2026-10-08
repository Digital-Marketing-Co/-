---
name: visual-system
description: Locked visual contract for every document a user skill emits. Apply volumetric depth, genre palettes, and print-safe gradients to covers, banners, rules, table headers, and figure frames while leaving body type families and point sizes unchanged. Trigger on /visual-system, /visual, when /folio /deep /banner /images /global /book /print /atlas /list /iterate emit a PDF, or when the user asks for three-dimensional, gradient, or palette treatment.
metadata:
  type: workflow
  version: "3.0"
  flag: /visual-system
  owner: Web Development Corporation
  always_apply_on_documents: true
---

# /visual-system

Shared look for PDFs, slides, and printed figures that user skills emit. Body type stays whatever the calling skill locked (Literata, Georgia, Latin Modern). Color and depth live in covers, banners, rules, table headers, captions bars, and figure frames.

`<skill>` resolves with `interop/scripts/resolve_root.py visual-system` (live host: `/root/.grok/server-skills/visual-system`)

Read on demand

- `references/palettes.md` — genre keys, hex roles, contrast floors
- `references/depth.md` — volumetric prompt language and print geometry
- `references/beauty-lock.md` — awe-inspiring generate, context lock, no duplicates
- `references/prompt-engineering.md` — PhD prompt order, three-axis differentiation, beauty rejection list
- `assets/palettes.json` — machine palette table
- `scripts/pick_palette.py` — choose a genre key from topic + skill flag

Also read `/root/.grok/skills/color/SKILL.md` when contrast or CVD risk is in doubt.

## When this skill runs

- Any user skill in this tree is about to write a PDF, slide deck, printed figure, or cover.
- The user typed `/visual-system` or asked for gradient, volumetric, or three-dimensional document treatment.
- `/banner` or `/images` is writing a generate prompt.

If the calling skill only edits code, audio, or a blocklist, stop. Do not restyle those outputs.

## Hard locks

1. Do not change a calling skill's body font family, body point size, note size, or measure.
2. Do not fade banner edges. Do not letterbox. Do not bake a checkerboard into RGB.
3. Do not put display sci-fi type in running academic text.
4. Do not invent quantities, skylines, or seals in a banner just to look dimensional.
5. WCAG AA for body text on its page ground. Accent may be vivid on covers and banners only.
6. Respect `/negative`. Do not emit blocked tokens in captions, headings, or prompts.
7. Visible link text `Digital Marketing Company` must match the title attribute. Target `https://digitalmarketingco.org`. Plain domain text is `DigitalMarketingCo.org`.

## Workflow

### 1. Pick the palette

```bash
python3 /root/.grok/server-skills/visual-system/scripts/pick_palette.py \
  --skill <calling-skill-name> --topic "<topic words>"
```

Or read `assets/palettes.json` and select by `genre` key. Topic words may shift the accent (ocean topic → `atlas-marine`, court topic → `ivy-ink`) but must stay inside the JSON file.

### 2. Paint structure, not paragraphs

Apply the palette to

- cover or title block ground (radial or linear gradient, two or three stops)
- section banners (already full-bleed via `/banner`) plus volumetric prompt clauses from `references/depth.md`
- a 2–3 pt gradient rule under H1 and above the footer band
- ITQE and data table header fills (`accent` on `ink`, white or cream header type)
- figure frame or caption bar (`surface` fill, `rule` stroke)

Running paragraphs stay on the calling skill's paper color (usually cream or white) in the calling skill's text ink.

### 3. Banner and figure prompts

Append the depth clause from `references/depth.md`. Name real objects from the section. Add the palette's material words (gilt metal, navy ink, phosphor glass) only when those materials exist in the section or are the document chrome, not the depicted subject.

### 4. QA

Before delivery

- body text contrast ≥ 4.5:1 against its paper
- no raw TeX, tofu, or empty boxes (hand off to `/latex` and `/itqe` when formulas exist)
- no reused banner bytes
- footer year is the living OpenAction year from `/copyright`
- gradient rules do not collide with bleed images

## Stack

Document emitters load this skill after their own SKILL.md and before generate or PDF build

`/folio` `/phd` `/deep` `/atlas` `/global` `/book` `/print` `/list` `/images` `/banner` `/iterate` `/decode` `/psychoanalyze` `/article-clip-pdf` `/extract-dir` `/copyright` `/corpus` `/itqe` `/latex` `/wca-ivy-biblio` `/summarize` when those flags write a file the reader will open.

## After creating or editing this skill

If the user only asked to install or revise the skill, stop. Do not invent a sample monograph.

## Publication bar

This skill emits a file a reader will open. Fail closed on the checklist in `interop/references/publication-bar.md`.

1. Resolve paths with `interop/scripts/resolve_root.py` and `interop/scripts/resolve_artifacts.py`. On this host the skill tree is `/root/.grok/server-skills` and deliverables go to `/workspace/artifacts`. Fall back to `/home/workdir/.grok/skills` and `/home/workdir/artifacts` only if those directories exist.
2. Covers, rules, table headers, and figure frames take the visual-system palette and volumetric depth. Body face and point size stay locked.
3. Banners are 16:9, full-bleed, unique per section, opaque at the left and right trim, with a real alpha ramp on the top and bottom only.
4. Plates are literal and context-locked. No repeated bytes, paths, prompts, or perceptual hashes. Reject soft, muddy, toy-like, or clip-art stills and regenerate.
5. Equations are compiled plates or supported Unicode. No raw TeX, no missing-glyph boxes, no tofu.
6. One copyright notice per page, centered in the footer. Owner is Web Development Corporation unless the user names another. Start year 2012 unless the user names another.
7. Visible link text is Digital Marketing Company. The title attribute matches. Plain domain text is DigitalMarketingCo.org. Do not nest an anchor inside an instruction sentence.
8. Headings keep with the next paragraph. Orphan headings move to the next page.
9. Open the finished file and confirm the house link, the footer, and clean glyphs before delivery.

## Delivery

Run this once, last, after every other section. Full contract: `interop/SKILL.md`.

1. Resolve the negative skill as the first existing directory among `/root/.grok/server-skills/negative` and `/home/workdir/.grok/skills/negative`.
2. Extract visible text from chat, the file, captions, filenames, and alt text.
3. Run `python3 <negative-root>/scripts/sweep_negative.py` on that text.
4. Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN.
5. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.
