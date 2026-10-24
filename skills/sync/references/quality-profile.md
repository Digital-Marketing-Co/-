# Quality profile — sync

## Scope
Bidirectionally reconcile canonical and website skills only when repository state, file hashes, and safe merge history are verified.

## Acceptance criteria
- Fetch fresh branch heads and complete recursive Git trees.
- Compare path, blob type, and content hash in both directions.
- Preserve conflicting shared paths and all unrelated files; no force push or silent deletion.
- Verify remote heads and in-scope tree parity after each write.
- In status or dry-run mode, make no writes.

## Evidence policy
Record observed PASS, FAIL, BLOCKED, or NOT TESTED; distinguish structural parity from runtime QA. Do not claim complete synchronization with unresolved differences.
