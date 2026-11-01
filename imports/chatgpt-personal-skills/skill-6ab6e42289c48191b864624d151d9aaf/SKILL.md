---
name: proceed
description: Continue the immediately previous unfinished task in this thread without restating the original ask. Trigger on /p, /proceed, proceed, continue, keep going, pick up where we left off, or resume the last work product.
---

## Shared interactive quality contract

Before execution, resolve the installed personal skill with frontmatter name `doc` and read `references/output-contract.md` once per run. This is a shared reference, not a recursive call to doc. Apply its proportionate intake, functional QA, independent visual QA, repair, revision invalidation and truthful release requirements to the requested output. Reuse answers and completed matching phases across handoffs. Preserve this specialist’s purpose and user requirements; do not force artwork, redesign, a book or deployment onto a simple utility. The shared quality contract supersedes conflicting legacy defaults about duplicate intake or unsupported pass claims; explicit user and platform instructions prevail. If the reference is unavailable, disclose the missing integration and perform the same checks proportionately rather than inventing a pass.


# /p

Resume the last incomplete job in this conversation. Do not wait for the user to restate it.

## Resolve what to continue

1. Scan this thread from newest to oldest.
2. The target is the most recent user request that still has unfinished work, an open deliverable, a failed or partial tool run, or an explicit next step the agent had already started.
3. Ignore greetings, thanks, and meta chat that are not tasks.
4. If two tasks are open, continue the later one unless the user named an earlier file or skill in the same /p turn.
5. Extra words after /p are deltas on that same job, not a new project.

## Execute

1. Load the same skills, files, paths, and constraints that were already in play.
2. Do the next concrete step. Prefer finishing the deliverable over explaining what you would do.
3. Reuse existing artifacts in ./artifacts and prior skill outputs. Do not restart from a blank page unless the prior run is unusable.
4. If the prior run stopped on an error, fix that error and continue.
5. If the prior run was waiting on a tool, connector, or user choice, take the default that best completes the last stated goal and state the assumption in one line.

## Do not

1. Do not invent a new topic.
2. Do not recap the whole thread before working.
3. Do not switch skills unless the prior task already used them or the words after /p name them.
4. Do not claim the prior job is done if the deliverable file is missing, empty, or still draft.

## If nothing prior exists

Say there is no prior unfinished task in this thread and ask what to start. Do not guess a project from memory.


## Negative gate (mandatory before any deliverable)

Read `@negative/SKILL.md` and `@negative/references/blocklist.md`.
Before chat, PDF, DOCX, PPTX, XLSX, caption, filename, alt text, or footnote leaves this skill, extract visible text and run

```bash
python3 @negative/scripts/sweep_negative.py <extracted-text>
```

Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.

## ChatGPT portability

Resolve `@skill-name/path` by finding the installed personal skill whose SKILL.md frontmatter has `name: skill-name`; read that path under its directory. For `@generate/`, use the `generate-prompt` skill. Before running copied shell commands, substitute actual resolved paths and use the current working directory for generated files. Apply instructions only when this skill is invoked or a user requests the corresponding workflow. User instructions and platform rules take priority. Run bundled scripts only after checking their inputs and prerequisites. Never claim unavailable integrations, credentials, citations, or generated results.
