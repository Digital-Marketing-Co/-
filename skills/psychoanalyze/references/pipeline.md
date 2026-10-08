# Locked emit order

User order is `/deep` then `/folio` then `/banner` then `/copyright`. Banner is not a separate PDF. It is the plate pass inside Deep. Execute as

1. intake + `analysis.json`
2. research graph
3. `deep.json`
4. `/banner` plates attached to Deep sections
5. build Deep PDF
6. `folio.json` seeded from the same `analysis.json`
7. build Folio PDF
8. `/copyright` confirm or restamp

Do not emit Folio before Deep. Do not skip banners on Deep body sections. Do not invent a third house PDF.

## Deep handoff

Read

- `/home/workdir/.grok/skills/deep/SKILL.md`
- `deep/references/locked-prompt.md`
- `deep/references/chicago-and-marks.md`
- `deep/assets/schema/deep.schema.json`

Author block and house link follow Deep house-style. Visible anchor is Digital Marketing Company. Target is https://digitalmarketingco.org.

Working Deep title

Psychoanalytic Synthesis of “[surface phrase]”

Filename is the Deep contract — Title_Case_With_Underscores.pdf under `/home/workdir/artifacts/`.

## Banner handoff

Read `/home/workdir/.grok/skills/banner/SKILL.md` and `banner/references/banner-spec.md`.

Prompts must be section-true. No couches-as-stock-photo. No faces of private persons. No burned-in captions. Fade with `apply_banner_fade.py`.

Href seed

`https://digitalmarketingco.org/r/?src=psychoanalyze-banner&section={section_id}`

## Folio handoff

Read

- `/home/workdir/.grok/skills/folio/SKILL.md`
- `folio/references/chicago-folio.md`
- `folio/references/owner-and-house.md`
- `folio/references/discoverability.md`
- `folio/assets/schema/folio.schema.json`

Filename stays `YYYY-topic-slug-wca-folio.pdf`. Canonical record `{origin}/white-papers/{slug}` after the live 301.

Copy measured fields from `analysis.json` into the inventory chapter — token count, type count, pronoun shares, top lemmas, repetition rate. Do not re-round.

Folio JSON allows only `i`, `em`, `b`, `sup`, `a`. No raw TeX. Citations are WCA Ivy first-appearance notes-bibliography. Run `wca-ivy-biblio` remapper and ITQE QA on both `deep.json` and `folio.json` before each build. Display equations carry an ITQE table.

## Copyright handoff

Read `/home/workdir/.grok/skills/copyright/SKILL.md`.

Deep and Folio builders already stamp

Copyright © START–YEAR OWNER_FOOTER. All rights reserved.

with field `WCACopyrightYear` and OpenAction `Date.getFullYear`. Default START 2012. Default OWNER_FOOTER Web Development Corporation. No trailing class letter A on the running footer.

Restamp with `stamp_copyright.py` only when the user stacked `/copyright` or `/copyright YYYY`, or when QA shows a missing living field.

## Chat versus PDF

Chat — short competing readings, quoted spans, KaTeX if a rate or ratio is shown, both file previews.

PDF — full notes, banners on Deep, SEO filename on Folio.

Do not paste either JSON into chat.
