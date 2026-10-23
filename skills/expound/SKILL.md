---
name: expound
description: Iteratively expand and rigorously verify an existing document, renumbering all citations and notes in first-appearance order after every edit, regenerating its bibliography, and preserving its design, section banners, and inline-image requirements.
---
# /expound

Version: 1.3.0

Iteratively expound and expand until material resolvable gaps close within evidence and available resources. Preserve the user's thesis as a hypothesis; never manufacture support. Update the existing document and its complete citation and visual systems together. Changing this skill does not itself request expansion of a document.

## Establish the document contract

1. Resolve and read the actual document and its editable source. Preserve the original. Inspect the rendered document; do not infer its design from a filename or an earlier description.
2. Inventory headings and subsections, claims, citations, page notes, bibliography, source registry, equations, tables, banners, inline images, captions, cross-references, and links. Retain immutable IDs for sources and document objects.
3. Capture one design contract from the source and rendered pages: page geometry, typography and sizes, palette, backgrounds, heading hierarchy, spacing, column/grid rules, equation and table styles, caption styles, bleed and safe text insets, header/footer, pagination, and copyright/link behavior.
4. Read applicable source-document instructions and the latest relevant citation, banner, images, copyright, ITQE, and latex skills. Apply the canonical shared document-rendering standard when available. Explicit user directions prevail. Where a source has stricter applicable visual requirements, retain them.
5. Preserve the source's established design throughout the expanded document. Reuse its named styles, templates, tokens, and builder. Do not introduce a competing stylesheet, switch the document to a different aesthetic, or format only the new pages. Preserve existing usable artwork and its provenance. If only a PDF exists, reconstruct the design from inspected pages and disclose any fidelity limitations.

## Iterative protocol

1. Detect missing relevant definitions, context, evidence, counterarguments, derivations, limitations, reproducibility information, and source gaps. Rank them by materiality.
2. Research and add only substantiated content. Distinguish evidence, inference, conjecture, and unknowns. Attach immutable source IDs; never invent references, source metadata, measurements, or successful validation.
3. After EACH addition, deletion, replacement, move, or structural edit, rebuild the complete document citation sequence and bibliography using the citation-integrity contract below. Do not update only the inserted passage or append new numbers to an old sequence.
4. Reconcile the full heading and image inventory. Provide required new banners and inline images immediately; update affected captions, visual references, and citations.
5. Verify facts, mathematics, quotations, source identity, contradictions, style fidelity, visual coverage, and regressions. Reassess remaining gaps.
6. Repeat while material resolvable gaps remain and progress is measurable. Do not introduce arbitrary content-length caps. Respect actual execution/resource constraints; checkpoint work and report unresolved gaps honestly. Never claim literal exhaustiveness or research saturation without evidence.
7. Rebuild, paginate, and perform the final citation, equation, design, and visual audits on the actual exported file. Repair and repeat affected checks; recheck document-wide references and pagination after repairs.

## Citation-integrity contract

- Use stable source IDs and citation-event IDs. Treat display numbers as derived output. Normalize duplicate source records by verified DOI or other reliable identity without merging distinct editions or works accidentally.
- Traverse the entire final reading order, including new and old prose, equations, tables, captions, figure notes, appendices, and supplementary body material. Follow the document's actual reading order rather than raw file or object-storage order.
- For numeric reference systems, assign each distinct work its number at first appearance, keep the sequence contiguous from 1 through N, and reuse that number for later citations to the same work. Regenerate the unique-work bibliography in that first-appearance order.
- For Chicago notes, renumber citation-note events contiguously in reading order across the whole document, including page-local footnotes and endnotes. Repeated works may have separate shortened notes. Maintain a separate unique-work registry and order its bibliography by each work's first appearance; do not confuse note numbers with bibliography entry numbers.
- Preserve the document's chosen citation syntax and scholarly style. Honor an explicitly required alternative style, including an author-date or alphabetic bibliography, instead of inventing numeric labels for it; otherwise use the first-appearance house convention above.
- Update every affected superscript, bracketed marker, grouped citation, page note, endnote, short note, bibliography entry, hyperlink, back-reference, and cross-reference. Deduplicate grouped work references and keep their ordering consistent with the citation style.
- Reconcile removals and moved first appearances: eliminate gaps, resolve dangling references, and remove unused bibliography entries unless explicitly retained in a separately labeled further-reading list.
- Run the latest /wca-ivy-biblio remapping and validation where its tooling supports the source format. For another format, use native citation fields or an equivalent deterministic whole-document rebuild. Do not claim an unavailable command ran.
- After typesetting, verify the final PDF or other exported artifact against the source registry: contiguous first appearances, valid note sequence, correct destinations, no stale numbers, no unresolved placeholders, no uncited or duplicate bibliography records, and source-to-claim support. A source-only audit is insufficient.

## Design, banners, and inline images

- Apply the captured design contract to every inserted paragraph, heading, table, equation, caption, note, and page. Match existing page geometry, typography, color, spacing, backgrounds, figure treatment, navigation, and footer requirements unless the user explicitly changes them.
- Every body section AND subsection requires its own context-specific banner under /banner. Include newly inserted or subdivided nodes and appendices containing body content. A parent banner never satisfies a child's requirement.
- Generate a distinct banner for each new required slot. Keep compliant existing banners. Revise an existing banner only when its meaning or required treatment changes; preserve asset history. Never crop, recolor, resize, or reuse another node's banner as a substitute for a new one.
- Preserve the source's banner placement and compatible top/bottom alpha treatment. Enforce 16:9 aspect ratio and horizontal full bleed at the page trim, with zero left/right margin or padding. Keep readable text within safe insets. Do not stretch artwork or confuse digital edge-to-edge placement with printer bleed.
- Give every new image a brief grounded in its heading and surrounding verified content. Follow the latest applicable banner/images art direction while retaining the source document's visual language. Label synthetic artwork accurately; never present it as an authentic photograph or measured scientific evidence.
- Add distinct, relevant inline illustrations at least every 500 words of body prose, or at the source's stricter cadence. Audit the full expanded reading sequence, including insertion boundaries. Banners, page backgrounds, and equation plates do not count as inline illustrations.
- Keep inline images independent of banners: no duplicate bytes, paths, crops, recolors, or near-duplicate compositions. Use deterministic diagrams or plots when scientific precision is necessary; do not invent data in generated imagery.
- Maintain a heading-to-banner and passage-to-inline-image ledger with IDs, placement, caption, provenance, prompt when available, dimensions, hashes, and alt text where supported. Check exact and perceptual similarity and inspect visually; run /images uniqueness tooling when compatible.
- Reconcile figure/table numbering, captions, in-text references, illustration lists, bookmarks, and contents after additions or moves. Citations introduced by images or captions must trigger the same global citation rebuild.

## Equation-by-equation audits and final typesetting

- Give every mathematical equation its own corresponding /ITQE audit, including numbered and unnumbered displays, aligned lines expressing independent claims, and equations embedded in prose. For identical repeated equations, retain a canonical audit and an explicit equation-to-table cross-reference for every occurrence.
- Assign stable equation and audit-table IDs; maintain a machine-checkable coverage ledger. On addition, revision, movement, or removal, reconcile its table, source citations, and cross-references. Split compound displays or identify separate audit rows for independent equations.
- Include variables, definitions, units and dimensional consistency, derivation/provenance, assumptions and validity domain, source citations, epistemic classification, limiting cases, and verification/falsifiability. Include stock–flow interpretation only when relevant. An audit does not empirically prove a conjecture.
- Use the latest /ITQE presentation contract. Place the audit adjacent to its equation where feasible. Keep each displayed equation with its variable table; keep captions with illustrations. Prevent orphan headings and broken tables or entries that can fit on one page.
- After substantive changes and citation reconciliation, invoke the latest /latex preflight, compilation, and visual-QA requirements before export: compiled mathematical notation, supported glyphs, scholarly typography compatible with the source, readable spacing, clickable links, footer safety, and rendered-page inspection.
- Apply /copyright through its canonical helper and source rules. Maintain one notice per required page and preserve the source's authorized legal and brand links; do not paste a competing notice template into the document.

## Release gate

Require all of the following before describing the expansion as complete:

1. Added claims have verified support or explicit uncertainty labels.
2. The whole-document citation/notes sequence and bibliography pass after the last substantive or visual edit and after final pagination.
3. Every required section/subsection has its own compliant banner, full-document inline-image cadence passes, and image uniqueness passes.
4. Every equation resolves to its audit, and compiled math contains no raw notation, missing glyphs, or clipped symbols.
5. Source-design comparison passes on representative original/new pages and all exported pages have been rendered and inspected for bleed, aspect ratio, contrast, spacing, clipping, overlaps, caption/table separation, and footer collisions.
6. Figure/table references, contents, bookmarks, page numbers, bibliography links, and legal links resolve in the final export.
7. Record PASS, FAIL, BLOCKED, or NOT TESTED with actual evidence. Repair failures and rebuild until resolved or disclose a real blocker and label any delivered partial artifact accordingly. Never count unexecuted checks as passes.

Compatibility: /deep, /atlas, /iterate, /banner, /images, /latex, /copyright, /itqe, and /wca-ivy-biblio. Apply their current relevant requirements; preserve explicit user instructions.

Read [acceptance scenarios](references/acceptance.md) when validating an update to this skill.
