# Negative vocabulary

Before writing a concatenated generate prompt, load this skill's `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` (same array).

Never write these tokens into a concatenated prompt: plate, plates, gazette, atlas, folio, deep, exhaustive, AI, xAI, ChatGPT.

Do not write fade phrases into generate prompts. After generate, run banner or images `apply_tb_alpha_blend.py` so only the top and bottom of 16-9 full-bleed rasters receive a real alpha ramp. Left and right stay opaque. Do not bake a checkerboard into RGB.

Slash flags that collide with a banned word (`/atlas`, `/folio`, `/deep`, `/itqe`) stay routing tokens only. Do not copy the bare word into the prompt body.
