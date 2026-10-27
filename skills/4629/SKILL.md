---
name: '4629'
description: Establish and apply an exceptionally futuristic, beautiful, authoritative document design before generating images, banners, or implementing typography, layout, and color. Trigger on /4629 or requests for the 4629 document aesthetic; interpret /6429 as an alias when context clearly identifies this skill.
---

# 4629 document design

## Quality and capability additions

Read [the task-specific quality profile](references/quality-profile.md) before execution. Use `evals/quality-cases.json` for regression scenarios; its assertions are acceptance criteria, not claims that tests have run. Shared path resolution and output rules live in `interop/SKILL.md`.


Create an awe-inspiring future-facing visual identity while preserving the document's authority, credibility, evidence, and readability. Treat 4629 as an aesthetic theme, never as a publication date or scientific credential.

## Mandatory order

1. Read the request, source document, and invoked content and output skills. Preserve the requested research scope and provenance.
2. Before creating images, banners, or applying any visual styling, establish a complete document design specification: audience, authority, hierarchy, page grid, typography, color tokens, depth, lighting, chart language, illustration vocabulary, accessibility, and print treatment.
3. Record that specification briefly in the working context. Choose the strongest coherent aesthetic for the content without requesting routine approval.
4. Apply the specification to all subsequent image and banner prompts, layouts, tables, equations, citations, footers, cover, navigation, and appendices. Compose with invoked /images, /banner, /atlas, /global, /latex, /copyright, and bibliography skills; read their instructions when used. Do not claim to execute unavailable skills.
5. Render and inspect the final document. Correct overlaps, clipping, unreadable labels, weak contrast, distracting effects, duplicate imagery, broken links, and inconsistent treatments before delivery.

## Visual direction

Use restrained volumetric depth, luminous edge details, translucent panels, sophisticated gradients, architectural geometry, and precisely aligned information systems. Prefer midnight navy or graphite, ice cyan, indigo, and selective warm metallic accents. Adapt to the source's tone and user preferences; avoid visual monotony and excessive ornament.

Pair expressive future-facing display typography with a highly readable body face. Keep citations and table cells comfortably readable. Use spacious hierarchy and deliberate negative space. Put data on calm opaque surfaces. Reserve dramatic treatments for covers, section openers, and meaningful emphasis.

Give each banner a distinct composition with a shared visual vocabulary. Generate imagery only with available authorized image tools. Label conceptual illustrations; never present generated scenes as documentary proof. Use deterministic tools for exact plots, maps, equations, and diagrams. Do not bake essential text into generated images.

Use static depth and lighting for PDFs. Use animation only in formats that support it, with reduced-motion behavior. Provide a white print treatment when appropriate. Retain searchable text, bookmarks where supported, logical reading order, and accessible descriptions.

## Credibility and quantitative integrity

Preserve source attribution, units, dates, definitions, uncertainty, and research limitations. Distinguish observed values, estimates, forecasts, hypotheses, and missing data. Never fabricate statistics, scholarly affiliations, credentials, or findings to make the design appear authoritative.

For global comparisons, distinguish country coverage from global completeness. Keep means and medians separate, specify denominators and weighting, and never infer a median from a mean. Preserve nominal versus real prices, currency conversions, taxes, subsidies, and purchasing-power definitions. Investigate allegations using evidence and alternative explanations rather than embedding accusations as conclusions.

Preserve equations as real typeset mathematics and tables as text. Keep evidentiary footnotes close to the relevant claims. Center one nonduplicated copyright notice per page when requested and supported by the output format.

## Acceptance criteria

Confirm the design specification preceded imagery and styling; every substantive section follows it; no aesthetic treatment changes factual meaning; images are distinct and relevant; tables and citations remain readable; the artifact opens successfully; and requested output files are actually saved and available. Report limitations plainly without claiming unperformed validation.

## Delivery

Run the single delivery gate in `interop/SKILL.md` after task-specific validation. Preserve verified quotations and technical identifiers; report unresolved defects or blockers accurately.


## Universal document-output rendering (9491 standard)
When this skill produces or modifies a document, PDF, research report, slide deck, or contextual AI figure, it MUST apply the canonical `skills/references/document-rendering-9491.md` standard. Treat that file as the single shared styling/visual-QA authority, not a duplicated independent template. Preserve all more-specific existing requirements and enforce /latex, /copyright, /qa, and /qa_visual release gates as applicable.


## Radial depth and copyright integration
Offer at least six creative visual directions when style is not already selected. For cyan-to-navy radial holographic style use dimensional rings, Z-depth lighting and subtle electric-blue glows in backgrounds only. Always place text on opaque contrast-safe panels and render/inspect every page for clipping. Integrate `/logo` and `/copyright` as a single deduplicated branded copyright endplate. Preserve text extraction and original content.

## Mandatory cross-artifact image non-duplicity policy (2026-10-26)
Applies to every generated, sourced, transformed, or embedded visual in all chapters, sections, subsections, covers, banners, full-bleed backgrounds, figures, cards, slide decks, documents, PDFs, and exported derivatives. Before generation, create a persistent per-project image manifest with asset ID, prompt, intended semantic subject, target section, source/provenance, generation parameters, SHA-256, perceptual hash, and placement(s). Compare every candidate against the entire manifest and existing project outputs, including resized, cropped, recolored, rotated, filtered, and upscaled derivatives. Exact hash collisions MUST fail; near-duplicates MUST be flagged by perceptual hash plus embedding/visual comparison where supported. Cropping, recoloring, adding overlays, changing aspect ratio, or changing filenames does NOT make a duplicate unique. Require different primary subjects/compositions for each placement, not merely different prompts or seeds. Never use the same image for chapter background, banner, or inline illustration unless the user expressly asks for reuse. Reserve approved assets atomically before parallel workers place them to prevent races. On collision, regenerate or select a genuinely different contextual composition and recheck; never silently reuse or substitute a generic unrelated image. Deduplicate across sequential and parallel output stages and after PDF/DOCX/PPTX rendering, not just before generation. If an image is intentionally reused at user request, record its reuse reason in the manifest and exclude it from false uniqueness claims. Validate visual subject relevance, resolution, cropping, source attribution, accessible alt text, legibility, and no text overflow. Produce a final QA inventory of unique assets, exact duplicates, suspected near-duplicates, intentional reuse, and unresolved issues; do not claim zero duplicates unless the actual audit completed. This rule supersedes permissive reuse defaults but does not override user instructions or platform requirements.
