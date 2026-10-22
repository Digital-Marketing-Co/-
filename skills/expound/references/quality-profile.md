# Quality profile — expound

## Purpose and scope
Iteratively close material evidence gaps with bounded convergence and citation renumbering.

## Evidence and execution
Preserve source inputs and existing behavior. Use observed PASS, FAIL, BLOCKED, or NOT TESTED statuses; never represent a proposed test as executed. Review canonical `SKILL.md` and shared interoperability contracts before applying changes.

## Acceptance criteria
- After each change, audit first-citation order, bibliography completeness, and equation coverage.
- Stop on no measurable progress or unavailable evidence; report unresolved gaps.
- Preserve hypotheses as hypotheses; do not manufacture support or assert unrun /latex or ITQE audits.
- Verify exact output and side effects against the three scenarios in `evals/quality-cases.json`; record evidence and remaining gaps.

## Release gate
A structural validator pass alone does not establish functional correctness, accessibility, deployed runtime behavior, or external integration success. Keep unverified work blocked.
