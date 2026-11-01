---
name: check
description: "Audit and repair existing outputs with interactive target selection, reproducible defects and independent functional/visual acceptance evidence. Use /check for documents, data or apps."
---

# Check

Resolve the installed personal skill named `doc` and read its `references/output-contract.md` once per run. Read it as a reference; do not invoke doc or restart its intake.

## Interactive start

Show the proposed output plan and reuse prior choices. Ask at most two useful questions only for missing material context: Exact target/current version and audit-only versus repair when not implied. Honor explicit no-questions/bypass settings. Use the shared 4629 style phase for a new designed output, once across handoffs.

## Execution

Audit the identified existing artifact or implementation against its requirements. Inspect real files or behavior, reproduce defects, and separate failed, blocked, not applicable and not tested results. Check content/evidence, functional behavior, layout, accessibility, security, performance and deployment only where relevant. Repair root causes without unrelated rewrites. Revalidate changed and dependent behavior, inspect the final output, and deliver findings with evidence, repairs and unresolved issues. Do not describe a compiler pass, archive-integrity check or attractive preview as production acceptance.

## Specialist routing

Use wa for app audits; applicable PDF/documents/spreadsheet specialists for artifacts. Preserve originals and working behavior. An explicitly read-only audit must not mutate the target.

## Required QA and visual QA

Reproduce and prioritize defects; separate actual evidence from unavailable tests. Repair causes when authorized and rerun affected checks plus relevant regression flows. Inspect actual final pages or route/state/viewports; inherit the target’s profile rather than treating the findings report as proof the target passed. Disclose uninspected coverage. Follow the shared repair and release gates. Never mark unexecuted checks passed.

Read [the endpoint quality profile](references/quality-profile.md) for requirements and tests.
