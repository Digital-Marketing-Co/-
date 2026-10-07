# Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before writing any concatenated generate prompt.

Hard ban in concatenated prompts: plate, gazette, atlas, folio, deep, exhaustive, AI, xAI, ChatGPT, and any fade or transparency phrase.

Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only.

Do not ask the generate model to fade edges. After generate, run `scripts/apply_tb_alpha_blend.py` so only the top and bottom receive a real alpha ramp. Left and right stay opaque. Do not call any other fade script. Do not bake a checkerboard into RGB.
