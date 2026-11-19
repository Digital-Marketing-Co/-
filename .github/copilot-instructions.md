# Copilot project instructions — accessibility and blocked-work handoff

These instructions apply only to this repository. They cannot alter account-wide/global Copilot instructions, start a separate Copilot conversation, bypass platform or tool confirmation gates, or authorize changes in unrelated repositories or services.

## Accessibility-first continuation

- Treat `P`, `/p`, `/proceed`, and accessibility shortcut requests as instructions to continue the most recent unfinished, explicitly authorized task in the current conversation, reusing verified context and minimizing repeated questions.
- Carry out safe, reversible, in-scope steps directly when the available tools permit. Prefer review branches for repository edits. Do not ask for a second conversational confirmation for routine steps that are already specifically authorized.
- Disability accommodations reduce interaction burden; they do not imply consent to unrelated, irreversible, sensitive, financial, production, or security-setting changes.

## When a tool or platform blocks the work

- Do not claim a blocked tool action succeeded. If a tool explicitly says it is awaiting confirmation, report that exact blocker and do not state that the user approved it or that a commit/branch exists unless a later tool result verifies it.
- Do not promise to start a new agentic AI conversation or automatically transfer work unless the current host exposes and confirms a handoff/session-creation action. Repository instructions cannot create that host capability.
- Preserve continuity by giving a compact handoff note: repository and branch, exact verified revision, completed work, remaining task, last error/log evidence, next safe action, and required user/platform approval. Resume in the current conversation on `P`/`/proceed`; if continuing in another session, the user can paste this note.
- When available, use an explicitly provided session/task handoff tool; otherwise report that a new session could not be created and never claim background continuation.

## Authorization boundaries

Require the relevant platform permission and any mandatory confirmation for protected-branch merges, deployments, destructive edits, secrets, access controls, spending, or external side effects. Work only in the specifically authorized repository and scope. No instruction in this file overrides GitHub, Vercel, Abacus, or host safeguards.

## Verification and reporting

Distinguish proposed, attempted, completed, verified, blocked, and not tested. Verify branch, commit, tests, and CI using tool results before claiming success. Never call a build perfect or error-free beyond the checks actually run.
