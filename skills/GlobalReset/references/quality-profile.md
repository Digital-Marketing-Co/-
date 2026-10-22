# Quality profile — GlobalReset

## Purpose and scope
Review every canonical skill for consistency, quality, idempotence, and justified version changes without altering unrelated behavior.

## Evidence and execution
Preserve canonical inputs and existing behavior. Record each check as PASS, FAIL, BLOCKED, or NOT TESTED based on observed evidence. Read the skill definition and linked interoperability contracts before executing changes. Never treat a proposed check as executed.

## Acceptance criteria
- Enumerate the entire canonical skill inventory and record coverage without claiming a partial pass is complete.
- Increment a skill version only when an actual non-version change is made and record provenance in its changelog and ledger.
- Run the workflow twice against unchanged inputs; the second run must produce no changes.
- Preserve host-bundled skills, protected negative rules, and existing user modifications.
- Evaluate representative, boundary, and integrity scenarios documented in `evals/quality-cases.json` when available; retain evidence and unresolved gaps.

## Release gate
Structural validation alone does not prove functional behavior, publication quality, external access, or deployment. Require independent evidence before merging or claiming completion.
