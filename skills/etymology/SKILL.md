---
name: etymology
description: Evidence-grounded doctoral-level historical linguistic analysis of a user-supplied lemma, phrase, or reconstructed root, with attestations, cognates, phonology, and cited sources.
---

# ETYMOLOGY v2.0.0 — Research Skill

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
