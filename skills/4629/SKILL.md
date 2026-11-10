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

## Automatic post-document ITQE, LaTeX, and domain QA
After creating or transforming every document, render and execute `skills/references/post-artifact-itqe-latex-qa.md` alongside the preexisting `skills/references/document-rendering-9491.md` standard. This is mandatory, not an optional design check: enumerate and verify every significant equation, run post-creation /ITQE and /latex, inspect all exported pages/slides (including all mathematics), apply format-specific QA, fix defects, re-render, and require two complete clean evidence-backed passes before claiming verification. Record unexecuted checks as NOT TESTED and blockers explicitly. Preserve design precedence, image uniqueness, citations, single copyright authority, and accessibility. Present the optional post-run menu only after automatic QA and artifact delivery, never as a substitute for validation.

## /karma visual and document forensic learning
Apply `skills/karma/SKILL.md` to every document-specific visual, mathematical, accessibility, citation, image duplication and export error. Capture page/figure/equation identifiers and safe screenshots or diagnostics, create regression fixtures, verify fixes, and add prevention rules. Preserve originals, protect sensitive evidence, and record monitoring/storage as NOT DEPLOYED until configured and independently tested.

## Interactive styling without regression or truncation
Read `skills/references/document-error-prevention.md` before any new or revised document. Present the six-direction compact style plan with an optimal preselected default only when a fresh user style choice is appropriate; honor prior direction and /p or /disabled without interrupting. Preserve source manifest and complete sections through /expound iterations. Never remove substantial text to fit artwork; enforce pre/post-export completeness checks, unique figure IDs, single footer owner, and the full post-export QA gate. /karma records and reproduces observed errors; only verified fixes become prevention rules.

## Default electric cyan / midnight navy animated experience
For web, interactive presentations, holographic modals and product imagery use `skills/references/4629-electric-cyan-motion.md` as the recommended default visual profile: electric cyan and dark navy gradients, layered aurora and light-field motion, tasteful Siri-like animated modal border, optional gyro/touch parallax, reduced-motion static fallback, measured performance and visual QA. Respect previously chosen styles and never force animation into PDF/DOCX or source imagery. The referenced external admin-modal design was not accessible for verification; treat it solely as a conceptual inspiration rather than claiming visual fidelity.

## /God coordination and visual authority
When /God is active, /4629 retains sole visual direction authority and cooperates with the canonical cross-skill DAG in `skills/God/SKILL.md`; do not overwrite equations, citation numbering, copyright, or forensic evidence. Optimize cyan/navy visuals subject to user preferences, reduced motion, performance and document readability.


## Enforced original visual vision and release acceptance (2026-11-10)
Preserve the strongest coherent original /4629 design vision: an authoritative, futuristic, visually compelling document, never sacrificing scientific truth, accessibility, mathematical integrity, source completeness, or legibility. When several acceptable design variants exist, automatically select the highest-scoring output using the evidence-based visual QA rubric below; do not silently choose the first generated version. User-selected style takes precedence over defaults.

For every banner or full-bleed chapter image where the user requests the 16:9 treatment, require exactly 16:9 source and displayed content geometry (tolerance <= 0.1%); no stretching or distortion. For portrait pages, fit 16:9 across the full page width and preserve the ratio rather than stretching to fill the entire page height. Image must reach both physical left and right trim edges (tolerance <= 1 pt), with print bleed beyond trim where requested. Feather upper and lower boundaries smoothly into the actual adjacent page background, without visible hard edges, halos, color discontinuities, or white bands. Inspect rendered raster pixels at normal and magnified scales; do not accept merely having a CSS gradient or alpha mask in source. Explicit user requests for other geometry override these defaults.

Require a visual QA scorecard for candidate outputs: (1) scientific/content fidelity and completeness 25%, (2) typography/readability/accessibility 20%, (3) image relevance, uniqueness and detail 15%, (4) exact geometry/bleed/feather continuity 20%, (5) composition, visual coherence and hierarchy 10%, (6) rendering integrity and mobile readability 10%. All critical and major checks are hard gates: a high aggregate score cannot excuse a failed gate. Select the highest-scoring candidate only among passing variants. Record rubric scores, candidate hashes and rationale; do not claim comparative testing if only one variant was rendered.

Run /ITQE and /latex after artifact generation using the canonical post-artifact contract, with an equation registry and explicit scientific-validation limitations. Require two consecutive clean complete /qa and /visual_QA passes on the final exported artifact; inspect all pages, not just samples. Missing execution evidence is NOT TESTED, not PASS. Track source/output hashes, figure IDs, exact dimensions, edge coordinates, feather samples, page counts, defects, and corrective iterations in /karma. Prevent stale exports, duplicated footer ownership, image reuse without approval, source truncation, and accidental modification of verified mathematics. When runtime support is unavailable, report BLOCKED/NOT TESTED and do not falsely claim completion.

Engine compatibility: the current skills/4629/SKILL.md is the single canonical behavioral source; engines/4629/ENGINE.md must remain content-equivalent for all mandatory requirements. Changes to either entry point require a parity regression and review before release. Never downgrade the stronger instruction set when composing loaders.
