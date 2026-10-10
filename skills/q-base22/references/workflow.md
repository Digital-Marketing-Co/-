

# /Q

Run a closed A1Z26 plus duovigesimal battery on the tokens and integers the user supplied. Rank readings. Do not invent a second plaintext.

Work in `./artifacts/q-<slug>/`.

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
python3 @q-base22/scripts/q_encode.py \
  --presidents --jfk \
  --integers 112263,11221963,221163,22111963 \
  --out ./artifacts/q-<slug>/ranked.json \
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

Visible house anchor in any later PDF is Digital Marketing Company at https://digitalmarketingco.org. Plain-text domain is DigitalMarketingCo.org.


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
