# Negative vocabulary

Load `assets/negative-keywords.csv` and `assets/negative-keywords.xlsx` before writing any concatenated generate prompt.

Hard ban in concatenated prompts: plate, gazette, atlas, folio, deep, exhaustive, AI, xAI, ChatGPT, and the fade phrase Real alpha one-inch fades on the top and bottom only.

Slash flags `/atlas`, `/folio`, `/deep`, `/itqe` stay routing tokens only.

Do not fade any edge of a banner. Do not call `apply_banner_fade.py`. Print at full opacity.
