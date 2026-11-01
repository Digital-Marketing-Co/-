---
name: chapter-banner
description: Create distinct AI-generated 16:9 chapter-opening images, full bleed at the top, left and right, with a smooth bottom alpha fade reaching complete transparency at 99 percent of image height. Use for /chapter-banner, /banner, /banners, pre-chapter cinematic banners, or this chapter-art treatment in books and reports.
---

## Shared interactive quality contract

Before execution, resolve the installed personal skill with frontmatter name `doc` and read `references/output-contract.md` once per run. This is a shared reference, not a recursive call to doc. Apply its proportionate intake, functional QA, independent visual QA, repair, revision invalidation and truthful release requirements to the requested output. Reuse answers and completed matching phases across handoffs. Preserve this specialist’s purpose and user requirements; do not force artwork, redesign, a book or deployment onto a simple utility. The shared quality contract supersedes conflicting legacy defaults about duplicate intake or unsupported pass claims; explicit user and platform instructions prevail. If the reference is unavailable, disclose the missing integration and perform the same checks proportionately rather than inventing a pass.


## Shared update and invocation contract
Before the workflow, resolve the installed `book` package and read `references/document-update.md` once per run. Apply its single execution graph, alias normalization, revision-aware invalidation, PDF-first evidence, whole-document citation rebuild, adaptive intake when applicable, and final-file QA gates. Do not invoke book to read this shared reference. For these coordinated updates, this contract supersedes conflicting legacy procedural defaults; explicit user and platform instructions prevail. Skill maintenance does not execute quoted book or translation requests.


# Chapter Banner

Establish the document design before generating artwork. Inventory chapters and assign one meaningful, distinct scene and filename per chapter. Generate each scene separately using the available image-generation tool; never substitute a collage, repeated image, crop of another chapter image, or programmatic scenery.

Default to grounded cinematic photorealism of contextually relevant real places, with optimistic and prosperous future-facing enhancements. Use psychedelic treatments only when explicitly requested. Keep essential labels and scholarly claims outside the artwork. Preserve original character designs where continuity matters. Identify generated art as conceptual illustration. Record actual clip URLs and observed timestamps for film references; never claim to inspect screenshots that were not inspected.

Compose an exact 16:9 banner at page width with no top, left or right margins. Crop minimally using cover behavior; never stretch faces. Prepend the banner before chapter content. Keep body text on a high-contrast, quiet surface below the banner. Do not put text into the fading region.

Keep alpha 1 from normalized vertical position 0 through 0.40. From 0.40 to 0.99 use a smoothstep fade: let t=(y-0.40)/0.59, then alpha=1-3*t*t+2*t*t*t. Set alpha 0 from 0.99 through 1. Apply a genuine alpha mask in supported web output. For PDFs, composite the same fade onto the page background using PDF transparency; distinguish that compositing effect from a standalone transparent PNG. Use scripts/banner.css for web rendering.

For a requested standalone transparent PNG, use image generation/editing with transparent_background=true and inspect its alpha. Do not promise an exact pixel mask from an unverified generative result.

Audit every banner: exact display ratio 16:9; distinct source and composition per chapter; complete chapter coverage; no duplicate imagery; complete bottom fade at 99%; no clipping or unreadable text. Render and inspect every chapter opening. Save user-facing deliverables using the current Library workflow. If edited in the Work Skills git workspace, validate, commit only this skill folder, and push the current branch.

## Real-place imagery and clean typography

Resolve the installed `images` skill and read `references/scenic-art-standard.md` before planning or generating scenic imagery. Apply its context-to-place plan, grounded real-location references, photorealistic optimistic future-facing enhancement, provenance labels, no baked-in text, artifact inspection and full-inventory uniqueness checks. Preserve the current user-selected design and subject; scenery must not replace exact diagrams, plots, maps or evidence. Keep titles and labels as separate crisp live/vector text. A generated scene is not documentary proof. Repair failures and reinspect the final placed image; do not promise zero artifacts from prompting alone.
