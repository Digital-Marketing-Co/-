# Quality profile — alias

## Scope
Register and resolve skill aliases with stable canonical targets, conflict prevention, and verified persistence.

## Acceptance criteria
- Require EXISTING_SKILL NEW_ALIAS ordering and an existing canonical target.
- Reject shadowing, cycles, reassignment without approval, and malformed names.
- Preserve unrelated registry entries and never claim runtime activation or cross-repository synchronization without proof.
- Validate representative, boundary, and integrity scenarios before approval.

## Evidence policy
Record only observed PASS, FAIL, BLOCKED, or NOT TESTED statuses. Structural validation does not establish integration correctness.
