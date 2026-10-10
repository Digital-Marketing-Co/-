# /decode → /folio handoff

After `analysis.json` exists, compile one WCA Folio PDF. Do not skip the PDF because the sample is short. Small-\(n\) caveats belong in the method chapter; they are not a reason to withhold the report.

`<folio>` = `/home/workdir/.grok/skills/folio`

Read before drafting

- `<folio>/SKILL.md`
- `<folio>/assets/schema/folio.schema.json`
- `<folio>/references/chicago-folio.md`
- `<folio>/references/owner-and-house.md`
- `<folio>/references/discoverability.md`

Work stays in `/home/workdir/artifacts/decode-<slug>/`. The public PDF is written under `/home/workdir/artifacts/` with the Folio filename contract.

## Title and identity

Working title form

Statistical Decode of “[surface phrase, trimmed to 8 words]”

Subtitle form

Closed-corpus information theory, Zipf diagnostics, and a classical-cipher battery

Author

Web Development Corporation Research Desk

Owner and house blocks are copied exactly from `<folio>/references/owner-and-house.md`. Do not invent a second house host. Visible anchor is Digital Marketing Company Seed href is https://DigitalMarketingCo.org. Plain-text domain is DigitalMarketingCo.org.

Keywords include at least — closed corpus, unigram entropy, index of coincidence, Zipf, Good-Turing, next-token interpolation, Chicago notes.

## Required Folio sections (relabel only the chapter titles, keep this order)

1. Introduction and research questions
2. Historiography or literature review (Shannon 1951 letter entropy, Zipf, Good-Turing, Friedman IC, CMOS method notes)
3. Sources and method (tokenizer regex, logs base 2, H0 vs H1 rule, small-n estimators)
4. Inventory and information theory (paste measured \(N, V, H_1, H_2, R, H_{\mathrm{let}}, \mathrm{IC}, \chi^2\) from `analysis.json`; do not round away the JSON digits)
5. Zipf, change-point, and compression
6. Cipher battery and hypothesis test
7. Next-token recommendation and device caveat
8. Synthesis (accept H1 only under the two-test-plus-reconstruction rule)
9. Conclusion and open problems
10. Notes
11. Bibliography

Paragraphs use `{{n}}` or `{{n, m, p}}` markers. No author-date parentheticals.

## Mathematics on the page

Folio JSON accepts only `i`, `em`, `b`, `sup`, `a`. It does not compile LaTeX.

- Do not leave raw backslash commands in `folio.json`.
- Prefer Unicode letters and subscripts already present in Literata / EB Garamond (`H₁`, `H₂`, `Hₘₐₓ`, `α`, `χ²`, `λ₃`) or a short spelled phrase (“unigram entropy H-sub-1”).
- If a displayed derivation is required, generate an equation plate PNG under `figures/fig-NN.png` with real alpha only if the plate itself needs transparency; cream or white paper ground is acceptable for a typeset plate. Caption the plate. Never bake a checkerboard into RGB.
- Chat still uses KaTeX. The PDF and the chat are separate renderers.

## Figures

Optional. One figure per body section except Notes and Bibliography. Honest plates only — rank-frequency bars from the measured counts, an IC comparison bar, a next-token score table rendered as a figure. Do not invent a historical photograph of a keyboard or a factory.

## Citations

Prefer primary sources

- C. E. Shannon, “Prediction and Entropy of Printed English,” *Bell System Technical Journal* 30, no. 1 (1951)
- G. K. Zipf, *Human Behavior and the Principle of Least Effort* (1949)
- I. J. Good, “The Population Frequencies of Species and the Estimation of Population Parameters,” *Biometrika* 40 (1953)
- William F. Friedman, index-of-coincidence papers / Riverbank publications
- Claude E. Shannon, “A Mathematical Theory of Communication,” *Bell System Technical Journal* 27 (1948)

Do not fabricate page numbers. If a page locator was not read, omit it. Cultural identifications of the surface phrase (film, sample, mashup) go in the synthesis chapter and must be cited from the search record actually used in that run.

## Build

Write `folio.json` in the decode work directory. Then

```bash
python3 /home/workdir/.grok/skills/folio/scripts/build_folio_pdf.py \
  /home/workdir/artifacts/decode-<slug>/folio.json \
  --print-filename
```

Write the PDF to that exact name under `/home/workdir/artifacts/`.

```bash
python3 /home/workdir/.grok/skills/folio/scripts/build_folio_pdf.py \
  /home/workdir/artifacts/decode-<slug>/folio.json \
  --out /home/workdir/artifacts/<YYYY-topic-slug-wca-folio.pdf>
```

Visual QA is mandatory (`pdftoppm` every page). Rebuild on tofu, clipped glyphs, a trailing class letter A in the running footer, a broken house link, or a trailing comma in a superscript run.

## Deliver

Give the user the PDF. State page count, note count, bibliography count, \(N\), \(V\), the accepted hypothesis, and the recommended first-bar word. Do not dump `folio.json` into chat. Do not print the full sample twice; point at `sample.txt`.
