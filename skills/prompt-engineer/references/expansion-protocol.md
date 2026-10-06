# Expansion protocol — pseudoprompt to PhD implementation

A pseudoprompt is a short product sentence. It is incomplete on purpose. This skill fills every missing plane before code is written.

## Input rules

1. Keep every concrete noun the user typed (mega menu, apps, 404, footer accordion, glass, Tailwind).
2. Do not replace the job with a different job.
3. Do not shrink a suite request into a single button.
4. If the sentence names an existing page (`/apps`, `/404`, footer), treat those as live surfaces to restamp, not as optional extras.

## Twelve expansion planes

Fill all twelve. A plane may be short. A plane may not be blank.

1. **Intent** — one sentence job-to-be-done and the primary user.
2. **Scope** — pages, components, and data sources in / out.
3. **Information architecture** — routes, landmarks, heading outline, source-of-truth arrays.
4. **Visual system** — palette, materials (glass, frost, metal edge), depth planes, type scale, amorphic geometry.
5. **Motion** — enter, idle, hover, focus, exit, reduced-motion fallback. Name specific Tailwind keyframes from `tailwind-motion.md`.
6. **Interaction** — pointer, keyboard, touch, screen reader. Focus trap rules for menus and dialogs.
7. **Inclusivity** — contrast pairs, hit targets >= 44 px, `prefers-reduced-motion`, `prefers-contrast`, language, skip link.
8. **Media** — unique still, OG 1200x630, Twitter summary_large_image per route. No shared bytes.
9. **Performance** — critical CSS, font subset, image dimensions, lazy below-fold, no layout shift from the menu.
10. **Semantics and discovery** — title, description, canonical, robots, hreflang if needed, JSON-LD types, AIO/GEO/AEO copy blocks.
11. **Security and headers** — HTTPS-only assets, no inline secrets, safe external script policy, form tokens if a form exists.
12. **Acceptance** — 521-metric self-score plan plus viewport matrix 320 / 768 / 1440.

## Density floor

The founding example in `exemplar-mega-menu.md` is the minimum density for navigation work. Match that level of surface coverage (nav + /apps order + 404 + footer + images + auditor) whenever the remainder is a site chrome request.

For a smaller remainder (one widget), still fill all twelve planes. Do not invent an apps suite the user did not name.

## Output shape

Write the spec in the heading order of `assets/expansion-skeleton.md`. Then implement. Do not leave the spec as the only deliverable unless mode is `spec`.
