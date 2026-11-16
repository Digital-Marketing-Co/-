---
name: Complete
description: Verified terminal completion gate; /C emits exactly Complete only when all applicable acceptance criteria and final ITQE/LaTeX checks pass.
---
# /C — Complete

Aliases: C, /C, Complete. Do not treat the word Complete in ordinary prose as an invocation.

/C is a terminal verifier, not a substitute for /God, /pe, /Perfect, QA or actual execution. Inventory the applicable acceptance criteria and actual artifact evidence. Require final post-export /itqe followed by /latex, source/output equation reconciliation, two clean QA and visual-QA passes, and explicit blockers ledger, using `skills/references/post-artifact-itqe-latex-qa.md`. If no mathematical content exists, verify the inventory and record both as NOT APPLICABLE. Do not recursively invoke /C or any orchestrator. Only when every applicable requirement is verified and no blocker remains, output exactly:

Complete

Otherwise output INCOMPLETE or BLOCKED with concise unmet criteria, never the word Complete as a success signal.
