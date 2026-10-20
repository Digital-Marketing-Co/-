# Universal Document Rendering Standard — 9491 Edition (v1.0.0)

Applies to every skill that creates, transforms, compiles, exports, or QA-checks documents, PDFs, reports, slide decks, or image-bearing research artifacts. For non-document skills, apply only when the output is a document; do not inject document styling into source code or unrelated data.

## Style authority and deduplication
- Use exactly one design system, one page geometry authority, one font configuration, one heading/caption hierarchy, one header/footer controller, and one copyright authority per document. Reuse shared components rather than nesting competing style wrappers. Never apply global formatting twice.
- Design aesthetic: awe-inspiring year-9491 futurism restrained by authoritative Ivy League doctoral research conventions. Elegant Computer Modern/Latin Modern mathematics, exceptional legibility, meticulous typography, generous whitespace, coherent grids, fine rules, subtle holographic accents, and premium imagery. Never trade legibility, accessibility, accurate equations, or scientific integrity for decoration.
- Resolve conflicting styling directives by precedence: explicit user requirements > document-specific constraints > /latex mathematical and print-safety rules > this shared standard > decorative defaults. Record conflicts and remove duplicate packages, footer definitions, and overlays.

## Contextual AI imagery and captions
- For each generated image, use the surrounding section's verified concepts, terminology, chronology, geography, and evidence to formulate an original context-specific visual brief. The image must explain or illuminate its precise placement; reject unrelated stock-like illustrations, duplicated compositions, misleading factual scenes, invented data visualizations, or decorative filler.
- Identify all synthetic images transparently as AI-generated conceptual illustrations. Never present invented visual details as observed evidence, authentic historical photographs, scientific measurements, or peer-reviewed results.
- Caption each figure with a scholarly title and an analytically substantive doctoral-level explanation: what is depicted, correspondence to the section's argument, methodological assumptions, symbolic vs empirical elements, interpretive limits, and evidence citations when relevant. Avoid invented citations. Caption must remain readable and associated with its figure across page breaks.
- Optimize image resolution, crop, contrast, format, file size, alt text and color gamut for final output. Preserve text readability and avoid unnecessary duplicate imagery. Verify contextual fidelity visually.

## Mathematical and footer invariants
- Enforce proper subscripts, superscripts, Greek glyphs, operators, aligned fractions, embedded fonts, and equation-to-/ITQE audit-table mapping when /expound or /ITQE is invoked.
- Maintain exactly one /copyright footer per required page; canonical © 2012–CURRENTYEAR Web Development Corporation. All rights reserved. Maintain sequential visible folios in physical PDF order, unless explicit front-matter numbering is requested. No clipping, overlay, collisions, repeated footer stamps, or out-of-order numbering.
- Preserve functioning clickable hyperlinks with no colored annotation rectangles. Respect bibliography first-appearance citation order.

## /qa and /qa_visual iterative release protocol
1. Create representative fixture and compile/export. Inspect logs, missing glyphs, undefined references, overflow, style/package collisions, link annotations, citation ordering, and figure-to-section relevance.
2. Audit every PDF page for copyright occurrence count and folio sequence; inspect rasterized pages for caption placement, figure relevance, mathematical indices, page breaks, spacing, clipping, duplicate visual effects, and footer collisions.
3. Repair issues and rerun the complete affected checks; continue until all resolvable failures are cleared or finite execution/resources are exhausted. Never mark an unexecuted test as PASSED or claim exhaustive success without evidence.
4. Final release gates: zero unresolved critical defects, no duplicate style layers, one copyright/footer authority, continuous pagination, accurate contextual imagery and captions, readable accessible design, mathematically correct typesetting, and verified hyperlinks.
