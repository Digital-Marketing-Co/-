# Handoff to /deep, /folio, and /banner

`/summarize` does not compile PDFs. It prepares prose. Other skills consume that prose.

## Keep-list when the source is a house skill

These tokens must survive a rewrite of `deep`, `folio`, or `banner`.

### /deep

- flag `/deep`
- Georgia / Gelasio registered as Georgia
- BODY_PT 22
- work path `/home/workdir/artifacts/<slug>/`
- builder `build_deep_pdf.py`
- schema `deep.json`
- depth cap 4, keeper cap 80
- banner default href `https://digitalmarketingco.org/r/?src=deep-banner&section={section_id}`
- visible house name <a href="https://digitalmarketingco.org" title="Digital Marketing Company">Digital Marketing Company</a>
- Chicago notes-bibliography, no author-date parentheticals

### /folio

- flag `/folio`
- owner line Web Development Corporation, a Delaware Corporation
- type stack EB Garamond display, Literata 18pt body, Libre Franklin chrome
- filename `YYYY-topic-slug-wca-folio.pdf`
- canonical `{origin}/white-papers/{slug}`
- seed `https://digitalmarketingco.org`
- field `WCACopyrightYear`
- builder `build_folio_pdf.py`
- schema `folio.json`

### /banner

- flag `/banner`
- real alpha, RGBA
- width 8.5 in at 150 px/in
- total height 4.35 in
- top inch fade 0 → 1, bottom inch fade 1 → 0
- script `apply_banner_fade.py`
- raw `banners/raw-NN.png`, faded `banners/banner-NN.png`
- no burned-in caption, no visible URL on the plate

## Stacked flags

User typed `/summarize` with `/deep` or `/folio`

1. Finish the summarize walk on the supplied topic or source.
2. Put the level-2 abstract in the report abstract slot (150–250 words after expansion from sources, not by padding).
3. Put the level-4 prose in the draft sections only where it still matches research keepers.
4. Research, notes, and bibliography still come from /deep or /folio. The summary is not a source.

User typed `/summarize` with `/banner`

- Wait until body sections exist.
- Banner prompts still come from section claims, not from the abstract.

User typed `/summarize` on a skill file

- Rewrite the instruction voice in place.
- Run a keep-list diff before declaring done.
- Re-run `python3 /home/workdir/.grok/skills/copyright/scripts/append_prompt_appendix.py` if the appendix moved.
- Validate with `bash /root/.grok/skills/skill-creator/scripts/validate-skill.sh <dir>`

## What /summarize must not do

- Invent a research topic so that /deep or /folio has something to compile.
- Change START year, owner legal line, or fade geometry to sound nicer.
- Print a trailing class letter A on a running footer.
