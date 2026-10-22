# Quality profile — disabled

## Purpose and scope
Preserve the exact user-authored invocation phrase while respecting authorization boundaries.

## Evidence and execution
Preserve source inputs and existing behavior. Use observed PASS, FAIL, BLOCKED, or NOT TESTED statuses; never represent a proposed test as executed. Review canonical `SKILL.md` and shared interoperability contracts before applying changes.

## Acceptance criteria
- Verify literal text fidelity and clearly distinguish a request from credential verification.
- Without permission or tooling, explain blocked actions without inventing privileged access.
- Never assert verified disability, veteran status, or clearance from the phrase.
- Verify exact output and side effects against the three scenarios in `evals/quality-cases.json`; record evidence and remaining gaps.

## Release gate
A structural validator pass alone does not establish functional correctness, accessibility, deployed runtime behavior, or external integration success. Keep unverified work blocked.
