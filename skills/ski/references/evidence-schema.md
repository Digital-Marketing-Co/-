# Evidence schema

## sources.jsonl (one JSON object per line)

- id: S1, S2, ...
- authors
- year
- title
- venue_or_institution
- doi_or_stable_url
- pdf_url: only if opened, else empty
- access: pdf-opened | html-opened | abstract-only | inaccessible
- design
- sample
- methods
- findings
- limitations
- relevance
- accessed

## evidence-matrix.csv

claim_id, section, observation, interpretation, grade, source_ids, page_or_unverified, confounds, human_response, professional_referral, training_link

Grades: robust | provisional | consensus | hypothesis | unsupported

Do not fill page with a number unless that page was read in the opened file.
