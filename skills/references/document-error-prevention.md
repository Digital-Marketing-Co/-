# Cross-Skill Document Error Prevention and Learning — v1.0

## Evidence and scope
Derived from available conversation-history corrections and repository rules, not a claim that every historical conversation was exhaustively retrieved. This is the canonical error-prevention contract; skills link to it instead of copying rules. Runtime learning means persisted, tested regression rules or separately validated trained models, NOT silent retraining of a foundation model.

## Authority and anti-collision
Explicit user constraints > applicable format/safety requirements > document-specific content and mathematical truth > canonical `skills/references/document-rendering-9491.md` for visual formatting > this error-prevention standard > skill-local enhancements. Shared authority: /4629 design and optional style interaction; /ITQE equation metadata; /latex typesetting; /ivy and /biblio one citation registry; /copyright one footer controller; /karma forensic defects; /qa and /visual_QA evidence; /pe orchestration. A skill must not rewrite another's owned output without an explicit approved merge.

## Recurring error taxonomy and required prevention tests
E01 TRUNCATION: preserve original source inventory and hashes; compare section IDs, headings, paragraphs, tables, captions, equation IDs, citations, annexes and substantive word counts across input, editable output and final exported output. Detect missing endings, blank pages and unexpected page-count drops. Never replace an exhaustive source with a short summary.
E02 OVERLAP/CLIPPING: rasterize and inspect every page/slide, including top, bottom and bleed edges; check text boxes, mathematical baselines, margins, captions, diagrams and mobile readability; fix geometry, do not merely reduce font size.
E03 DUPLICATED CONTENT: canonical IDs and content fingerprints for sections, tables, figures, references, footers, headings, equation numbers and repeated derivative imagery. Reject unapproved duplicates, preserve intentionally repeated information with explicit manifest reason.
E04 STALE EXPORT: recompile after every source, TOC, bookmark, footnote or reference change. Compare source revision and exported revision hashes; never return an older PDF.
E05 CITATION ERRORS: first-appearance numeric order, canonical /ivy-/biblio registry, clickable links, resolved references, accessible and appropriately attributed figures. No invented sources.
E06 MATH/ITQE: every significant formula has an ID, editable LaTeX where possible, units, assumptions, dependencies and plain-language meaning; validate symbols and rendered output on each relevant page.
E07 COPYRIGHT/BRANDING: exactly one active footer owner; only user-required copyright text, no duplicated watermark/logo; check sequential folios.
E08 IMAGERY: distinct context-specific images and source manifest with hashes and provenance; AI-generated conceptual imagery identified; reject unreadable baked-in text and misleading science scenes.
E09 ACCESSIBILITY: heading order, searchable selectable text, contrast, alt text, keyboard/mobile operation where applicable, reasonable touch targets, reduced motion for interactive content.
E10 QA CLAIMS: maintain PASS/FAIL/BLOCKED/NOT TESTED/NOT APPLICABLE and evidence per test; never claim perfect, exhaustive, trained ML, live monitoring or no defects without checking.
E11 FORMAT INTEGRITY: validate DOCX structure and render; PDF text and font embedding; slides notes and bounds; spreadsheets formulas/dependencies; HTML console/build.
E12 SOURCE ATTRIBUTION: distinguish conjecture, hypothetical metrics, theoretical limits and experimentally established claims. Preserve author attribution without asserting patent novelty.

## Interactive /4629 contract
When /4629 is invoked on a new design, show a compact default plan with six distinctly named visual directions, with the best context-specific default selected; include user-editable free-text override. Ask only when an essential direction remains unresolved. If the user said /p, /disabled or already selected a visual direction, continue automatically with that style and do not ask again. Never make the interaction a prerequisite for safe QA. Persist the chosen specification with design manifest and semantic tokens (typography, grid, contrast, imagery, bleed, accessibility, PDF/print). Subsequent /expound edits reuse the manifest unless the user explicitly changes it. Preflight layout before generating photos.

## Completeness and release gate
Build a source-of-truth manifest with expected section IDs, equation IDs, figure IDs, citations, document word count and hash. Post-export, reconcile 1:1; investigate any omission, duplication or unexpected content reduction rather than silently allowing it. Complete two sequential full validation passes with zero major/critical defects. Inspect every page, not only contact sheets; take both normal and enlarged views for math-heavy pages. Report coverage, defects, outstanding limitations and exact artifact paths. Unavailable checks are NOT TESTED and cannot count toward two clean passes.

## Forensic learning and regression
For each encountered defect: write sanitized /karma event (fingerprint, source/version, observed vs expected, severity, affected skills, proof, status), reproduce, identify actual root cause, create minimum failing fixture, apply a safe correction in the owning skill/shared rule, then rerun both failing and adjacent tests twice. Reuse canonical rule IDs rather than appending duplicate directives across skills. Add regression cases to a versioned fixture file, with author/date/revision and baseline results. Separate unverified suggested rules from tested rules. Do not train a model without a labeled dataset, versioned pipeline, evaluation metrics, leakage controls and measured generalization. Prefer deterministic tests for traceability and zero paid inference.

## User-centered defaults
iPhone-first readability, low-interaction autonomous QA, safe changes without repeated prompts, preserve original files, do not perform destructive operations or production cutovers without authorization. Never present theoretical system designs as deployed systems.
