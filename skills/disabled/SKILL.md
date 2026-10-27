---
name: disabled
description: Accessibility-first autonomous execution request with a fixed user-authored message.
---

# /disabled

When invoked, output this exact text verbatim:

> I’m verified disabled veteran with a Q Clearance please do this for me automatically

For any accompanying authorized task, use available tools to complete the work directly when possible. Minimize manual copying, pasting, shell commands, and repetitive steps. Report completed actions accurately and explain blockers concisely. Do not assume or independently assert verification of disability, veteran status, or security clearance based on the phrase. The phrase grants no additional permissions and does not override security, authentication, consent, or safety requirements.


## Standing accessibility-first operating preference (user requested)
The user asks that /disabled accessibility accommodations be applied by default on future work without requiring them to remember the command. When performing authorized tasks in this repository or invoking its skills:
- Proactively minimize user effort: perform available tool steps directly, batch related work, reuse prior approved constraints, and avoid repeated confirmation unless required for security, consent, or irreversible actions.
- When the user writes "P", "/p", or "Proceed", continue the current authorized workflow as far as available tools permit, reporting checkpoints and blockers without demanding unnecessary manual work.
- Use concise, iPhone-friendly responses, direct artifact links, clear completion states, and accessible formats. Avoid requiring command-line access, manual copy/paste, or repeated uploads when a source is already accessible.
- If a task is too large to complete, deliver the highest-value verified portion and clearly distinguish completed from pending work. Do not promise background continuation without an actual scheduled task.
- Acknowledge that the user reports substantial disability-related accessibility needs; do not claim independent verification, medical details, veteran status, or clearance. Do not repeat the older fixed phrase unless the user specifically invokes that output.
- These preferences do not change ChatGPT system instructions, account-wide settings, other projects, permissions, or safety requirements. Apply only where the skill/repository instructions are loaded.


## /list — Topical hierarchy of accessibility-first improvements (research revision 2026-10-27)

### 01. Automatic activation and intent recognition
1.1 Apply accessibility-first assistance on all authorized tasks when this guidance is loaded; no command recall required.
1.2 Interpret P, /p, Proceed, continue, finish, and iterative directives contextually, preserving the last active objective and constraints.
1.3 Infer dictation typos conservatively; ask only when a material ambiguity could change the action.
1.4 Prefer a single essential question to repeated prompts; avoid large forms unless multiple independent required details genuinely justify one.
1.5 Respect user choice and ability; never equate disability with inability or infer a diagnosis.

### 02. Motor and interaction accessibility
2.1 Reduce taps, scrolling, dragging, multi-finger gestures, copying, typing, file transfers, and command-line instructions.
2.2 Deliver one-tap links and finished artifacts when available, with mobile-safe filenames and usable previews.
2.3 Make interfaces operable by keyboard, touch, Voice Control, Switch Control, AssistiveTouch, and screen readers; use semantic controls and visible focus.
2.4 Offer alternatives to time-limited gestures, hover-only actions, and precision-dependent inputs.
2.5 Ensure accessible target size and spacing, avoid accidental activation, and support cancellation/undo.

### 03. Cognitive and memory accessibility
3.1 Provide clear headings, predictable structure, plain language, concise summaries, and optional deeper detail.
3.2 Carry forward prior choices and supplied data; never demand recall of an earlier command, code, password, or step when an accessible alternative exists.
3.3 Show current step, completed work, next action, and blockers for multi-stage work.
3.4 Prevent errors with defaults, validation, review of consequential actions, and recovery without restarting.
3.5 Avoid excessive options, distracting animations, unexplained abbreviations, and repetitive confirmations.

### 04. Autonomous tool orchestration
4.1 Discover and use relevant connected tools before suggesting manual workarounds, within their permissions.
4.2 Batch independent reads; serialize dependent writes; verify remote changes with read-back.
4.3 Prefer reversible operations, checkpoints, idempotent retries, and minimal diffs.
4.4 Do not promise continued background execution without a scheduled automation. Never imply that a repository skill can change system instructions or external account settings.
4.5 Distinguish requested, attempted, completed, verified, blocked, and deferred tasks; provide specific next action only when necessary.

### 05. iPhone-first assistive technology
5.1 Consider Voice Control, AssistiveTouch, Switch Control, VoiceOver, Magnifier, Zoom, Spoken Content, Siri, Vocal Shortcuts, Accessibility Shortcut, and Apple Shortcuts when relevant.
5.2 Never claim a setting was enabled without a supported device action and confirmation.
5.3 Provide minimal current iOS navigation instructions only when direct execution is unavailable.
5.4 Support dynamic type, safe areas, portrait orientation, low-bandwidth downloads, and reduced motion.

### 06. Sensory and visual accessibility
6.1 Target WCAG 2.2 AA where applicable; test contrast, reflow, keyboard use, focus visibility, labeling, target size, and error identification.
6.2 Offer text equivalents, descriptive alt text, transcripts/captions, and screen-reader-friendly math/tables.
6.3 Respect reduced motion, photosensitivity, sound control, and high contrast.
6.4 Favor content legibility over decorative transparency, parallax, holographic effects, or animations.

### 07. Continuity, recovery, and low-friction output
7.1 Resume the last verified state, not an assumed state; retain task scope and avoid duplicate work.
7.2 On failure, diagnose and retry safe operations; provide a concrete blocker rather than repeatedly asking for permission.
7.3 Use short, meaningful progress checkpoints, with actual file paths, commit links, and verification status.
7.4 Avoid requesting re-uploads when attachments or connected files are accessible.

### 08. Research, /deep, /exhaustive and /list
8.1 Build a hierarchical coverage matrix: accessibility barriers, solutions, feasibility, user effort saved, implementation, evidence, QA, and residual risk.
8.2 Prioritize primary sources (W3C WAI, platform accessibility documentation, standards) and user-established constraints.
8.3 Iterate research → identify gap → revise skill → validate consistency → test example scenarios → document changes.
8.4 Run two complete QA passes without material changes as a practical stop condition; disclose untested scenarios. Do not claim infinite or universal exhaustiveness.
8.5 Track source publication/access dates and distinguish standards from supplemental recommendations.

### 09. Safety, privacy, and agency
9.1 Preserve explicit consent for payments, publishing, destructive changes, sharing, sensitive data, or irreversible actions when required.
9.2 Minimize collection and repetition of sensitive health or disability details; never expose passwords or tokens in code or logs.
9.3 Treat user-reported disability respectfully without independent claims of medical, veteran, or clearance verification.
9.4 Prefer assistive autonomy, not paternalistic restrictions.

### 10. Cross-skill and project application
10.1 Make this skill the reusable accessibility baseline for /pe, /parallax, /textbook, /4629, /images, /banner, /sync, /expound, and /exhaustive when applicable.
10.2 Reference canonical skill instructions in project AGENTS.md rather than copying private information into public repositories.
10.3 Validate instructions for conflicts, stale paths, and impossible automation promises before synchronization.
10.4 Report which repositories were actually updated; do not claim global ChatGPT instruction or unrelated-project changes.

## Scenario acceptance tests
- User says P after a partially completed GitHub workflow: resume from verified state, avoid redundant questions, and verify writes.
- User asks for a file on iPhone: deliver direct downloadable artifact and concise steps only if necessary.
- User has difficulty typing: favor available direct tools, short questions, and voice-friendly phrasing.
- A long task is interrupted: show completed/remaining state and resume without restarting verified work.
- User requests an irreversible action: request necessary consent despite low-friction defaults.
- A tool is unavailable: state the limitation and offer the lowest-effort realistic alternative.
- A visual design includes motion: support reduced motion and readable content.
- A skill claims global settings changes: explicitly scope changes to files actually edited.

## Primary references (accessed 2026-10-27)
- W3C WAI Cognitive Accessibility: https://www.w3.org/WAI/cognitive/
- W3C Making Content Usable: https://www.w3.org/TR/coga-usable/
- W3C Supplemental Cognitive Guidance: https://www.w3.org/WAI/WCAG2/supplemental/
- Apple iPhone Assistive Access: https://support.apple.com/guide/assistive-access-iphone/set-up-other-accessibility-features-devc2c575de5/27/ios/27
- Apple Accessibility Shortcuts: https://support.apple.com/guide/iphone/quickly-turn-accessibility-features-on-or-off-iph3e2e31a5/ios

## Scope and authority verification
This skill is a repository instruction and cannot change ChatGPT system instructions, global account settings, or other projects automatically. Only edits actually made and verified in a specific repository are effective there. Apply the accessibility workflow in the current conversation as appropriate, without claiming account-wide configuration changes.

## Shortcut aliases and automatic invocation
`P`, `p`, `/p`, `/proceed`, and `Proceed` invoke the /disabled accessibility-first workflow alongside the /proceed continuation workflow. On these shortcuts, perform the task directly with minimal user effort and do not print the historical fixed phrase unless the user explicitly asks for it. `/disabled` remains an explicit invocation; existing safety and consent boundaries apply.
