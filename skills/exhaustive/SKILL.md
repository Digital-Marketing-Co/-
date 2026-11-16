---
name: exhaustive
description: Iteratively apply /expound with rigorous citations and bibliography until two consecutive quality passes find no material gaps.
---
# /exhaustive — Iterative Exposition and Verification

## Invocation
/exhaustive [subject, text, or artifact] [scope and constraints]. Continue the latest relevant work if the user supplies no new subject. Respect /p as authorization to continue permissible steps, not to invent missing inputs or bypass external confirmation.

## Execution
1. Preserve the user's original scope and retrieve applicable existing /expound, /academy-ivy-biblio, /latex, /ITQE, and other skill instructions before invoking them. When unavailable, say so and use the documented equivalents without claiming execution.
2. Construct an ordered hierarchical outline and coverage matrix of required concepts, examples, sources, equations, implementation and validation.
3. Run successive /expound-style passes: expand missing material, check logical consistency, eliminate repetition, add grounded examples and counterexamples, and reconcile terminology.
4. Use citations attached to claims and an ordered bibliography in the requested /academy Ivy/WCA style; cite only verified sources, never invent references or DOIs. Renumber references after every reordering.
5. For equations, define symbols, check dimensional consistency and derivations, provide readable LaTeX, and apply /ITQE where available. Do not claim mathematical or rendering validation unless performed.
6. For visuals, use contextual, nonduplicate images only when requested; enforce readability, accessible contrast, alt text, and page/viewport fitting.
7. Run factual, structural, citation, technical, accessibility, and visual QA. Record open issues and improvements. Repeat until two consecutive complete passes produce no material improvements or constraints prevent further work.
8. If work requires deployment, repo edits, data retrieval, or tool execution, use the appropriate connected tools and verify the result. Do not pretend future or unavailable operations were completed.

## Output
Provide the expanded result, ordered bibliography, equations where relevant, a concise iteration/QA log, unresolved limitations, and verified artifact/commit links only when created. Distinguish completeness relative to available evidence from universal exhaustiveness.

## Terminal mathematical integrity enforcement — 2026-11-16
For every applicable generated or modified artifact, invoke the canonical shared `skills/references/post-artifact-itqe-latex-qa.md` gate AFTER the last content edit and final export: inventory all math including figures/tables; run /itqe first (equation IDs, every symbol/operator/constant/index, units, assumptions, dimensional consistency, Unicode names and accessible glossary), then /latex (source parsing, rendering, superscripts/subscripts, font/glyph integrity, exported-page verification). If defects are repaired, re-export and repeat the terminal /itqe → /latex sequence on the new final output. Then require two independent complete evidence-backed QA and visual-QA passes; /karma records actual defects and prevention fixtures. A math-free artifact may mark both NOT APPLICABLE only after a verified inventory. Never treat missing tools, incomplete inspection, commits, or self-reported status as PASS. Use bounded, nonrecursive orchestration; /C can output exactly Complete only after all applicable acceptance criteria are verified. This addition preserves all prior skill-specific responsibilities and safety constraints.
