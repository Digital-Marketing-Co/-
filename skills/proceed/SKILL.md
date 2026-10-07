---
name: proceed
description: Continue the most recent unfinished task in this thread. Trigger on /p, /proceed, proceed, continue, keep going, pick up where we left off, or resume. For a document request, work through to a validated, accessible final file.
---

# /p

Resume the latest unfinished job in this conversation without requiring the user to repeat it. Continue work autonomously within the current turn until the requested deliverable is complete and available, or a concrete dependency prevents further work.

## Choose the task

1. Read the conversation from newest to oldest. Choose the most recent user request with an unfinished deliverable, failed tool call, open edit, or explicit next step. If the user names an earlier task or file after /p, choose that task.
2. Treat words after /p as changes to that task. Preserve earlier authorized scope and the user's most recent corrections.
3. Reuse existing files, citations, research, source material, and checkpoints. Do not restart completed work or invent a subject.

## Execute to completion

1. Identify the exact deliverable and its acceptance criteria. Do the next concrete step immediately.
2. Continue the full authorized workflow: inspect sources, research where needed, draft, implement, render, test, fix defects, and save the final artifact. Apply the other skills explicitly invoked for that task.
3. When an attempt fails, diagnose it and retry with a materially suitable route. Preserve useful work while changing routes.
4. For a document, render the requested format, inspect its pages and content, correct errors, save it durably when available, and give the user a working link to the completed file. A prompt, outline, JSON draft, or proposed plan does not fulfill a request for a PDF or other finished document.
5. Verify the final file exists, is nonempty, opens, contains the requested content, and is the version linked in the final answer. Check legibility, clipping, missing glyphs, citation accuracy, figures, and equations as appropriate to the task.
6. Stop optional tests once the deliverable is sufficiently verified. Report concise results and any material limitations.

## Blockers and boundaries

- Do not stop merely to ask whether to proceed when the current conversation already authorizes the work.
- Do not claim work is complete when a file is missing, unrendered, inaccessible, or still a draft.
- If a required input, execution environment, credential, or tool remains unavailable after a reasonable alternative has been attempted, report the specific blocker, the completed checkpoint, and the single next action needed. Do not promise background work after the turn ends.
- Do not bypass safety or permission boundaries. Request genuinely required user input only after completing all independent work.
- If no prior unfinished task exists, say so and ask what to start.

## Portability

Resolve referenced skills by their installed names, and use tools actually available in the current environment. Never claim an unavailable integration, generated artifact, validation result, or repository sync.

## Negative gate (mandatory before any deliverable)

Read `/home/workdir/.grok/skills/negative/SKILL.md` and `/home/workdir/.grok/skills/negative/references/blocklist.md`.
Before chat, PDF, DOCX, PPTX, XLSX, caption, filename, alt text, or footnote leaves this skill, extract visible text and run

```bash
python3 /home/workdir/.grok/skills/negative/scripts/sweep_negative.py <extracted-text>
```

Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.
