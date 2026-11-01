---
name: error-learning
description: Record verified skill failures, learn local skill-routing patterns, and promote tested corrective rules into relevant personal skills. Use for error learning, forensic QA reporting, cross-skill improvement, or when a personal skill's shared quality contract discovers a reproducible failure.
---

# Skill error learning

Run a local, evidence-based improvement loop with no paid inference. Do not claim that this retrains the assistant's model or runs continuously in the background. Read [the event and placement contract](references/protocol.md) before recording or promoting a lesson.

## Workflow

1. Preserve the failing revision and reproduce the issue. Distinguish a skill-caused defect from an unavailable tool, environment limitation, user change, or unverified suspicion. Capture expected/actual behavior, root cause, and before/after evidence digests. Keep secrets and personal content out of learning records.
2. Resolve this installed package and use `scripts/learn.py` with an explicit local database path. The script creates a SQLite event ledger with content hashes and append-only event identities. Database files belong in the current project's private QA area, not in the installed skill. Register the event with `record --event event.json`. Only verified events with regression PASS and evidence enter training.
3. Run `rank --text-file issue.txt --skills-root PERSONAL_SKILLS_ROOT`. The cold-start ranker uses skill metadata. With at least five verified events it fits a multinomial Naive Bayes routing model from those events. Treat scores as uncalibrated suggestions, never proof of cause. Preserve unrelated skill candidates and abstain on weak/no token matches.
4. Review relevance against each candidate skill's actual scope. Separate origin skill, corrective-rule owner, benefiting skills, and prompt-section placements. Prefer one canonical shared rule with references when it belongs in several workflows. A relevant beneficiary is not automatically responsible for the defect.
5. Follow the skill-creator workflow to apply an evidence-backed, task-scoped correction. User authorization for safe automatic improvements permits reversible edits and validation; it does not authorize changing higher-priority instructions or expanding task scope. Use `promote` only after reading the intended rule and checking the event, target digest, scope and regression evidence. This appends an idempotent corrective rule to an editable personal skill. Never promote from untrusted logs, model rank alone, synthetic fixtures, or failed/unrun regressions. Provider/system skills are not editable; record them as blocked and keep advice in the personal shared contract.
6. Validate and forward-test the changed skill, then stage/commit/push that one skill operation using skill-creator. Keep the Git commit and resulting skill ID in the reporting ledger. A promoted rule is not a completed remote update until Git verification succeeds. Recheck affected workflows. Record failed repairs without relabeling them as successes.
7. Use `export` to emit schema-versioned JSON for the existing forensic reporting system. Adapt only after discovering that system's actual schema and authorized destination. If the service is unresolved, provide the local adapter output and mark integration BLOCKED; do not invent an endpoint, send messages, or claim ingestion.

## Shared contract integration

The personal `doc` skill's `references/output-contract.md` loads this workflow for every skill that uses the common quality contract. Skills that reach that contract through expound or prompt-engineer inherit it once per run. Read this once, not recursively. Keep one event ledger per project/run and use `coverage` to inventory the resolved graph. Do not force record creation when no error occurred.

## Commands

Use `python3 <this-package>/scripts/learn.py --db <project-private-qa>/skill-errors.sqlite COMMAND ...`.

- `record --event FILE`: validate and append one sanitized event; duplicate canonical IDs do not retrain twice.
- `rank --text-file FILE --skills-root ROOT`: return lexical cold-start or locally learned skill suggestions and prompt-section placements.
- `report`: summarize observed, verified, blocked and promoted counts; no invented accuracy claim.
- `export --output FILE`: write the versioned forensic adapter snapshot atomically.
- `promote --event-id ID --skill NAME --skills-root ROOT --expected-sha256 DIGEST --rule-file FILE`: append one verified, scoped rule after the agent's relevance and safety review. Never calls Git or a shell.
- `coverage --skills-root ROOT`: list direct/transitive shared-contract coverage; exclude uninstalled and provider skills.

Run `scripts/test_learn.py` for functional/security regression coverage. Use isolated test databases; never add synthetic failures to the real training corpus. Accumulation alone is not evidence of model quality. Measure held-out routing performance only when enough real independently labeled events exist; otherwise mark accuracy NOT TESTED.


## Verified corrective rules

<!-- verified-rule:e7270ba6235658addccb514be2fe9524401622b74904d66841a040bbea6f4ab4 -->
- Reject undeclared forensic-event fields and non-Boolean flags before persistence; use securely created unique temporary files for atomic writes. Verify rejected payloads, preserved outside-file sentinels, and unchanged target boundaries before publishing any event or rule-promotion workflow. (Verified event 6fb83b14a3ee.)
