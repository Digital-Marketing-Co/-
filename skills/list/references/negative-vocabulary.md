# Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before writing any concatenated prompt (image generate, caption sent to a generate tool, locked execution block copied into a model call).

## Hard ban

Do not write any token from the array into a concatenated prompt. That includes plate, gazette, atlas, folio, deep, exhaustive, AI, xAI, ChatGPT, and the fade phrase Real alpha one-inch fades on the top and bottom only.

## Invocation exception

Slash flags that collide with a banned word stay as routing tokens only

- `/atlas`
- `/folio`
- `/deep`
- `/itqe`

Never copy the bare word into the prompt body. On-disk names (`deep.json`, `folio.json`) stay as file paths, not as prompt words.

## Fade ban

Do not fade the top or bottom of a banner or figure. Do not call a fade script. Print at full opacity. Left and right stay edge-to-edge when the page-width pixel floor is already met.

## How to use the files

- CSV is the portable array (column `token`).
- XLSX is the preserved workbook (sheet `negative_keywords`, sheet `array_only`).
- Keep both files in lockstep when the array changes.
