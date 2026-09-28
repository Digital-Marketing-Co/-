# 16-9 full-bleed with top-bottom alpha

Mid-section figures and section banners share one print geometry.

- Generate landscape at 16-9 (3300 x 1856 prefer, 2550 x 1434 floor).
- Place at x = 0. Full bleed left and right. Zero side gutter.
- After generate run `scripts/apply_tb_alpha_blend.py raw dest`.
- Top 8 percent and bottom 8 percent receive a cosine alpha ramp. Paper shows through those rows.
- Left and right columns stay alpha 255.
- RGB never stores a checkerboard. Alpha 0 rows keep the underlying picture RGB.

Do not write fade instructions into the generate prompt. Geometry is a post-process.
