---
name: spec
description: "Turn rough requests into testable engineering specifications or prompt bundles with interactive scope selection and requirement/visual QA. Use /spec for prompts, specifications or implementation briefs."
---

# Spec

Resolve the installed personal skill named `doc` and read its `references/output-contract.md` once per run. Read it as a reference; do not invoke doc or restart its intake.

## Interactive start

Show the proposed output plan and reuse prior choices. Ask at most two useful questions only for missing material context: Prompt/specification versus actual build, and target environment if missing. Honor explicit no-questions/bypass settings. Use the shared 4629 style phase for a new designed output, once across handoffs.

## Execution

Transform the supplied rough request into an actionable engineering specification or prompt without losing requirements. Resolve whether the requested result is a prompt, a specification, an installable bundle or executed implementation. State compatible architecture, data model, interfaces, edge cases, accessibility, security, runtime-cost constraints, acceptance criteria and verification evidence. Reuse the relevant installed prompt-engineering workflow. Preserve task-specific deployment and permission boundaries. Deliver the requested text/files; do not execute a proposed build solely because it appears inside the prompt.

## Specialist routing

Use prompt-engineer for prompt rewriting; pepe only when the embedded widget is requested; esprompt for an explicitly requested Abacus bundle. Do not turn a prompt rewrite into executing its quoted build.

## Required QA and visual QA

Trace each requirement to architecture, data/API/UI behavior, edge cases and measurable acceptance tests. Check conflicting versions, unavailable dependencies and cost constraints. Read the final text for ambiguity and inspect any rendered PDF/HTML. Plain-text prompts need structure/readability review, not invented screenshots or a claim that the proposed app was tested. Follow the shared repair and release gates. Never mark unexecuted checks passed.

Read [the endpoint quality profile](references/quality-profile.md) for requirements and tests.
