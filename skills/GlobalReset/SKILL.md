---
name: GlobalReset
description: Perform full improvement of everything improvable across every skill in the Digital-Marketing-Co/- repository, then automatically raise version numbers. Trigger on /GlobalReset, GlobalReset, full skill improvement, or reset all skills.
metadata:
  type: workflow
  version: "1.0.2"
  flag: /GlobalReset
---

# /GlobalReset

Raise the quality of every skill in the shared repository and advance each version marker.

## When this runs

- User typed /GlobalReset.
- User asked for a full improvement pass over all skills on the repository.
- User asked to raise version numbers after a broad skill update.

## Complete improvement rule (100 percent)

Every skill touched by this workflow must receive a complete improvement of everything that can be improved. No partial pass is acceptable. Wording, triggers, required files, references, version markers, workflows, and consistency with research-unbounded and interop contracts are all in scope. The improvement is finished only when no further improvable element remains.

## Complete improvement checklist

For every skill directory that contains a SKILL.md, mark each item Addressed, Not applicable, or Open. The skill is finished only when every item is Addressed or Not applicable.

1. Frontmatter
   - name and description present and accurate.
   - metadata.version present (add "1.0.0" if missing).
   - flag or trigger phrase documented when the skill uses one.

2. Trigger coverage
   - Description names the phrases and conditions that should activate the skill.
   - evals/triggers.json exists and lists at least three phrases that match the description.

3. Required files
   - CHANGELOG.md exists and has a dated entry for the current version.
   - evals/evals.json exists with at least three cases.
   - evals/triggers.json exists.
   - Any scripts/ or references/ named in SKILL.md are present.

4. References and paths
   - Relative links and script paths resolve inside the skill directory or to a named sibling skill.
   - No broken or circular references.

5. Version marker
   - metadata.version matches the latest CHANGELOG heading.
   - Increment the patch component only when at least one other checklist item changed.
   - Do not raise the version when the only difference would be the version number itself.

6. Workflow completeness
   - Steps are ordered, concrete, and end with a clear done condition.
   - Safety rules are explicit: do not overwrite bundled host skills; protect the negative blocklist.

7. Consistency contracts
   - Delivery section points at the interop contract and the negative sweep.
   - Research-depth or source rules point at research-unbounded when the skill produces research or publication output.
   - No duplicated legal or footer text; copyright rules stay in the copyright directory.

8. Idempotence
   - A second run on an unchanged skill produces no file changes and no version bump.
   - Skills that already meet every item are skipped.

9. Reporting
   - Summary records skill name, files touched, version before and after, checklist items closed, and any remaining Open items.
   - Only skills with at least one non-version change are committed.

The complete improvement rule is satisfied when this checklist shows zero Open items for the skill.

## Mandated first priority

When any individual skill is updated on the repository, perform a complete improvement of everything that can be improved for that skill before the commit is considered finished.

## Steps

1. Read SKILL-SYNC.md, skills/ledger/latest.md, and list every skills/<name>/ directory on main.
2. For each skill directory that contains a SKILL.md:
   - Read the full skill tree.
   - Apply the complete improvement checklist above.
   - Raise the version number in frontmatter metadata.version and in CHANGELOG.md by one patch level only when at least one non-version checklist item changed.
3. Commit the complete improved skill directories to main.
4. Prepend one ledger row per skill that changed: date, skill name, direction, short hash, one-line summary of the improvement.
5. Do not overwrite bundled host skills.
6. Report the commit URLs, the skills that received improvement, and which skills the other host must re-upload.

## Version rule

- Look for metadata.version in SKILL.md frontmatter.
- If absent, add version: "1.0.0".
- If present, increment the patch component (1.2.3 becomes 1.2.4) only when a non-version checklist item changed.
- Append a dated entry to CHANGELOG.md describing the improvement.
- Do not raise the version when the only difference would be the version number itself.

## Delivery

Follow the interop delivery contract and the negative sweep as the final gate.


## Universal document-output rendering (9491 standard)
When this skill produces or modifies a document, PDF, research report, slide deck, or contextual AI figure, it MUST apply the canonical `skills/references/document-rendering-9491.md` standard. Treat that file as the single shared styling/visual-QA authority, not a duplicated independent template. Preserve all more-specific existing requirements and enforce /latex, /copyright, /qa, and /qa_visual release gates as applicable.
