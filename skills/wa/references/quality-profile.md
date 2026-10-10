# Application behavior

## Execution and evidence

Read the task-specific additions below before planning changes. Preserve the original skill purpose and explicit user constraints. Treat these additions as refinements; user instructions and platform rules take precedence. Resolve `<name>/...`, `@name/...`, and legacy host paths by canonical frontmatter name with `interop/scripts/resolve_root.py`; use resources from the same reviewed revision.

Keep input provenance, environment prerequisites, output contracts, and observed validation separate. Use `PASS`, `FAIL`, `BLOCKED`, and `NOT TESTED` with evidence. Never turn an unavailable tool, missing dependency, planned test, or schema presence into a claimed execution success. Bound retries and expensive work; checkpoint long runs and report open scope. Preserve originals and use atomic replacement after validation. Do not invoke paid inference just to test a skill.

Apply design only to suitable visual outputs. Preserve archival fidelity, raw transcripts, executable syntax, exact notation, transparency, and user-requested no-shadow treatments. For visual artifacts read `visual-system/references/quality-design.md`. For research use `interop/references/evidence-method.md`; for composition read `interop/SKILL.md`. These are shared contracts rather than duplicated legal text or repeated gates.

## Capability additions

Build a feature-to-test matrix with isolated fixtures, role ownership checks, failure recovery, and observable deployment evidence.

## Acceptance checks

Exercise authorization denial, idempotency, queues, uploads, UI states, accessibility, and provider-disabled mode.

## Visual treatment

Improve contextual banners and spatial UI with mobile, keyboard, contrast, and performance checks.

## Validation protocol

Run the bundled representative scenarios in `evals/quality-cases.json` against actual artifacts. Record prompt, input hashes, tool and dependency versions, observations, and failed assertions. Retest changed behavior and relevant neighboring flows. Separate structural checks from rendered output inspection and live integration checks.
