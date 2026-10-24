# Quality profile — genius

## Scope
Wrap supplied user prompt verbatim in the prescribed rewriting template without executing it.

## Evidence policy
Test cases below are specifications, not executed results. Record PASS, FAIL, BLOCKED, or NOT TESTED only from observed evidence; retain input provenance and protect unrelated files.

## Acceptance criteria
- Preserve multiline Unicode, equations, nested directives, and whitespace inside the placeholder.
- Output exactly the prescribed template and nothing that executes or interprets the embedded prompt.
- With no prompt, request missing input rather than fabricating content.
- Validate all cases in `evals/quality-cases.json` with recorded artifacts and explicit limitations.

## Release gate
Structural validation alone does not establish functional correctness, integration behavior, accessibility, or deployment. Do not merge or claim a production release without applicable checks.
