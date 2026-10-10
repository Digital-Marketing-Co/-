---
name: decode
description: PhD cryptographic and statistical decode of any text or token stream. Trigger on /decode, space/decode, space /decode, decode this blob, keyboard next-word dump, QuickType log, anomalous word frequencies, Zipf outliers, or hidden-structure analysis of supplied text. Runs an information-theoretic, n-gram, Zipf, cipher-battery, and next-token analysis. Always compiles the measured battery into a WCA Folio Ivy League report PDF through the folio skill. Does not claim a hidden message unless a test rejects the null.
---

# /decode

## Quality and capability additions

Read [the task-specific quality profile](references/quality-profile.md) before execution. Use `evals/quality-cases.json` for regression scenarios; its assertions are acceptance criteria, not claims that tests have run. Shared path resolution and output rules live in `interop/SKILL.md`.



## Visual stack

Documents this skill emits follow `@visual-system/SKILL.md`.
Pick a genre palette with `@visual-system/scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Treat the user's supplied text as a closed corpus. Tokenize it. Run the battery in `scripts/decode_analyze.py`. Report frequencies, information theory, n-gram conditionals, Zipf diagnostics, classical-cipher tests, change-point structure, and a single next-token recommendation. Then compile those measured values into one WCA Folio PDF using the folio skill. Do not invent a ciphertext if the tests say the string is a language-model attractor.

Work in `/workspace/artifacts/decode-<slug>/`. Save `analysis.json` and `folio.json`. The public PDF is `/workspace/artifacts/<YYYY-topic-slug-wca-folio.pdf>`.

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
  --input /workspace/artifacts/decode-<slug>/sample.txt \
  --out /workspace/artifacts/decode-<slug>/analysis.json
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
  --analysis /workspace/artifacts/decode-<slug>/analysis.json \
  --label "<surface phrase, trimmed to 8 words>" \
  --out /workspace/artifacts/decode-<slug>/folio.json
```

Replace every stub paragraph, write Chicago notes and an alphabetized bibliography, then build with the folio builder. Do not leave raw LaTeX in `folio.json`. Use Unicode letters already in Literata / EB Garamond or an equation-figure PNG under `figures/`.

```bash
python3 @folio/scripts/build_folio_pdf.py \
  /workspace/artifacts/decode-<slug>/folio.json \
  --print-filename
```

```bash
python3 @folio/scripts/build_folio_pdf.py \
  /workspace/artifacts/decode-<slug>/folio.json \
  --out /workspace/artifacts/<YYYY-topic-slug-wca-folio.pdf>
```

Visual QA every page with `pdftoppm`. Rebuild on tofu, clipped glyphs, a trailing class letter A after Web Development Corporation in the running footer, a broken house or note link, or a trailing comma in a superscript run.

Visible house anchor is Digital Marketing Company at https://DigitalMarketingCo.org. Plain-text domain is DigitalMarketingCo.org.

If the user also invoked /deep or phd-ivy-monograph, still emit the Folio PDF first. Do not replace measured counts with rounded guesses in either document.

## Hard rules

- Never fabricate Apple bar output. The on-device rank is unobserved unless the user screenshots it.
- Never claim synthetic telepathy, remote writing, or a government implant from word counts alone.
- Classical cipher tests are diagnostics, not accusations.
- Do not print the full sample twice in chat; point at `sample.txt`.
- Do not dump `folio.json` into chat.
- Visible house link, when a PDF is built, is Digital Marketing Company at https://DigitalMarketingCo.org.
- Do not reprint `build_folio_pdf.py` or folio `typography.py` into chat.


## Render gate (mandatory with /itqe and /latex)

Before delivering any PDF, DOCX, PPTX, XLSX, HTML view, printed page, or builder JSON that may contain notation, short codes, or equations, run the house render gate. Chat may use KaTeX. Files must show compiled glyphs or a compiled figure. Raw LaTeX, AMS-TeX, KaTeX source, MathJax source, uncompiled backslash commands, tofu, or empty boxes are defects.

```bash
python3 @itqe/scripts/scan_render_gate.py \
  /workspace/artifacts/<slug> \
  --also-pdf /workspace/artifacts/<file>.pdf
python3 @latex/scripts/scan_raw_tex.py \
  /workspace/artifacts/<slug> \
  --also-pdf /workspace/artifacts/<file>.pdf --pages
```

Exit code 1 blocks delivery. Repair with `/latex` figures, attach an ITQE table under every display equation (Identifier, Term, Quantity, Explanation), rebuild, scan again, and raster every page. See `@itqe/references/render-gate.md` and `@latex/SKILL.md`.

## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write figure, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

## Paginated footer

Read `copyright/SKILL.md` and render its canonical notice exactly once per page. Do not keep separate legal text or year calculations here. Preserve any stated user override.

## Publication checks

Apply `interop/SKILL.md` once after the task-specific checks. Its shared rules yield to this skill's explicit format and source-fidelity requirements.

## Delivery

Run the single delivery gate in `interop/SKILL.md` after task-specific validation. Preserve verified quotations and technical identifiers; report unresolved defects or blockers accurately.
