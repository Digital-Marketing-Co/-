# /pe Automatic Implementation Policy

## Default behavior
When /pe or the pe function generates an implementation prompt, immediately treat that prompt as an authorized implementation specification, not the final deliverable, unless the user explicitly asks for prompt-only, specification-only, or a non-executable artifact. Discover the actual repository, application, tools, and deployment state, then execute safe reversible steps using available access without repeatedly asking to proceed. Do not claim this policy changes ChatGPT system-level instructions or creates unattended background execution.

## Execution sequence
1. Resolve the target and inspect existing project instructions, canonical skills, code, branches, deployment, and source of truth.
2. Expand and reconcile the prompt with the real architecture; record evidence, requirements, and acceptance criteria. Never invent metrics, version numbers, or results.
3. Create an appropriately scoped development branch; preserve unrelated changes and production data.
4. Implement the smallest coherent changes, reuse existing components, and avoid paid runtime LLM inference where prohibited.
5. Run available deterministic build, type, lint, unit, integration, security, accessibility, responsive, and visual QA checks. Correct defects and repeat until two complete consecutive passes produce no new material defects, or disclose a genuine blocker.
6. Commit verified changes on a safe branch, prepare a PR or preview deployment when supported, and report commit hashes, URLs, evidence, and unresolved blockers. Never imply an unexecuted action succeeded.

## Safety and user experience
Use accessibility-first, iPhone-first, low-interaction workflow. /p, P, and Proceed continue authorized work. Ask before destructive data changes, irreversible security actions, production cutovers, or actions needing external consent. Never bypass authentication or expose credentials. An image-generation /pe invocation produces an image, not an invented software deployment. An explicit request for a prompt alone remains prompt-only.

## FWA v6.0.0 specific requirements
For DigitalMarketingCo.org/free-website-auditor, implement the full master specification: verify the authoritative 16-dimension manifest; derive metric and dimension totals from a versioned registry rather than hardcoding historical 495/521/540/587 values; distinguish catalog from executed metrics; protect Super Administrator guides with server-side authorization; enforce SSRF, redirect, download, and secret controls; align dashboard, API, documentation, and PDF outputs; retain historical audit reproducibility; target WCAG 2.2 AA; use zero paid inference at runtime; and require two evidence-backed clean QA passes before release. No web interface can guarantee prevention of screenshots or OCR; do not claim it can.

## Scope
This file is repository-level agent guidance. For cross-project reuse, include it in each target repository or its canonical skill loading mechanism. Personal ChatGPT preferences do not themselves modify external project settings.
