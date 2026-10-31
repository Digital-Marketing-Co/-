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


## /4269 compatibility and 20-option futuristic UX/CRO studio
Treat explicit /4269 as an alias for /4629 unless a separate canonical skill is subsequently defined. Preserve all existing /4629 authority and requirements.

On /4629, /4269, or /God invocations involving visual production, offer a **progressively disclosed** interactive design studio when selection is materially helpful; otherwise proceed using accessible recommended defaults. Do not block /p, D, or /disabled continuation on nonessential selections. Provide up to 20 distinct, meaningful options in each relevant dimension, not 20 mandatory questions. Offer more only when the interface can present them accessibly without decision overload.

Dimensions and recommended first options:
1. Visual theme: midnight-cyan, rainforest glass, orbital copper, alpine glass, underwater teal, pearl minimal, dark editorial, sunrise coral, holographic violet, botanical ivory, aurora indigo, graphite gold, terracotta cream, ocean cobalt, monochrome ink, solar amber, arctic silver, emerald obsidian, pastel prism, accessible high-contrast.
2. Typography: responsive editorial serif, humanist sans, geometric sans, accessible slab, neo-grotesk, variable serif, variable sans, technical mono accents, classic book, modern textbook, scientific notation, bilingual-ready, dyslexia-conscious, large print, compact dashboard, high-legibility UI, luxury display, newspaper, academic journal, minimalist.
3. Layout: narrative single column, split editorial, responsive cards, immersive chapter, dashboard grid, guided wizard, stepper, masonry gallery, interactive atlas, table-first, longform scrollytelling, paginated book, sidebar reference, comparative columns, cinematic hero, sticky contents, expandable sections, timeline, accessible reader, print-first.
4. Visual enhancement: subtle depth, user-requested parallax, static photography, holographic overlay, light-field gradient, cinematic banner, ambient video, data visualization, interactive diagram, 3D model viewer, layered illustration, soft translucency, restrained glow, microinteraction, responsive transitions, contextual captions, tactile cards, typographic hierarchy, accessible contrast boost, reduced-motion mode.
5. Output: PDF, accessible HTML, offline PWA, EPUB, DOCX, Markdown, plain text, PPTX, SVG, PNG, JPEG, WebP, AVIF, MP4, WebM, JSON design tokens, CSS theme, React component, ZIP source bundle, print-ready PDF.
6. CRO objective: comprehension, trust, signup completion, qualified leads, purchase completion, donation completion, contact requests, appointment requests, reader retention, content discovery, product adoption, app installation, subscription opt-in, checkout clarity, cart recovery, newsletter signup, onboarding success, accessibility completion, repeat visits, reduced abandonment.

Provide idea, deliverable and output-format selection in the /God prompt studio, with at least seven choices and up to twenty when useful. Multi-select with a clear recommended default, a no-animation option, and a no-selection automatic continuation path. Every control must be keyboard/VoiceOver usable, clearly labeled and readable on an iPhone.

### Measurable optimization
Define a primary user outcome and guardrail metrics before changes. Compare alternatives with legitimate consent-aware experiments where traffic permits; do not promise conversion gains without data. Check task completion, time to task, bounce/abandonment where measurable, Core Web Vitals, accessibility, content integrity, visual hierarchy, and interaction cost. Avoid dark patterns, misleading urgency, forced consent, manipulative defaults or inaccessible animation.

### Type and color constraints
Use fluid typography with tested minimum readable sizes, comfortable line lengths and contrast; prevent text clipping at 200% zoom and narrow viewports. Generate coherent semantic color tokens with WCAG 2.2 AA contrast verification; never assume a palette passes without measuring. Differentiate each selected palette meaningfully and preserve print-safe fallbacks. Parallax remains style-neutral: do not change source appearance or add objects, lighting, color or scenery without an explicit subsequent user request.

### Quality gates
Run deterministic checks, cross-browser and responsive visual tests, assistive technology checks, mathematics /ITQE and /latex where applicable, export rendering, and applicable canonical Free Website Auditor checks. Iterate root-cause repairs and require two consecutive clean complete QA passes before claiming verified completion. If unexecuted, report NOT TESTED. No invented CRO metrics or deployment claims.
