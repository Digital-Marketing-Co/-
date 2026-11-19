# Continuation handoff for accessibility-first repository work

Use this note as a compact continuity format when the active conversation or tool session cannot continue the authorized task.

## Required handoff fields

- **Repository / branch:** exact `owner/repo` and branch, or “not verified.”
- **Revision:** commit SHA confirmed by GitHub, or “not verified.”
- **Goal:** one-sentence user-authorized task and scope.
- **Completed:** only changes confirmed by tool results.
- **Remaining:** the next safe, concrete action(s).
- **Evidence:** exact failing workflow, job, test, or error and links when available.
- **Blocker:** exact missing permission, unavailable tool, confirmation requirement, or missing input.
- **Safety boundary:** any action that still requires explicit approval or platform authorization.

## Continuation behavior

1. First use existing conversation context and available tools; do not make the user restate information already present.
2. If a current-session continuation command exists, resume the latest unfinished task and re-check live repository state before editing.
3. Create a separate agent/session only through an actual host-provided handoff capability. Never imply that a branch, issue, task, or conversation was created unless the host confirms it.
4. If the host has no handoff capability, return the handoff fields above in a copyable, concise form. A repository file cannot launch another AI conversation or override platform confirmations.
5. Keep changes scoped to the authorized repository and use a review branch. Do not merge or deploy unless that specific action is authorized and permitted.
