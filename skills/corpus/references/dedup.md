# Deduplication

One intellectual work, one keeper.

## Keys, in order

1. Normalized DOI (`https://doi.org/` stripped, lowercased)
2. PMID
3. PMCID mapped through PubMed to a PMID/DOI
4. ISBN-13 (hyphens stripped)
5. Patent number (kind code stripped for grouping, kept on the record)
6. NCT ID
7. Grant ID (activity + institute + serial)
8. Fallback fingerprint — `norm_title + year + first_author_family`

`scripts/dedup_works.py` applies this order.

## Title normalize

Lowercase. Strip punctuation. Expand common Greek and numeral words only when they already appear as words. Remove trailing noise

- `: a review`
- `: case report` kept if it is the real subtitle (do not strip unique subtitles)
- publisher prefixes (`accepted manuscript`, `author manuscript`)

Two titles that match after normalize and share year + first author merge even without a DOI.

## Merge policy

When two records collapse

- Prefer the record that has a DOI
- Then the record that has pages and volume
- Then the publisher URL over PMC, ResearchGate, or Academia.edu
- Union of identifiers (keep PMID and DOI together)
- Union of `source` tags
- Keep the earliest `accessed` and the richest `affiliation_evidence`

Reprints, translations, and PMC author manuscripts are the same work. Put the alternate appearance in `also` on the keeper. Do not list them as separate bibliography lines.

Errata and retractions are **separate** works with `type` `erratum` or `retraction` and a `corrects` / `retracts` id pointing at the original. They stay in the catalog so the record is honest.

## Near-duplicates that stay separate

- Distinct chapters in the same book
- Serial review updates with different years (`2012` vs `2019` guideline)
- Conference abstract later expanded into a paper — keep both, link with `related_id`
- Continuation grants with different years

## Report

`dedup-report.md` lists merge groups, the winning id, and the discarded ids. A human should be able to undo a bad merge from that file alone.
