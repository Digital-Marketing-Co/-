---
name: sync
description: Resume and verify synchronization of the canonical skills directory from Digital-Marketing-Co/- to Digital-Marketing-Co/Digital-Marketing-Co until no canonical supporting files remain missing or different; safe resumable bounded batches.
metadata:
  type: workflow
  version: "1.0.0"
  flag: /sync
---
# /sync — Canonical skill synchronization

## Direction and scope
Canonical source: `Digital-Marketing-Co/-`, branch `main`.
Destination: `Digital-Marketing-Co/Digital-Marketing-Co`, branch `main`.
Synchronize **all** canonical `skills/` files, including SKILL.md, scripts, references, assets, tests, fonts, PDFs and binary files, not just text. Never modify source files or delete destination-only files. Do not overwrite divergent destination work without explicitly identifying conflicts and applying the canonical-source policy approved by the user.

## Executable algorithm
```pseudo
while (countCanonicalDifferences(source.skills, destination.skills) > 0) {
    snapshot = fetchFreshGitTrees(source.main, destination.main)
    remaining = diffByPathAndBlobSha(snapshot.source.skills, snapshot.destination.skills)
    if (remaining.length == 0) break
    batch = selectBoundedBatch(remaining, supportedFormatsAndLimits)
    if (batch.length == 0) { reportBlockers(remaining); break }
    copyEachFileExactly(source, destination, batch) // preserve binary bytes, not text-decoding
    commitToDestinationWithBaseTreeAndExpectedHead(batch) // non-force, optimistic lock
    verifyCommitAndReReadTrees()
    if (failureOrNoProgress) { reportBlocker(); break }
}
reportVerifiedCountsAndCommits()
```

## Mandatory reliability
1. Compute remaining count from GitHub tree SHA comparisons at the start and after each successful batch. Never infer counts solely by subtracting a planned batch size.
2. Use bounded batches appropriate to the tool's call/size limits. Continue batches in the current invocation while feasible; if the execution budget is reached, report incomplete status and resume from a fresh diff on the next /sync invocation. Do not imply autonomous background execution.
3. Fetch content and create blobs in the destination repository. Cross-repository SHA-only tree entries are invalid. For binary files use binary-safe Git blob transfer (base64/blob API or equivalent), not a text file API that corrupts bytes.
4. Use fresh destination branch head, base tree, new commit, and non-force expected-head ref update. On conflict re-read head and recompute differences. Never rewrite history or force-push.
5. Preserve destination-only files and avoid unrelated paths. Skip already identical files. Validate all 77 canonical SKILL.md files as well as supporting assets.
6. If any file cannot be copied safely, record its path and reason, continue safe batches, and report exact unresolved items. Never mark complete while any source path differs.
7. After final batch, independently re-fetch both recursive trees and require zero missing or differing canonical `skills/` blobs. Run available validation checks; distinguish verification of file parity from runtime QA.
8. Do not claim a GitHub push, test pass, or full sync unless the remote API confirms it.
9. Honor the shared document-rendering standard when creating reader-facing documents; keep internal skill execution details out of those documents.

## Invocation
`/sync` — begin or resume safe synchronization until parity or the current execution limit.
`/sync status` — compare trees and report exact counts without writing.
