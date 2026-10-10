# Doctoral research and delivery protocol

## Scope and reproducibility

Translate the supplied subject or text into research questions, definitions, testable propositions, rival explanations, disciplinary lenses, period, geography, and exclusions. Preserve the input separately. Treat unsupported premises as hypotheses. Define coverage before searching and record languages, databases, date searched, time period, accessibility, and stopping criteria. Pursue comprehensive coverage within documented limits; never assert that all literature was searched.

Create scope.md, search-log.jsonl, sources.jsonl, nodes.jsonl, evidence-matrix.jsonl, rounds/round-N.md, gaps.md, image-inventory.json, and qa-report.md in the research working folder. Preserve checkpoints; reuse verified extraction on continuation and recheck changed or time-sensitive material.

## Source discovery and verification

Search available academic indexes, institutional repositories, government archives, and official publication catalogs. Prefer direct readable PDF files hosted by Ivy League universities (Brown, Columbia, Cornell, Dartmouth, Harvard, Penn, Princeton, Yale); also search other universities, academic publishers, government departments, military and intelligence agencies, international organizations, standards bodies, and authoritative learned societies as relevant. Do not limit discovery to preferred hosts or geography. Institutional prestige and PDF format are preferences, never substitutes for relevance, methodology, or evidentiary quality.

Follow backward references, forward citations where available, authors, datasets, methods, foundational works, newer reviews, corrections, retractions, and dissenting findings. For each central question search both support and counterevidence. Add graph children only when they change explanation, inference, or uncertainty. Track visited works by DOI, identifier, and normalized title; avoid cycles and duplicate editions masquerading as independent corroboration.

Open and inspect sources before using them for substantive claims. Verify PDF content, author, exact title, date/version, publisher, stable landing page/DOI, direct PDF URL, actual hosting institution, access date, and relevant printed pages or sections. A search snippet or catalog record supports discovery or metadata only. Record inaccessible sources in gaps.md; never invent their content or page locators. Prefer stable public links over expiring signed URLs. Check that PDF links resolve to the intended document, not login pages or unrelated files.

Keep peer-reviewed research, dissertations, working papers, archival primary materials, official statements, and declassified intelligence assessments distinct. Record provenance, methodological limitations, conflicts of interest, redactions, institutional viewpoint, revision status, and jurisdiction. An official assertion is evidence that the institution asserted it, not automatic proof of its substance.

## Claim-level evidence matrix

For every substantive externally checkable claim record: claim_id, section_id, exact claim, source_ids, exact page/section locators, supporting extraction or concise paraphrase, evidence type, quality rationale, corroboration group, counterevidence, uncertainty, and status (supported, qualified, contested, inference, hypothesis, unsupported). Link note events to stable work IDs.

Use multiple independent sources for central disputed claims where available. Do not inflate confidence by counting derivative sources that copy one origin. Explain discrepancies in definitions, samples, measurement, study design, time period, and causal identification. Distinguish observation, association, mechanism, causal inference, prediction, and normative judgment. Label original synthesis and derivations clearly. Restrict conclusions to what inspected sources establish.

## Iterative recursion and synthesis

Pass 1: map foundations, terminology, history, methods, and central evidence.
Pass 2: deepen each material branch through primary PDFs and citation chains.
Pass 3: challenge the draft with contradictory results, alternative mechanisms, missing populations, methodological weaknesses, and boundary conditions.
Pass 4: synthesize across disciplines, check claim support and calculations, then target remaining gaps.
Repeat passes when material gaps remain. Each round logs queries, inspected candidates, inclusion/exclusion reasons, new claims and sources, changed conclusions, open nodes, and marginal information gain. Avoid cosmetic expansion and bibliography padding.

Start at depth 4 and 80 included sources as review checkpoints; increase in logged batches when justified. Two consecutive targeted rounds with no material new evidence or explanatory branch permit branch closure. Budget exhaustion, blocked access, and unavailable tools are distinct stopping reasons. State achieved depth, source count, closed/open branches, and residual gaps. Never hide unresolved questions behind the word exhaustive.

## Scholarly composition

Produce a doctoral-level argument with abstract, research questions, literature review, methods, thematic chapters, counterarguments, interdisciplinary synthesis, limitations, conclusion, open problems, relevant appendices, and bibliography. Depth must come from critical comparison, explicit assumptions, inspected evidence, and reproducible reasoning rather than adjectives or word count.

Enforce /wca-ivy-biblio Chicago notes-bibliography: contiguous superscript citation events in reading order, full/short note forms with exact locators, page-local notes, and one bibliographic entry per work in first-appearance order. Provide verified academic PDF hyperlinks when available, plus DOI or institutional landing page for persistence. Cite datasets, methods, equations, tables, and reconstruction captions. Remap citations after every insertion. Do not present house ordering as conventional alphabetical Chicago ordering.

Use /latex for genuine compiled mathematics. Maximize relevant supported equations, identities, estimators, constraints, and quantitative descriptions without inserting ornamental or invented mathematics. Check syntax, delimiters, dimensions, units, domain restrictions, assumptions, significant figures, and derivation steps. Place an /itqe Identifier–Term–Quantity/unit–Explanation table immediately below each display equation, covering every symbol, constant, index, and operator with its role. Quantitative inventories receive ITQE when applicable. Do not fabricate quantities for qualitative subjects; explicitly mark math not applicable if warranted. Static PDFs show readable tables; only call companion tables interactive when actual interaction exists.

## Visual coverage and QA

Inventory every printed section type and heading level before generation. Assign one unique context-specific banner to each section and subsection, including abstract, Notes, Bibliography, glossary, and appendices. Exempt only title-only covers, automatic contents, and running furniture. A parent never covers a child. Generate separate relevant inline illustrations under /images; compiled equations and precise charts use exact renderers and never count as banners.

Use futuristic, beautiful, volumetric imagery while preserving subject fidelity, legibility, contrast, and scholarly credibility. Label generated illustrations accurately; do not simulate archival proof, agency seals, measurements, or historical photographs. Keep evidence captions outside image pixels. Use distinct compositions and unique published paths; audit paths, bytes, prompts, and perceptual similarity with /images and inspect a contact sheet. Render banners full-opacity, 16:9, full bleed left/right, without fades. Verify the actual final document has every required image, not just a manifest entry.

Before release run WCA citation QA, ITQE and LaTeX render gates, image uniqueness and coverage checks, source-link verification, claim support review, and every-page visual inspection. Check footnote readability, caption/source accuracy, bibliography links, missing glyphs, equations, clipped text/tables, contrast, pagination, and footer collisions. A legacy renderer that ignores fields must be extended or replaced; JSON compliance alone is insufficient. Unresolved rendering or citation defects block a claim of finished delivery.

Deliver the verified PDF and summarize pages, included works, notes, research nodes, equations/ITQE tables, banners, inline images, passed checks, and material research limitations. Save final deliverables persistently through the available Library workflow. If a dependency or check is unavailable, name the limitation and preserve work; never report an unperformed check as passed.
