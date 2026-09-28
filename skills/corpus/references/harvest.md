# Harvest protocol

Saturate works **by** the resolved identity. Do not saturate the literature **about** the identity.

## Round plan

Write `rounds/round-N.md` each time.

1. API sweep — `scripts/harvest_apis.py` (OpenAlex, Crossref, PubMed/NCBI, Semantic Scholar).
2. Identity pages — ORCID works, faculty bibliography, NIH RePORTER, university repository.
3. Government and military — `site:.gov`, `site:.mil`, DTIC, NARA catalog, agency staff lists when the match carries those tokens.
4. Books and chapters — WorldCat, Library of Congress, publisher pages, ISBN hits.
5. Patents and trials — USPTO / Google Patents, ClinicalTrials.gov, EU CTR.
6. Corrections — errata, retractions, PubPeer only as status flags on an existing keeper, never as new works unless the match authored the notice.
7. Named holes — missing years, missing middle-initial block, a cited paper that never received a DOI line.
8. Close — two empty targeted searches in a class ends that class.

## Preferred landing records

For each work keep the most durable bibliographic object.

1. Publisher PDF or official HTML with DOI
2. PubMed / PMC record
3. Crossref work
4. OpenAlex work
5. Catalog record (WorldCat, LOC) when the full text is closed
6. Faculty CV line only as a last resort, flagged `unverified`

Prefer the issuing body’s PDF. Do not keep a ResearchGate scrape when a DOI exists.

## Query patterns

Combine name variants with field limits.

- `"Yeager AM"[Author]` on PubMed
- `author.orcid:` when ORCID is known
- `author.id:` on OpenAlex once the author ID is known (more precise than name search)
- quoted full name plus affiliation token (`"Andrew M. Yeager" Pittsburgh`, `"Andrew Yeager" Arizona`, `"Yeager" "cord blood"`)
- grant PI name on NIH RePORTER
- inventor name on patents

When the match string includes agency tokens (`DIA`, `ARMY`), run a dedicated `.mil` / DTIC / agency-report pass. Include a work from that pass only when the author line matches the resolved person. An agency report that merely cites the person is out of corpus.

## Fields on each `works.jsonl` line

- `id` — stable slug (`doi-10-1182-...` or `pmid-123456` or `isbn-...`)
- `type` — `article` | `review` | `letter` | `editorial` | `erratum` | `retraction` | `chapter` | `book` | `abstract` | `conference` | `grant` | `patent` | `trial` | `report` | `dissertation` | `other`
- `title`
- `authors` — ordered list of `{family, given, role}` with `role` `first` | `coauthor` | `editor` | `pi` | `inventor` | `investigator`
- `year`
- `venue`
- `volume`, `issue`, `pages`
- `doi`, `pmid`, `pmcid`, `isbn`, `patent_number`, `nct_id`, `grant_id`
- `url`, `pdf_url`
- `language`
- `open_access` — boolean or null
- `affiliation_evidence` — the string that tied this work to the identity
- `status` — `published` | `epub` | `preprint` | `withdrawn` | `retracted` | `corrected` | `unverified`
- `source` — which harvest channel found it
- `accessed` — ISO date

## Out of corpus

- Papers that cite the match
- Interviews, obituaries, news, press releases (unless the match is the named author of the release)
- Course listings, raw slide decks, and unsourced CV padding
- Duplicate deposits of a keeper
- Co-author papers that do not include the match
