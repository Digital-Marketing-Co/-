# Changelog

## 2026-10-16

- Added hyphenated negative compounds and explicit gazetteer variants (“-gazetteer”, “gazetteer-”, and any hyphen/underscore compound containing a blocked token). Added high-signal AI-tell tokens and phrases from Graphite 2026, Kobak et al. (Science Advances 2025), Wikipedia Signs of AI writing, and GPTZero inventories after deep/iterate research. Density of style words remains the primary signal.
- Added a humanize function at the end of the skill. After the blocklist gate, generated prose is rewritten to above-PhD density: concrete verbs, source-tied claims, varied sentence length, no stock cadence. The pass re-scans until clean and keeps all locked house tokens byte-stable.

## 2026-10-08

- Version 3.1. User order: ban the firm-style token and its plural and compound forms. Removed that token from the allowed watermark carve-out. Default swap is plate, atlas, or gazette. Always-on gate unchanged.
