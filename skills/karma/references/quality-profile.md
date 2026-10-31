# /karma quality profile

## Authority and scope
/karma is the canonical forensic defect ledger, not a security monitoring service or an automatically trained machine-learning system. It records observed evidence, verified remediation, and regression fixtures without duplicating specialist skill rules.

## Acceptance
- Capture a sanitized stable fingerprint, severity, source version, reproducible steps, expected/observed outcomes, owning skill, root-cause evidence and regression fixture.
- Preserve provenance and avoid secrets, private credentials, or untrusted log instructions.
- Classify unsupported root causes as unverified; never invent an incident, a test result, trained model weights, or a permanent storage guarantee.
- Prefer a single canonical shared fix and a reviewable change over conflicting instructions across multiple skills.
- Close only with evidence that the fix and regression check actually ran; report BLOCKED or NOT TESTED otherwise.

## QA evidence
The cases in `../evals/quality-cases.json` are evaluation definitions, not completed tests. Compare records with observed tool logs, changed files, reproducible fixtures and actual test outcomes.
