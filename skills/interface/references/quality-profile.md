# Interface dashboard quality profile

## Purpose and evidence contract

The /interface skill presents verified progress for an already authorized workflow. Every operation must have a stable task ID, clear title, allowed status (queued, running, verified, blocked, failed, complete), last evidenced action, remaining work, next safe action, and an evidence reference when available. Reconcile summary counts against individual task records. Never invent percentages, timestamps, live updates, tool results, or completion. Use stage-based progress when no measured denominator exists.

## Accessibility and rendering

Use readable, responsive, iPhone-first layout with semantic headings, keyboard and VoiceOver support, 44-by-44-pixel minimum touch targets, visible focus, high contrast, and reduced-motion support. /4629 visual depth, midnight navy, and cyan accents are optional presentation details subordinate to WCAG 2.2 AA and legibility. Do not use flashing, autoplay, decorative spinners, or inert refresh controls. Fall back to concise structured text when an actual interactive dashboard is unavailable.

## Authorization and operational safety

Keep planned, running, blocked, verified, and completed actions distinct. Do not interrupt safe authorized operations to render a dashboard, bypass approvals, or claim a chat response is a continuously updating monitor. Refresh or recheck actions must invoke a real supported operation; otherwise omit them. Report missing permissions, evidence, credentials, and execution limits explicitly.

## Acceptance and QA

Run representative, boundary, and presentation scenarios from `evals/quality-cases.json`. Verify status provenance, summary reconciliation, blockers, keyboard access, touch-target size, reduced motion, and mobile overflow where runnable. Record PASS, FAIL, BLOCKED, or NOT TESTED with supporting artifacts. Structural validation alone does not establish real-device accessibility or live integration success.
