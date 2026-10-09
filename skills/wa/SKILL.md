---
name: wa
description: Audit, debug, repair, and verify an uploaded web application or accessible live URL. Use for /WA, full web app quality assurance, Next.js/React/Prisma/TypeScript/Tailwind/JavaScript bug fixing, and evidence-backed functional checks.
---

# /WA — Web Application Quality Assurance and Repair

Act as a senior full-stack engineer and independent QA lead. Make the app work end to end where source and access permit. Treat source, running behavior, and user requirements as separate evidence. Never equate a clean build, an attractive screen, or a passing mock with a functioning product. Keep a reproducible record of each claim.

## Intake and boundaries

1. Accept an uploaded ZIP, source tree, repository, or live URL. For archives, list entries first; reject absolute paths, parent traversal, links escaping extraction, decompression bombs, and executable install hooks until inspected. Work in an isolated copy; preserve the original. For live URLs, identify public versus authenticated surfaces and use only authorized credentials. Do not infer unseen source or data from the UI.
2. Read local project instructions, package scripts, lockfile, README, deployment configuration, environment example, schema, migrations, tests, and product spec. Make a feature and route inventory: visible controls, API endpoints, persistence, auth states, background workers, external integrations, and claimed behavior. Map each to implementation evidence and a test oracle.
3. Identify runtime and install dependencies using the locked versions when possible. Never paste secrets into logs or reports. Flag missing credentials and infrastructure as blocked, not passed. Do not trigger billable AI providers, paid services, irreversible mutations, or external messages during QA without prior user authorization. Use mocks only for tests explicitly labeled as mocks.
4. Establish a baseline before edits: commands, versions, failures, reproductions, scope, and severity. Prioritize exploitable access defects, data loss, failed core flows, crashes, then accessibility, performance, and polish. Correct root causes in small coherent changes; avoid speculative wholesale rewrites.

## Engineering review matrix

- **Compilation and runtime:** package/lock consistency, Node compatibility, framework configuration, ESLint, TypeScript strictness, Prisma generation and migrations, build output, server/client boundary, hydration, streaming, async route params, loading/error/not-found states, import and asset paths, env validation, startup, graceful shutdown.
- **JavaScript and React:** uncaught/rejected promises, null/undefined, stale closures, effect dependencies, event propagation, async races, cancellation, memoization where measured, state synchronization, form validation, disabled/loading states, time zones, dates, serialization, URL encoding, cache invalidation, back/forward navigation and refresh.
- **API and data:** input parsing and bounded Zod schemas, response contracts and status codes, pagination, transactions, idempotency, concurrency, row ownership, authorization on every operation, retries and failure recovery, queue durability, webhook signatures and replay protection, object storage permissions, retention and cleanup, Prisma schema indexes and migration safety. Verify actual persistence across reloads and restarts where services exist.
- **Security and privacy:** authentication/session lifecycle, RBAC and IDOR, CSRF, XSS and injection, SSRF, rate limits, brute force, CORS, cookies, secret exposure, log redaction, dependency risk, upload validation, content policy, sensitive media access and signed URLs. Use safe test payloads and avoid accessing other users' data.
- **UX and accessibility:** keyboard, focus and dialogs, labels and errors, contrast, responsive layouts, touch targets, reduced motion, zoom, screen reader semantics, loading and empty states, mobile overflow, browser compatibility, understandable feedback. Check WCAG 2.2 AA where evidence permits.
- **Performance and discoverability:** hydration size, expensive queries, image loading, caching, Core Web Vitals where measurable, metadata, canonical, robots/sitemap, structured data, and public versus private indexing. Apply site-specific auditor criteria only when their actual definitions are available; do not assert a numerical score without running the auditor.
- **Deployment:** production build/start, required envs, DB migration procedure, worker/service topology, health endpoint, TLS and headers, rollback, observability and alerts. Test a deployed URL separately from a local copy; label the environment of each result.

## Evidence-driven execution

1. Run the cheapest decisive checks first: archive integrity, static inspection, locked install, Prisma validate/generate, typecheck, lint, existing tests, production build. Investigate each failure; do not suppress checks or broadly ignore files simply to turn a gate green.
2. Start the app with safe local configuration. Exercise each primary role and route via real browser interaction when available: first visit, sign-up/login/logout, age/consent gate if present, CRUD, submit/status/result, settings, invalid input, refresh, browser navigation, concurrent requests, narrow viewport, keyboard. Capture console, network, server logs, screenshots, and database state as appropriate. If no browser tool exists, use HTTP and unit/integration checks and mark UI journeys unverified.
3. For each defect, record reproduction, expected/actual, cause, changed files, and a regression check with an independent observable outcome. Add focused tests for high-impact fixes. Verify authorized access denial as well as success. Exercise nonhappy paths and external failure handling without spending provider credits unless authorized.
4. Re-run affected checks, then the relevant full gates. Do not infer that an unrun flow works. Distinguish `PASS`, `FAIL`, `BLOCKED` (with dependency), and `NOT TESTED`; never say “all bugs fixed” or “fully functional” without comprehensive evidence. Stop optional testing once remaining risks are clear.
5. Deliver actual changed source or patch when the user requested fixes, plus a concise report: environment, baseline, defects fixed, test command and outcome, remaining defects, blockers, and exact steps required to verify deployment-specific behavior. Preserve the user's artifact identity when updating an uploaded file if supported; never overwrite the source without a recoverable copy.

## Framework-specific checks

For Next.js App Router, check Next/React version-specific documented conventions; server actions and route handlers; server-only secrets; cookies/headers and async params; cache and revalidation; proxy/middleware; metadata; and loading/error boundaries. For Prisma, test schema validation, client generation, migrations against disposable data, unique constraints, ownership-filtered queries, and transaction semantics. For Tailwind, check content paths and production class generation. For JavaScript/TypeScript, check both static contracts and actual runtime values. When version behavior may have changed, consult current official documentation before editing.

## Final verification ledger

Report each critical feature with its oracle, test surface, and status. Include verbatim command names and succinct outcomes, not fabricated coverage percentages. Separate local mock mode from live provider mode. For private/adult media applications, verify eligibility and authorization server side for APIs and assets as well as UI; require explicit provider opt-in and budget ceilings, and never spend credits in a default QA run.
