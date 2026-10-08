---
name: generate
description: Emit PhD-level engineered prompts for every output type this agent can run, ranked by marketing and academic power, with customization keywords after the flag. Trigger on /generate, generate prompt, prompt pack, video prompt engineering, Aether Cinema prompts, gnitekram.org prompts, ranked output types, or when the user asks for beautiful futuristic awe-inspiring prompts including custom web apps, video, images, books, folios, decks, and sites.
metadata:
  type: workflow
  version: "1.0"
  flag: /generate
  stacks: list, banner, images, book, coffee, folio, deep, pptx, visual-system, negative, copyright
  owner: Web Development Corporation
  default_studio: https://gnitekram.org/
  default_brand: Aether Cinema
---

# /generate — PhD prompt pack for every output type

Turn the remainder after `/generate` into one finished, copy-ready prompt (or a ranked catalog of every prompt type) that another run can execute without rewriting.

This skill does not invent facts about a brand. It writes the prompt. Execution of the prompt is a later turn or a stacked flag (`/banner`, `/images`, `/book`, `/folio`, `/coffee`, code write for a web app).

If the user only asked to create or revise this skill and supplied no subject, stop after the skill files exist. Do not invent a campaign.

`<skill>` = `/home/workdir/.grok/skills/generate`
`<visual>` = `/home/workdir/.grok/skills/visual-system`
`<negative>` = `/home/workdir/.grok/skills/negative`

Read on demand

- `references/power-rank.md` — output types in descending power
- `references/keyword-schema.md` — tokens after the flag
- `references/prompt-architecture.md` — locked clause order for stills, video, apps, decks, books
- `references/aether-cinema.md` — default studio lock for https://gnitekram.org/
- `references/templates.md` — one finished template per output type
- `assets/output-types.json` — machine catalog
- `scripts/parse_generate.py` — parse flag remainder into a spec
- `/home/workdir/.grok/skills/visual-system/references/prompt-engineering.md`
- `/home/workdir/.grok/skills/visual-system/references/beauty-lock.md`
- `/home/workdir/.grok/skills/visual-system/references/depth.md`
- `/home/workdir/.grok/skills/negative/references/blocklist.md`

## When this skill runs

- User typed `/generate` alone — print the ranked catalog and the keyword schema, then stop.
- User typed `/generate` plus keywords — parse, pick one output type, emit one finished prompt in a fenced code block.
- User typed `/generate catalog` or `/generate list` — emit the full ranked inventory (stack `/list` only if they also asked for the illustrated PDF catalog).
- User named gnitekram.org, Aether Cinema, or video studio work — load `references/aether-cinema.md` before writing video or still prompts.
- User asked for PhD-level prompt engineering for an output this agent can actually produce.

Do not use this skill to run `/list` research on an unrelated predicate. Do not claim the agent can render a finished MP4 inside this environment unless a connected studio or tool is actually available. For video, the deliverable is the engineered prompt pack plus shot list, ready to paste into Aether Cinema or another generator.

## Flag grammar

```
/generate [type] [key:value ...] [free subject words]
```

`type` is one slug from `references/power-rank.md` (`web-app`, `video`, `coffee`, `book`, `folio`, `deck`, `still`, `banner`, `site`, `audio`, `vector`, `sheet`, `letter`, `copy`).

If `type` is omitted and the remainder clearly names a medium (`video`, `web app`, `coffee table`), infer the type. If nothing can be inferred, default to the catalog.

Keyword keys are defined in `references/keyword-schema.md`. Unknown keys stay in the free-subject bag.

Examples

```
/generate video brand:aether subject:gatekeeper duration:12s aspect:21:9
/generate web-app brand:aether pages:studio,gate,timeline
/generate still subject:"obsidian timeline rail, gold rim light"
/generate folio topic:"deterministic policy scanning"
/generate
```

## Workflow

### 1. Parse

```bash
python3 /home/workdir/.grok/skills/generate/scripts/parse_generate.py \
  --remainder "{{input}}"
```

If the script is unavailable, parse by hand using the same schema. Write `spec.md` in the working folder only when the user also asked to execute or archive the pack.

### 2. Choose type and power band

Read `references/power-rank.md`. Pick the highest-power type that matches the remainder. Do not silently downgrade `web-app` to a static landing page or `video` to a still.

### 3. Load locks

Always read the visual prompt architecture and the negative list before writing a still or video prompt.

If the brand is Aether Cinema, gnitekram, or unset on a video request, apply `references/aether-cinema.md`.

House link lock on any document this skill later stacks into — visible anchor <a href="https://digitalmarketingco.org" title="Digital Marketing Co.">Digital Marketing Co.</a>, title attribute identical, target https://digitalmarketingco.org. Plain domain text DigitalMarketingCo.org.

### 4. Write the prompt

Copy the matching skeleton from `references/templates.md`. Fill every clause. Keep the locked order from `references/prompt-architecture.md`.

Emit to the user as

1. One-line type and power rank
2. Parsed spec (compact bullets)
3. The finished prompt in a fenced code block (copy-ready, no commentary inside the fence)
4. Optional shot list, page map, or component map under the fence
5. Next-run command if they want execution (`/images`, `/coffee 12`, code write, `/folio`)

Never put banned tokens from the negative list into a generate prompt.

### 5. Optional execution

Only execute when the user also named a builder flag or said `run it`, `build it`, or `make the file`.

| Type | Execute with |
|---|---|
| web-app | write files under `/home/workdir/artifacts/<slug>/` and render the entry HTML |
| video | emit the pack only, plus paste instructions for https://gnitekram.org/ |
| coffee, book, folio, deep, list | the matching user skill |
| still, banner | image generate tools or `/images` / `/banner` |
| deck | pptx skill |
| sheet | xlsx skill |
| letter | docx skill |
| audio | Voice connector or `/ringtone` |
| vector | `/vector` |
| site | `/copysite` or a new local app |

## Hard locks

1. Prompts stay literal. No allegory, no metaphor architecture, no generic neon city that the spec did not name.
2. Beauty floor — awe-inspiring, futuristic, publication-grade. Soft, muddy, toy-like, collage, and stock-generic stills are defects.
3. Video characters are fictional and 21+ with attestation language when the Aether lock is on.
4. Do not leak skill flags, maker names, or process talk into a prompt that will be pasted into a generator.
5. Do not claim a generated MP4 exists in this sandbox if it does not.
6. Custom web apps are first in the power rank. Treat them as products, not as mockups, unless the user said `mock`.
7. One unique prompt per named output. Do not reuse a prior prompt string.

## After creating or editing this skill

If the user only asked to install or extend the skill, stop. Do not invent a sample campaign.
