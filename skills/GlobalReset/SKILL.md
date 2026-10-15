---
name: GlobalReset
description: Perform full improvement of everything improvable across every skill in the Digital-Marketing-Co/- repository, then automatically raise version numbers. Trigger on /GlobalReset, GlobalReset, full skill improvement, or reset all skills.
metadata:
  type: workflow
  version: "1.0.0"
  flag: /GlobalReset
---

# /GlobalReset

Raise the quality of every skill in the shared repository and advance each version marker.

## When this runs

- User typed /GlobalReset.
- User asked for a full improvement pass over all skills on the repository.
- User asked to raise version numbers after a broad skill update.

## Mandated first priority

When any individual skill is updated on the repository, perform a complete improvement of everything that can be improved for that skill before the commit is considered finished.

## Steps

1. Read SKILL-SYNC.md, skills/ledger/latest.md, and list every skills/<name>/ directory on main.
2. For each skill directory that contains a SKILL.md:
   - Read the full skill tree.
   - Improve every improvable element: wording clarity, trigger accuracy, missing required files (CHANGELOG, evals), broken references, outdated version markers, incomplete workflows, and consistency with research-unbounded and interop contracts.
   - Raise the version number in frontmatter metadata.version and in CHANGELOG.md by one patch level unless a larger bump is justified by the change set.
3. Commit the complete improved skill directories to main.
4. Prepend one ledger row per skill that changed: date, skill name, direction, short hash, one-line summary of the improvement.
5. Do not overwrite bundled host skills.
6. Report the commit URLs, the skills that received improvement, and which skills the other host must re-upload.

## Version rule

- Look for metadata.version in SKILL.md frontmatter.
- If absent, add version: "1.0.0".
- If present, increment the patch component (1.2.3 becomes 1.2.4).
- Append a dated entry to CHANGELOG.md describing the improvement.

## Delivery

Follow the interop delivery contract and the negative sweep as the final gate.
