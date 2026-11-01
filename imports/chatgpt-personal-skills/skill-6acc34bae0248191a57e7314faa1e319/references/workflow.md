# Annotation and publication reference

## Evidence-bearing annotations

Use exact IDs from records.json; use the document_id for document assertions. An annotation is a semantic decision by the invoking agent, not a discovered fact merely because the CLI accepts it.

```json
{
  "claims": [
    {
      "subject": "urn:uuid:REPLACE-WITH-SOURCE-DOCUMENT-ID",
      "predicate": "@type",
      "value": "ScholarlyArticle",
      "record_id": "urn:uuid:REPLACE-WITH-RECORD-ID",
      "quote": "exact contiguous supporting source excerpt",
      "rationale": "Explain why the excerpt and document context justify this classification.",
      "status": "accepted",
      "explicit": false,
      "context": "assertion"
    }
  ],
  "coverage": {
    "urn:uuid:REPLACE-WITH-RECORD-ID": {
      "status": "mapped",
      "rationale": "Explain the mapping or why document context suffices."
    }
  },
  "review_rounds": 2
}
```

Allowed statuses: mapped, inherits, no-useful-mapping, unresolved. Use source quotations without fabrication. Types and relations are derived semantic decisions even when explicitly justified. Literal values marked explicit must appear in the quote (except identity URLs and type labels). Every relationship must independently have evidence. New referenced local entities need accepted type/name assertions. `sameAs` requires established identity, not a similar name or a citation.

Repeated exact entity IDs are merged. Automatic document duplicates are detected by byte digest; sources remain in manifest. Claims with competing scalar values are withheld and appear in conflicts. Review conflict resolution manually rather than substituting a multi-valued array. Types and genuine relationships can be multivalued. Ordinary text in a quotation does not authorize asserting real-world prices, events, or affiliations.

## Mapping review

Investigate CreativeWork, Article, ScholarlyArticle, Book, Chapter, Dataset, Table, ImageObject, VideoObject, AudioObject, SoftwareApplication, Person, Organization, DefinedTerm, FAQPage, Question, Answer, HowTo, and procedural components only when their definitions fit. Plain headings are not necessarily chapters. A table is not necessarily a dataset. Questions without supplied answers are not an FAQPage. Do not infer purchase offers from product mentions. Classify entities using source context and vocabulary definitions, not keywords alone.

Use `hasPart`/`isPartOf` for genuine composition, `about` for central subject matter, `mentions` for incidental subjects, and `citation` for referenced works. Use `encodingFormat` for file format; distinguish file metadata timestamps from publication dates. Do not copy organization defaults from unrelated projects.

Schema.org domainIncludes/rangeIncludes express guidance. The CLI checks known vocabulary, inheritance/domain guidance, numeric/date shapes, types, absolute identifiers, local references, JSON-LD expansion/compaction and RDF equivalence. The agent must inspect range guidance from term lookup and resolve warnings; syntax validation cannot prove contextual truth.

## Outputs and privacy

Public candidates: corpus.jsonld, corpus.min.jsonld, corpus-jsonld.html, documents/*.jsonld. Private working records: manifest.json, records.json, evidence.json, annotations.json, identity-registry.json, cache/, index.sqlite. Validation reports may expose private identifiers or conflicts; review before sharing.

The HTML block uses application/ld+json and escapes less-than characters. The full corpus belongs only on an appropriate corpus page. For individual pages, use a relevant per-document graph. PDFs and office documents use JSON-LD sidecars unless their format supports an expressly requested attachment/metadata integration. No universal script injection into binary files exists.

The bundled vocabulary is retrieved from Schema.org's latest published download endpoint. See vocabulary-provenance.json for actual retrieval/checksums; graph isPartOf/version terms preserve release information. Runtime never fetches remote contexts. A new release requires replacing both official files and recording checksums before retesting. Official sources:

- https://schema.org/docs/datamodel.html
- https://schema.org/docs/developers.html
- https://www.w3.org/TR/json-ld11/
- https://www.w3.org/TR/json-ld11-api/
- https://developers.google.com/search/docs/appearance/structured-data/sd-policies
