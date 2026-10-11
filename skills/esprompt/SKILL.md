---
name: esprompt
description: Create detailed Abacus.ai engineering prompts packaged as verified ZIP files for applications using Next.js, React, Prisma ORM, TypeScript, and Tailwind CSS. Trigger on /ESPrompt, /esprompt, $esprompt, or requests for an ESPrompt Abacus.ai implementation bundle.
---

# ESPrompt

Convert the project description following the invocation into a standalone engineering prompt for Abacus.ai. Interpret “above genius” and “above PhD” as precision, completeness, justified decisions, and observable acceptance evidence. Create the prompt bundle; execute the application only when separately requested.

## Workflow

1. Extract objectives, users, workflows, data, integrations, deployment target, constraints, and success criteria. Preserve explicit requirements. If no subject follows, produce a clearly labeled general-purpose production scaffold brief. Record reasonable assumptions; ask only when missing information prevents a useful deliverable.
2. Read `references/prompt-contract.md`. Adapt the contract to the actual scope without inventing business features.
3. Verify changing dependency compatibility and Abacus capabilities through official documentation when available. Record URLs and retrieval dates. If verification is unavailable, mark versions unresolved and instruct Abacus to verify them before installation. Never invent versions, APIs, services, prices, or capabilities.
4. Write `MASTER_PROMPT.md` directing Abacus to inspect, plan, install, implement, test, repair, and report observed results. Supply exact commands only when their compatibility is established; otherwise supply an explicit resolution procedure. Use one consistent package manager and stack throughout.
5. Write the supporting files below. Map every requirement to an acceptance check. Replace template blanks with concrete specifications or documented assumptions; reserve placeholders for genuine external inputs.
6. Package the files inside one `<project>-esprompt/` directory in a ZIP. Exclude secrets, caches, dependencies, unrelated files, and application builds. Include executable installation scripts only when requested and reviewed for safe, repeatable behavior.
7. Verify ZIP integrity, inventory, UTF-8 readability, cross-file consistency, absence of credentials, and SHA-256 checksums. Save using the available Library workflow and return the ZIP link. Report saving failures accurately.

## Required bundle

- `MASTER_PROMPT.md`: Standalone mission, architecture, implementation phases, repair loop, and definition of done.
- `INSTALLATION_PLAN.md`: Environment discovery, compatible dependency resolution, installation, database setup, build/start/deploy instructions, and rollback.
- `ACCEPTANCE_CHECKLIST.md`: Observable functional, database, security, accessibility, responsive design, and deployment checks with required evidence and blocked/not-run status handling.
- `.env.example`: Placeholder-only variables actually used by the proposed implementation, with server/public boundary comments.
- `README.md`: How to submit the prompt to Abacus, assumptions, required external inputs, and file inventory.
- `manifest.json`: Relative paths and SHA-256 checksums for every payload file except the manifest itself.

## Reporting discipline

Make the prompt usable without conversation history. Favor executable engineering requirements over superlatives. Never claim that generating the ZIP installs software or verifies deployment. Do not claim tests, migrations, public availability, or restart survival passed without execution evidence. Keep ordinary runtime functions free of paid language-model calls unless requested; distinguish Abacus development credits from operating costs.
