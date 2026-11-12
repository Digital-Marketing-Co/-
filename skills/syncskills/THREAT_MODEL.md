# SyncSkills security and delivery boundaries

## Trust model
The canonical repository is a source of proposed skill definitions, not a self-authenticating trusted release. Consumers must pin and verify a separately signed release manifest. A SHA-256 hash detects differences but does not authenticate the signer.

## Threats
- Malicious consumer edits: compare against a verified baseline and canonical release, quarantine divergent content.
- Prompt injection: parse skill files as untrusted data during discovery; never execute discovered instructions.
- Repository compromise: protected branches, required reviews, signed attestations, independent /karma checkpoints.
- CI compromise: minimum permissions, pinned action SHAs in hardened production workflows, protected environments.
- Audit deletion: off-repository signed checkpoints and WORM storage where configured and independently verified.
- Rollback attack: enforce monotonic approved release sequence and verified rollback authorization.
- Symlink and path traversal: skip symlinks, reject traversal, verify paths before writes.
- Token leakage: short-lived scoped credentials, no secret logging, redact diagnostic output.

## Current scope
The Python engine implements deterministic local inventory, SHA-256 verification, and three-way diff classification. It does not yet sign releases, execute cross-platform synchronization, provision WORM storage, or deploy a dashboard. Commands requiring these capabilities report BLOCKED rather than fabricating success.

## Operational controls
Existing /sync owns the special two-repository bidirectional reconciliation contract. /SS controls one-way distribution to other consumers. High-risk or destructive changes require explicit authorization. CI is read-only. Production deployment requires independent QA and verified consumer-state checks.
