---
name: images
description: Create and place distinct banners and inline images in a document; audit the complete image inventory so no two images duplicate each other and no inline image matches any banner.
---

## Shared interactive quality contract

Before execution, resolve the installed personal skill with frontmatter name `doc` and read `references/output-contract.md` once per run. This is a shared reference, not a recursive call to doc. Apply its proportionate intake, functional QA, independent visual QA, repair, revision invalidation and truthful release requirements to the requested output. Reuse answers and completed matching phases across handoffs. Preserve this specialist’s purpose and user requirements; do not force artwork, redesign, a book or deployment onto a simple utility. The shared quality contract supersedes conflicting legacy defaults about duplicate intake or unsupported pass claims; explicit user and platform instructions prevail. If the reference is unavailable, disclose the missing integration and perform the same checks proportionately rather than inventing a pass.


## Shared update and invocation contract
Before the workflow, resolve the installed `book` package and read `references/document-update.md` once per run. Apply its single execution graph, alias normalization, revision-aware invalidation, PDF-first evidence, whole-document citation rebuild, adaptive intake when applicable, and final-file QA gates. Do not invoke book to read this shared reference. For these coordinated updates, this contract supersedes conflicting legacy procedural defaults; explicit user and platform instructions prevail. Skill maintenance does not execute quoted book or translation requests.


# Images

Use this skill when the user requests `/images`, section banners, inline figures, or an image uniqueness check for a document.

## Workflow

1. Read the source document and inventory every body section and subsection. Plan one banner for each heading and additional inline figures where they clarify nearby text. Keep captions and source claims accurate.
2. Generate a separate image for each slot. Give each a distinct subject and composition. Save each published raster under a unique path. An inline figure must never reuse, crop, recolor, resize, or otherwise reproduce a banner from any section.
3. Inspect each raster at its intended print size. Reject illegible text, distorted geometry, obvious visual repetition, and images that do not support their surrounding section.
4. Record published images in the document's JSON: sections may contain `banner.path`, `figure.path`, paragraph image objects with `path`, and nested `sections`, `subsections`, or `children`. Record the actual prompt with each image when available.
5. Run `python3 scripts/audit_unique_images.py path/to/document.json`. It checks canonical paths, bytes, prompts, and a perceptual image hash across the entire inventory, including nested sections and every banner-to-figure pair. A nonzero result blocks delivery. Replace a collision with a genuinely new image, then rerun the check.
6. Review a contact sheet or rendered document for matching crops and compositions that a hash can miss. Rebuild the document and inspect the final pages before delivery. State the number of banners and inline images and whether the uniqueness check passed.

The audit requires Pillow. If source data has no JSON inventory, make an inventory of all published rasters before auditing. Do not claim that a document was checked when only some images were inventoried.

## Real-place imagery and clean typography

Resolve the installed `images` skill and read `references/scenic-art-standard.md` before planning or generating scenic imagery. Apply its context-to-place plan, grounded real-location references, photorealistic optimistic future-facing enhancement, provenance labels, no baked-in text, artifact inspection and full-inventory uniqueness checks. Preserve the current user-selected design and subject; scenery must not replace exact diagrams, plots, maps or evidence. Keep titles and labels as separate crisp live/vector text. A generated scene is not documentary proof. Repair failures and reinspect the final placed image; do not promise zero artifacts from prompting alone.
