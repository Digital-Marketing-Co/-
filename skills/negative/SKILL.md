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

Maintain and enforce a persistent blocklist of banned AI-tell tokens, maker names, and skill-process leaks so they never appear in generated chat, PDFs, docs, slides, code comments, filenames, alt text, or figure captions.

## When this skill runs

- User typed /negative, /negative add, /negative list, /negative sweep.
- User said blocklist, banned words, or never use this word again.
- Any skill is about to deliver user-visible text after the list exists.

## Steps

1. Resolve the negative skill as the first existing directory among `/root/.grok/server-skills/negative` and `/home/workdir/.grok/skills/negative`.
2. Extract visible text from chat, the file, captions, filenames, and alt text.
3. Run `python3 <negative-root>/scripts/sweep_negative.py` on that text.
4. Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN.
5. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.

## Substitutes

When a banned noun must be replaced, use atlas, gazette, or plate.

## Firm style ban

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

- Prefer the verb that names the operation.
- Prefer the number that is in the source over the adjective that is not.
- Prefer the source name over "research shows".
- Prefer the page-local note over a trailing parenthetical.
- Prefer the concrete noun over the abstract one when both are available.

The humanize pass does not add claims. It only removes stock cadence and banned tokens.
