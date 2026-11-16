---
name: sync
description: Safely pull, reconcile, and push skills bidirectionally between Digital-Marketing-Co/- and Digital-Marketing-Co/Digital-Marketing-Co, verifying both remote heads.
metadata:
  type: workflow
  version: "2.0.0"
  flag: /sync
---
# /sync — Bidirectional skills synchronization

## Repositories
- A: `Digital-Marketing-Co/-` (`main`)
- B: `Digital-Marketing-Co/Digital-Marketing-Co` (`main`)
- Scope: `skills/**` including text, scripts, references, assets and binary files. Do not touch unrelated paths.

## Pull → reconcile → push → verify
1. Fetch fresh branch heads and recursive Git trees from **both** repositories on each iteration; this is the pull/read stage. Never assume local state is current.
2. Compare path, Git object type and blob content hash in both directions. Skip identical entries; preserve unique files from either side.
3. For a path present only on one side, copy its exact bytes to the other side. For an identical path with different contents, inspect history and merge only when a common base and safe non-conflicting merge can be established. Otherwise mark a conflict and preserve both versions; never arbitrarily select a winner.
4. Build bounded batches of non-conflicting changes for each repository. Use binary-safe Git blob operations for binary assets. Create new trees/commits against fresh heads and update refs with expected-head concurrency checks; never force-push.
5. After each push, re-pull both remote heads and trees, re-diff, and verify changes landed. If heads moved, recalculate instead of overwriting concurrent work.
6. Repeat while safe differences remain and the execution budget allows. If no progress is possible, stop and report exact conflicting/unsupported paths. Never claim full parity when unresolved differences remain.
7. Independently verify remote tree parity for all in-scope paths; run applicable checks and distinguish tree parity from runtime QA.

## Safety
- No automatic deletion, force push, history rewrite, or destructive conflict resolution.
- Do not expose secrets or sync ignored/private credentials.
- Respect GitHub permissions, API limits and file-size limits.
- Keep exact records of pull heads, push commit SHAs, conflicts, and remaining differences.
- No autonomous background execution is implied by the loop.

## Invocation
- `/sync`: pull both, reconcile safe changes, push both as needed, verify.
- `/sync status`: pull/compare both, report only, do not write.
- `/sync dry-run`: preview proposed changes and conflicts without writing.

## Terminal mathematical integrity enforcement — 2026-11-16
For every applicable generated or modified artifact, invoke the canonical shared `skills/references/post-artifact-itqe-latex-qa.md` gate AFTER the last content edit and final export: inventory all math including figures/tables; run /itqe first (equation IDs, every symbol/operator/constant/index, units, assumptions, dimensional consistency, Unicode names and accessible glossary), then /latex (source parsing, rendering, superscripts/subscripts, font/glyph integrity, exported-page verification). If defects are repaired, re-export and repeat the terminal /itqe → /latex sequence on the new final output. Then require two independent complete evidence-backed QA and visual-QA passes; /karma records actual defects and prevention fixtures. A math-free artifact may mark both NOT APPLICABLE only after a verified inventory. Never treat missing tools, incomplete inspection, commits, or self-reported status as PASS. Use bounded, nonrecursive orchestration; /C can output exactly Complete only after all applicable acceptance criteria are verified. This addition preserves all prior skill-specific responsibilities and safety constraints.
