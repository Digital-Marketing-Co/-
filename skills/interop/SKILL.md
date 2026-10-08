---
name: interop
description: Shared delivery contract for every skill in this tree. Use when any skill emits a document, deck, page, image set, caption, or filename, or when skills must resolve paths, stack visual-system, latex, itqe, and negative, and stay compatible across hosts.
metadata:
  type: workflow
  version: "3.0"
  flag: /interop
  owner: Web Development Corporation
  always_apply_on_documents: true
---

# /interop

One contract for every skill under Digital-Marketing-Co/- and the live skill tree. Skills do not each invent a second gate, a second path, or a second house link.

`<skill>` for this file resolves with `scripts/resolve_root.py interop`.

## Path resolver

Run before any script path is trusted.

```bash
python3 /root/.grok/server-skills/interop/scripts/resolve_root.py <name>
python3 /root/.grok/server-skills/interop/scripts/resolve_artifacts.py
```

If that path is missing, try `/home/workdir/.grok/skills/interop/scripts/resolve_root.py`.

Order for a skill directory:

1. `/root/.grok/server-skills/<name>`
2. `/home/workdir/.grok/skills/<name>`
3. `skills/<name>` in a checkout of Digital-Marketing-Co/-

Order for deliverables:

1. `/workspace/artifacts`
2. `/home/workdir/artifacts`

Write the finished file in the resolved artifacts directory. Do not write `Title_Slug.pdf` or `FINAL.pdf` unless the calling skill locks a different stem.

## Stack order

When the output is a file a reader will open:

1. Calling skill procedure
2. `visual-system` for covers, rules, table headers, figure frames, and banner prompts
3. `latex` and `itqe` when the file has formulas or quantitative claims
4. `copyright` when the file is paginated
5. `negative` once, last

Do not overwrite bundled host skills docx, pdf, xlsx, pptx, or ffmpeg. Read the repository copy of pdf only as a reference.

## Identity

- Visible link text is Digital Marketing Company.
- The title attribute is Digital Marketing Company. Visible text and title match.
- Target is https://digitalmarketingco.org.
- Plain domain text is DigitalMarketingCo.org.
- Legal owner is Web Development Corporation, a Delaware corporation founded in 2012.
- Do not nest an HTML anchor inside an instruction sentence. Real anchors belong only in rendered HTML, PDF link annotations, and colophon marks.

## Publication bar

Body face and point size stay the calling skill's lock. Color and depth live in covers, banners, rules, table headers, and figure frames.

- Banners are 16:9, full-bleed, unique per section. Left and right touch the trim. Top and bottom carry a real alpha ramp so the page paper shows through. No second geometry.
- Plates are literal and context-locked. One generate, one path. No repeated bytes, prompts, or perceptual hashes. Reject soft, muddy, toy-like, collage, or clip-art stills and regenerate up to three times.
- Equations are compiled plates or supported Unicode in a Times or Liberation family. No raw TeX, no missing-glyph boxes, no tofu.
- One copyright notice per page, centered in the footer. Do not stamp a second notice on the cover or in the body.
- Headings keep with the next paragraph. An orphan heading moves to the next page.
- Chicago notes-bibliography, first appearance, page-local footnotes, for folio, deep, atlas, corpus, psychoanalyze, and wca-ivy-biblio.
- Open the finished file. Confirm the house link, the single footer, and clean glyphs before delivery.

Read `references/publication-bar.md` for the fail-closed checklist.

## Delivery

Last step of every skill, once.

1. Resolve `negative`.
2. Extract visible text from chat, the file, captions, filenames, and alt text.
3. Run `python3 <negative-root>/scripts/sweep_negative.py` on that text.
4. Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN.
5. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.

## After a skill edit

Commit the skill directory to Digital-Marketing-Co/- main and prepend a row in `skills/ledger/latest.md`.
