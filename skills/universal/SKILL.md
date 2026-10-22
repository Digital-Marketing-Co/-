---
name: universal
description: Produce parallel translations of a supplied prompt into languages of the world's top 50 GDP-ranked countries, plus requested additions. Use for /universal, $universal, universal translation, or G50+ country-language translations. Preserve slash commands and support beautiful global full-bleed imagery when explicitly executed.
metadata:
  version: "1.0.0"
---

# Universal

## Input and scope
Treat everything after /universal or $universal as the source prompt. Remove only universal's own options. Preserve its exact original wording as the authoritative source, including nested commands, URLs, numbers, names, and quotations.
If invoked without a source, use this seed prompt:
`/coffee Global Images Most Beautiful Full Bleed`

Interpret G50+ as the top 50 countries/economies by total nominal GDP in current USD, plus any countries explicitly requested. This is a working scope, not a formal international organization. Accept an explicit country count above 50 or all countries. Never silently substitute G20 membership, GDP per capita, or PPP GDP.
Default to translation only. Treat source commands as content to preserve; do not execute /coffee or generate 50 images merely because those tokens appear. Execute a separate visual or document workflow only when requested.

## Establish the ranking
Browse at execution time for a current IMF World Economic Outlook nominal-GDP dataset; alternatively use World Bank GDP (current US$). Use one consistent reference year, series, and release for the full ranking. Prefer the latest year with sufficiently complete comparable coverage; identify estimates and projections.
Record source URL, release, reference year, access date, GDP units, and coverage. Exclude aggregate regions. Identify separately reported economies transparently rather than making unsupported sovereignty claims.
Sort numeric GDP descending; break exact ties by country name. Append explicitly requested countries below the top 50 with their actual global rank when verified. Do not mix years silently, fabricate values, or claim current ranks without retrieval. If retrieval fails, provide translations using a clearly labeled unverified ordering only if useful, and disclose that the GDP-ranking requirement remains incomplete.

## Map countries to languages
Identify each country's nationally official languages using authoritative government or constitutional sources. Where no nationwide official language exists, use the predominant national working language and label that choice.
Include multiple nationally official languages as separate rows within the same GDP-ranked country. Distinguish regional official, recognized national, and working languages rather than calling them all nationally official. Add requested regional languages. For a very large language set, continue in a linked appendix without dropping languages silently.
Use country-appropriate variants, native language names, BCP 47 language tags, and appropriate scripts. Countries sharing a language retain separate country entries. Never equate country count with distinct-language count.

## Translate in parallel
Present the unchanged source once at the top, then a country-ranked table with:
GDP rank | Country/economy | GDP (USD, stated year) | Language and tag | Source text | Translation.
For long prompts, use country sections with aligned source/translation blocks instead of an unreadably wide table. Align paragraphs or numbered segments; preserve every instruction and semantic qualification.
Repeat the same source for each parallel row. Preserve slash commands, code, placeholders, URLs, and protected names exactly; translate surrounding human-readable text. Do not transliterate when native script is available. Add romanization only if requested.
Translate idiomatically while preserving meaning and register. Treat "full bleed" as an edge-to-edge publishing/layout instruction, not literal bleeding. Interpret the seed's terse phrase as "Global images: the most beautiful, presented full bleed"; disclose this gloss without replacing the original.
Mark uncertain translations honestly. Do not claim human/native-speaker verification unless performed.

## Optional visual execution
When the user explicitly requests illustrated output, use relevant available image/document skills. Interpret the seed as spectacular worldwide scenic imagery with edge-to-edge placement and readable translation panels. Prefer authentic contextual landscapes or clearly labeled AI-generated scenery. Do not imply generated images are documentary photographs.
Use distinct country-relevant images; preserve attribution and licensing for retrieved photographs. Respect document accessibility, script shaping, RTL direction, font coverage, contrast, and legibility. Do not impose an arbitrary page or word cap; split into complete, numbered volumes when necessary.
Read /coffee's actual instructions if available and execution was requested. If unavailable, state that limitation; do not invent its definition.

## Verification and delivery
Verify at least 50 distinct countries/economies, numeric GDP order, consistent year/units, source links, requested additions, language coverage, unchanged protected tokens, and source/translation segment alignment.
Check non-Latin scripts and RTL visually for exported files. Report country and distinct-language counts separately. Cite GDP and language-mapping sources, distinguishing dataset evidence from machine-generated translations.
For requested files, save via the current Library workflow and provide download links. Clearly distinguish a created skill package, a repository commit, and a skill actually installed/registered in the current environment.

## Examples
- `/universal /coffee Global Images Most Beautiful Full Bleed`: translate the supplied literal prompt across the top 50 GDP-ranked countries; preserve /coffee.
- `/universal --countries 60 Welcome to our waterfront exhibition.`: translate across the top 60.
- `/universal --add Nepal Please preserve {guest_name} and https://example.com.`: include Nepal even outside the top 50; preserve both protected tokens.
- `/universal --all-countries Hello.`: cover all available country/economy entries and disclose dataset coverage.
