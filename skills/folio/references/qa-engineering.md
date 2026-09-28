# QA engineering — unified WCA compact Ivy report

This is the locked design review that made `/folio` and `/phd-ivy-monograph` the same product.

## What “Ivy report” means here

Not a costume of seals and Latin. A working document a dissertation committee, a university press editor, or a think-tank research director can read without fighting the page.

| Property | Decision |
|---|---|
| Page | US letter, cream `#FBF7F0`, near-black ink `#1A1916` |
| Column | 6.55 in (0.95 / 0.90 side margins) |
| Body | Literata 18pt optical **set at 10 / 14.2** |
| Display | EB Garamond 20 / 24 title, 13 / 16.5 H1 |
| Chrome | Libre Franklin 7–7.5 pt |
| Citations | Chicago notes-bibliography, WCA superscript runs, **page-local footnotes**, first-appearance order |
| Back matter | Optional collected Notes concordance + hanging bibliography in citation order |
| Equations | Primary ITQE mandate — maximize relevant formulas from any academic class; compiled plate (never raw TeX) plus an **ITQE** table — Identifier, Term, Quantity, Explanation |
| Discoverability | `YYYY-topic-slug-wca-folio.pdf`, XMP + Info, `{origin}/white-papers/{slug}` |
| Living footer | © 2012–YEAR Web Development Corporation (no trailing class A) |

v1 Folio body was 11.5 / 17. That is a large-print seminar handout. Compact 10 / 14.2 is the university-press and NBER / Brookings working-paper range: more argument per leaf, still above 9 pt notes.

## Genre (one skill, four kickers)

Set `genre` in the JSON. The builder only changes the title-leaf kicker and the implied figure rule.

- `report` (default) — academic report
- `monograph` — PhD-depth study; one generated figure per body section
- `working-paper` or `paper` — article / working paper
- `living-document` or `think-tank` — dated edition + version + revised fields; open-problems chapter is required

## Citation QA

1. Every `{{n}}` has a `notes[].n`.
2. Superscript run is `12, 15, 18` — comma and space inside the run, no trailing comma.
3. The page that carries the mark reprints those notes in the footnote band.
4. Collected Notes, if present, is concordance only.
5. Note numbers are exactly `1..N` in first-appearance order. Run `wca-ivy-biblio` after every insertion.
6. Bibliography is hanging, unnumbered, and sorted by first appearance of each work. Alphabet is not the house sort.
7. No author-date parentheticals.
8. No invented page locators.
9. Every display equation has a compiled plate and a complete four-column ITQE table. Quantitative claims that can be written as relations must appear as plates, not only as prose. Field of origin is not a reason to omit a relevant formula.

## Type and glyph QA

After `pdftoppm -png -r 140`, reject the PDF if any page shows tofu, black or white boxes over glyphs, clipped descenders, colliding footnote and copyright lines, a figure sitting on type, a broken house link, or a footer that ends with a stray class letter A.

Stay inside bundled OFL faces. No emoji. Equations must be typeset (compiled plate or proven Unicode, not raw TeX source) and followed by an ITQE table. Explain every symbol the first time it appears.

## Accessibility and pedagogy

- Contrast of body ink on cream exceeds WCAG 2.2 AAA.
- PDF outline for every section.
- House name is a URI.
- Running header carries a shortened title.
- Measure stays near 68–74 characters at 10 pt.

## Living-document fields

Optional JSON keys the title leaf will print when present: `edition`, `version`, `revised`, `status`, `series`.

## What this skill is not

Not `/deep` (Georgia 22 display plates). Not `/banner`. Not `/atlas`. Those remain separate.
