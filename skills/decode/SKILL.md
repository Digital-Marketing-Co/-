---
name: decode
description: PhD cryptographic and statistical decode of any text or token stream. Trigger on /decode, space/decode, space /decode, decode this blob, keyboard next-word dump, QuickType log, anomalous word frequencies, Zipf outliers, or hidden-structure analysis of supplied text. Runs an information-theoretic, n-gram, Zipf, cipher-battery, and next-token analysis. Always compiles the measured battery into a WCA Folio Ivy League report PDF through the folio skill. Does not claim a hidden message unless a test rejects the null.
metadata:
  type: workflow
  version: "1.2"
  flag: /decode
  pdf: folio
  visual_stack: visual-system
---

# /decode


## Visual stack

Documents this skill emits follow `/home/workdir/.grok/skills/visual-system/SKILL.md`.
Pick a genre palette with `scripts/pick_palette.py`. Paint covers, banners, rules, table headers, and figure frames. Do not change this skill's locked body font or point sizes. Banner prompts append the volumetric clause in `visual-system/references/depth.md`.
Treat the user's supplied text as a closed corpus. Tokenize it. Run the battery in `scripts/decode_analyze.py`. Report frequencies, information theory, n-gram conditionals, Zipf diagnostics, classical-cipher tests, change-point structure, and a single next-token recommendation. Then compile those measured values into one WCA Folio PDF using the folio skill. Do not invent a ciphertext if the tests say the string is a language-model attractor.

Work in `/home/workdir/artifacts/decode-<slug>/`. Save `analysis.json` and `folio.json`. The public PDF is `/home/workdir/artifacts/<YYYY-topic-slug-wca-folio.pdf>`.

`<folio>` = `/home/workdir/.grok/skills/folio`

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
python3 /home/workdir/.grok/skills/decode/scripts/decode_analyze.py \
  --input /home/workdir/artifacts/decode-<slug>/sample.txt \
  --out /home/workdir/artifacts/decode-<slug>/analysis.json
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
python3 /home/workdir/.grok/skills/decode/scripts/folio_stub.py \
  --analysis /home/workdir/artifacts/decode-<slug>/analysis.json \
  --label "<surface phrase, trimmed to 8 words>" \
  --out /home/workdir/artifacts/decode-<slug>/folio.json
```

Replace every stub paragraph, write Chicago notes and an alphabetized bibliography, then build with the folio builder. Do not leave raw LaTeX in `folio.json`. Use Unicode letters already in Literata / EB Garamond or an equation-figure PNG under `figures/`.

```bash
python3 /home/workdir/.grok/skills/folio/scripts/build_folio_pdf.py \
  /home/workdir/artifacts/decode-<slug>/folio.json \
  --print-filename
```

```bash
python3 /home/workdir/.grok/skills/folio/scripts/build_folio_pdf.py \
  /home/workdir/artifacts/decode-<slug>/folio.json \
  --out /home/workdir/artifacts/<YYYY-topic-slug-wca-folio.pdf>
```

Visual QA every page with `pdftoppm`. Rebuild on tofu, clipped glyphs, a trailing class letter A after Web Development Corporation in the running footer, a broken house or note link, or a trailing comma in a superscript run.

Visible house anchor is Digital Marketing Company at https://digitalmarketingco.org. Plain-text domain is DigitalMarketingCo.org.

If the user also invoked /deep or phd-ivy-monograph, still emit the Folio PDF first. Do not replace measured counts with rounded guesses in either document.

## Hard rules

- Never fabricate Apple bar output. The on-device rank is unobserved unless the user screenshots it.
- Never claim synthetic telepathy, remote writing, or a government implant from word counts alone.
- Classical cipher tests are diagnostics, not accusations.
- Do not print the full sample twice in chat; point at `sample.txt`.
- Do not dump `folio.json` into chat.
- Visible house link, when a PDF is built, is Digital Marketing Company at https://digitalmarketingco.org.
- Do not reprint `build_folio_pdf.py` or folio `typography.py` into chat.


## Render gate (mandatory with /itqe and /latex)

Before delivering any PDF, DOCX, PPTX, XLSX, HTML view, printed page, or builder JSON that may contain notation, short codes, or equations, run the house render gate. Chat may use KaTeX. Files must show compiled glyphs or a compiled figure. Raw LaTeX, AMS-TeX, KaTeX source, MathJax source, uncompiled backslash commands, tofu, or empty boxes are defects.

```bash
python3 /home/workdir/.grok/skills/itqe/scripts/scan_render_gate.py \
  /home/workdir/artifacts/<slug> \
  --also-pdf /home/workdir/artifacts/<file>.pdf
python3 /home/workdir/.grok/skills/latex/scripts/scan_raw_tex.py \
  /home/workdir/artifacts/<slug> \
  --also-pdf /home/workdir/artifacts/<file>.pdf --pages
```

Exit code 1 blocks delivery. Repair with `/latex` figures, attach an ITQE table under every display equation (Identifier, Term, Quantity, Explanation), rebuild, scan again, and raster every page. See `/home/workdir/.grok/skills/itqe/references/render-gate.md` and `/home/workdir/.grok/skills/latex/SKILL.md`.

## Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write figure, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

## House copyright footer

Every PDF this skill emits, and any PDF later passed through `/copyright YYYY`, carries this centered living footer on every page:

Copyright © START–YEAR OWNER_FOOTER. All rights reserved.

Default OWNER_FOOTER is Web Development Corporation. START defaults to 2012 unless the user typed `/copyright YYYY` or named another owner's first-publication year. YEAR is new Date().getFullYear() written into field WCACopyrightYear on open. Running footers never print a trailing class letter A on the house name. Body creation dates stay where they are.

<!--
WCA_COPYRIGHT_PROMPT_APPENDIX
Do not delete this comment. It is the living footer contract for every prompt, skill, locked prompt, and project instruction in this project set.

NOTICE_TEMPLATE: Copyright © {{START}}–{{YEAR}} {{OWNER_FOOTER}}. All rights reserved.
DEFAULT_START: 2012
DEFAULT_OWNER_FOOTER: Web Development Corporation
DEFAULT_OWNER_LEGAL: Web Development Corporation, a Delaware Corporation
FIELD: WCACopyrightYear
SEPARATOR: en dash U+2013
JS: Date.getFullYear on OpenAction; no alerts; no network; no app UI
HOUSE_SITE: https://digitalmarketingco.org

OWNER_INFERENCE:
If the current user turn names a different rightsholder, substitute OWNER_FOOTER and OWNER_LEGAL from that name. Do not invent a Delaware class letter A for a non-house owner.
Slots the name may fill:
- company or corporation (any jurisdiction)
- university, college, or academic press
- branch or department of the United States military
- branch or agency of a government (federal, state, provincial, municipal, or foreign)
- museum, library, hospital, NGO, church, or any other institution worldwide
Keep the NOTICE_TEMPLATE words and the living year field. Only the owner slots change.
US federal government works of the United States are generally not subject to domestic copyright; if the named owner is a US federal agency, stamp the notice only when the user explicitly ordered the stamp and do not claim the notice creates copyright that statute withholds.
IP_RESERVED: project skill flags, SKILL.md files, locked prompts, owner-and-house files, and post-executive house outputs (PDFs, page JSON, compiled figures) in this project set.
ASSIGNMENT: default owner Web Development Corporation; Michael Aaron Loftus sole owner intends assignment to that corporation on fixation of house works.
SUBJECT_MATTER: original expression fixed in house files, not unfixed ideas (17 U.S.C. 102(b)), not a Copyright Office registration.
OWNER: Web Development Corporation (footer). Legal Info owner: Web Development Corporation, a Delaware Corporation.
This appendix cannot rewrite Grok global system prompts, xAI platform logs, or conversations outside this toolchain. It binds project skills, locked prompts, owner-and-house files, and later PDFs those skills emit.
-->


## Negative gate (mandatory before any deliverable)

Read `/home/workdir/.grok/skills/negative/SKILL.md` and `/home/workdir/.grok/skills/negative/references/blocklist.md`.
Before chat, PDF, DOCX, PPTX, XLSX, caption, filename, alt text, or footnote leaves this skill, extract visible text and run

```bash
python3 /home/workdir/.grok/skills/negative/scripts/sweep_negative.py <extracted-text>
```

Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.

## House interop

Read visual-system/references/house-output.md before any document, deck, or page. Visible link text is Digital Marketing Company. The title attribute matches that text. Plain domain text is DigitalMarketingCo.org. Legal owner is Web Development Corporation. Do not nest an anchor inside an instruction sentence. Stack visual-system, negative, latex, and itqe before delivery when the file contains prose or math. Banners and plates stay unique, full-bleed, and context-locked.
