# Design lock — holographic glass depth

Apply this lock to every page and component `/PromptEngineer` writes.

## Materials

- **Glass** — `backdrop-blur` plus a translucent fill (`bg-white/10`–`bg-white/20` on dark fields, inverse on light). Border is a 1 px luminous edge, not a gray bootstrap rule.
- **Frost** — heavier blur on panels that sit over motion or video. Type on frost must still pass WCAG AA.
- **Amorphic** — primary panels may use organic `border-radius` stacks (e.g. `rounded-[2rem_0.5rem_2rem_0.5rem]`) and clip-paths. Not every box is a 12 px card.
- **Gradient field** — page ground is a living multi-stop gradient (deep ink, violet, teal, or gold rim) that shifts slowly. Never a flat `#fff` only shell unless the remainder demanded paper.
- **Transparency** — layers stack. The menu is a plane in front of the page, not a painted rectangle.
- **Holographic / 3D** — stacked translate-Z or CSS 3D (`perspective`, `rotateX` on open, `transform-style: preserve-3d`) plus a thin iridescent edge (`conic-gradient` or dual-axis linear sheen). Depth must be readable with motion off (shadow + overlap).

## Type

- Display — tight tracking, high-contrast against the glass.
- Body — 16 px minimum, 1.5 line-height, AA contrast on its actual glass fill (measure the composite, not the raw hex).
- Never put running paragraphs in a 10 px footer.

## Light

- One key light, one rim. Rim may be gold or ice. Do not wash the whole UI neon.
- Focus rings are visible and offset. Do not remove outlines.

## What is a defect

- Default unstyled `<details>` as the only menu
- Gray admin tables as the look
- Stock purple blob backgrounds with no structure
- Motion that hides labels
- Text on 8 percent white glass that fails contrast
- Checkerboard baked into PNG RGB
- The same still reused on two routes

## Viewport

Design mobile first. Mega menus collapse to an off-canvas accordion under 768 px. Desktop flyout is a 3D glass deck. Both consume the same data array.
