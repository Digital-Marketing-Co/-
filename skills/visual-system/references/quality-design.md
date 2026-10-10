# Visual quality contract

Choose an output-specific visual system before generating artwork: type roles, spacing, contrast, material, depth, figure geometry, and motion. Preserve existing font locks and source-fidelity requirements. Full bleed concerns artwork at the trim; body text and labels still need safe inset and unclipped geometry.

Use a small palette with sharp luminous accents, consistent light direction, architectural depth, and independent section compositions. Keep dimensional effects in covers, banners, rules, and figure frames. Maintain quiet body text, precise legends, and readable notes. Never add shadows to an output that requires no shadows or opaque backgrounds to a transparent product cutout.

Measure contrast against the actual composited background, including translucent panels and gradient extremes. Require 4.5:1 for ordinary text and 3:1 for qualifying large text; use 7:1 for dense labels where feasible. White labels on navy table headers are a useful default, but verify the actual colors. Do not encode meaning solely by color. Use repeat table headers, meaningful captions, and readable bibliography URLs.

For interfaces provide visible focus, keyboard operation, meaningful labels, responsive layout, reduced-motion behavior, and static alternatives to decorative spatial effects. Test actual smallest viewport and longest label. For print retain vector text and real math, correct reading order, bookmarks where supported, and a readable white-paper variant where requested. Do not claim WCAG conformance from contrast checks alone.

Generated imagery is conceptual unless verified as documentary. Use deterministic plotting or diagram tools for exact quantitative content. Keep provenance, rights status, raw image dimensions, alpha mode, and image hashes. Resampling increases pixel count, not recovered detail. Verify actual embedded image placement and caption correspondence.

Primary references checked 2026-10-10:

- https://www.w3.org/TR/WCAG22/ — contrast, focus, resize, reflow, motion, and interaction requirements.
- https://pillow.readthedocs.io/en/stable/handbook/concepts.html — image modes and transparency.
- https://pymupdf.readthedocs.io/en/latest/page.html — PDF geometry, text, annotations, and redaction behavior.

Keep an inspection ledger: file and page, observed issue, correction, and repeated check. Judge evidence fidelity, label legibility, composition, consistency, and actual output presence separately. Do not invent numerical beauty scores without a declared evaluation method.
