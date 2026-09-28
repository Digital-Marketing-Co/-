# What /corpus is not

`/corpus` inventories works **by** a match. It does not argue a thesis about a field.

| User intent | Skill |
|---|---|
| All papers by one person or lab | `/corpus` |
| Ivy catalog PDF of that inventory | `/corpus` (this skill prints the catalog) |
| Narrative report that *uses* those papers | `/folio` after corpus |
| Recursive topic monograph | `/deep` |
| Dissertation-style study with section figures | `phd-ivy-monograph` |
| Reprint one URL as a clip | `article-clip-pdf` / `print` |

Do not copy chapter templates, banner plates, or Georgia 22-pt locks from `/deep` into a corpus catalog. Times / Liberation Serif, letter size, bibliography-first.

## Stacking

`/corpus /folio <match>` means

1. Run this skill to saturation.
2. Hand `works.dedup.jsonl` to `/folio` as the source list.
3. Folio writes a report **about** the corpus (career arc, methods, open problems). It does not re-harvest.

`/corpus /deep <match>` is allowed only when the user wants the person treated as a historical subject with a source graph. Still start with this skill so the graph is not a homonym mix.

## Residual gaps

State in the catalog preface

- years with no recovered work
- known CV items that never received a DOI
- closed full texts
- agency tokens that produced zero `.mil` hits

Gaps are part of the corpus, not a failure of the skill.
