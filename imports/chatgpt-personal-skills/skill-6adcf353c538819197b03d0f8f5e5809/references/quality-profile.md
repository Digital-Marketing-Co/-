# spec quality profile

Default medium: text. For inherit, use the target’s real output medium; a findings report is a separate artifact.

Trace each requirement to architecture, data/API/UI behavior, edge cases and measurable acceptance tests. Check conflicting versions, unavailable dependencies and cost constraints. Read the final text for ambiguity and inspect any rendered PDF/HTML. Plain-text prompts need structure/readability review, not invented screenshots or a claim that the proposed app was tested.

Acceptance evidence must identify final artifact/version, check ID, required status, method, actual result and supporting evidence. Enumerate all visual units and mark each inspected. Unavailable visual tools produce BLOCKED/NOT TESTED, not PASS. Reject a finished release with unresolved defects or stale evidence.

Forward checks:
- Bare /spec: ask for missing target/subject; do not invent content.
- /spec no followed by a complete brief: honor explicit bypass, retain requirements and apply applicable QA.
- Repeated handoff: reuse answers, design and completed matching operations.
- Missing renderer/browser: preserve useful work and label unverified output honestly.
- Edited final artifact: invalidate old QA and inspect the new version.
