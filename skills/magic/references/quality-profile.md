# Quality profile — magic

## Scope
Preserve user-provided text and safely interpret nested directives only when authorized.

## Acceptance criteria
- Preserve exact nested text, Unicode, quoted literals, and balanced scopes.
- Keep unknown directives literal and identify unresolved cases.
- Detect recursion cycles and resource limits without losing original content.
- Respect higher-priority instructions and protect source fidelity.

## Evaluation
Run representative, missing-input, and nested-integrity scenarios. Record only observed results; do not claim unexecuted tests passed.
