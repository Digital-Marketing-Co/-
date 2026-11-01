# Execution environment contract

## Parsing and mode

Treat `-geo` as an execution-environment selector. Accept a single token or a quoted multiword value in the option prefix, before the task remainder. Preserve literal flag text inside the remainder. Keep explicit modes; select prompt mode when a selector is present without a mode. Reject missing, empty, repeated, or unclosed values without consuming task text as an inferred environment.

Examples:

- `/pepe -geo "Abacus.AI Next.js Agent" "Repair all application workflows"`: prompt mode, the quoted environment, and the quoted task.
- `/pepe prompt -geo Abacus.AI Repair Next.js forms`: prompt mode, Abacus.AI environment, remainder `Repair Next.js forms`.
- `/pepe build -geo "Browser JavaScript" a billing widget`: build mode; retain embed requirements.
- `/pepe prompt Explain the literal string -geo`: no environment selector; keep the literal string.

## External application prompt

Write one reusable prompt directed to the selected environment. Include role and objective, repository discovery, existing stack, prioritized implementation, data and permission boundaries, design requirements, validation, deployment constraints, and evidence-based deliverables. Preserve every requirement from the active conversation. Do not replace an application repair request with an unrelated widget.

Make the target environment explicit in the title and opening instruction. Distinguish writing a prompt from executing it. A selector never grants account access, credentials, paid services, or deployment authority.

For Abacus.AI and Next.js, direct the Abacus agent to work in its current project, inspect the actual Next.js routing model, React, TypeScript, styling, database, package manager, and available hosting/runtime resources. Preserve compatible installed versions; verify version-sensitive behavior from official documentation. Use server-side boundaries for secrets and authorization. Choose durable storage and background processing from resources actually available in that project. Do not assume a VM, Vercel, PostgreSQL, provider credential, or service exists solely from the selector.

Keep deterministic validation separate from AI suggestions. Require actual commands and observed results before claims of repairs, publication, API conformance, or deployment. Report unavailable resources as blockers.

## Acceptance

Check quoted and unquoted values, explicit-mode precedence, unchanged task text, missing values, repeated selectors, and backward-compatible invocations. For prompt-only tasks verify that the prompt names its environment and preserves task scope, and that no application build or paid inference is initiated.
