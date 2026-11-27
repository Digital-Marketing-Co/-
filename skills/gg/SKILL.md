---
name: gg
description: GeniusGod checkpointed orchestration for authorized outstanding work.
metadata:
  version: "1.2.0"
  flag: /GG
  aliases: [GG, /GG, GeniusGod, /GeniusGod, gg, /gg]
---
# /GG — GeniusGod

```text
I {
    GENIUS GOD {
        Batch(W,W.len()) {
            /FA /VE /QA /VQA /Perfect
            Checkpoint
        }
        AutoResume
        if RemainingLimitations.len() > 0 {
            GENIUS GOD /Perfect GG
        }
    } u E u C
} u E u C
```

Resolve W to outstanding work; order dependencies topologically, flag cycles, and snapshot W once per discovery cycle and set the logical batch size to the snapshot length. Internally partition into resource-safe operational chunks (default at most ten), preserving dependency order and full logical scope. If W is empty, skip batching and verify global acceptance. Execute the block for each pending batch, verify applicable gates, and persist evidence, source HEAD, item identities, status and next unfinished checkpoint. Partial checkpoints must distinguish retrieval from acceptance. AutoResume restores the first unfinished valid checkpoint, invalidates changed items and dependents, and rediscovers work after each cycle. Use a single bounded scheduler, not recursive orchestrator calls. Stop on verified global acceptance or a concrete blocker; do not claim unattended execution without a scheduler. Preserve aliases and unrelated changes; zero paid inference credits. Use existing universal QA and Perfect contracts. Never treat untested work as complete.

## Automatic limitation resolution
Collect actual remaining limitations from acceptance evidence, not mere textual mentions. Convert each into a tracked W item with cause, evidence, dependencies and retry history. GENIUS GOD /Perfect GG in the conditional is a tail continuation of the existing scheduler, never a nested invocation. Repair actionable limitations and reverify; checkpoint before continuing. Bound retries, detect no progress, and persist externally blocked items without falsely claiming completion. Resume when prerequisites change or authorized scheduling permits. Never bypass approval, resource limits, or safety gates.
