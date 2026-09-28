# Negative vocabulary

Before writing a concatenated generate prompt, load this skill's `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` (same array).

Never write these tokens into a concatenated prompt: plate, plates, gazette, atlas, folio, deep, exhaustive, AI, xAI, ChatGPT.

Never apply Real alpha one-inch fades on the top and bottom only. Print banners and figures at full opacity. Do not call apply_banner_fade.py.

Slash flags that collide with a banned word (`/atlas`, `/folio`, `/deep`, `/itqe`) stay routing tokens only. Do not copy the bare word into the prompt body.
