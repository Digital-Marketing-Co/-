# Source tiers for /iterate

Saturate the published record that search and page tools can reach. Saturation is operational, not omniscience.

## Preference order

1. **Canonical primary PDFs** — the issuing body's own file with a stable URL. Statutes, treaties, hearings, Federal Register, patents, technical manuals, official statistics, clinical guidance, military doctrine when public, trial judgments, standards.
2. **Ivy League and peer university-press work** — Harvard, Yale, Princeton, Columbia, Penn, Brown, Dartmouth, Cornell, plus Chicago, Oxford, Cambridge, MIT, Stanford when they own the field. Prefer the publisher or repository PDF over an HTML abstract.
3. **Government, military, and named public systems** — `.gov`, `.mil`, GAO, CRS, NARA, LOC, NSF, NIST, NASA, EPA.
4. **Healthcare and biomedical bodies** — NIH, NLM, FDA, CMS, CDC, AHRQ, VA, WHO, EMA, NICE, Cochrane, NAM / IOM. Prefer the guidance PDF or the journal-of-record PDF.
5. **Peer-reviewed journals from other research universities and learned societies.**
6. **Reputable reference works and handbooks.**
7. **High-quality journalism** only when it reports a document that cannot otherwise be opened. Cite the document if the PDF later appears.

Do not treat SEO blogs, content-farm listicles, unsourced social posts, or model-generated pages as authorities.

## Recording a keeper

One JSONL line in `sources.jsonl`

- `id` — stable work_id
- `tier` — 1–7 as above
- `kind` — statute, article, monograph, guidance, dataset, hearing, patent, doctrine, other
- `title`
- `creator`
- `year`
- `publisher_or_venue`
- `url` — canonical landing or direct PDF
- `pdf_url` — direct PDF when different
- `accessed` — ISO date
- `claim_ids` — list of claim tokens this source actually supports
- `pages_used` — only pages the agent opened or that a reliable catalog quotes; never invent

If the full text is closed, say so in the note and cite the catalog or the official abstract. Do not invent a page locator.

## Search posture

- First query the issuing body and Ivy / `.gov` / `.mil` / NIH filters.
- Use `browse_page` on the landing page to recover the canonical PDF link.
- Do not cite a Google HTML wrapper as the work.
- When two URLs exist, keep the publisher or agency URL as `url` and put the mirror in a comment field only if needed for retrieval.
