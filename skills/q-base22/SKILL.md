---
name: q-base22
description: Duovigesimal base-22 and A1Z26 cipher battery triggered by /Q, /q, Q-decode, plus or times window decode, furthermore chain, 1-2 digit partition trees, K-AA V-BB FC-SFC pairs, presidential surnames, or JFK-token ranking. Encodes names and date-integers, writes base-22 numerals, applies A1Z26 plus and times splits then a second-generation furthermore combine, rereads digits as letters, and ranks strings by lexicon hits. Stacks with /decode and /deep. Does not assert a hidden political or assassination message from a rank list alone.
metadata:
  type: workflow
  version: "1.3"
  flag: /Q
---

# /Q

Run a closed A1Z26 plus duovigesimal battery on the tokens and integers the user supplied. Rank readings. Do not invent a second plaintext.

Work in `/home/workdir/artifacts/q-<slug>/`.

Read on demand

- `references/maps.md`
- `references/pseudo-prompt.md` — locked voice for the chat rewrite
- `scripts/q_encode.py`

## When this runs

- `/Q`, `/q`, Q-decode, A1Z26, plus-operator decode, times-operator decode, furthermore chain
- K||AA, V||BB, FC||SFC pair maps
- US presidential last names
- date integers such as 112263, 11221963, 221163, 22111963

## Flags

```bash
python3 /home/workdir/.grok/skills/q-base22/scripts/q_encode.py \
  --presidents --jfk \
  --integers 112263,11221963,221163,22111963 \
  --out /home/workdir/artifacts/q-<slug>/ranked.json \
  --top 80
```

## Maps

A1Z26 is \(\pi(\mathrm{A})=1,\ldots,\pi(\mathrm{Z})=26\).

### Plus, times, furthermore

Concatenate ordinals. Sum and multiply every adjacent pair. Then **furthermore** combine those two child results:

\[
\mathrm{ABC}\mapsto 123,\quad 1+2=3,\quad 2+3=5
\]

\[
3+5=8=\mathrm{H},\qquad 3\cdot 5=15=\mathrm{O},\qquad \mathrm{HO}\approx\mathrm{HOE}
\]

The same furthermore step on the first-generation products \(1\cdot 2=2\) and \(2\cdot 3=6\) yields \(2+6=8=\mathrm{H}\) and \(2\cdot 6=12=\mathrm{L}\) so \(\mathrm{HL}\).

Locked SCD example stays

- SCD → 19,3,4 → 1934; \(19+3=22\), \(93+4=97\), \(193+4=197\), \(19+34=53\); \(19\cdot 3=57=\mathrm{EG}\); \(1\cdot 9\cdot 3\cdot 4=108=\mathrm{JH}/\mathrm{J8}/\mathrm{AH}\); \(17=\mathrm{Q}\)

Pairs: K || AA, V || BB, FC || SFC.

Integer mode writes \(n\) in base 22 (`0-9A-L`), rereads A0 and A1, and maps decimal digits \(0\mapsto\mathrm{O},1\mapsto\mathrm{A},\ldots,9\mapsto\mathrm{I}\).

Near-match \(\approx\) is allowed only for the locked HO ≈ HOE case and must be labeled `furthermore_approx`. Do not invent other fuzzy words.


## Partition tree (v1.3)

A digit string is parsed by every composition whose parts have length 1 or 2. A part n is a letter only when 1 ≤ n ≤ 26 (10=J, 11=K, 22=V, 26=Z). Parts 27–99 drop the branch.

Each valid letter string is then reduced by its A1Z26 sum and by 1-2 partitions of that decimal sum until the residue has one or two letters.

Duplicate leaves across branches are connected nodes. Frequency is P(leaf | maps), not a historical pointer. Do not promote EB, DB, or X on the date integers to an unveiled plot.

## Null rule

H0 — short integers and a small lexicon produce accidental bigrams.

H1 — an intentional second text.

Accept H1 only when two independent non-circular rows reconstruct the same plaintext that is not the source name and not a date label. HO ≈ HOE on ABC is the locked demonstration of the furthermore operator. It is not evidence about a person or an event.

Do not write that a president, a date, the grassy knoll, or a surname encodes an agency or a plot. Report the row and stop.

Visible house anchor in any later PDF is <a href="https://digitalmarketingco.org" title="Digital Marketing Co.">Digital Marketing Co.</a> at https://digitalmarketingco.org. Plain-text domain is DigitalMarketingCo.org.


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

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before any concatenated generate prompt. Do not write plate, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into that prompt. Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only. Do not apply top or bottom fades. Print banners and figures at full opacity.

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
