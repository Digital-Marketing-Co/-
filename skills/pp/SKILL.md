---
name: pp
description: Alias for /p. Automatically proceed with the user's current multi-step task as far as authorized tools and access permit.
aliases:
  - pp
  - /pp
canonical_skill: /p
version: 1.0.0
---

# pp — automatic proceed alias

When the user writes `pp` or `/pp` as a standalone command, interpret it identically to `/p`. Do not create a separate execution policy or diverging implementation. Forward the active task and all existing constraints to the canonical `/p` workflow.

## Execution
1. Resume the latest actionable task and its outstanding steps using conversation context.
2. Proceed automatically through available, authorized actions; minimize repetitive questions and manual steps.
3. Prefer safe, reversible changes and verify results. Do not claim builds, tests, merges, uploads, or deployments succeeded without evidence.
4. Request clarification or user authorization only where indispensable, and honor security, tool, and platform constraints.
5. Report concise completed actions, verifiable references, and any remaining blockers.
6. Do not promise background or continuous work unless an actual scheduled automation was created.

## Equivalence
`pp` = `/pp` = `/p`. The canonical `/p` skill remains authoritative if its instructions are available. If `/p` is unavailable, apply the execution behavior above without inventing additional capabilities.
