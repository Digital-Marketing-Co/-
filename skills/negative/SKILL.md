---
name: negative
description: Maintain and enforce a persistent blocklist of banned tokens so they never appear in generated chat, PDFs, docs, slides, code comments, filenames, alt text, or figure captions. Trigger on /negative, /negative add, /negative list, /negative sweep, blocklist, banned words, never use this word again, or when adding House, plate, or later tokens. Apply on every user-visible output after the list exists.
metadata:
  type: workflow
  version: "1.0"
  flag: /negative
  always_apply: true
---

# /negative

Persistent blocklist. After this skill exists, every user-visible string you emit must pass it. Do not wait for the user to type the flag on later turns.

`<skill>` = `/home/workdir/.grok/skills/negative`

## Files

- `references/blocklist.md` — canonical list and default swaps
- `scripts/sweep_negative.py` — scan a file or stdin; exit 1 on hits

## Always-on rule

1. Read `references/blocklist.md` before writing a long document or after any `/negative` edit.
2. Do not emit a blocked token in generated prose, headings, captions, footnotes, metadata, filenames, code comments you author, or TTS scripts.
3. The blocklist file itself may contain the tokens. User-quoted verbatim source may contain them. Chat that only manages the list may name a token once, in a fenced inventory, when adding or confirming it.
4. If a draft still contains a hit, rewrite with the default swap in the blocklist file. Then re-scan.
5. Before delivering a PDF or other binary, extract visible text when possible and run `python3 scripts/sweep_negative.py <file-or-extracted-txt>`. Fail closed on hits.

## Commands

- `/negative` — print the current list as a compact inventory (tokens only, one per line) and confirm always-on enforcement.
- `/negative add TERM` — append the term and obvious plural/compound forms to `references/blocklist.md` if missing. Confirm the add. Do not echo the term in later free prose.
- `/negative remove TERM` — delete that bullet if present.
- `/negative sweep` plus attached or pathed files — run the script and report CLEAN or the hit offsets.
- `/negative swap OLD NEW` — add or change the replacement map row.

## Seed families (locked 2026-09-18)

Keep the document-jargon family and the AI-tell family in `references/blocklist.md`. Prefer swaps `firm` / `locked` / `standing` for the style sense and `figure` / `display equation` / `title block` for the figure sense. For AI-tell hits, drop the stock opener or closer, or swap to short plain English per the replacement map.

Do not rewrite the user's own typed program names or street addresses when the user is talking about their life. That carve-out is only for user-supplied facts, not for generated report jargon.

## What this skill is not

It is not a general style guide. It does not invent new banned words. Only list members and their listed variants are banned.

## After creating or editing this skill

If the user only asked to install or extend the skill, stop. Do not emit a sample essay.
