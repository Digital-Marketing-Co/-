---
name: etymology
description: Evidence-grounded doctoral-level historical linguistic analysis of a user-supplied lemma, phrase, or reconstructed root, with attestations, cognates, phonology, and cited sources.
---

# ETYMOLOGY v3.0.0 — Research Skill

## Mission
Produce evidence-grounded, doctoral-level historical linguistic analysis of exactly the user-supplied lemma, phrase, or reconstructed root. Never invent a target when omitted.

## Invocation
`/etymology WORD`
`/etymology lang:fr savoir-faire`
`/etymology *bʰer-`
Optional flags before target: `-deep`, `-brief`, `-pdf`, `-md`, `-json`, `-timeline`, `-cognates`, `-phonology`, `-morphology`, `-semantic`, `-disputes`, `-bibliography`, `-images`, `-banner`, `-qa`, `-visual_QA`, `-negative`, `-no-pdf`, `lang:<BCP47>`.
Treat remaining input as exact target, preserving accents, asterisks, hyphens, spaces, and IPA characters. Quoted strings are literal. Unknown flags produce a helpful error. No target: ask for a word or phrase.

## Research protocol
1. Establish language, lemma, script, pronunciation, sense, and part of speech; distinguish homographs and senses.
2. Consult authoritative language-specific historical dictionaries (OED, TLFi/CNRTL, DWB, FEW, DELI, etc.) as applicable; corroborate with peer-reviewed scholarship, critical editions, corpus evidence, and specialist reconstruction works. Etymonline and Wiktionary are discovery aids, not substitutes for primary authority. Record access limits.
3. Trace earliest *verified* attestation, with original orthography, source, date/range, manuscript versus composition dates, and a short licensed quotation if permissible. Distinguish earliest found from earliest ever.
4. Trace donor forms and intermediate languages, loans versus inherited developments, morphological segmentation, sound changes, and semantic changes. Provide IPA and glosses when reliable.
5. Separate attested forms from reconstructed forms marked `*`; distinguish conventional reconstructed notation from actual pronunciations. Describe disputed sound laws, laryngeals, ablaut, and uncertainty where relevant.
6. Build a cognate table with language, form, transliteration, gloss, correspondence, confidence, and source. Exclude false cognates; mark uncertain cognacy.
7. Provide dated chronological semantic timeline, derivatives, compounds, borrowing paths, and competing hypotheses with evidence and scholarly status.
8. Cite each substantive assertion inline. Bibliography uses Chicago notes/bibliography style, ordered by first citation, with stable URLs/DOIs and access dates as applicable. Do not fabricate citations, quotes, pages, or attestations.
9. If sources cannot be accessed, state what is unverified; never imply live research or exhaustive internet coverage without it.
10. Run editorial, linguistic, bibliographic, Unicode, layout, and accessibility QA; document limitations.

## Mandatory output sections
Headword and scope; pronunciation and grammatical profile; definitions and sense disambiguation; morphological structure; attestation evidence; transmission and historical ancestry; sound correspondence analysis; comparative cognates; semantic chronology; derivatives; rival etymologies; confidence and evidence gaps; notes and bibliography; QA record.

## Confidence rubric
`High`: supported by multiple independent authoritative sources and regular correspondences. `Moderate`: plausible with material unresolved evidence. `Low`: speculative or substantially contested. `Unknown`: insufficient verification. Confidence applies to individual claims, not entire word histories.

## Delivery
Default: US-letter academic PDF plus accessible Markdown source when generation tools are available. If PDF tools are unavailable, return a complete structured Markdown report and clearly state that no PDF was generated. Optional machine-readable JSON. Apply `/folio` or `/deep` only when available; `/images` and `/banner` for relevant sourced/clearly illustrative plates; `/copyright` for footer; `/negative` final audit. Never silently require absent skills. No arbitrary word/page cap, but prioritize verified material and technical feasibility.

## Typography and QA
Embed or use fonts with Unicode coverage for IPA, combining diacritics, superscripts, macrons, Greek, Cyrillic, and PIE notation. Check line wrapping, nonbreaking grapheme clusters, references, page breaks, accessibility, and no clipping. No fabricated bibliography. Mark illustrations as illustrative, not evidence. Never assert production deployment without verification.

## Examples
`/etymology yellow`
`/etymology lang:fr savoir-faire -deep` (flags may be parsed anywhere outside quoted target; normalize first)
`/etymology *bʰer- -phonology -cognates`


## ENGINE compatibility
This is the ENGINE counterpart of `skills/etymology/SKILL.md`. Keep the legacy path available. Old skill terminology and new engine terminology refer to the same instructions wherever supported.

## Required definitions and word-by-word evolution (v2.1.0)
For every invocation, present definitions **before** historical analysis. Enumerate current primary and secondary senses, historical/obsolete senses, literal and figurative meanings, domain-specific meanings, grammatical categories, and regional distinctions where evidenced. Date and cite senses where possible; distinguish definitions of the full expression from those of its constituents.

For multiword phrases, idioms, compounds, and hyphenated forms, first tokenize into meaningful lexical constituents (including affixes when relevant), preserving original spelling and order. For **each constituent**, provide its own earliest securely attested form, language and family, gloss, dated intermediate forms and languages, inheritance/borrowing/derivation routes, phonological and orthographic changes, grammatical and semantic shifts, and modern form. Then trace the **whole phrase** separately: earliest verified occurrence as an expression, its composition or borrowing, idiomatic shift, and current senses. Do not falsely assign the phrase's date to its constituent words.

Produce a chronological, word-by-word evolution map with one node per evidenced historical form and edges labeled inherited, borrowed, calqued, compounded, derived, or uncertain. Each node records language, approximate date or date range, original script/transliteration, form, gloss, source, and confidence. Where multiple paths are plausible, show branching alternatives rather than a fabricated linear chain. Mark unattested reconstructions with an asterisk and distinguish proposed prehistoric ancestry from the earliest written attestation. When evidence is missing, explicitly show a gap, not an invented bridge.

Required output order: (1) headword/phrase and scope, (2) definitions and sense inventory, (3) pronunciation and grammar, (4) morpheme-by-morpheme breakdown, (5) earliest recoverable origin and attestation, (6) independently traced history of **every constituent word**, (7) chronological language-evolution tree for the full expression, (8) phonetic/orthographic/grammatical shifts, (9) semantic evolution, (10) cognates and false cognates, (11) competing hypotheses and evidence gaps, (12) inline notes and bibliography, (13) visual and accessibility QA. Prefer three independent authoritative dictionaries or specialist linguistic sources where available; disclose when fewer are accessible. Never confuse a reconstructed form, cognate, or speculative etymology with a proven direct ancestor.

Aliases: `ET`, `/ET`, and `/etymology` invoke this same research contract wherever the command router supports aliases. Preserve optional `/banner` and `/images` workflows for relevant, clearly illustrative imagery.

## /Perfect + /Final integration — ET v3.0.0

### Purpose and precedence
This release is additive to all earlier ET rules. On explicit `/Perfect`, `/4629`, `F`, `/Final`, or `u C` invocation, enhance the research plan and its presentation without replacing user input or asserting completion prematurely. `F` in an explicit command context means improve the specification/prompt; it does not silently transform the target word into a different target. Research accuracy and evidence outrank visual polish. The user may request brief mode, but evidence gaps cannot be concealed.

### Deterministic research workflow
1. Parse target, language (BCP-47), historical period, script, word boundaries, output format, and requested depth. Normalize Unicode for comparison while preserving original graphemes. Handle homographs, polysemy, inflected forms, mixed-language expressions, proper names, and ambiguous word segmentation explicitly.
2. Build a sense inventory before ancestry: headword, part of speech, region/register, modern definition, historical definition, obsolete/technical/figurative senses, example paraphrase, first documented sense date (if known), and independent citation. Avoid inventing unattested senses.
3. Segment compounds and multiword expressions into lexical tokens and productive affixes. For each token independently, trace the earliest attested form through every **documented** intermediate language and stage. Separately investigate the earliest documented occurrence and semantic development of the complete phrase. A component's date is not a phrase's date.
4. Create a structured evidence ledger for every historical claim: unique ID, claimed form, language/script, original orthography, transliteration, IPA (only if supported), meaning/gloss, grammatical role, approximate date/range, attestation type, original source/edition and location, dictionary or corpus reference, URL/DOI if available, and confidence. Distinguish composition, manuscript, and edition dates.
5. Construct a directed acyclic graph where nodes are forms or reconstructed protoforms and edges have explicit types: inherited, borrowed, calqued, derived, compounded, semantic extension, cognate (lateral relationship, NOT ancestry), or disputed. Permit convergent paths, multiple donors, and unknown ancestors; never fabricate missing intermediate nodes or equate language-family membership with direct borrowing.
6. For proposed sound changes, identify phonological environment, chronology, relevant sound law, exceptions, and corroborating correspondences. Show IPA with uncertainty; avoid treating reconstructed IPA as recorded speech. For semantic changes, distinguish attested shift from scholarly hypothesis and identify mechanisms such as metaphor, metonymy, pejoration, amelioration, broadening, narrowing, or reanalysis.
7. Compare at least three independent authoritative linguistic resources where genuinely available, prioritizing historical dictionaries, peer-reviewed linguistic studies, original attestations, and critical editions. Report fewer sources honestly. Wiktionary and popular summaries may guide discovery but do not alone establish contested historical pathways. Cite individual edges and dates, not merely the entire chart.
8. Generate dual views from the same evidence ledger: a chronological table for assistive technology and a branching tree for sighted readers. Provide one constituent-by-constituent timeline plus a separate whole-phrase timeline. In a graphic, use arrows and edge labels rather than relying on color; provide textual equivalents.
9. Explain alternatives and counterevidence, competing reconstructions, folk etymologies, false friends/cognates, areal contact, and unverified gaps. Confidence is per claim/edge: high, moderate, low, unknown. Never claim completeness beyond accessible evidence.
10. Deliver in the established order: scope; **definitions**; pronunciation/grammar; segmentation; earliest attestation; each word's independent evolution; whole phrase's development; chronological tree/table; sound changes; semantic history; cognates; disputes and gaps; footnotes and bibliography; QA summary. Provide machine-readable JSON only when requested; validate its fields before claiming validity.

### Structured data contract (optional JSON)
`target`, `language`, `senses[]`, `constituents[]`, `attestations[]`, `nodes[]`, `edges[]`, `semantic_events[]`, `sources[]`, `uncertainties[]`, `qa`. Each node has `id`, `form`, `language`, `date_range`, `gloss`, `attested`, `source_ids[]`, `confidence`. Each edge has `from`, `to`, `type`, `evidence_ids[]`, `confidence`. Validate all referenced IDs, ordering constraints, and graph acyclicity for ancestry edges. Cognate links are nonancestral and excluded from ancestry cycle tests. Unknown fields must be null or explicitly absent, never made up.

### /Perfect visual system
Set the visual specification **before** generating any requested illustration: midnight navy, restrained electric cyan, high-contrast opaque text panels, typographically faithful IPA and historical scripts, responsive iPhone-first layout, WCAG 2.2 AA targets, keyboard navigation, accessible tables, reduced-motion support, and an alternate print-friendly view. Distinct contextual imagery may accompany /banner and /images, but never serves as historical proof. Prefer vector/SVG for exact tree diagrams; do not use generative imagery to render critical linguistic labels. No duplicate illustrations without explicit user authorization. Preserve the existing /copyright and source-credit rules.

### /Final iterative release gates
Run a substantive research QA pass and a separate accessibility/visual QA pass. Required checks: target unchanged; every sense sourced or marked uncertain; every constituent covered or identified as unresolved; all graph nodes and edges supported or marked hypothetical; chronology consistent; reconstructed forms prefixed `*`; cognates not mislabeled ancestors; quotations and bibliographic details verified; no invented dates, IPA, citations, or sources; no clipped diagrams; readable Unicode; functioning links where verifiable; consistent output between text, chart, and JSON. Correct defects and rerun checks until all verifiable criteria pass or a genuine blocker is documented. Stop rather than endlessly looping when no additional evidence or tools are available. `C` (Complete) may be asserted only for verified applicable acceptance criteria; otherwise report `Partial — unresolved evidence/QA` with precise blockers. Do not claim a PDF, deployment, synchronization, or rendered audit occurred unless actually performed.

### Regression cases
Test `ET yellow` (single word and historical sound changes), `ET savoir-faire` (hyphenated multiword phrase), `ET *bʰer-` (reconstructed root), `ET bank` (homographs), and `ET hot dog` (independent constituent histories versus idiomatic phrase meaning). Verify language detection and quoted target preservation. Regression cases are specifications until actually executed; never mark them passed solely because they are listed.
