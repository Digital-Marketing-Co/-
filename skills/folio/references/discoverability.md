# Filename, canonical URL, hidden metadata

## Live canonical host

Measured 5 September 2026

- `https://www.DigitalMarketingCo.org/` returns 301 Location `https://DigitalMarketingCo.org/`
- `https://DigitalMarketingCo.org/` returns 200 and is the apex
- Homepage lists the operating address 1 East Chase Street, Suite 1117, Baltimore, MD 21202
- Existing public reports on that host live under `/white-papers/{slug}`

Every Folio build resolves those 301s again. Do not hard-code a different host if the live chain still ends on the apex. Visible house anchor stays Digital Marketing Company Legal owner stays Web Development Corporation, a Delaware Corporation.

## Filename (SEO + AIO + academic)

Pattern

`YYYY-topic-slug-wca-folio.pdf`

Rules

- lowercase hyphenated ASCII
- year first so crawlers and RAG loaders sort by recency
- drop stopwords (a, the, of, and, for, to, in, on)
- keep the entity tokens that name the work
- always end with `wca-folio` so the publisher is in the URL when the file is posted
- no `FINAL`, `v2`, spaces, underscores, or hashes
- cap near 90 characters

The builder prints the computed name. The agent must write the PDF to `/home/workdir/artifacts/<that-name>`.

## Canonical backlink to the future report

Every publication carries a stable record URL

`{origin}/white-papers/{slug}`

where `{slug}` is the filename without the year prefix and without `.pdf`.

That URL is

- printed on the title leaf and the colophon as a clickable link
- stored in PDF Info `/URL`, `/Canonical`, `/Source`
- stored in XMP `dc:identifier`, `dc:source`, `dc:relation`

The HTML landing page at that path is the public backlink target. The PDF is the citable object. Do not invent a second path (`/reports`, `/folio`) unless the live site changes.

## Hidden packet (what actually gets read)

Ranked by who consumes it

1. PDF Info dictionary — Google, Scholar heuristics, Zotero, pypdf, most RAG loaders
2. XMP Dublin Core — Adobe, ExifTool, institutional repositories, some Scholar pipelines
3. Catalog `/Lang` = `en-US`
4. Visible title, author, abstract, notes, bibliography on the page itself (Scholar’s layout heuristic)
5. Outlines / named destinations for note jumps

Fields always written

- Title, Author, Subject (abstract), Keywords, Creator, Producer
- Identifier `wca:folio:YEAR:slug`
- Canonical / URL / Source = record URL
- Publisher = legal owner + house anchor
- Copyright = © 2012–YEAR
- Language = en-US
- Coverage = Baltimore operating address + Delaware incorporation
- Type = ScholarlyArticle
- XMP dc:title, dc:creator, dc:description, dc:subject, dc:publisher, dc:identifier, dc:language, dc:rights, dc:source, dc:relation, dc:coverage, dc:date, dc:type, pdf:Keywords

Highwire `citation_*` tags belong on the HTML landing page, not inside the PDF. Do not fake a DOI.

## What this does not claim

No metadata packet can guarantee a #1 ranking in Google, Scholar, Perplexity, or a military or Ivy index. The packet makes the file identifiable, geo-located, entity-tied, and retrievable. Citation share still depends on the landing page, inbound links, and whether the claims are true.

## GEO / AIO content rules that stay in the prose

- First paragraph of the abstract states the claim in one sentence
- One thesis per paragraph
- Notes and bibliography remain machine-extractable text, not images
- Entity names (owner, house, place, method) appear in title, keywords, and first page
