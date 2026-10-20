---
name: expound
description: Iteratively expand and rigorously verify a document until material resolvable gaps are closed, synchronizing verified citations and bibliography at every pass.
version: 1.1.0
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
