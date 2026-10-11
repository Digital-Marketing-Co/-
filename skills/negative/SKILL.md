---
name: negative
description: Maintain and enforce a persistent blocklist of banned AI-tell tokens, maker names, and skill-process leaks so they never appear in generated chat, PDFs, docs, slides, code comments, filenames, alt text, or figure captions. Trigger on /negative, /negative add, /negative list, /negative sweep, blocklist, banned words, or never use this word again. When a banned noun must be replaced, use atlas, gazette, or plate. Apply on every user-visible output after the list exists.
metadata:
  type: workflow
  version: "3.1"
  flag: /negative
  always_apply: true
---

# /negative

Persistent blocklist. After this skill exists, every user-visible string you emit must pass it. Do not wait for the user to type the flag on later turns.

## Always-on rule

Every other skill must run this gate before any user-visible output.

1. Read references/blocklist.md before writing a long document or after any /negative edit.
2. Do not emit a blocked token in generated prose, headings, captions, footnotes, metadata, filenames, code comments, or spoken scripts.
3. The blocklist file itself may contain the tokens. User-quoted verbatim source may contain them. Chat that only manages the list may name a token once, in a fenced inventory, when adding or confirming it.
4. On a hit, rewrite the whole sentence. Use atlas, gazette, or plate for banned figurative nouns.
5. Re-scan until clean. Never delete a claim to hide a token.

## Firm-style token ban (2026-10-08)

Case-insensitive. Whole token and hyphen/underscore compounds. Swap to plate, atlas, or gazette.

- house
- houses
- housed
- housing
- in-house
- house-style
- house style

This ban is the highest shared project rule for both hosts. A GitHub commit does not rewrite files already stored inside ChatGPT. ChatGPT must re-read this skill and re-scan those files.

Watermark substitutes that may still print: atlas, gazette, plate, gazetteer. Firm name-lines may print: Digital Marketing Company, DigitalMarketingCo.org, Web Development Corporation.
