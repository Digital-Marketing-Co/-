# Strata

Both lanes use the same four strata. A filter removes a stratum from collection and logs the removal in `gaps.md`.

## Statistics

One row per published figure.

| Field | Rule |
|---|---|
| `id` | `d1-stat-###` or `d2-stat-###` |
| `claim` | The sentence the figure supports |
| `value` | Numeric or categorical as published |
| `unit` | Unit or `n/a` |
| `date` | Publication or observation date |
| `geo` | Geography or `unspecified` |
| `source_title` | Work title |
| `source_url` | Canonical URL |
| `uncertainty` | Interval, sample size, or `not stated` |
| `status` | `cited` or `unknown` |

Do not average unpublished cells. Do not convert a forecast into a fact. If two sources disagree, keep both and add a conflict row.

## Images

One row per still.

| Field | Rule |
|---|---|
| `id` | `d1-img-###` or `d2-img-###` |
| `subject` | Literal subject |
| `source_url` | Page that hosts the still |
| `local_path` | Saved path or empty |
| `rights` | `public-domain`, `cc`, `press`, `unknown` |
| `width` | Pixels or `unknown` |
| `prompt` | House still prompt if a generate is required |
| `byte_hash` | Short hash so a later pass can reject reuse |

No reused bytes across lanes or routes. No baked checkerboard in RGB when alpha is required.

## Motion picture

One row per public film, clip, or engineered shot.

| Field | Rule |
|---|---|
| `id` | `d1-mov-###` or `d2-mov-###` |
| `title` | Published title or shot name |
| `runtime` | Published runtime or target seconds |
| `date` | Release or capture date |
| `source_url` | Watch page or `prompt-only` |
| `shot_prompt` | Literal shot list prompt |
| `file_path` | Only if a file was written in this sandbox |

Do not claim an MP4 exists because a prompt exists.

## Virtual holography

One row per entity or route. This stratum is a volumetric / light-field / holographic UI plane, not a physical hologram file.

| Field | Rule |
|---|---|
| `id` | `d1-holo-###` or `d2-holo-###` |
| `plane` | What the plane shows, literal |
| `route` | Public page it binds to, or `unbound` |
| `prompt` | Volumetric still prompt: glass, layered planes, edge light, readable type |
| `file_path` | Only if a still was generated |

Depth cues stay in the image. Do not describe the plane as a metaphor for the topic.
