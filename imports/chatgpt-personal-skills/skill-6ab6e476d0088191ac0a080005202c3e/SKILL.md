---
name: format
description: Reformat quoted text after the /format flag into Proper Case, UPPERCASE, lowercase, or Small Caps using case-insensitive acronyms PC, UC, AC, LC, and SC. Use when the user types /format, asks for Proper Case email subjects, All Caps, lowercase, or small-caps restyling of a quoted string.
---

## Shared interactive quality contract

Before execution, resolve the installed personal skill with frontmatter name `doc` and read `references/output-contract.md` once per run. This is a shared reference, not a recursive call to doc. Apply its proportionate intake, functional QA, independent visual QA, repair, revision invalidation and truthful release requirements to the requested output. Reuse answers and completed matching phases across handoffs. Preserve this specialist’s purpose and user requirements; do not force artwork, redesign, a book or deployment onto a simple utility. The shared quality contract supersedes conflicting legacy defaults about duplicate intake or unsupported pass claims; explicit user and platform instructions prevail. If the reference is unavailable, disclose the missing integration and perform the same checks proportionately rather than inventing a pass.


# /format

Take the quoted string after `/format` and rewrite only its letters into the case the acronym names. Do not invent text. Do not edit unquoted instructions.

`<skill>` = `@format`

If the user only asked to create or revise this skill and supplied no quoted payload, stop after the skill files exist. Do not invent a subject line.

## Read on demand

- `references/modes.md` — alias table and Unicode small-cap map
- `scripts/format_case.py` — locked transformer

## Trigger

- `/format` plus a mode token plus text in `'...'` or `"..."`
- `/format PC`, `/format Proper Case`, `/format ProperCase`
- `/format UC`, `/format UPPERCASE`, `/format AC`, `/format All Caps`
- `/format LC`, `/format lowercase`
- `/format SC`, `/format smallcaps`, `/format Small Caps`
- Same request in prose (`put this subject in proper case`) when the payload is still quoted or fenced

Mode tokens are case-insensitive. `pc`, `PC`, `Pc`, `proper case`, and `ProperCase` are the same mode.

## Parse the prompt

1. Strip the `/format` flag (any capitalization).
2. Read the first mode token. A mode token is one of the aliases in `references/modes.md`, including multi-word names `Proper Case`, `All Caps`, `small caps`. Match case-insensitively.
3. Take every single-quoted or double-quoted span after the mode as a payload. Also accept one fenced code block. Do not treat the wrapping quotes as part of the string.
4. If there is a mode and no payload, ask for the quoted string. If there is a payload and no mode, ask which of `PC`, `UC`/`AC`, `LC`, `SC` to use. Do not guess.

Several quoted spans in one prompt are several jobs. Run each span through the same mode. Keep span order.

## Transform

Always run the locked script. Do not hand-case the letters.

```bash
python3 @format/scripts/format_case.py --mode MODE --json -- "PAYLOAD"
```

`MODE` is the raw alias the user typed (`PC`, `All Caps`, `sc`, …). The script normalizes it.

Locked behavior

- `PC` — first letter of each whitespace-separated token uppercase; later letters lowercase
- `UC` / `AC` — every letter uppercase
- `LC` — every letter lowercase
- `SC` — first letter of each token a full capital; later letters Unicode small capitals (`Hᴇʟʟᴏ`)

Whitespace, digits, emoji, and punctuation stay exactly where they were. Do not collapse spaces. Do not wrap lines. Do not "fix" spelling.

## Reply

For each payload, in this order

1. One-line label of the mode (`Proper Case`, `UPPERCASE`, `lowercase`, `Small Caps`)
2. The reformatted string in a fenced code block so it pastes cleanly into an email subject or form
3. Nothing else unless the user also asked a question

Do not add quotation marks around the result unless the source inside the quotes already had inner quotes.

If the script exits non-zero, print the stderr and stop. Do not silently fall back to a manual rewrite.

## Stacking

`/format` only changes case. If the user also stacked `/summarize`, `/folio`, `/deep`, or another house flag, apply `/format` to the quoted payload first, then hand the reformatted string to the other skill only when that other skill was explicitly requested.

Do not emit a PDF, banner, or monograph for a `/format` request alone.


## Negative gate (mandatory before any deliverable)

Read `@negative/SKILL.md` and `@negative/references/blocklist.md`.
Before chat, PDF, DOCX, PPTX, XLSX, caption, filename, alt text, or footnote leaves this skill, extract visible text and run

```bash
python3 @negative/scripts/sweep_negative.py <extracted-text>
```

Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.

## ChatGPT portability

Resolve `@skill-name/path` by finding the installed personal skill whose SKILL.md frontmatter has `name: skill-name`; read that path under its directory. For `@generate/`, use the `generate-prompt` skill. Before running copied shell commands, substitute actual resolved paths and use the current working directory for generated files. Apply instructions only when this skill is invoked or a user requests the corresponding workflow. User instructions and platform rules take priority. Run bundled scripts only after checking their inputs and prerequisites. Never claim unavailable integrations, credentials, citations, or generated results.
