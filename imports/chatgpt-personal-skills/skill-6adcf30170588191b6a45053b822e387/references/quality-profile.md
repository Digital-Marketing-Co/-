# data quality profile

Default medium: dataset. For inherit, use the target’s real output medium; a findings report is a separate artifact.

Verify source provenance, schema/types, units, nulls, row/unique counts, deduplication, ranking ties, formulas and round-trip exports. Check human-readable tables/charts for label collisions, number/date formats, legends, contrast and narrow-screen readability. Pure machine-readable data may mark visual QA not applicable with a concrete reason; any preview or workbook still needs inspection.

Acceptance evidence must identify final artifact/version, check ID, required status, method, actual result and supporting evidence. Enumerate all visual units and mark each inspected. Unavailable visual tools produce BLOCKED/NOT TESTED, not PASS. Reject a finished release with unresolved defects or stale evidence.

Forward checks:
- Bare /data: ask for missing target/subject; do not invent content.
- /data no followed by a complete brief: honor explicit bypass, retain requirements and apply applicable QA.
- Repeated handoff: reuse answers, design and completed matching operations.
- Missing renderer/browser: preserve useful work and label unverified output honestly.
- Edited final artifact: invalidate old QA and inspect the new version.
