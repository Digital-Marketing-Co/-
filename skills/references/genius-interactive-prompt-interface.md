# GENIUS Interactive Prompt Interface

A reusable, accessible interaction and visual contract for skills that create an interactive prompt-writing or prompt-guided interface. This is a repository standard, not a claim that the absent `/Perfect` skill was inspected or installed. It complements `skills/genius/SKILL.md`; it must never change `/genius`'s exact prompt-wrapping contract.

## Applicability and authority

Use this contract only when the requested deliverable is an interactive visual interface. Do not add a UI, holographic treatment, or extra interaction to a text-only prompt, document, script, command-line workflow, audio output, archival reproduction, or other nonvisual task. Preserve the user's explicit visual direction and the calling skill's existing font, content, format, source-fidelity, and safety requirements. Where `/4629` or `/visual-system` applies, use its canonical references as the visual authority; this document does not override them.

## Interaction model

- Make the primary prompt task immediately clear: a labeled prompt field, a concise purpose statement, and one obvious primary action.
- Offer optional, task-relevant controls as progressively disclosed groups (for example: audience, format, tone, constraints, or output length). Do not overwhelm the initial view.
- Preserve user-entered text exactly unless the user explicitly requests transformation. Clearly distinguish source prompt, optional controls, generated result, and any edits.
- Provide copy, clear, reset, and preview actions only when implemented. Confirm before destructive clearing if unsaved user text would be lost.
- Prefer sensible defaults and continue when enough information is present. Ask at most one concise, high-value clarification at a time; make optional questions skippable. Do not create a forced wizard when a direct prompt is sufficient.
- Show a visible processing, success, empty, and recoverable error state. Never imply a prompt was executed when the interface only generated or formatted it.
- Keep keyboard order predictable; use semantic labels, buttons, status announcements, visible focus, adequate touch targets, and screen-reader-readable validation.

## Holographic visual direction

When holography is requested or suitable, use a refined optical treatment rather than decorative clutter: deep ink or midnight-navy grounds; restrained cyan, violet, or palette-compatible edge light; translucent layered glass surfaces; soft radial light behind interface chrome; precise fine rules; controlled perspective; and clear focal hierarchy. Use real gradients and alpha where transparency is intended. Keep the prompt text surface opaque or sufficiently stable for comfortable reading. Avoid visual noise, illegible glow, fake data, fabricated technical readouts, and motion that competes with the task.

Treat “best holography” as a quality goal, not permission to change content or impose a single palette. Inherit the calling skill's palette and user direction. Use depth on panels and controls, not on long reading text. For print or static exports, use a static, print-safe equivalent; do not pretend animation survives export.

## Accessibility, motion, and responsive behavior

- Meet WCAG 2.2 AA contrast for text and controls; do not rely on color, glow, or blur alone to communicate state.
- Support keyboard-only use, screen readers, zoom/reflow, and narrow viewports down to 320 CSS pixels where the target platform permits.
- Respect `prefers-reduced-motion`; provide a genuinely low-motion or static experience. Avoid flashing, forced parallax, auto-rotating content, or motion that blocks operation.
- Keep text selectable and maintain semantic reading order. Ensure glass transparency does not reduce contrast across changing backgrounds.
- Test long prompts, long labels, empty input, validation, error recovery, reduced motion, keyboard navigation, and responsive layouts.

## Validation and reporting

Before delivery, verify the implemented controls and states rather than reporting planned controls as present. Record checks as PASS, FAIL, BLOCKED, or NOT TESTED with concrete evidence. A visual polish claim is not a substitute for functional, accessibility, or responsive validation. Do not claim a live interface, deployment, or `/Perfect` parity unless it was actually observed and tested.
