# /summarize scale

Locked names. Do not rename levels in chat or in `pass.json`.

## 0 Verbatim

Return the source. Useful when the user wants a lock file, a clip, or a before-copy.

Tells — the text matches the source, including faults.

Ban — silent cleanup. If you fix a typo, that is already level 1.

## 1 Compress

Delete throat-clearing, doubled explanations, and chrome. Keep the original order and most of the original sentences.

Tells — same nouns in the same order, shorter.

Ban — new metaphors. Ban merging two claims into a third claim.

## 2 Summarize

Keep the argument. Drop the tour.

Must keep

- every proper name the user will need later
- every measurement, year, URL, path, and flag
- the actual conclusion of the source, including "we do not know"

May drop

- repeated examples after the first one that does the job
- methodology theater that does not change the result
- site chrome, share modules, related-story blurbs

Length guide — about 10–20 percent of a long source; a paragraph for a short source. Do not pad.

Ban — a summary that sounds certain where the source was tentative.

## 3 Rewrite

New sentences. Same claims. Clean syntax. Still institutional.

Use this when the source is tangled, machine-translated, or written as notes.

Tells — a reader who knows the source recognizes every claim and finds no extras.

Ban — swapping a precise house term for a prettier synonym (`Literata` stays `Literata`. `WCACopyrightYear` stays `WCACopyrightYear`. `/banner` stays `/banner`).

## 4 Humanize

Spoken cadence. Concrete verbs. Short and long sentences mixed because that is how people write when they are paying attention.

Keep

- the source's temperature. If the source is dry, stay dry.
- disagreement and limits.
- numbers as numbers, not "several" or "many."

Drop

- stock LLM polish listed in `humanize.md`
- fake first-person memory ("when I first read this")
- fake camaraderie ("let's dive in")

Ban — adding color that is not in the source (weather, mood, interior lives of named people).

## 5 Teach

Level 4 plus one plain reason the claim matters, drawn only from the source.

Use when the user asked to explain, teach, or "say it so a smart non-specialist can use it."

Ban — a tutorial that introduces a method the source did not use.

## Default walk

`/summarize` with no extra verb runs 2 then 3 then 4.

Deliver

1. a level-2 abstract (6–12 lines)
2. the level-4 body

Keep level 3 in `passes/L3.md` for the folder. Do not print it unless they ask to see the workshop.

## Stacked verbs

`summarize and rewrite and humanize` = 2 → 3 → 4.

`rewrite then humanize` = 3 → 4, skip the standalone abstract only if the source is already short.

`humanize` on a skill file = 4 against the instruction prose, with the keep-list from `handoff.md` frozen.
