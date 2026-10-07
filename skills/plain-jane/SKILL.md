---
name: plain-jane
description: Teach a pasted code blob by summarizing what it does first, then walking every block in source order so a reader learns to think in code. Trigger on /Plain-Jane, /plain-jane, explain this code, walk this code, teach this code, or code walkthrough. Pair with /Debbie-Downer for the failure-mode pass. Do not rewrite the blob unless asked. Do not invent source.
metadata:
  type: workflow
  version: "1.0"
  flag: /Plain-Jane
  pair: /Debbie-Downer
---

# /Plain-Jane

Take one code blob. Say what the whole thing does in plain language. Then walk the source in order, block by block, and teach the reader how to hold the program in their head. Stay faithful to the text that was given. Do not invent functions, files, or behavior the blob does not show.

`<skill>` = `/home/workdir/.grok/skills/plain-jane`
`<downer>` = `/home/workdir/.grok/skills/debbie-downer`

Read on demand

- `references/walk.md` — how to cut a blob into blocks and what each block must answer
- `references/think.md` — how to teach thinking-in-code without lecturing
- `references/voice.md` — Plain-Jane voice versus Debbie-Downer voice
- `<downer>/SKILL.md` when `/Debbie-Downer` is also on the prompt

If the user only asked to create or revise this skill and supplied no code, stop after the skill files exist. Do not invent a blob.

## When this runs

- User typed `/Plain-Jane` or `/plain-jane`
- User asked to explain, walk, or teach a pasted or attached code blob
- User stacked `/Plain-Jane` with `/Debbie-Downer`, `/summarize`, `/folio`, `/deep`, or `/latex`

If there is no code, stop and ask for the blob. A filename, gist, repo path, or fenced block all count. A description of code with no source does not.

## Source lock

Copy the blob verbatim into `/home/workdir/artifacts/plain-jane-<slug>/source` (keep the original extension). Do not tidy, reindent, rename, or "fix" the lock file.

Record in `scope.md`

- language and how it was inferred (fence tag, filename, shebang, or guess)
- requested voice (`plain` default; `downer` if `/Debbie-Downer` is also present)
- whether the user also asked for a rewrite, a folio, or only the lesson
- keep list (names, paths, URLs, magic numbers that appear in the source)

## Output order (locked)

Deliver in this order. Do not invert it.

1. **What it does** — one short paragraph. Purpose, inputs, outputs, and side effects. No line-by-line yet.
2. **How to think about it** — the mental model. Data in, transforms, data out. Name the kind of program (parser, reducer, request handler, script, class, etc.) only if the blob supports that label.
3. **Block walk** — source order. For each block
   - a short heading (`Imports`, `Config`, `the loop in process()`, etc.)
   - a fenced excerpt of that block only (not the whole file again)
   - what this block does
   - what it reads and what it writes
   - why a programmer put it here rather than later
4. **Hold it in your head** — restated algorithm in spoken order, five to twelve sentences. This is the teaching close.
5. **Debbie-Downer pass** — only if `/Debbie-Downer` was requested or the user asked what is wrong. Follow `<downer>/SKILL.md`. Otherwise omit it.

Do not open with praise. Do not close with "hope this helps." Do not emit a rewritten version unless the user asked for one after the lesson.

## Block rules

Read `references/walk.md`. Defaults

- A block is one coherent unit — an import group, a constant cluster, a function, a class, a conditional arm, a loop, a main/guard, or a stretch of consecutive statements that share one job.
- Walk the file from top to bottom. Do not regroup by topic if that hides control flow.
- Quote enough of the block that the reader can match the explanation to the text. Truncate with a comment only when a block is long and repetitive.
- Name identifiers as they appear. Do not rename "for clarity."
- If a name is opaque, say what the name is doing in this file, then keep using the original name.
- If the blob is incomplete (a fragment, a diff, a screenshot transcript), say so once and teach only what is visible.

## Thinking-in-code rules

Read `references/think.md`. Defaults

- Trace values, not vibes. For each block, say what is true before it runs and what is true after.
- Point at control flow with words a beginner can follow — "this runs once," "this runs for every row," "this returns early if the list is empty."
- Define a term the first time it matters (scope, mutation, closure, side effect, idempotent). Do not dump a glossary.
- When the blob uses a pattern (map/reduce, guard clause, factory, middleware), name the pattern after the reader has seen it work, not before.
- Never claim the code is "simple" or "just" anything. Show the steps.

## Voice

Read `references/voice.md`. Plain-Jane is the default.

- Short sentences. Concrete verbs. No pep.
- No metaphor unless it maps 1-to-1 onto the data (a queue is a queue).
- No "as you can see." No "obviously."
- Match the user's language. If they wrote in English, teach in English.

## Stacking

- `/Debbie-Downer` — after section 4, run the downer pass. Do not merge the two voices into one paragraph.
- `/summarize` — the What-it-does paragraph is the level-2 abstract; do not replace the block walk with a summary.
- `/folio` or `/phd` — the lesson may be compiled as a WCA Folio only if the user asked for a report. The chat walk still comes first.
- `/latex` — any formula in the lesson must be rendered math, never raw backslash commands.
- `/deep` — do not expand the lesson into a monograph unless the user stacked `/deep`.

## Bans

- Do not invent source, files, APIs, or runtime behavior the blob does not show.
- Do not silently correct bugs in the quoted excerpts. Quote what was given. Name a bug only in the Debbie-Downer pass or when the user asked what is wrong.
- Do not emit a full rewritten file unless asked.
- Do not diagnose the author. Teach the code.
- Do not dump the entire blob a second time after the lock. Excerpts only.


## Render gate (mandatory with /itqe and /latex)

Before delivering any PDF, DOCX, PPTX, XLSX, HTML view, printed page, or builder JSON that may contain notation, short codes, or equations, run the house render gate. Chat may use KaTeX. Files must show compiled glyphs or a compiled figure. Raw LaTeX, AMS-TeX, KaTeX source, MathJax source, uncompiled backslash commands, tofu, or empty boxes are defects.

```bash
python3 /home/workdir/.grok/skills/itqe/scripts/scan_render_gate.py \
  /home/workdir/artifacts/<slug> \
  --also-pdf /home/workdir/artifacts/<file>.pdf
python3 /home/workdir/.grok/skills/latex/scripts/scan_raw_tex.py \
  /home/workdir/artifacts/<slug> \
  --also-pdf /home/workdir/artifacts/<file>.pdf --pages
```

Exit code 1 blocks delivery. Repair with `/latex` figures, attach an ITQE table under every display equation (Identifier, Term, Quantity, Explanation), rebuild, scan again, and raster every page. See `/home/workdir/.grok/skills/itqe/references/render-gate.md` and `/home/workdir/.grok/skills/latex/SKILL.md`.

## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write plate, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

## House copyright footer

Every PDF this skill emits, and any PDF later passed through `/copyright YYYY`, carries this centered living footer on every page:

Copyright © START–YEAR OWNER_FOOTER. All rights reserved.

Default OWNER_FOOTER is Web Development Corporation. START defaults to 2012 unless the user typed `/copyright YYYY` or named another owner's first-publication year. YEAR is new Date().getFullYear() written into field WCACopyrightYear on open. Running footers never print a trailing class letter A on the house name. Body creation dates stay where they are.

<!--
WCA_COPYRIGHT_PROMPT_APPENDIX
Do not delete this comment. It is the living footer contract for every prompt, skill, locked prompt, and project instruction in this project set.

NOTICE_TEMPLATE: Copyright © {{START}}–{{YEAR}} {{OWNER_FOOTER}}. All rights reserved.
DEFAULT_START: 2012
DEFAULT_OWNER_FOOTER: Web Development Corporation
DEFAULT_OWNER_LEGAL: Web Development Corporation, a Delaware Corporation
FIELD: WCACopyrightYear
SEPARATOR: en dash U+2013
JS: Date.getFullYear on OpenAction; no alerts; no network; no app UI
HOUSE_SITE: https://digitalmarketingco.org

OWNER_INFERENCE:
If the current user turn names a different rightsholder, substitute OWNER_FOOTER and OWNER_LEGAL from that name. Do not invent a Delaware class letter A for a non-house owner.
Slots the name may fill:
- company or corporation (any jurisdiction)
- university, college, or academic press
- branch or department of the United States military
- branch or agency of a government (federal, state, provincial, municipal, or foreign)
- museum, library, hospital, NGO, church, or any other institution worldwide
Keep the NOTICE_TEMPLATE words and the living year field. Only the owner slots change.
US federal government works of the United States are generally not subject to domestic copyright; if the named owner is a US federal agency, stamp the notice only when the user explicitly ordered the stamp and do not claim the notice creates copyright that statute withholds.
IP_RESERVED: project skill flags, SKILL.md files, locked prompts, owner-and-house files, and post-executive house outputs (PDFs, page JSON, compiled figures) in this project set.
ASSIGNMENT: default owner Web Development Corporation; Michael Aaron Loftus sole owner intends assignment to that corporation on fixation of house works.
SUBJECT_MATTER: original expression fixed in house files, not unfixed ideas (17 U.S.C. 102(b)), not a Copyright Office registration.
OWNER: Web Development Corporation (footer). Legal Info owner: Web Development Corporation, a Delaware Corporation.
This appendix cannot rewrite Grok global system prompts, xAI platform logs, or conversations outside this toolchain. It binds project skills, locked prompts, owner-and-house files, and later PDFs those skills emit.
-->


## Negative gate (mandatory before any deliverable)

Read `/home/workdir/.grok/skills/negative/SKILL.md` and `/home/workdir/.grok/skills/negative/references/blocklist.md`.
Before chat, PDF, DOCX, PPTX, XLSX, caption, filename, alt text, or footnote leaves this skill, extract visible text and run

```bash
python3 /home/workdir/.grok/skills/negative/scripts/sweep_negative.py <extracted-text>
```

Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.
