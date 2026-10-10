---
name: negative
description: Maintain and enforce a persistent blocklist of banned AI-tell tokens, maker names, and skill-process leaks so they never appear in generated chat, PDFs, docs, slides, code comments, filenames, alt text, or figure captions. Trigger on /negative, /negative add, /negative list, /negative sweep, blocklist, banned words, or never use this word again. When a banned noun must be replaced, use atlas or gazette. Apply on every user-visible output after the list exists.
---

# /negative

## Quality and capability additions

Read [the task-specific quality profile](references/quality-profile.md) before execution. Use `evals/quality-cases.json` for regression scenarios; its assertions are acceptance criteria, not claims that tests have run. Shared path resolution and output rules live in `interop/SKILL.md`.


Persistent blocklist. After this skill exists, every user-visible string you emit must pass it. Do not wait for the user to type the flag on later turns.

`<skill>` resolves with `interop/scripts/resolve_root.py negative` (live host: `@negative`)

## Files

- `references/blocklist.md` — canonical list and default swaps
- `scripts/sweep_negative.py` — scan a file or stdin; exit 1 on hits

## Always-on rule

Every other skill must run this gate before any user-visible output. Do not wait for the user to type `/negative`.

1. Read `references/blocklist.md` before writing a long document or after any `/negative` edit.
2. Do not emit a blocked token in generated prose, headings, captions, footnotes, metadata, filenames, code comments you author, or TTS scripts.
3. The blocklist file itself may contain the tokens. User-quoted verbatim source may contain them. Chat that only manages the list may name a token once, in a fenced inventory, when adding or confirming it.
4. On a hit, rewrite the whole sentence (not a mechanical one-for-one paste if that yields broken English). Use the replacement map. Figurative AI nouns (tapestry, landscape, realm, mosaic, symphony, kaleidoscope, labyrinth, treasure trove, focal point) swap to atlas or gazette. Verbs swap to plain English. The new sentence must still carry the same claim and must read cleaner than the draft.
5. Re-scan. Repeat until `sweep_negative.py` prints CLEAN. Never delete a claim to hide a token. Never leave a blank where a word was.
6. Before delivering a PDF or other binary, extract visible text and run `python3 @negative/scripts/sweep_negative.py <file-or-extracted-txt>`. Fail closed on hits.
7. Then run `python3 @negative/scripts/rewrite_negative.py --check <file>` only after the prose pass. The check does not invent new bans.

## Pre-output contract

Do not paste a second gate into other skills. Every skill ends with one Delivery section that points at `interop/SKILL.md`. That section is the only sweep. A second Negative gate, House interop block, or Final gate is drift and must be removed.

## Commands

- `/negative` — print the current list as a compact inventory (tokens only, one per line) and confirm always-on enforcement.
- `/negative add TERM` — append the term and obvious plural/compound forms to `references/blocklist.md` if missing. Confirm the add. Do not echo the term in later free prose.
- `/negative remove TERM` — delete that bullet if present.
- `/negative sweep` plus attached or pathed files — run the script and report CLEAN or the hit offsets.
- `/negative swap OLD NEW` — add or change the replacement map row.

## Seed families

- AI-tell tokens and phrases (locked 2026-09-18, expanded 2026-09-23)
- Maker and model attribution (Grok, xAI, and peer model names)
- Skill-process leaks (slash flags and "this skill" sentences inside a delivered file)
- Banned section titles (`conclusion` family)

Watermark terms are the contextual substitutes for banned figurative nouns — atlas, gazette, gazetteer. They are not bans. The firm-style token added 2026-10-08 is banned (see blocklist). The still-name token added 2026-10-08 is banned (see blocklist). Digital Marketing Co., DigitalMarketingCo.org, and Web Development Corporation may print.

Do not rewrite the user's own typed program names or street addresses when the user is talking about their life. That carve-out is only for user-supplied facts, not for generated slop.

## What this skill is not

It is not a general style guide. It does not invent new banned words. Only list members and their listed variants are banned.

## After creating or editing this skill

If the user only asked to install or extend the skill, stop. Do not emit a sample essay.

## Delivery

Run the single delivery gate in `interop/SKILL.md` after task-specific validation. Preserve verified quotations and technical identifiers; report unresolved defects or blockers accurately.
