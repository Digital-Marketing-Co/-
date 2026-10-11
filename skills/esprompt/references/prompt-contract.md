# Abacus implementation contract

Adapt these requirements into the project-specific master prompt.

## Mission and discovery

State the product, workflows, measurable success criteria, constraints, existing repository if provided, and external blockers. Inspect repository instructions, manifests, lockfiles, schema, infrastructure, and current failures before edits. Preserve existing data and unrelated behavior. Map requirements to phases and acceptance checks.

## Compatible stack

Require Next.js App Router, React, strict TypeScript, Prisma ORM, and Tailwind CSS. Resolve mutually compatible supported stable versions at execution time against official documentation; never blindly upgrade existing apps. Verify Node support, React peer dependencies, Prisma generator/client/adapter configuration, and Tailwind setup. Preserve an existing package manager; prefer pnpm for new projects when supported. Pin the resolved toolchain, use one lockfile, and record versions and commands. Avoid mixing Tailwind major-version configuration conventions or forcing installs to bypass incompatibility.

## Architecture and data

Define routes, server/client boundaries, reusable components, domain services, API/server actions, validation, error contracts, schema, relations, and indexes appropriate to scope. Default new persistent production apps to PostgreSQL unless requirements or observed infrastructure dictate another compatible database. Never assume Abacus supplies SQL. Keep Prisma and secrets server-side; manage connections/pooling for the actual runtime. Enforce authorization on the server, validate writes, use transactions where needed, and prevent duplicate submissions. Commit migrations, test against a disposable database, and use deployment-safe migration commands. Require backups and a rollback plan before destructive changes. Make seeds repeatable; exclude fixed production credentials. Add durable background jobs only when needed.

## Futuristic Tailwind design

Create a coherent token system for colors, spacing, typography, surfaces, focus, elevation, and motion. Use restrained gradients, dimensional surfaces, crisp typography, and purposeful microinteractions. Target WCAG 2.2 AA: readable contrast, semantic HTML, keyboard operation, visible focus, accessible forms, reduced-motion behavior, usable touch targets, and responsive layouts. Include loading, empty, error, disabled, success, and offline states where relevant. Keep essential content independent of animation. Choose accessible compatible component libraries only when justified. Require working user flows rather than fake metrics or decorative placeholders.

## Security and efficiency

Validate environment configuration and separate public/server variables. Avoid logging secrets or personal data. Add authentication and role enforcement when required, input validation, appropriate rate limits, security headers, upload controls if needed, and CSRF protection suited to the auth mechanism. Use HTTPS in production. Improve queries, pagination, caching, server/client boundaries, images, fonts, and bundle size without exposing private data. Document tradeoffs. Avoid runtime language-model calls unless requested.

## Execution and repair

Direct Abacus through discovery, dependency resolution, scaffold/integration, schema/migrations, working vertical slice, design refinement, validation, and deployment. Maintain a redacted evidence log of commands, versions, changed files, results, and blockers. Run type checks, supported lint commands, production build, database integration checks, and meaningful full-workflow tests for primary workflows. Check unauthorized access, invalid input, duplicate submissions, failure recovery, keyboard use, narrow/wide layouts, and browser errors as applicable. Repair root causes and rerun affected checks. Never disable strictness, remove checks, fabricate results, or weaken security to claim success.

## Deployment and evidence

Discover whether the Abacus target is an agent workspace, managed deployment, or persistent VM/SuperComputer. Never assume Docker, sudo, SSH, systemd, storage, domains, public HTTPS, or reboot access. Use the observed supported mechanism. On a confirmed VM, configure an available process manager with environment loading, health checks, logging, startup, and restart policy. Verify a public URL and primary flows when deployment is authorized and possible. Test restart/reboot survival only when required and authorized; otherwise mark it not tested. Separate code complete, locally validated, deployed, and externally verified status. End with exact setup/start/deploy commands, versions, migration status, evidence, limitations, and external actions remaining.
