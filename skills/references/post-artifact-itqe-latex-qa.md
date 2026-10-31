# Post-Artifact Verification Contract — ITQE / LaTeX / Visual QA

Applies after every document, PDF, slide, spreadsheet, report, textbook, or image-bearing artifact is generated or changed. This augments, rather than replaces, the canonical document-rendering-9491 style and release standard.

## Required lifecycle
1. Identify output type and determine applicable test matrix. Snapshot original and preserve the editable source.
2. Finish content and preliminary layout; then run post-creation ITQE and LaTeX verification on *all* relevant mathematical expressions (including captions, tables, charts, appendices, metadata, and alt text).
3. Maintain one canonical numbered equation and variable registry: equation ID, source LaTeX, symbol meanings/units, domains, assumptions, dependencies, dimensions, boundary cases, provenance/citation, plain-language interpretation, and rendered location. Where no equations are present, record ITQE and LaTeX as NOT APPLICABLE, not as passed tests.
4. Check LaTeX parsing, delimiter balance, symbolic and numeric consistency, math fonts/glyphs, subscripts, superscripts, line breaks, overflow and readable accessible equivalents. Distinguish checks automated by tools from unverified scientific validity.
5. Render/export the finished artifact, inspect *every page or slide containing mathematical content*, then inspect *all remaining pages or slides* for visual defects. Inspect at mobile reading scale and magnified scale where supported.
6. Verify source-to-output fidelity, citation/reference ordering, hyperlinks, file integrity, copyright, figure captions, alt text, pagination, and document-specific tests below.
7. Repair, re-render and run the relevant full regression suite until two consecutive complete passes have zero unresolved critical/major defects, or stop with explicit BLOCKED/NOT TESTED flags. Do not call a sample inspection exhaustive.
8. After successful export, scan both source and final PDF/output for internal production-label leakage per document-rendering-9491. Verify exact output paths before sharing.

## Document-type-specific metrics
- PDF/textbook/research: all pages raster-inspected, math and ITQE consistency, bibliography first-appearance ordering, metadata, bookmarked headings if supported, text extraction, accessibility structure, font embedding, accurate scientific claims.
- DOCX/Google Docs: styles/heading navigation, equation editability or documented fallback, table layout, pagination after rendering, images/alt text, comments and change preservation.
- PPTX/slides: every slide and speaker-note math, safe margins, object overlap, readable projection-scale typography, contrast, note/citation alignment, animation fallback.
- XLSX/spreadsheets: formulas/cell errors, references, dependency cycles, units, number formats, calculated values, chart-source links, hidden-sheet/print inspection; use native spreadsheet tools rather than substituting a PDF QA pass.
- Images/banners: semantic relevance, visual accuracy, license/provenance, crop, pixel size, perceptual nonduplication, alt text, no misleading baked-in equations or scientific data.
- HTML/apps: math rendering, semantic markup, keyboard and touch usability, responsive clipping, WCAG-oriented accessibility, console errors, secure handling and build/test status.

## Evidence-based report
Publish a compact QA ledger: artifact type, pages/slides/sheets, equations found/validated, pages visually checked, unique figures, test coverage, defects detected/fixed/open, two-pass status, tools used, and unresolved limitations. Use PASS/FAIL/BLOCKED/NOT TESTED/NOT APPLICABLE honestly. No claims of guaranteed perfection.

## Optional post-run menu
After delivering a validated artifact, offer a compact menu of *actionable* next steps without delaying automatic mandatory QA: (1) open/download, (2) inspect equation registry/ITQE table, (3) review QA ledger, (4) run deeper domain-specific tests, (5) revise and re-export, (6) authorized commit/publish. Only show actions possible with current tools. The menu must not imply missing tests already passed or require input before safe corrections.

## Interoperability
/pe orchestrates and /4629 designs; /latex owns mathematical typesetting; /ITQE owns equation metadata; /qa and /visual_QA verify; /wca and /ivy or /biblio provide their domain checks and one canonical citation numbering system; /copyright controls the single footer authority. Do not duplicate the same authority or inject command names into reader-facing artifacts.

## Automatic /karma forensic learning hook
On each QA finding, emit a sanitized structured event following `skills/karma/SKILL.md`, including category, severity, evidence, fingerprint, artifact/source hashes and test result. After a reproducible root cause is established, create a regression fixture and propose minimal rule updates; mark fixes VERIFIED only after two complete clean passes. Record nonissues and unrun tests distinctly. Never claim forensic cloud storage, external alerts or ML training are active merely because they are specified.

## Cross-skill completeness and collision gate
Apply `skills/references/document-error-prevention.md` rule IDs E01-E12. Preflight the source manifest and reconcile every section, equation, table, figure, citation and ending against final exported text and pagination. Check accidental duplication, stale exports and conflicting formatting/footer controllers. Source-only inspection never replaces full page-by-page visual QA. Send actual defect evidence to /karma. Test results without execution must remain NOT TESTED.
