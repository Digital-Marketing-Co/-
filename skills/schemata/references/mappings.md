# Schema.org Mapping Guidance

Load only when performing semantic mapping or reviewing candidates.

## Core Distinctions

| Concept | Schema.org | Rule |
|---------|------------|------|
| Document itself | CreativeWork (or specialized) | Always when the file is the work |
| Discussed entity | about / mentions | about only for principal subject; mentions for incidental |
| Structural part | hasPart / isPartOf + CreativeWork | Prefer over forcing unsupported specialized types |
| Explicit person/org | Person / Organization | Only when identity is clear in source |
| Dataset / Table | Dataset / Table | Only for actual data tables or datasets |
| FAQ | FAQPage + Question/Answer | Only for real Q&A pairs |
| Procedure | HowTo | Only for actual step-by-step instructions |

## Never Invent

Do not emit: Review, AggregateRating, Offer, PriceSpecification, PostalAddress, OpeningHoursSpecification, credential, biography, publication date, author, or sameAs unless explicitly established by the source or authorized enrichment with separate provenance.

## Identity Resolution

1. Exact canonical IRI or persistent identifier wins.
2. Name match alone is insufficient for Person or Organization merge.
3. Retain ambiguous candidates in the evidence/conflict report.
4. Keep distinct works, editions, and file representations separate.

## Evidence Ledger (separate from graph)

For every assertion record: subject, predicate, object, document ID, locator, short excerpt or digest, explicit vs derived, rationale.

Omit low-confidence or unverified claims from the publication graph.
