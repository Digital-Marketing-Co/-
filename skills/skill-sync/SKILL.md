---
name: skill-sync
description: Sync custom skills with the Digital-Marketing-Co/- GitHub repository so Grok and ChatGPT use the same committed skill tree. Use when the user types /skill-sync, asks to sync skills, update a skill on GitHub, or keep ChatGPT and Grok on the same skill revision.
metadata:
  type: workflow
  version: "3.0"
  flag: /skill-sync
  owner: Web Development Corporation
---

# /skill-sync

Keep Digital-Marketing-Co/- as the shared skill source for Grok and ChatGPT.

## When this skill runs

- User typed /skill-sync.
- User asked to update the GitHub skill repo after a skill change.
- User asked Grok and ChatGPT to stay on the same skill revision.

## Steps

1. Read SKILL-SYNC.md and skills/ledger/latest.md on main.
2. List skills/<name>/SKILL.md on main.
3. Compare each with the installed copy. Decide direction from commit time and the ledger, not from a hash alone.
4. If the installed copy is the newer verified version, commit that skill directory to main and prepend a ledger row: date, skill, direction, short hash, one-line change.
5. If the repository copy is newer, use that copy for the current task and say which path was read.
6. Do not overwrite bundled host skills.
7. Report the commit URL, the skills checked, and the skills ChatGPT still has to re-upload.

## ChatGPT

ChatGPT cannot install from this push by itself. Tell the user to run the prompt in CHATGPT-PROMPT.md, or to re-upload only the skills named in the latest ledger.

## Delivery

Run this once, last, after every other section. Full contract: `interop/SKILL.md`.

1. Resolve the negative skill as the first existing directory among `/root/.grok/server-skills/negative` and `/home/workdir/.grok/skills/negative`.
2. Extract visible text from chat, the file, captions, filenames, and alt text.
3. Run `python3 <negative-root>/scripts/sweep_negative.py` on that text.
4. Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN.
5. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.
