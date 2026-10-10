---
name: pepe
description: Expand a remainder into an above-PhD embed prompt, code a promptform 3D JavaScript widget that installs inside another web app, then run automatic QA and apply every fix. Use when the user types /pepe, asks for a drop-in promptform 3D web component, or wants prompt-then-code-then-QA for an embeddable panel.
---

# /pepe — prompt, code, QA, embed

## Quality and capability additions

Read [the task-specific quality profile](references/quality-profile.md) before execution. Use `evals/quality-cases.json` for regression scenarios; its assertions are acceptance criteria, not claims that tests have run. Shared path resolution and output rules live in `interop/SKILL.md`.


Take every word after `/pepe` as the product remainder. Expand it into a full implementation prompt, code a drop-in promptform 3D JavaScript widget that another web app can install, then run the QA checklist and apply every defect fix before delivery.

This skill writes the product. A prompt alone does not finish the job.

`<skill>` resolves with `interop/scripts/resolve_root.py pepe` (live host: `@pepe`).

Read on demand

- `references/prompt-contract.md` — expansion skeleton
- `references/embed-contract.md` — install API and isolation rules
- `references/qa-checklist.md` — checks and fail-closed fixes
- `references/visual-floor.md` — promptform, depth, motion
- `assets/mount-snippet.html` — host install sample

## When this skill runs

- User typed `/pepe` plus a remainder.
- User asked for a promptform panel, animated and 3D, to install inside another web application, and named this flag.
- User asked to prompt-engineer, code, and QA that embed in one pass.

`/pepe` alone with no remainder — print the flag grammar and the expansion headings, then stop. Do not invent a product.

## Flag grammar

```
/pepe [mode] [key:value ...] [remainder]
```

`mode` is optional. Allowed slugs — `prompt`, `code`, `qa`, `build`. Default is `build`.

- `prompt` — write the expansion only under artifacts. Do not code.
- `code` — code from an existing expansion, then still run QA.
- `qa` — run the checklist on an existing widget folder and apply fixes.
- `build` — expand, code, QA, fix, deliver.

Keyword keys

- `slug` — artifact folder stem (default `pepe-promptform`)
- `mount` — custom element name (default `pepe-promptform`)
- `host` — `shadow` (default) or `light`

Unknown keys stay inside the remainder.

## Workflow

### 1. Parse

Split the first token if it is a mode. Split `key:value` pairs. Keep the rest as the remainder. Never drop the user's nouns.

### 2. Expand

Read `references/prompt-contract.md`. Write `PROMPT.md` in the artifact folder. The expansion must name the job, the mount API, visual floor, states, motion, inclusive rules, and acceptance checks. Do not paste skill-process talk into the widget UI.

### 3. Code

Read `references/embed-contract.md` and `references/visual-floor.md`.

Write under the resolved artifacts directory (`/workspace/artifacts/<slug>/`):

- `pepe-promptform.js` — custom element, Shadow DOM, public `PepePromptform.mount` / `unmount`
- `pepe-promptform.css` — imported by the element; also loadable by a host that wants light DOM
- `index.html` — host page that installs the widget inside a foreign layout
- `PROMPT.md` — the expansion
- `README.md` — install steps and acceptance list

Isolation rules

- Default Shadow DOM so host CSS cannot break the panel and the panel cannot restyle the host.
- One custom element. No global element selector leakage.
- Public API is `customElements.define` plus `window.PepePromptform`.
- Honor `prefers-reduced-motion`.
- Keyboard path, visible focus, labels, 44 px hit targets.
- No remote font or script required for first paint.

### 4. QA and fix

Read `references/qa-checklist.md`. Run:

```bash
python3 @pepe/scripts/qa_pepe.py /workspace/artifacts/<slug>
```

Exit 1 means defects remain. Fix the widget, re-run, until the script prints PASS. Do not weaken a check to force a pass. Record the report in `QA.md`.

### 5. Negative

Sweep widget copy, alt text, README, and PROMPT before delivery. Skill flags may appear in SKILL.md only.

## Delivery

Run the single delivery gate in `interop/SKILL.md` after task-specific validation. Preserve verified quotations and technical identifiers; report unresolved defects or blockers accurately.
