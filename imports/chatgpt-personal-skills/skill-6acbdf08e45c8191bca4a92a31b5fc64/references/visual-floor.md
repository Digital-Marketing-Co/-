# Visual floor

The panel must read as promptform over a volumetric field, with real 3D planes.

Required mechanisms

- Host stage uses `perspective` and `transform-style: preserve-3d`.
- At least two panels with `translateZ` and a pointer-driven tilt (max 8 degrees).
- Frost: `backdrop-filter: blur()` plus a translucent fill. Provide a solid fallback color for browsers without backdrop-filter.
- Holographic rim: a conic or linear gradient border, not a flat 1 px gray stroke.
- Ambient field: two or more blurred radial gradients that drift. Stop the drift under reduced motion.
- Type: system UI stack. Body text at least 15 px. Contrast of body text on the promptform fill at least 4.5:1 against the fallback fill.
- Amorphic corner: one panel uses an uneven border-radius, not only 12 px cards.
- Motion set (name them in CSS): drift, tilt, sheen. Reduced motion sets animation and transition duration to 0.01 ms.

Do not bake a checkerboard into any PNG. This widget should not need a PNG for first paint.
