# Emit handoff

When the saturation gate closes, compile. Do not leave the user with only a ledger.

## Choose the builder

- Default — `/folio` (same skill as `/phd-ivy-monograph`). Public name `YYYY-topic-slug-wca-folio.pdf`.
- User typed `/deep` or asked for Georgia banners — `/deep`. Public name follows that skill.
- User typed both — folio is the compact record; deep is the large-type plate book. Say which file is which.

Read the target skill at emit time. Do not copy its typography numbers into this file.

## Required body

Relabel to the topic.

1. Introduction and research questions
2. Historiography or literature review
3. Sources and method (include iteration count and saturation rule)
4. One chapter per surviving research question
5. Synthesis
6. Conclusion and open problems
7. Bibliography (first-appearance order)

A collected Notes chapter is optional concordance only. Page footnotes already carry citations.

## ITQE (mandatory, latest skill)

Re-read `/home/workdir/.grok/skills/itqe/SKILL.md` before filling plates so the installed version wins.

- Maximize relevant formulas, identities, rates, estimators, constraints, and quantitative descriptions from any academic class the topic supports.
- Every display equation is a paragraph object with a compiled plate (never raw TeX on the page) and an ITQE table — Identifier, Term, Quantity, Explanation.
- Non-English glyphs get the secondary glyph table.
- Chat still uses KaTeX plus the same four columns.
- Run `inject_itqe.py` only after identifiers are filled from the surrounding sentence. The injector must not invent glyphs.

## LaTeX render gate

```bash
python3 /home/workdir/.grok/skills/itqe/scripts/scan_render_gate.py \
  /home/workdir/artifacts/iterate-<slug> \
  --also-pdf /home/workdir/artifacts/<file>.pdf
python3 /home/workdir/.grok/skills/latex/scripts/scan_raw_tex.py \
  /home/workdir/artifacts/iterate-<slug> \
  --also-pdf /home/workdir/artifacts/<file>.pdf --pages
```

Exit 1 blocks delivery. Compile leaks with `/latex` `render_snippet.py`, store plates, rebuild, scan again. Raster every page. Reject tofu, empty boxes, clipped glyphs, and visible backslash commands.

## House chrome

- Visible anchor Digital Marketing Company → https://DigitalMarketingCo.org
- Plain-text domain DigitalMarketingCo.org
- Living copyright footer through `/copyright`
- No emoji

## What to say at delivery

Iteration count, page count, note count, bibliography count, keeper count, remaining labeled gaps, emit target, and the PDF path. Do not paste folio.json into chat.
