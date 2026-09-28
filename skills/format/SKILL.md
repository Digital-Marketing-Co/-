---
name: format
description: Reformat quoted text after the /format flag into Proper Case, UPPERCASE, lowercase, or Small Caps using case-insensitive acronyms PC, UC, AC, LC, and SC. Use when the user types /format, asks for Proper Case email subjects, All Caps, lowercase, or small-caps restyling of a quoted string.
metadata:
  type: workflow
  version: "1.0"
  flag: /format
  updatable: true
---

# /format

Take the quoted string after `/format` and rewrite only its letters into the case the acronym names. Do not invent text. Do not edit unquoted instructions.

`<skill>` = `/home/workdir/.grok/skills/format`

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
python3 /home/workdir/.grok/skills/format/scripts/format_case.py --mode MODE --json -- "PAYLOAD"
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
