

# /decode


## Visual stack

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Treat the user's supplied text as a closed corpus. Tokenize it. Run the battery in `scripts/decode_analyze.py`. Report frequencies, information theory, n-gram conditionals, Zipf diagnostics, classical-cipher tests, change-point structure, and a single next-token recommendation. Then compile those measured values into one WCA Folio PDF using the folio skill. Do not invent a ciphertext if the tests say the string is a language-model attractor.

Work in `./artifacts/decode-<slug>/`. Save `analysis.json` and `folio.json`. The public PDF is `./artifacts/<YYYY-topic-slug-wca-folio.pdf>`.

`<folio>` = `@folio`

Read on demand

- `references/battery.md` — meaning of every statistic
- `references/folio-handoff.md` — section map, math-on-page rules, build commands
- `<folio>/SKILL.md` and `<folio>/assets/schema/folio.schema.json`

## When this runs

- User typed `/decode`, `space/decode`, or `space /decode`
- User pasted a keyboard, QuickType, or "next word" blob and asked for frequencies, outliers, or the first suggested word
- User asked for cryptographic analysis of arbitrary following input

If no input text is present, stop and ask for the blob. Do not invent a corpus. If the user only asked to revise this skill and supplied no blob, stop after the skill files exist.

## Workflow

### 1. Lock the sample

Copy the user text verbatim into `sample.txt`. Do not normalize away apostrophes until the tokenizer runs. Record device claims (e.g. iPhone 16 Pro Max) as metadata, not as observed outputs.

### 2. Run the battery

```bash
python3 @decode/scripts/decode_analyze.py \
  --input ./artifacts/decode-<slug>/sample.txt \
  --out ./artifacts/decode-<slug>/analysis.json
```

Read `references/battery.md` for the meaning of every statistic. Do not drop a test because the sample is short; report the estimator and its small-n caveat.

### 3. Interpret under two hypotheses

H0 — ordinary language, keyboard prediction, or a collapsed n-gram / transformer loop.

H1 — an intentional cipher, steganographic channel, or planted code.

Accept H1 only when at least two independent tests reject chance at a pre-declared threshold and a concrete encoding (acrostic, substitution, book cipher index, etc.) reconstructs a second text that is not a restatement of the surface words. Otherwise state that the surface process explains the anomalies.

Typical QuickType collapse signatures (do not treat these as ciphers)

- type-token ratio far below English prose of the same length
- a 3- or 4-word formula that occupies more than half the tokens after a change-point
- letter inventory missing rare consonants (q, x, z) while a, e, t, h, s, y dominate
- last-token continuation mass concentrated on one or two types

### 4. Next-token recommendation

The first recommended suggestion is the word \(\hat{w}\) that maximises a backoff mixture

\[
\hat{w} = \arg\max_w \big[\lambda_3 \hat{p}_{\mathrm{ML}}(w\mid w_{n-2},w_{n-1}) + \lambda_2 \hat{p}_{\mathrm{ML}}(w\mid w_{n-1}) + \lambda_1 \hat{p}_{\mathrm{ML}}(w) + \lambda_0 / V\big]
\]

with \((\lambda_3,\lambda_2,\lambda_1,\lambda_0)=(0.5,0.3,0.15,0.05)\) unless the analysis JSON supplies a better interpolated set. State the word first in the user-facing reply when the user asked for the iPhone first bar. Then give the runner-up and why a closed Apple model could still disagree (personal LM, contacts, locale).

### 5. Mathematics in the chat reply

Render every equation with KaTeX. Name every symbol the first time it appears. Give the numerical value computed on this sample immediately after the formula.

### 6. WCA Folio PDF (mandatory)

Follow `references/folio-handoff.md` and `<folio>/SKILL.md`. Seed numeric fields from the battery so they are not re-rounded

```bash
python3 @decode/scripts/folio_stub.py \
  --analysis ./artifacts/decode-<slug>/analysis.json \
  --label "<surface phrase, trimmed to 8 words>" \
  --out ./artifacts/decode-<slug>/folio.json
```

Replace every stub paragraph, write Chicago notes and an alphabetized bibliography, then build with the folio builder. Do not leave raw LaTeX in `folio.json`. Use Unicode letters already in Literata / EB Garamond or an equation-figure PNG under `figures/`.

```bash
python3 @folio/scripts/build_folio_pdf.py \
  ./artifacts/decode-<slug>/folio.json \
  --print-filename
```

```bash
python3 @folio/scripts/build_folio_pdf.py \
  ./artifacts/decode-<slug>/folio.json \
  --out ./artifacts/<YYYY-topic-slug-wca-folio.pdf>
```

Visual QA every page with `pdftoppm`. Rebuild on tofu, clipped glyphs, a trailing class letter A after Web Development Corporation in the running footer, a broken house or note link, or a trailing comma in a superscript run.

Visible house anchor is Digital Marketing Co. at https://DigitalMarketingCo.org. Plain-text domain is DigitalMarketingCo.org.

If the user also invoked /deep or phd-ivy-monograph, still emit the Folio PDF first. Do not replace measured counts with rounded guesses in either document.

## Hard rules

- Never fabricate Apple bar output. The on-device rank is unobserved unless the user screenshots it.
- Never claim synthetic telepathy, remote writing, or a government implant from word counts alone.
- Classical cipher tests are diagnostics, not accusations.
- Do not print the full sample twice in chat; point at `sample.txt`.
- Do not dump `folio.json` into chat.
- Visible house link, when a PDF is built, is Digital Marketing Co. at https://DigitalMarketingCo.org.
- Do not reprint `build_folio_pdf.py` or folio `typography.py` into chat.


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
