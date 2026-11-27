---
name: gg
description: GeniusGod checkpointed orchestration for authorized outstanding work.
metadata:
  version: "1.0.0"
  flag: /GG
  aliases: [GG, /GG, GeniusGod, /GeniusGod, gg, /gg]
---
# /GG — GeniusGod

```text
I {
    GENIUS GOD {
        Batch(W,10) {
            /FA /VE /QA /VQA /Perfect
            Checkpoint
        }
        AutoResume
    } u E u C
} u E u C
```

Resolve W to outstanding work; order dependencies topologically, flag cycles, and partition into batches of at most ten. Execute the block for each pending batch, verify applicable gates, and persist evidence, source HEAD, item identities, status and next unfinished checkpoint. Partial checkpoints must distinguish retrieval from acceptance. AutoResume restores the first unfinished valid checkpoint, invalidates changed items and dependents, and rediscoveries work after each cycle. Use a single bounded scheduler, not recursive orchestrator calls. Stop on verified global acceptance or a concrete blocker; do not claim unattended execution without a scheduler. Preserve aliases and unrelated changes; zero paid inference credits. Use existing universal QA and Perfect contracts. Never treat untested work as complete.
