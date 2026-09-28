# Identity resolution

The match string is a query, not a finished heading.

## Parse

Split tokens into four buckets.

1. Name core — given, middle, surname, particles (`de`, `van`, `Jr`).
2. Credentials — `MD`, `PhD`, `DO`, `RN`, `DVM`, board letters.
3. Agency / employer — university, hospital, `NIH`, `NCI`, `ARMY`, `USA`, `USN`, `USAF`, `DIA`, `DoD`, institute.
4. Hard IDs — ORCID (`0000-0000-0000-0000`), email, grant PI ID, Semantic Scholar author ID, OpenAlex author ID (`A` + digits).

Credentials and agency tokens **filter** the name core. They are not extra subjects.

## Variant set

Always search at least

- Full official form (`Andrew M. Yeager`)
- No middle (`Andrew Yeager`)
- Initials (`A. M. Yeager`, `Yeager AM`, `Yeager A`)
- All-caps PubMed style (`Yeager AM`)
- Hyphen / no-hyphen if the surname can take either

Add a maiden or earlier professional name only when a source states it.

## Confirm

A hit is the match when **two** of these agree, or when one hard ID agrees.

- ORCID record whose name + affiliation match
- Faculty / emeritus page
- PubMed affiliation string that contains a known employer or city
- NIH RePORTER PI profile
- Author ID from OpenAlex or Semantic Scholar whose institutions overlap the disambiguators
- Named investigator on a `.gov` / `.mil` report that also carries the name core

A single Google hit on the surname is not confirmation.

## Reject

Write every rejected homonym to `rejected.jsonl` with `reason`. Typical collisions

- same surname, different middle initial, different decade of publication
- same name in an unrelated field (engineering vs pediatric hematology)
- news quotation, not authorship
- “et al.” lists that do not include the resolved person after the full text or PubMed author list is checked

If two plausible living researchers remain after the filters, stop harvest and ask. Do not merge labs.

## Identity card fields

`identity.json`

- `heading`
- `variants` (array)
- `orcid`
- `openalex_id`
- `s2_author_id`
- `affiliations` (name, place, years)
- `disambiguators` (the leftover tokens)
- `rejected_homonyms`
- `confidence` (`high` | `medium` | `blocked`)
