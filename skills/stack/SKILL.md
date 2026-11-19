---
name: stack
description: Resolve the current compatible Next.js stack and architecture for a target application, or refresh its version and file-convention inventory.
---

# /stack

Use /stack <app or repo> for a project stack and /stack update <app or repo> for a refresh and a reviewable upgrade. When no target is supplied, work from the active project or produce the reference inventory with project versions marked unknown. Use this for Quantum Global Radio and Universal File Viewer when they move into Next.js.

## Resolve the stack

1. Inspect the requested branch and commit, workspace manifests, lockfile, package manager, Node version, Next configuration, structure, CI and hosting constraints. If a previous /stack definition exists, compare its history against known trusted revisions and preserve evidence before changing it. Report observed changes and verified provenance. Treat missing files, unexpected commits and compromise as distinct findings.
2. For each installed component record package, declared range, locked version, latest upstream stable version, latest supported compatible patch, release channel, peer constraints, source URL, retrieval time, and rollout decision. Cover Next.js, React/React DOM, Node, package manager, TypeScript, linting and build tools, test tools, and all direct dependencies. Track security advisories and relevant transitive lockfile changes. If data is unavailable, retain the last verified value with its date and mark it stale.
3. Use official Next.js project-structure and file-convention references, release notes, support policy, official package metadata, and hosting documentation. Select a compatible supported baseline. Treat stable, LTS/security patches, and canary as separate channels.
4. Map installed and optional architecture layers. Classify project conventions as present, applicable, optional, unsupported on the target, or deprecated. Add documentation references and validate against the project's actual framework version.

## Architecture and file-convention inventory

- App Router UI: layouts, pages, templates, loading, errors, not-found, supported auth boundaries, parallel and intercepting routes, dynamic/catch-all routes, route groups and private folders.
- Pages Router: pages, layouts via application entry points, API routes, data fetching and coexistence or migration constraints.
- Behavior: static and dynamic rendering, revalidation, caching, streaming/Suspense, Server and Client Components, route handlers, Server Actions, proxy/middleware as appropriate to the installed version, instrumentation, deployment runtimes, and static export constraints.
- MVC mapping where it helps: model/domain and persistence modules, views as UI components, controllers as thin handlers or actions, and service functions for shared behavior. Include BFF, static/content and SPA-oriented variants with compatibility and deployment notes.
- Source and build: .ts, .tsx, .js, .jsx, .mjs, .cjs, .mts, .cts, .mdx, styles and modules, assets, fonts, configuration, lockfiles and workspace files. For each convention specify exact accepted extensions in that version, including configured pageExtensions or MDX support where relevant.
- Metadata, localization, data and tests: icons, manifests, OG/Twitter images, robots, sitemap, dictionaries, translation assets, schema/migrations, fixtures, unit/E2E tooling, accessibility tests and release pipelines. Separate framework conventions from ecosystem/project formats and Universal File Viewer document extensions.
- Integrations: database, authentication, storage, streaming/media, analytics and hosting only when applicable. Preserve zero paid inference credits and label browser, simulator and real-device verification separately.

## Daily refresh and upgrade

Fetch source evidence daily, compare to the last verified inventory, and report deltas by element. Identify urgent compatible patches, migrations, blocking peer dependencies, changed conventions and upstream sources. For an authorized target, stage compatible updates on a dedicated branch and refresh the lockfile with the project's own package manager. Run frozen install, type-check, lint, build, targeted tests and a primary workflow smoke check. Review dependency provenance, package scripts and unexpected configuration changes before installing unfamiliar dependencies. Preserve the last good deploy and report rollback steps, the branch/revision, exact checks run and any gaps. Release eligibility requires demonstrated compatibility and the project's normal release gates.
