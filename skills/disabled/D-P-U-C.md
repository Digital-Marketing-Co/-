# Disabled Proceed Until Completed (D P u C)

**Meaning:** When the user sends `D P u C`, it means **Disabled Proceed until Completed**. Apply the combined accessibility-first and continuation policy below.

## Operating rule

1. Resume the latest unfinished, explicitly authorized repository task in this conversation. Do not restate or unnecessarily repeat the original request.
2. Continue through verified milestones and the next safe executable step without repeated proceed prompts.
3. Reuse repository context, review branches, tool results, existing diffs, and verified handoff notes.
4. Minimize typing, taps, uploads, confirmation dialogs, and repeated questions. Preserve required platform and security approvals.
5. Stop only for a genuine missing prerequisite, a required external approval, an unavailable credential/tool, an unauthorized or destructive action, or an action that would change protected production state.

## Completion loop

- Re-read live repository and CI state before editing.
- Deduplicate resolved items and map each remaining item to a file, test, and safe action.
- Apply only reversible, in-scope fixes where authorization permits.
- Commit coherent changes to an appropriate review branch, but do not claim merge or deployment without platform confirmation.
- Run structural checks and applicable tests.
- Inspect exact failures; repair the verified root cause and rerun.
- Perform two complete clean passes before claiming `Verified Complete`.
- Recheck the exact target branch and commit before reporting.

## Status language

Use only evidence-backed labels:

- `Queued`
- `Running`
- `Verified`
- `Blocked`
- `Failed`
- `Complete`
- `NOT TESTED`

Do not call a build perfect or complete merely because the intended change was made. Distinguish planned work from observed work.

## Safety and accessibility

Accessibility accommodations reduce interaction burden but do not bypass GitHub protections, merge reviews, production authorization, Vercel/host safeguards, secret handling, financial actions, or unrelated repository access. Do not claim background work continues after the response unless an actual host automation confirms it.
