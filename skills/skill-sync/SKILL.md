---
name: skill-sync
description: Reconcile custom skill directories with Digital-Marketing-Co/- main, preserve verified newer behavior, validate changes, and record separate GitHub and editable-host save results. Use for /skill-sync or requests to save and sync skills.
---

# Skill synchronization

Read [the quality profile](references/quality-profile.md) and `evals/quality-cases.json`. Read repository AGENTS.md, SKILL-SYNC.md, .skill-sync/policy.json, and skills/ledger/latest.md from the same base commit before edits.

1. Verify repository access and account identity. Record the complete base SHA and commit time.
2. Inventory complete canonical and relevant installed directories, including references, scripts, assets, evaluations, and agent metadata. Decide direction from commit history, ledger and verified behavior, never byte size or file timestamp alone.
3. Merge intended newer improvements, preserving unrelated files and local work. Skip generated caches. Preserve binaries regardless of an arbitrary size threshold. Do not replace bundled host tools.
4. Validate frontmatter, resource paths, Python compilation, schemas, and changed-script fixtures. Record unrun network, provider, UI, or device checks as NOT TESTED or BLOCKED.
5. Create one reviewed commit with the changed directories and prepend ledger provenance. Check the branch head before publishing; reject a changed lease, inspect new changes, and reconcile without force overwriting another writer.
6. Save editable personal installations through their host's actual installation workflow. Where the Skills workspace is a git repository, commit the intended directories and push its current branch. A successful canonical GitHub write is not installation proof.
7. Verify the remote commit, per-skill hashes, and host save outcome. Report exact revisions, checked and saved counts, unresolved installation boundaries, and tests.

Use `interop/SKILL.md` for the single delivery gate. Do not invent cross-host access or imply unattended synchronization continues after the turn.
