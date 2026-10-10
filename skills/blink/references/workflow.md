

# /blink — memorable available bit.ly link

Turn one long URL into the shortest easy-to-say `https://bit.ly/{keyword}` that still looks free, then create it when a Bitly token exists.

`<skill>` = `@blink`.

If the user only asked to create or revise this skill and supplied no URL, stop after the skill files exist. Do not invent a destination.

## Read on demand

- `references/bitly.md` — API body, probe rules, token source
- `scripts/blink.py` — candidate generator, public availability probe, optional create

## Workflow

### 1. Collect input

Need a destination URL. Optional preferred keyword (`--keyword`) and Bitly bearer token (`BITLY_ACCESS_TOKEN` or `--token`).

Normalize missing scheme to `https://`.

### 2. Generate and probe

```bash
python3 @blink/scripts/blink.py "URL" [--keyword KW] [--create]
```

The script fetches the page title, builds short slugs from host + path + title, probes `https://bit.ly/{kw}` without following off-site redirects, and prints JSON.

Prefer the first `available` entry (already sorted shortest then speakable).

### 3. Create when possible

If `BITLY_ACCESS_TOKEN` is set, rerun with `--create`. Confirm the returned `link` resolves to the original URL.

If there is no token, do not pretend the short link is reserved. Return the ranked available list and tell the user to paste the chosen back-half in the Bitly UI or to export `BITLY_ACCESS_TOKEN`.

### 4. Reply

Give the user, in this order:

1. Best link as `https://bit.ly/{keyword}` plus the long URL
2. Two to five shorter or equal runners-up
3. Create status (created / needs token / Bitly rejected custom keywords on this plan)

Do not use a random Bitly hash unless every memorable candidate failed and the user accepts a non-memorable link.


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

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write figure, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

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

The uploaded package does not include a Bitly API client or credentials. Use a connected Bitly integration if available; otherwise explain the missing connection and provide a ready-to-use manual workflow. Never invent a shortened URL.
