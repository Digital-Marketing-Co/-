# Dedup keys

One real-world instance equals one row in `items.jsonl`.

## Preferred identity key (first match wins)

1. Persistent public identifier (`DOI`, `ISBN`, `ISSN`, `PMID`, `ORCID` of a work, `CAS`, `NAICS` plus establishment id, official registry number, statute citation, ICAO/IATA, FIPS, NCES, UEI, DUNS when the user supplied it)
2. Canonical official name plus jurisdiction plus inception year
3. Normalized title plus first author plus year plus page or URL host
4. Lat/long to four decimals plus feature type (places only)

Store every key that exists. Merge when any strong key collides.

## Merge rules

- Keep the fullest official name.
- Union aliases into `also_known_as`.
- Keep the oldest attested date and the newest status date.
- Keep every source id. Do not drop a weaker source because a stronger one arrived.
- If two rows share a name but conflict on a strong identifier, they are not the same instance. Write the collision in `gaps.md` and keep both rows with a `disambiguation` note.

## Reject

- Homonyms that fail the unit of analysis
- Redirects and duplicate URLs of an already-kept row
- Aggregate headings that are not themselves instances (`see also`, category pages)
- Invented or reconstructed identifiers

## Printed number

The master inventory number is assigned after merge, in stable sort order (class, then official name, then year). Do not number during harvest. Renumber only when a later round inserts a row ahead of an existing one and the catalog has not yet been delivered.
