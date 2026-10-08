---
name: prompt-engineer
description: Expand the text after /PromptEngineer into an Above-Genius PhD implementation of that pseudoprompt, then build it with holographic 3D glass gradient animated Tailwind, OG and Twitter cards, and the 521 auditor metrics. Trigger on /PromptEngineer, /prompt-engineer, PromptEngineer, PhD implementation of this prompt, expand this pseudoprompt, mega menu apps nav, Greg 521, or 521 metrics of the free website auditor.
metadata:
  type: workflow
  version: "3.0"
  flag: /PromptEngineer
  stacks: generate, visual-system, negative, images, banner
  owner: Web Development Corporation
  auditor: https://digitalmarketingco.org/free-website-auditor
  brand_link: https://digitalmarketingco.org
---

# /PromptEngineer — pseudo to PhD implementation

Take every word after the flag as a **pseudoprompt**. Do not treat it as finished copy. Expand it into an Above-Genius PhD product spec, then implement that spec in working files.

This skill is not `/generate`. `/generate` writes a prompt for a later run. This skill writes the spec **and** the product.

If the user only asked to create or revise this skill and supplied no separate product remainder, stop after the skill files exist. Do not invent a campaign.

`<skill>` resolves with `interop/scripts/resolve_root.py prompt-engineer` (live host: `/root/.grok/server-skills/prompt-engineer`)
`<visual>` = `/root/.grok/server-skills/visual-system`
`<negative>` = `/root/.grok/server-skills/negative`
`<generate>` = `/root/.grok/server-skills/generate`

Read on demand

- `references/expansion-protocol.md` — how a loose sentence becomes a complete build
- `references/design-lock.md` — holographic, 3D, glass, amorphic, gradient, transparency
- `references/tailwind-motion.md` — motion catalog that must appear in CSS
- `references/metrics-521.md` — the 521 auditor checks the page must pass
- `references/og-social.md` — AI stills, Open Graph, Twitter cards per route
- `references/ia-sync.md` — `/apps` order, nav Apps item, footer accordion, 404 inventory
- `references/exemplar-mega-menu.md` — locked quality floor from the founding example
- `assets/expansion-skeleton.md` — spec template
- `assets/metrics-521.json` — machine checklist
- `scripts/parse_prompt_engineer.py` — remainder parser
- `/root/.grok/server-skills/visual-system/references/beauty-lock.md`
- `/root/.grok/server-skills/negative/references/blocklist.md`

## When this skill runs

- User typed `/PromptEngineer` or `/prompt-engineer` plus a remainder.
- User asked for a PhD implementation of a pasted UI or product sentence.
- User named Greg 521, 521 metrics, or the free website auditor as the pass bar for a page being built.
- User asked for a mega menu, Apps nav, 404 app list, or footer accordion of apps in `/apps` order.

`/PromptEngineer` alone with no remainder — print the flag grammar, the expansion skeleton headings, and the twelve auditor dimensions, then stop.

## Flag grammar

```
/PromptEngineer [mode] [key:value ...] [pseudoprompt]
```

`mode` is optional. Allowed slugs — `spec`, `build`, `audit`, `nav`. Default is `build`.

- `spec` — expand only. Emit the PhD spec in a fenced block. Do not write app files.
- `build` — expand, then write the product under `/workspace/artifacts/<slug>/`.
- `audit` — score an existing local page or URL against `references/metrics-521.md`.
- `nav` — treat the remainder as an Apps-suite change. Force `references/ia-sync.md`.

Keyword keys

- `slug` — folder and route stem
- `stack` — `next`, `html`, `react` (default `html` unless the remainder names Next.js)
- `apps` — comma list when `/apps` cannot be fetched
- `brand` — default Digital Marketing Company
- `auditor` — default https://digitalmarketingco.org/free-website-auditor

Unknown keys stay inside the pseudoprompt bag.

Examples

```
/PromptEngineer Make a beautiful and futuristic mega menu drop down for all apps
/PromptEngineer spec glass pricing table with holographic tiers
/PromptEngineer build slug:apps stack:html mega menu in /apps order
/PromptEngineer audit https://digitalmarketingco.org/apps
```

## Workflow

### 1. Parse

```bash
python3 /root/.grok/server-skills/prompt-engineer/scripts/parse_prompt_engineer.py \
  --remainder "{{input}}"
```

If the script is missing, split on the first mode slug or key:value, keep the rest as the pseudoprompt. Never drop the user's nouns.

### 2. Expand the pseudoprompt

Read `references/expansion-protocol.md` and `assets/expansion-skeleton.md`.

The expansion must add, without being asked again

1. Product one-liner and job-to-be-done
2. Information architecture and route map
3. Visual system — glass, amorphic form, volumetric depth, gradient, transparency, 3D / holographic planes
4. Tailwind motion — pick from `references/tailwind-motion.md`, never a single `transition-colors`
5. Component inventory with empty, loading, error, and reduced-motion states
6. Image plan — unique AI still, OG image, and Twitter card per route (`references/og-social.md`)
7. Inclusive design — keyboard, screen reader, hit targets, contrast, `prefers-reduced-motion`
8. 521-metric mandate — every HTML route must be built to pass `references/metrics-521.md`
9. House link lock — visible anchor Digital Marketing Company, matching title attribute, target https://digitalmarketingco.org. Plain domain text DigitalMarketingCo.org
10. Acceptance checks

The founding quality floor is `references/exemplar-mega-menu.md`. New work must meet or exceed that density. Do not paste the exemplar when the remainder is a different product.

### 3. Design lock

Read `references/design-lock.md` and `references/tailwind-motion.md` before writing markup.

Hard visual floor

- Futuristic, publication-grade, three-dimensional
- Glass and frost over a real gradient field
- Amorphic panels (not only axis-aligned cards)
- Transparency with readable type (WCAG AA body)
- Holographic edge light and layered planes, not a neon-city metaphor the spec did not name
- Animated Tailwind that still works at 320 px, 768 px, and 1440 px
- No baked checkerboard in PNG RGB when alpha is required

### 4. Auditor lock

Every page this skill writes is scored against the twelve dimensions on https://digitalmarketingco.org/free-website-auditor and the 521 checks in `references/metrics-521.md`.

Dimensions — SEO, Performance, Mobile, Security, Accessibility, AI Readiness, AIO, GEO, AEO, Local SEO, Schema.org, WCAG.

Do not ship a route that is missing title, unique meta description, canonical, robots, language, viewport, charset, OG tags, Twitter card, JSON-LD, H1, skip link, or a footer landmark.

### 5. Apps-suite lock

When the remainder names apps, mega menu, navigation, footer accordion, or 404 inventory, read `references/ia-sync.md`.

- Fetch live `/apps` order when the network can reach https://digitalmarketingco.org/apps
- One source-of-truth array. Nav mega menu, `/apps` grid, footer accordion, and 404 list consume that array in the same order
- Every app card gets its own still, OG, and Twitter image
- Do not invent a second sort

### 6. Implement

`spec` mode stops after the fenced spec.

`build` and default modes write files under `/workspace/artifacts/<slug>/`.

Minimum file set for an HTML product

- `index.html` (or the named routes)
- `styles.css` or a Tailwind entry that the page actually loads
- `app.js` when interaction is required
- `data/apps.json` when an Apps suite is in scope
- `public/og/` and `public/twitter/` with one image plan file per route
- `README.md` with the acceptance checklist

Use Tailwind via CDN only when a local build toolchain is not available. Prefer a real Tailwind config when the stack is Next.js.

Generate route stills with the image tools when the user also wants pixels in this turn. Otherwise write the prompt and path contract from `references/og-social.md` and leave a manifest the next `/images` run can fill.

### 7. Negative and house gates

Read `/root/.grok/server-skills/negative/SKILL.md` before delivery. Sweep visible copy, alt text, captions, and filenames.

Do not leak skill flags, maker names, or process talk into user-facing UI copy.

### 8. Show the work

Return to the user

1. One-line product and mode
2. Parsed remainder (compact bullets)
3. The PhD spec in a fenced block when they asked for spec or when the build is large
4. Paths written
5. Auditor self-score against the twelve dimensions (honest gaps, not a fake 100)
6. Next command if pixels or a live `/apps` scrape are still open

Render local HTML with the file render component when a preview file exists.

## Hard locks

1. The remainder is the product. Do not swap it for a different app.
2. Beauty floor — awe-inspiring, futuristic, glass-volumetric. Soft, muddy, toy-like, Bootstrap-default, and stock-generic admin chrome are defects.
3. Motion floor — at least three coordinated Tailwind animations from `references/tailwind-motion.md` on any primary nav or hero. Honor `prefers-reduced-motion`.
4. Metric floor — build to the 521 checks. Do not claim a live auditor score you did not run.
5. Inclusive floor — keyboard path, visible focus, labels, contrast, touch targets, reduced motion, semantic landmarks.
6. Image floor — unique still + OG + Twitter per route. No reused bytes across routes.
7. Order floor — Apps lists stay in `/apps` order everywhere.
8. Link floor — Digital Marketing Company / DigitalMarketingCo.org lock above.
9. After skill-only install — stop. Do not invent a mega menu unless the remainder asked for one.

## After creating or editing this skill

If the user only asked to install or extend the skill, stop. Do not invent a sample site.

## Delivery

Run this once, last, after every other section. Full contract: `interop/SKILL.md`.

1. Resolve the negative skill as the first existing directory among `/root/.grok/server-skills/negative` and `/home/workdir/.grok/skills/negative`.
2. Extract visible text from chat, the file, captions, filenames, and alt text.
3. Run `python3 <negative-root>/scripts/sweep_negative.py` on that text.
4. Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN.
5. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.
