---
name: god
description: Orchestrate all applicable canonical skills and fail-closed QA for documents, posts, apps and sites; automatically invoke ITQE and LaTeX when mathematical content occurs.
---

# /god — universal orchestration and verification

## Source authority
Use canonical definitions in this repository, particularly `skills/itqe/SKILL.md`, `skills/latex/SKILL.md`, `skills/disabled/SKILL.md`, and relevant QA, visual QA, textbook, book, and publishing skills. Never substitute this orchestration summary for their complete instructions. Resolve discrepancies by preserving existing skill behavior and reporting conflicts.

## Execution
1. Inventory requested deliverables, all known requirements, sources, output formats, affected repositories, dependencies, routes, posts (including orphaned and dynamic routes), and tests. Build a requirement-to-output traceability matrix.
2. Classify output and invoke only applicable skills. Preserve originals, avoid destructive changes and paid inference without approval.
3. Detect mathematical expressions in prose, Markdown, HTML, MathML, SVG, tables, generated content, PDFs and source code. Distinguish ordinary code operators from displayed mathematics.
4. For each substantive equation, run the canonical /itqe process after equation authoring and before final layout. Record equation ID, variables, units, domain, assumptions, meaning, numerical or symbolic verification and provenance as appropriate. For inline expressions, provide accessible definitions without clutter.
5. Run canonical /latex after ITQE normalization and before final rendering. Verify actual compiled visible notation, semantics, clipping, glyph coverage, text alternatives and fallback behavior. Re-run ITQE and LaTeX if math changes.
6. Apply functional, integration, regression, content, citation, security, privacy, accessibility (WCAG 2.2 AA), performance, responsive and visual QA. Inspect actual renders, not just source.
7. For web applications, enumerate all discoverable routes, public post types, generated pages, redirects, sitemap entries and orphan candidates. Determine the installed authoritative Free Website Auditor API version from source, then execute its applicable page and site checks. Do not invent API endpoints, metrics, scores or pass results. For protected admin/API surfaces, supplement with authorized authenticated security and integration tests; public auditing alone is insufficient.
8. Fix reproducible root causes in batches, minimize repeated inference, and run affected tests plus complete regression. Require two consecutive complete clean QA passes with no critical/major defects and no unverified mandatory gates before claiming verified completion.
9. Record actual findings, reproducible steps, changes, evidence, residual risks, and release decision. If access or test infrastructure is unavailable, mark blocked/unverified rather than passing.
10. Never claim commits, deployments, videos, PDF outputs, tests or audits without actual tool evidence. Require explicit authorization for destructive actions, production cutovers or other high-impact changes.

## Accessibility and continuation
Honor /disabled and /p as one accessibility-first continuation workflow. Prioritize iPhone-readable status, low interaction, non-destructive autonomous steps, and transparent blockers.

## Acceptance
Every equation has correct accessible rendering and quantitative context when applicable; every applicable route has a traceable audit disposition; every output has an evidence-based QA report; two complete clean passes are required for verified completion.
