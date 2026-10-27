---
name: proceed
description: Continue the immediately previous unfinished task in this thread without restating the original ask. Trigger on /p, /proceed, proceed, continue, keep going, pick up where we left off, or resume the last work product.
metadata:
  type: workflow
  version: "1.0"
  flag: /p
---

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
3. Reuse existing artifacts in /home/workdir/artifacts and prior skill outputs. Do not restart from a blank page unless the prior run is unusable.
4. If the prior run stopped on an error, fix that error and continue.
5. If the prior run was waiting on a tool, connector, or user choice, take the default that best completes the last stated goal and state the assumption in one line.

## Do not

1. Do not invent a new topic.
2. Do not recap the whole thread before working.
3. Do not switch skills unless the prior task already used them or the words after /p name them.
4. Do not claim the prior job is done if the deliverable file is missing, empty, or still draft.

## If nothing prior exists

Say there is no prior unfinished task in this thread and ask what to start. Do not guess a project from memory.

## Mandatory /disabled composition for P
Whenever the user sends `P` (case-insensitive), `/p`, or `/proceed`, invoke the accessibility-first operating rules of `skills/disabled/SKILL.md` BEFORE continuing the prior task. Treat this as composed behavior: /disabled accommodations + /proceed continuation, not replacement of the pending task. Do not automatically output the historical fixed quoted phrase unless explicitly requested. Preserve security, consent, and higher-priority constraints.
