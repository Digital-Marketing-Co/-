# Banner geometry

Locked print contract for every banner this skill emits.

## Frame

- Aspect ratio 16-9 landscape.
- Target generate size 3300 x 1856 px. Floor 2550 x 1434 px.
- Print width equals page width. x = 0. Zero left margin, zero right margin, zero left padding, zero right padding.
- Height follows 16-9 after the page-width scale. Do not letterbox. Do not side-crop.

## Opacity

- Left edge column and right edge column stay fully opaque (alpha 255) so the picture touches trim.
- Pictorial interior stays fully opaque.
- Top edge and bottom edge only receive a real alpha ramp so the page paper shows through.
- Ramp height is 8 percent of banner height on the top and 8 percent on the bottom, cosine ease, alpha 0 at the extreme row to alpha 255 at the inner end of the ramp.
- Apply the ramp with `scripts/apply_tb_alpha_blend.py` after generate. Do not write the fade phrase into the generate prompt.
- RGB must not contain a checkerboard. Transparent rows are alpha 0 over real picture RGB, not a preview pattern.

## Prompt

- Literal objects from that section or subsection only.
- Futuristic cinematic still, stunning editorial stock-photo quality, photoreal volumetric lighting.
- No caption text, watermark, logo, agency seal, or private-person portrait.
- No token from `assets/negative-keywords.csv`.
- Do not write AI, xAI, or ChatGPT into the prompt.
- Do not ask the model to fade edges. Geometry is a post-process.
- Fresh generate per node. No reuse, crop, or near-duplicate of another banner.

## Coverage

One unique banner per body section and per subsection. Parent files never stand in for a child heading.
