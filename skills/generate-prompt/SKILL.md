---
name: generate-prompt
description: Emit PhD-level engineered prompts for every output type this agent can run, ranked by marketing and academic power, with customization keywords after the flag. Trigger on /generate, generate prompt, prompt pack, video prompt engineering, Aether Cinema prompts, gnitekram.org prompts, ranked output types, or when the user asks for beautiful futuristic awe-inspiring prompts including custom web apps, video, images, books, folios, decks, and sites.
---

# generate-prompt

## Quality and capability additions

Read [the task-specific quality profile](references/quality-profile.md) before execution. Use `evals/quality-cases.json` for regression scenarios; its assertions are acceptance criteria, not claims that tests have run. Shared path resolution and output rules live in `interop/SKILL.md`.


Read [the complete workflow](references/workflow.md) before applying this skill. Follow its steps for the current task.

## ChatGPT portability

Resolve `@skill-name/path` by matching the installed skill’s frontmatter name. Substitute the actual path before running a command. Use the current working directory for generated files. Apply shared rules only when the current task calls for them. User instructions and platform rules take priority. Check script prerequisites, and never claim results that were not produced.

## Delivery

Run the single delivery gate in `interop/SKILL.md` after task-specific validation. Preserve verified quotations and technical identifiers; report unresolved defects or blockers accurately.
