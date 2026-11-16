# Complete (/C) quality profile

## Purpose
A fail-closed terminal completion verifier. Never emit the exact success token unless all applicable criteria have evidence.

## Acceptance
- Enumerate acceptance criteria, final artifacts, tests and provenance.
- Confirm final /itqe then /latex after the last export for mathematical outputs, with symbol coverage and rendered-page checks.
- Require two complete clean QA and visual QA passes where applicable.
- Mark unavailable evidence BLOCKED or NOT TESTED, not PASS.
- For math-free artifacts, document an inspected no-math inventory and mark mathematical checks NOT APPLICABLE.
- Output exactly Complete only after verified closure; otherwise report blockers.

## Validation
Run evals/quality-cases.json; structural metadata checks do not prove runtime behavior.
