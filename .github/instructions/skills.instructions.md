---
applyTo: "skills/**/*.md"
---
# Shared skill authoring instructions

For every skill under `skills/`, preserve its existing purpose, trigger names, aliases, workflow, output contracts, and safety requirements. Do not copy these instructions into every skill or introduce visual styling into a nonvisual task.

When a skill creates or modifies an interactive prompt interface, prompt builder, web UI, or interactive presentation, follow the shared **GENIUS Interactive Prompt Interface** contract in `skills/references/genius-interactive-prompt-interface.md`. Read that contract before implementation. This is a repository-wide conditional requirement: apply it only when the output is interactive and visual; otherwise mark it not applicable and preserve exact text, source fidelity, data, code, audio, and other format-specific requirements.

The repository currently has `skills/genius/`, whose purpose is to wrap supplied prompt text; it is not the requested `/Perfect` interface specification. Do not claim that a `/Perfect` skill was found or that its interface was copied. The shared contract is a new, compatible repository standard, and must not alter `/genius`'s exact-output behavior.

Use the canonical repository skill and its quality profile and evaluation fixtures. Make scoped edits on the active review branch, run relevant checks when available, and report actual results. Do not apply a blanket holographic theme to every skill output: visual-system rules, accessibility, user direction, and format/source-fidelity locks remain controlling.
