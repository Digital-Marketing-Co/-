# Production Engineering quality profile

## Contract
Respect the explicitly requested deliverable: image, code, specification, deployment, or document. Prefer existing repository patterns, accessible design, secure defaults, and zero paid inference where required. Never substitute a static illustration for working software or claim deployment without verification.

## Acceptance
- Requirements and output medium match the user's request and authorized actions.
- Source edits preserve originals unless regeneration is requested; image crops, depth, lighting, alt text, and non-duplication are verified where applicable.
- Web work uses an appropriate production architecture, strict typing, responsive semantics, keyboard support, contrast, focus states, reduced motion, authorization checks, and safe secrets handling.
- SEO and auditor claims distinguish measured passes, failures, inapplicable checks, and untested checks.
- Equations use valid rendering when tested; missing ITQE/LaTeX integration is reported as a blocker rather than silently simulated.
- Builds, tests, PRs, deployment URLs, and runtime costs are reported only with actual evidence.

## QA protocol
Use representative, boundary, and presentation cases in `evals/quality-cases.json`. Run technical, security, accessibility, visual, and viewport QA as available; iterate until two complete passes find no material improvements or a genuine blocker. Report PASS, FAIL, BLOCKED, or NOT TESTED with links or artifacts. A structural skill check does not certify deployed software or visual quality.
