# Repository-wide skill sync and QA audit — 2026-10-15

Repository: Digital-Marketing-Co/-, branch main.

## Verified remotely
- Git tree inventory: 1,328 entries, 935 tracked blobs, 68 direct skills/*/SKILL.md definitions.
- No zero-byte tracked blobs found in the inspected tree.
- Core paths present: SKILL-SYNC.md, skills/ledger/latest.md, scripts/sync-skills.sh, skills/interop/SKILL.md, skills/research-unbounded/SKILL.md, skills/wicca/SKILL.md.
- skills/ResearchPlus/SKILL.md exists and delegates to research-unbounded.
- Inspected skill-sync, qa-universal, wca-ivy-biblio, ResearchPlus and skills README.
- Discovered synchronization defect: rsync --ignore-existing prevented upstream changes to already installed files from updating. Fixed to overwrite with timestamped backups, preserve local-only files, and compare every upstream SKILL.md after copying.

## Not verified / outstanding
- This was a remote Git tree and selected-content audit, not a local clone-and-execute test of all 935 files.
- No local sync execution, shellcheck, Python tests, rendering tests, secret scan, or full cross-skill dependency resolution was performed.
- Existing local customizations will be backed up on sync; review backup differences before discarding them.
- ChatGPT managed skill installation cannot be modified merely by committing to GitHub.
- Other skills have not all been rewritten to explicitly import research-unbounded. The canonical standard exists, but enforcement in every independent skill is not verified.
- No claim of complete QA pass or runtime installation is made.

## Required release gate
1. Clone/pull main on a trusted Linux/WSL host.
2. Run bash -n scripts/sync-skills.sh and shellcheck if available.
3. Run scripts/sync-skills.sh; compare local/upstream skill manifests.
4. Validate every SKILL.md frontmatter, referenced local paths, slash aliases, and circular dependencies.
5. Run tests in safe sandbox; audit secrets and unsafe commands.
6. Validate representative PDF, DOCX, XLSX, PPTX, and image outputs.
7. Record failures with reproducible steps; repair and rerun.
8. Only label full audit PASS after every required test is actually executed and passed.

## Research depth policy
ResearchPlus is an alias for research-unbounded. No arbitrary page or citation caps; real technical limits are handled through checkpointed volumes. Source validity and nonfabrication remain mandatory.
