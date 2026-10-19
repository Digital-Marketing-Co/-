---
name: negative
description: Maintain and enforce a persistent blocklist of banned AI-tell tokens, maker names, and skill-process leaks so they never appear in generated chat, PDFs, docs, slides, code comments, filenames, alt text, or figure captions. Trigger on /negative, /negative add, /negative list, /negative sweep, blocklist, banned words, or never use this word again. When a banned noun must be replaced, use atlas, gazette, or plate. Apply on every user-visible output after the list exists.
metadata:
  type: workflow
  version: "3.2"
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

## Humanize function (above-PhD level)

After the blocklist gate passes, run this humanize pass on any long generated prose, abstract, section text, caption, or skill connective tissue before delivery. The target is above-PhD density: precise, evidence-bearing, and free of stock cadence, while remaining inside the source claims.

### Procedure

1. Sweep the draft with `scripts/sweep_negative.py`. Exit 1 blocks the pass. Rewrite every hit so the sentence is tighter and still carries the original claim. Use atlas, gazette, or plate only when a banned figurative noun must stay.
2. Raise register without filler. Prefer concrete verbs that name an operation (project, slice, differentiate, tabulate, cite) over vibe verbs. Prefer measured quantifiers and source-tied claims over intensifiers.
3. Vary sentence length. A long evidential sentence may be followed by a short one that states the consequence. Do not open with throat-clearing about importance, landscape, or realm.
4. Keep every proper name, date, measurement, equation identifier, path, URL, and house rule that the source already contains. Do not invent facts, citations, page numbers, or locked house numbers.
5. Re-scan. The final text must exit 0 from the sweep and contain none of the high-signal phrases listed in references/blocklist.md under the 2026-10-16 sections.

### Above-PhD voice rules

Do

- Lead with the claim or the measurement.
- Attach every quantitative relation to its source or to the local equation.
- Use the ordinary English name of a symbol on first appearance, then the glyph.
- Let technical terms stand; do not replace them with decorative synonyms.
- Preserve citation markers and ITQE column headers exactly.

Do not

- Open with “in today’s,” “it is important to note,” “when it comes to,” or “this matters because.”
- Stack three elevated adjectives in front of one noun.
- Use negative parallelism (“it is not X, it is Y”) as a default hinge.
- Insert a moral, an anecdote, or a metaphor domain the source does not contain.
- Print any token from the blocklist, including hyphenated compounds that contain a blocked component.

When the source is a house skill file, humanize only connective sentences. Flag names, paths, owner strings, point sizes, and the copyright appendix stay byte-stable.

Default swaps for residual style density appear in references/blocklist.md. After the humanize pass, re-run the sweep once more. Delivery is blocked until the text is clean.
