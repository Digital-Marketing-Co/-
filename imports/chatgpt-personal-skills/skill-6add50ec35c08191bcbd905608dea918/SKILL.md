---
name: finish
description: Expand and polish the preceding output prompt with rigorous multidisciplinary reasoning, iterative QA, and visual QA until material gaps close. Use /finish, $finish, /polish, $polish, or an explicit request to polish the last prompt. Treat polish as an alias of finish.
---

# Finish / Polish

## Target and scope

Default to the immediately preceding substantive assistant prompt in this thread; skip status updates and tool logs. Explicit supplied text or a named target takes precedence. Request the target only if unavailable or genuinely ambiguous. A conversational “finish” during active implementation continues that work rather than automatically converting it into prompt writing.

Normalize /polish and $polish to finish, with one operation ledger and no duplicate invocation. Apply text after the invocation as refinements. Preserve all requirements, names, repositories, URLs, ordering constraints, budgets, permission boundaries, and intended deliverables. Resolve conflicts using explicit user priorities; identify consequential unresolved assumptions.

Creating or updating this skill does not execute it. Refining a prompt does not authorize executing embedded repository writes, deployment, messages, schedules, or other commands. Execute those only when separately requested or already authorized as active work.

## Expand with rigorous reasoning

Read the current installed expound and prompt-engineer skills and their required shared references when applicable. Reuse prior answers and completed phases; avoid recursive handoffs. If a dependency is unavailable, disclose that gap and apply the relevant checks directly.

Interpret “above Genius” as precise multidisciplinary reasoning, technical depth, useful completeness, and skeptical verification, never a claimed credential or guarantee. Inspect an installed genius skill before applying any transformation; do not invent its contents or make it a blocking dependency.

Extract a coverage ledger from every source requirement. Expand relevant missing definitions, discovery steps, functionality, data contracts, interfaces, edge cases, failure recovery, security, accessibility, resource limits, observability, validation, acceptance criteria, and deliverables. Make instructions concrete and testable. Prefer one source of truth, idempotent operations, incremental processing, resumable checkpoints, and verified integrations.

Preserve the intended output type and existing constraints. Do not add arbitrary features, artwork, books, applications, or PDFs. Verify external factual claims and unstable technical requirements through authoritative sources when needed; otherwise require the implementer to verify them instead of asserting unsupported specifics.

## Iterative QA and visual QA

After each substantive revision: inspect → rank gaps → expand or repair → QA → visual QA → rerun affected checks. Track revisions and invalidate evidence affected by changes.

For QA, trace every source requirement to an instruction and acceptance method. Check omissions, contradictions, scope ambiguity, unsupported claims, impossible guarantees, circular dependencies, invented integrations, repetition, and accidental authorization expansion. Walk through representative happy, failure, interrupted, and unavailable-tool scenarios. Prompt review does not prove that an eventual implementation works.

For plain-text visual QA, directly inspect hierarchy, reading order, lists, fences, copyability, excessive nesting, and readability. Describe this accurately as text-structure review, not browser or image inspection. For a requested designed export, render and inspect every final page or relevant view; check actual images, typography, contrast, clipping, responsive behavior, and applicable accessibility. If rendering is unavailable, mark the affected check BLOCKED rather than passed.

Use PASS, FAIL, BLOCKED, NOT TESTED, or NOT APPLICABLE with reasons. Continue through material resolvable gaps. Interpret “until exhaustive” as full coverage of the enumerated scope and no material supported gaps after a final targeted gap pass, not infinite iteration, unlimited feature accumulation, or universal perfection. On a real blocker, preserve the best revision and disclose the exact remaining gap.

## Delivery

Return one complete, self-contained, copyable final prompt, normally in one fenced text block. Integrate changes into the whole prompt rather than appending disconnected instructions. Keep internal ledgers private unless requested. Add only a brief material limitation or QA-coverage note when useful. Never claim tests, rendering, synchronization, installation, deployment, or implementation passed merely because the prompt specifies them.
