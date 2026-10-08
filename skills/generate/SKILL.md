---
name: generate
description: Emit PhD-level engineered prompts for every output type this agent can run, ranked by marketing and academic power, with customization keywords after the flag. Trigger on /generate, generate prompt, prompt pack, video prompt engineering, Aether Cinema prompts, gnitekram.org prompts, ranked output types, or when the user asks for beautiful futuristic awe-inspiring prompts including custom web apps, video, images, books, folios, decks, and sites.
metadata:
  type: workflow
  version: "3.0"
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

`<skill>` resolves with `interop/scripts/resolve_root.py generate` (live host: `/root/.grok/server-skills/generate`)
`<visual>` = `/root/.grok/server-skills/visual-system`
`<negative>` = `/root/.grok/server-skills/negative`

Read on demand

- `references/power-rank.md` — output types in descending power
- `references/keyword-schema.md` — tokens after the flag
- `references/prompt-architecture.md` — locked clause order for stills, video, apps, decks, books
- `references/aether-cinema.md` — default studio lock for https://gnitekram.org/
- `references/templates.md` — one finished template per output type
- `assets/output-types.json` — machine catalog
- `scripts/parse_generate.py` — parse flag remainder into a spec
- `/root/.grok/server-skills/visual-system/references/prompt-engineering.md`
- `/root/.grok/server-skills/visual-system/references/beauty-lock.md`
- `/root/.grok/server-skills/visual-system/references/depth.md`
- `/root/.grok/server-skills/negative/references/blocklist.md`

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
python3 /root/.grok/server-skills/generate/scripts/parse_generate.py \
  --remainder "{{input}}"
```

If the script is unavailable, parse by hand using the same schema. Write `spec.md` in the working folder only when the user also asked to execute or archive the pack.

### 2. Choose type and power band

Read `references/power-rank.md`. Pick the highest-power type that matches the remainder. Do not silently downgrade `web-app` to a static landing page or `video` to a still.

### 3. Load locks

Always read the visual prompt architecture and the negative list before writing a still or video prompt.

If the brand is Aether Cinema, gnitekram, or unset on a video request, apply `references/aether-cinema.md`.

House link lock on any document this skill later stacks into — visible anchor Digital Marketing Company, title attribute identical, target https://digitalmarketingco.org. Plain domain text DigitalMarketingCo.org.

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
| web-app | write files under `/workspace/artifacts/<slug>/` and render the entry HTML |
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

## Publication bar

This skill emits a file a reader will open. Fail closed on the checklist in `interop/references/publication-bar.md`.

1. Resolve paths with `interop/scripts/resolve_root.py` and `interop/scripts/resolve_artifacts.py`. On this host the skill tree is `/root/.grok/server-skills` and deliverables go to `/workspace/artifacts`. Fall back to `/home/workdir/.grok/skills` and `/home/workdir/artifacts` only if those directories exist.
2. Covers, rules, table headers, and figure frames take the visual-system palette and volumetric depth. Body face and point size stay locked.
3. Banners are 16:9, full-bleed, unique per section, opaque at the left and right trim, with a real alpha ramp on the top and bottom only.
4. Plates are literal and context-locked. No repeated bytes, paths, prompts, or perceptual hashes. Reject soft, muddy, toy-like, or clip-art stills and regenerate.
5. Equations are compiled plates or supported Unicode. No raw TeX, no missing-glyph boxes, no tofu.
6. One copyright notice per page, centered in the footer. Owner is Web Development Corporation unless the user names another. Start year 2012 unless the user names another.
7. Visible link text is Digital Marketing Company. The title attribute matches. Plain domain text is DigitalMarketingCo.org. Do not nest an anchor inside an instruction sentence.
8. Headings keep with the next paragraph. Orphan headings move to the next page.
9. Open the finished file and confirm the house link, the footer, and clean glyphs before delivery.

## Delivery

Run this once, last, after every other section. Full contract: `interop/SKILL.md`.

1. Resolve the negative skill as the first existing directory among `/root/.grok/server-skills/negative` and `/home/workdir/.grok/skills/negative`.
2. Extract visible text from chat, the file, captions, filenames, and alt text.
3. Run `python3 <negative-root>/scripts/sweep_negative.py` on that text.
4. Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN.
5. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.
