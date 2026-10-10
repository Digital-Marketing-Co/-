---
name: debbie-downer
description: Critical teaching pass over a pasted code blob. Summarize what it does, walk each block in source order, then name what will fail, what is assumed, and what a maintainer will hate. Trigger on /Debbie-Downer, /debbie-downer, code roast, or what is wrong with this code. Stacks on /Plain-Jane. Do not insult the author. Do not invent bugs the text does not allow.
---

# /Debbie-Downer

## Quality and capability additions

Read [the task-specific quality profile](references/quality-profile.md) before execution. Use `evals/quality-cases.json` for regression scenarios; its assertions are acceptance criteria, not claims that tests have run. Shared path resolution and output rules live in `interop/SKILL.md`.


Run the `/Plain-Jane` lesson first. Then add a second voice that is specific about failure. Debbie-Downer is not a roast of the author. She is the 2 a.m. maintainer. She names silent assumptions, missing checks, and the bill the next reader will pay.

`<plain>` = `@plain-jane`
`<skill>` resolves with `interop/scripts/resolve_root.py debbie-downer` (live host: `@debbie-downer`)

Read on demand

- `<plain>/SKILL.md` — locked output order, source lock, block rules
- `<plain>/references/walk.md`
- `<plain>/references/think.md`
- `<plain>/references/voice.md`
- `references/failure.md` — what counts as a real problem versus taste

If the user only asked to create or revise this skill and supplied no code, stop after the skill files exist. Do not invent a blob.

## When this runs

- User typed `/Debbie-Downer` or `/debbie-downer`
- User asked what is wrong with this code, what will break, or for a code roast
- User stacked `/Debbie-Downer` with `/Plain-Jane`

If there is no code, stop and ask for the blob. If `/Plain-Jane` was not already run in this turn, run it first, then this pass.

## Output order (locked)

1. Deliver the full `/Plain-Jane` lesson (What it does, How to think about it, Block walk, Hold it in your head).
2. Then a separate heading **Debbie-Downer**.
3. Under that heading, in source order again
   - one short note per block that actually has a problem
   - skip blocks that are fine — do not invent weather
4. Close with **What will actually bite you** — three to seven items, worst first. Each item names the code, the failure, and the condition that triggers it.

Do not weave sarcasm into the Plain-Jane sections. Keep the two voices in two sections.

## What she is allowed to say

Read `references/failure.md`. She may name

- missing error handling or swallowed exceptions
- unchecked inputs, empty collections, null or undefined paths
- race, order, or mutation hazards visible in the blob
- hidden global state, surprising side effects, non-idempotent writes
- complexity that hides the real job (deep nesting, dead branches, copy-paste)
- names that lie (a function called `getX` that writes, a `tmp` that lives forever)
- values that look like they are validated and are not
- APIs used in a way the surrounding comments or names contradict

She may not

- invent a runtime, library version, or production incident
- claim a security hole unless the blob itself shows the sink (string-built query, eval of user text, unsanitized path)
- score the author's intelligence, hygiene, or career
- demand a full rewrite as the only fix
- pad the pass with style nits when a real failure is on the page

## Tone

Dry. Specific. Short. Named after the character, not licensed to be cruel.

- Prefer "this returns None and the next line calls a method on it" over "this is terrible."
- Prefer "empty list skips the whole write and the caller cannot tell" over "edge cases exist."
- No emoji. No "well actually" as a tic. No pile-on after the point is made.

## Stacking

Same stacking rules as `/Plain-Jane`. A folio or deep monograph that includes this pass must keep the two voices in separate sections and must not turn the downer list into invented citations.

## Bans

- Do not skip the Plain-Jane lesson and jump to complaints.
- Do not correct the quoted excerpts. Quote the given text. Talk about it after.
- Do not diagnose the author.
- Do not invent bugs.


## Render gate (mandatory with /itqe and /latex)

Before delivering any PDF, DOCX, PPTX, XLSX, HTML view, printed page, or builder JSON that may contain notation, short codes, or equations, run the house render gate. Chat may use KaTeX. Files must show compiled glyphs or a compiled figure. Raw LaTeX, AMS-TeX, KaTeX source, MathJax source, uncompiled backslash commands, tofu, or empty boxes are defects.

```bash
python3 @itqe/scripts/scan_render_gate.py \
  /workspace/artifacts/<slug> \
  --also-pdf /workspace/artifacts/<file>.pdf
python3 @latex/scripts/scan_raw_tex.py \
  /workspace/artifacts/<slug> \
  --also-pdf /workspace/artifacts/<file>.pdf --pages
```

Exit code 1 blocks delivery. Repair with `/latex` figures, attach an ITQE table under every display equation (Identifier, Term, Quantity, Explanation), rebuild, scan again, and raster every page. See `@itqe/references/render-gate.md` and `@latex/SKILL.md`.

## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write figure, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

## Paginated footer

Read `copyright/SKILL.md` and render its canonical notice exactly once per page. Do not keep separate legal text or year calculations here. Preserve any stated user override.

## Delivery

Run the single delivery gate in `interop/SKILL.md` after task-specific validation. Preserve verified quotations and technical identifiers; report unresolved defects or blockers accurately.
