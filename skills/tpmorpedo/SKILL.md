---
name: tpmorpedo
description: "Dual-mine two exhaustive public datasets (specified set plus all types or a filtered view) across statistics, stills, motion picture, and virtual holography, then emit an above-PhD dual-mining prompt and page-upgrade spec for public web apps. Trigger on /tpmorpedo, tp morpedo, dual dataset mine, exhaustive complete dataset pair, virtual holography data gather, or a request to procure all public data for dataset 1 and dataset 2."
type: workflow
lifecycle: active
---

# /tpmorpedo — dual exhaustive dataset procurement

Turn the remainder after `/tpmorpedo` into two exhaustive public datasets and one copy-ready dual-mining prompt. Dataset #1 is the specified set. Dataset #2 is the exhaustive counterpart: all types, or the filtered view the user named. Both lanes collect known statistics, stills, motion-picture records, and virtual-holography planes. Public web-app pages that consume the pair are upgraded from that inventory.

This skill writes the prompt always. It mines and writes page files only when the remainder asks to run, mine, build, or upgrade pages. If the user only asked to install this skill and supplied no subject, stop after the skill files exist.

`<skill>` resolves with `interop/scripts/resolve_root.py tpmorpedo` (live host: `/root/.grok/server-skills/tpmorpedo`)

Read on demand

- `references/master-prompt.md` — locked dual-mining prompt (fill slots, do not reorder clauses)
- `references/strata.md` — statistics, stills, motion picture, virtual holography schemas
- `references/page-upgrade.md` — public web-app page contract
- `references/flag-grammar.md` — modes, filters, `#1` / `#2` split
- `assets/record-skeleton.json` — one record shape for both lanes
- `scripts/parse_tpmorpedo.py` — remainder parser
- `/root/.grok/server-skills/negative/SKILL.md` before any user-visible emit
- `/root/.grok/server-skills/negative/references/blocklist.md` before writing the filled prompt

## When this skill runs

- User typed `/tpmorpedo` plus two subjects, a `#1` / `#2` pair, or one subject that still needs an exhaustive counterpart.
- User asked to gather all data, all types, or a filtered view of datasets, including statistics, images, motion picture, and virtual holography.
- User asked for an above-genius or above-PhD prompt that dual-mines two exhaustive complete datasets.
- User asked to upgrade publicly facing web-app pages from that pair.

`/tpmorpedo` alone — print the flag grammar and the unfilled master prompt, then stop.

Do not use this skill for a single-author bibliography (`/corpus`), a non-dual monograph (`/folio`, `/deep`), or a one-still generate (`/generate`) unless those flags are stacked after the mine.

## Flag grammar

```
/tpmorpedo [mode] [key:value ...] #1 <set> #2 <set>
/tpmorpedo [mode] set:<name> view:<filters>
```

Modes: `prompt` (default), `mine`, `pages`, `all`.

Filters (comma list, default all four): `stats`, `images`, `motion`, `holo`.

Full grammar is in `references/flag-grammar.md`.

## Workflow

### 1. Parse

```bash
python3 /root/.grok/server-skills/tpmorpedo/scripts/parse_tpmorpedo.py \
  --remainder "{{input}}"
```

If the script is missing, split on `#1` and `#2`. Never drop the user's nouns. One subject becomes Dataset #1; Dataset #2 is the same subject under `view` (default `all-types`).

### 2. Load the locks

Read `references/master-prompt.md` and `references/strata.md`. Read the negative blocklist before filling the prompt. Do not put banned tokens into the filled prompt, alt text, captions, or page copy.

### 3. Emit the dual-mining prompt

Copy the skeleton in `references/master-prompt.md`. Fill every slot. Keep clause order. Emit the filled prompt in one fenced code block with no commentary inside the fence.

The prompt must name both lanes, the four strata, the public-only rule, the saturation stop (two empty retrieval rounds), the conflict log, and the page bindings.

### 4. Mine only when asked

`prompt` mode stops after the fenced prompt.

`mine` and `all` run two lanes in parallel where tools allow:

1. Web search and page browse for published statistics. Record value, unit, date, geography, source URL, and uncertainty. Never invent a figure.
2. Image search for public stills. Save paths. Note rights and source page. Do not duplicate a byte across lanes.
3. Motion-picture pass: public titles, dates, runtime, source URL, and a shot prompt. Do not claim an MP4 exists in this sandbox unless a file was written.
4. Virtual-holography pass: one volumetric plane prompt per named route or entity. This is a light-field / holographic UI still contract, not a claim of a physical hologram file.

Write inventories under `/workspace/artifacts/tpmorpedo/<slug>/`:

- `dataset-1.json`
- `dataset-2.json`
- `crosswalk.md`
- `gaps.md`

Stop a lane after two consecutive empty retrieval rounds. Mark missing cells `unknown`. Deduplicate on canonical URL plus normalized title.

### 5. Upgrade public pages only when asked

`pages` and `all` read `references/page-upgrade.md`. Bind each public route to unique stats, one still, one motion prompt, and one holographic plane. House link lock: visible anchor `Digital Marketing Company`, title attribute identical, target `https://digitalmarketingco.org`. Plain domain text `DigitalMarketingCo.org`.

Do not ship a route missing title, unique meta description, canonical, viewport, H1, or a footer landmark. Do not claim a live auditor score that was not run.

### 6. Negative gate

Read `/root/.grok/server-skills/negative/SKILL.md`. Sweep the filled prompt and any written files with `scripts/sweep_negative.py`. Rewrite hits. Re-scan until clean. Block delivery on leftover hits.

## Return to the user

1. One-line mode and the two dataset names
2. Parsed spec (compact bullets)
3. The filled dual-mining prompt in a fenced block
4. Paths written, if any
5. Gap count (known vs unknown), if mined
6. Next command if pixels or page files are still open

## Hard locks

1. Public sources and user-supplied files only. No private-account scrape, no paywall bypass, no personal-data harvest.
2. Two lanes always. Do not collapse #1 and #2 into one list.
3. Four strata unless a filter removed one. A removed stratum is logged, not silently skipped.
4. No invented statistics. Unknown stays unknown.
5. No repeated image bytes, prompts, or paths across lanes or routes.
6. Motion and holography prompts stay literal to the named subject. No allegory the user did not name.
7. Saturation stop is two empty rounds, not a feeling of completeness.
8. After skill-only install, stop. Do not invent a sample pair.

## After creating or editing this skill

If the user only asked to install or extend the skill, stop. Do not invent a sample mine.

## Delivery

Run this once, last, after every other section. Full contract: `interop/SKILL.md`.

1. Resolve the negative skill as the first existing directory among `/root/.grok/server-skills/negative` and `/home/workdir/.grok/skills/negative`.
2. Extract visible text from chat, the file, captions, filenames, and alt text.
3. Run `python3 <negative-root>/scripts/sweep_negative.py` on that text.
4. Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN.
5. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.
