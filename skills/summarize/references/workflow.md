

# /summarize


## Visual stack

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Take one source and walk it through a locked scale. The default walk is summarize, then rewrite, then humanize (levels 2 then 3 then 4). The output must keep every proper name, date, measurement, path, URL, and house rule that the source actually contains.

`<skill>` = `@summarize`

Read on demand

- `references/scale.md` — the 0-5 scale, tells, and bans
- `references/handoff.md` — how this skill talks to /deep, /folio, and /banner
- `references/humanize.md` — voice rules that stop stock LLM cadence

Work in `./artifacts/summarize-<slug>/` when the pass is more than a short chat reply.

If the user only asked to create or revise this skill and supplied no source, stop after the skill files exist. Do not invent a source.

## When this runs

- User typed `/summarize`
- User asked to summarize, rewrite, humanize, destock, or make this sound like a person
- User stacked `/summarize` with `/deep`, `/folio`, and/or `/banner`
- User pointed at a skill file, a PDF, a URL, a prior folio, or pasted text

If there is no source, stop and ask for it.

## Source lock

Copy the source into `source.md` or `source.txt` before touching it. Do not edit the lock file.

Acceptable sources

- pasted text
- a URL (clip the article first with article-clip-pdf extract, then summarize the article body)
- a project skill path (`deep/SKILL.md`, `folio/SKILL.md`, `banner/SKILL.md`)
- a prior `deep.json`, `folio.json`, or finished PDF text extract
- the current user prompt when they say "this prompt"

Never treat a skill rewrite as a license to change locked type sizes, fade inches, owner strings, OpenAction field names, or filename patterns.

## The scale

Full definitions live in `references/scale.md`. Use these names in chat and in `pass.json`.

- 0 Verbatim — return the source. No compression.
- 1 Compress — cut filler. Keep original sentences where they already work.
- 2 Summarize — keep the argument, drop the tour. Facts stay.
- 3 Rewrite — new sentences, same claims. Clean syntax. Still institutional.
- 4 Humanize — spoken cadence. Concrete verbs. No fake warmth. No invented color.
- 5 Teach — humanize plus why it matters, still inside the source's facts.

Default when the user types `/summarize` with no level — run 2, then 3, then 4, and deliver the level-4 text with a short level-2 abstract on top.

If they name a single verb, map it.

- summarize → 2
- rewrite → 3
- humanize → 4
- rewrite then humanize → 3 then 4
- teach / explain like a person → 5

## Workflow

### 1. Scope

Write `scope.md`

- source kind and path
- requested level or the default 2-3-4 walk
- keep list (names, numbers, paths, flags, owner lines)
- drop list (ads, chrome, repeated throat-clearing)
- stacked skills, if any (`/deep`, `/folio`, `/banner`)

### 2. Passes

Write `passes/L2.md`, `passes/L3.md`, `passes/L4.md` as needed. Each pass reads only the previous pass plus the source lock. A later pass may not add a fact the source lock does not contain.

Record the walk in `pass.json` with keys source, walk, kept, dropped, handoff.

### 3. Voice check

Read `references/humanize.md`. Reject the draft and rerun level 4 if any of these appear

- In today's rapidly evolving landscape
- It is important to note that
- delve, tapestry, underscore, leverage, robust, seamless, cutting-edge used as decoration
- a claim the source lock does not support
- a locked house number that drifted (22 pt, 18 pt, 4.35 in, 2012, WCACopyrightYear)

### 4. Optional handoff

If the user also typed `/folio` or `/deep`, follow `references/handoff.md`. The humanized text becomes the working abstract and section prose. It does not become a license to skip research or to invent notes.

If they also typed `/banner`, banners still come from section claims after the draft exists. Do not generate figures from the summary alone.

### 5. Deliver

Give the user the final level they asked for. If the walk was 2-3-4, lead with a 6-12 line abstract, then the humanized rewrite.

When the pass is a skill rewrite, write the new `SKILL.md` in place only after a keep-list diff. Locked tokens listed in `references/handoff.md` must survive as the same words or the same numeral.

Do not dump `pass.json` into chat unless they ask.

## Hard rules

- No new facts. No new citations. No new page numbers.
- No change to locked typography, fade geometry, owner legal lines, or OpenAction field names when the source is a house skill or house PDF.
- Visible house name stays Digital Marketing Company. Legal owner line stays Web Development Corporation when that line is already in the source.
- Running footers never print a trailing class letter A on the house name.
- No emoji in skill files or in PDFs this skill hands off.
- This skill does not compile a PDF by itself. PDF output goes through /folio, /deep, /print, or article-clip-pdf.


## Render gate (mandatory with /itqe and /latex)

Before delivering any PDF, DOCX, PPTX, XLSX, HTML view, printed page, or builder JSON that may contain notation, short codes, or equations, run the house render gate. Chat may use KaTeX. Files must show compiled glyphs or a compiled figure. Raw LaTeX, AMS-TeX, KaTeX source, MathJax source, uncompiled backslash commands, tofu, or empty boxes are defects.

```bash
python3 @itqe/scripts/scan_render_gate.py \
  ./artifacts/<slug> \
  --also-pdf ./artifacts/<file>.pdf
python3 @latex/scripts/scan_raw_tex.py \
  ./artifacts/<slug> \
  --also-pdf ./artifacts/<file>.pdf --pages
```

Exit code 1 blocks delivery. Repair with `/latex` figures, attach an ITQE table under every display equation (Identifier, Term, Quantity, Explanation), rebuild, scan again, and raster every page. See `@itqe/references/render-gate.md` and `@latex/SKILL.md`.

## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write plate, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

## Canonical footer

Render `copyright/SKILL.md` and its canonical notice helper once per page. Do not reproduce independent legal text or calculate years here.

## Negative gate (mandatory before any deliverable)

Read `@negative/SKILL.md` and `@negative/references/blocklist.md`.
Before chat, PDF, DOCX, PPTX, XLSX, caption, filename, alt text, or footnote leaves this skill, extract visible text and run

```bash
python3 @negative/scripts/sweep_negative.py <extracted-text>
```

Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.

## ChatGPT portability

Resolve `@skill-name/path` by finding the installed personal skill whose SKILL.md frontmatter has `name: skill-name`; read that path under its directory. For `@generate/`, use the `generate-prompt` skill. Before running copied shell commands, substitute actual resolved paths and use the current working directory for generated files. Apply instructions only when this skill is invoked or a user requests the corresponding workflow. User instructions and platform rules take priority. Run bundled scripts only after checking their inputs and prerequisites. Never claim unavailable integrations, credentials, citations, or generated results.
