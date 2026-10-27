---
name: interface
description: /interface invokes an accessible futuristic 4629-style operation dashboard for current tasks, verified progress, blockers, and next actions.
---

# /interface — accessible operation dashboard

When invoked, present a real, readable progress dashboard for the current authorized workflow. Apply /4629 visual language (midnight navy, cyan accents, layered depth) without sacrificing WCAG 2.2 AA, VoiceOver labels, reduced motion, or iPhone readability.

## Status data contract
For each operation show: stable task ID, human-readable title, status (queued, running, verified, blocked, failed, complete), latest verified action, remaining work, next safe action, and evidence link or commit when available. Never fabricate percentages, elapsed times, live telemetry, completion, or tool outcomes. If progress is not measurable show a stage-based checklist, not a fake percent. Distinguish planned actions from executed actions.

## Rendering
Prefer a native interactive dashboard when available: summary counts, progress stages, task cards, expandable evidence, blockers, and accessible refresh/recheck action only when wired to a real operation. Otherwise provide a concise structured text dashboard. Use /4629 design tokens; no unnecessary animations, autoplay, flashing, or decorative progress spinners. Honor prefers-reduced-motion. Ensure 44x44px targets, high contrast, semantic headings, keyboard navigation, and responsive portrait layout.

## Execution integration
/disabled, /disability, P, and D should show the dashboard at useful checkpoints while continuing safe authorized operations without repeated confirmation. Never hold execution merely to render the dashboard. Report genuine tool limitations, approvals, and completion gates. A chat response is not a continuously updating monitor: background updates require a real connected scheduler or running application. Do not imply a live background worker without one.

## Acceptance
Every status is grounded in current tool output or explicitly labeled pending; all task counts reconcile; no blocked item is displayed as complete; dashboard remains usable with VoiceOver and reduced motion.
