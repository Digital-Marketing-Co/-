---
name: expound
description: Iteratively expand and rigorously verify a document until material resolvable gaps are closed, synchronizing verified citations and bibliography at every pass.
version: 1.2.0
---
# /expound

Iteratively expound and expand until exhaustive within evidence, resources, and a finite execution budget. Preserve the user's thesis as a hypothesis, never manufacture support.

## Iterative protocol
1. Parse document structure, claims, citations, bibliography, figures, tables, equations, and existing source registry.
2. Detect missing relevant information: definitions, context, evidence, counterarguments, derivations, limitations, reproducibility, and source gaps. Rank by materiality.
3. Research and add only substantiated content, explicitly distinguishing evidence, inference, conjecture, and unknowns. Attach immutable source IDs to every sourced addition; never fabricate references.
4. After EACH addition or structural edit, invoke the /wca-ivy-biblio citation-integrity rules: traverse first appearances, renumber all affected citations, regenerate notes and bibliography, and check completeness.
5. Verify facts, math, quotes, and source metadata; check contradictions and regressions; reassess gaps.
6. Repeat while material resolvable gaps remain and progress is measurable, subject to explicit max iterations and resource/time constraints. Stop on convergence, no material progress, or exhausted resources; report unresolved gaps honestly.
7. Run final citation and bibliography validation after typesetting and before export. A failed citation audit blocks successful completion.

## Pseudocode
```js
let state = assess(document), iteration = 0;
while (state.hasMaterialResolvableGaps && iteration < maxIterations && resourcesAvailable()) {
  const changes = expandWithVerifiedSources(document, state.prioritizedGaps);
  document = applyChanges(document, changes);
  document = synchronizeCitationsAndBibliography(document); // /wca-ivy-biblio
  assertCitationIntegrity(document);
  const next = assessAndVerify(document);
  if (!materialProgress(state, next)) { state = next; break; }
  state = next; iteration++;
}
validateFinalTypesetCitations(document);
return { document, iterations: iteration, unresolvedGaps: state.gaps };
```

Compatibility: /deep, /atlas, /iterate, /latex, /copyright, /wca-ivy-biblio. Honor chosen citation style; numeric numbering by first appearance, Chicago notes numbered by appearance with bibliography order as appropriate to style.


## v1.2.0 — equation-by-equation ITQE audits and mandatory final /latex

- Treat **every mathematical equation** as requiring its own corresponding /ITQE-generated audit table, including numbered and unnumbered display equations, aligned equation lines expressing independent claims, and mathematical equations embedded inline in prose. For repeated identical equations, maintain one canonical table and an explicit equation-to-table cross-reference for each occurrence; never leave an equation without a resolvable audit.
- Assign stable equation IDs and matching ITQE table IDs; maintain a machine-checkable equation-to-table coverage ledger. When an equation is added, revised, moved, or removed, immediately regenerate or reconcile its ITQE table and cross-references. If a compound display contains multiple independent equations, split or provide separately identified audit rows/tables for each equation.
- Each /ITQE table must include: equation and ID; variables and definitions; dimensional units and consistency; derivation or provenance; assumptions and domain of validity; evidence/source citations; classification (identity, established, derived conditionally, conjectural, contradicted, or unknown); limiting cases; falsifiability or verification; and ITQE stock–flow interpretation **only when relevant**. Never imply that a physics equation establishes an economic identity or that an ITQE audit empirically proves a conjecture.
- Cite any nontrivial external evidence used in the equation or its table, and rerun /wca-ivy-biblio first-appearance citation ordering after every addition. Tables must be placed adjacent to the equation when feasible, with adequate separation and page-break controls.
- Near the end of /expound, after substantive research, equation/table generation, and citation reconciliation but **before PDF/document output**, invoke the latest /latex skill as a mandatory preflight and typesetting/visual-QA gate. Its current requirements include scholarly serif/math fonts, true vertically stacked fractions, adequate text-to-table spacing, borderless but clickable hyperlinks, footer safety, citation integrity, and page-by-page rendered inspection.
- Final export is blocked until (1) all equations map to ITQE tables, (2) the /latex compilation and visual QA pass, and (3) final citations and bibliography pass. On failure, repair and rerun /ITQE → /latex → citation audit until passed or report the unresolved blocker without falsely claiming completion.
- Preserve finite execution budgets; if a requested skill is unavailable, do not claim it ran. Clearly report the missing step and provide the artifact only with explicit qualification.
