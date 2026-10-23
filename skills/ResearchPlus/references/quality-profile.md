# Quality profile — ResearchPlus

## Purpose and scope
Resolve /ResearchPlus to the canonical research-unbounded standard without weakening requirements.

## Evidence and execution
Preserve source inputs and existing behavior. Use observed PASS, FAIL, BLOCKED, or NOT TESTED statuses; never represent a proposed test as executed. Review canonical `SKILL.md` and shared interoperability contracts before applying changes.

## Acceptance criteria
- Preserve source verification, citation traceability, and checkpointed multi-volume handling.
- An unavailable canonical target is reported as blocked rather than silently replaced.
- Do not claim unlimited physical compute or fabricate sources.
- Verify exact output and side effects against the three scenarios in `evals/quality-cases.json`; record evidence and remaining gaps.

## Release gate
A structural validator pass alone does not establish functional correctness, accessibility, deployed runtime behavior, or external integration success. Keep unverified work blocked.
