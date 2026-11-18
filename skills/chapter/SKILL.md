---
name: chapter
description: Create a contextually relevant, document-native full-bleed background on the actual first page of each chapter, PDF by default.
---
# /chapter v2.1 — Document-native chapter opening

## Invocation
`/chapter [document or chapter]`; aliases `/Chapter` and `/CHAPTER`. When invoked with no supplied manuscript, request the needed source or operate on the current available document. PDF is the default final format unless explicitly overridden.

## Non-negotiable placement
The background belongs **on the actual first page containing the chapter number, heading, and beginning of substantive chapter content**, not on a separate decorative cover page. Preserve chapter text, equations, references, tables, figures, citations, numbering, and bookmarks. Later pages follow normal layout.

## Geometry-first workflow
1. Determine the exact output page dimensions, orientation, section-specific variations, and trim/bleed requirements before image generation.
2. For PDF read or set MediaBox, CropBox, TrimBox, and BleedBox appropriately. For DOCX use section page geometry and verify export; PPTX uses slide dimensions; HTML uses viewport and print CSS; reflowable EPUB uses responsive imagery and must not claim a fixed universal aspect ratio.
3. Compute `ratio = page_width / page_height` in consistent units. The image must fill the full page or bleed region, not merely the text margins. For print, minimum pixels are `ceil(width_inches * PPI)` by `ceil(height_inches * PPI)`, preferably at 300 PPI when practical.
4. Generate an original, contextually relevant image from the chapter title, headings, and substantive content. Use composition-aware focal points and negative space behind text. Do not depict unsupported scientific or historical claims as verified evidence.
5. If native image generation cannot match the exact ratio, outpaint or use controlled, focal-safe crop without stretching. Verify the placed image covers all four edges with no letterboxing, clipping of important subjects, white strips, or seams.
6. Layer chapter heading and opening paragraphs above the image with legible contrast, accessible typography, and appropriate overlays. A bottom alpha fade is optional but must not expose blank paper unintentionally.
7. For print-ready PDF, extend background through required bleed beyond trim, and validate effective resolution. For digital PDFs, ensure page-edge coverage without assuming a printer bleed requirement.
8. Preserve pagination intent including deliberate recto starts; avoid unintended blank pages or duplicated chapter openings.

## QA and visual QA
- Inventory all chapters and map each to its first page and image provenance.
- Compare source versus exported content for omissions, duplications, and reordered material.
- Validate page boxes, target versus effective aspect ratios, pixel resolution, edge coverage, and readability.
- Render every chapter-opening page in the final format and inspect for margins, seams, obscured headings, clipping, incorrect page orientation, and bad gradients.
- Run two clean QA and visual QA passes when tooling supports them; record failures and bounded corrections without recursively calling /iterate.
- Check image licensing, accessibility, metadata, and source attribution where applicable.
- Report exactly which checks ran and which could not run. Never claim visual verification from source-only inspection.

## Deliverables and completion
Provide the completed document (PDF by default), plus a chapter-image manifest, geometry summary, and QA report when appropriate. Provide editable sources or separate images when requested. `C = Complete` only after all applicable deliverables exist and final rendered checks pass; otherwise label implementation or verification pending.
