# 4629 Electric-Cyan / Midnight-Navy Immersive Motion Profile

## Intent and authority
Default recommended interactive visual identity for /4629 web experiences, modal windows, app/product backgrounds and supported live presentations. Supplement, never override, the canonical design, document QA, parallax style-neutrality, accessibility or user-specified styling. Static PDF/DOCX/images use a carefully composed still frame; do not imply embedded live animation.

## Visual tokens
- Canvas: deep navy #030B22, midnight #071533, deep-blue #10264B. Accent: electric cyan #00DFFC, ice #83F5FF, subtle violet #5369D8; print/contrast variants permitted.
- Surface: translucent deep navy panel with sufficient opaque backing to protect readability; cyan edge glow and restrained reflective highlights; avoid busy motion behind body copy.
- Signature background: flowing cyan aurora ribbon, refractive gradient field, subtle concentric Z-depth luminous rings, scattered low-opacity spectral particles, volumetric fog and physically coherent layered motion. Prefer elegant low-frequency motion over strobing, pulsing, or noisy effects.
- Siri-inspired modal treatment: custom independent dual-orbit luminous border, gradient edge diffusion, slowly shifting cyan/blue/violet perimeter bloom, glass interior, sharp text surface, sensible focus order and escape-to-close. Do not represent an Apple asset or copy the referenced site's actual code.

## Motion engine
- CSS-first gradients and transforms; use requestAnimationFrame/WebGL only when justified by measured needs, with visibility pause, GPU context-loss fallback, adaptive quality tiers and no background network inference.
- Depth architecture: background gradient field; distant low-parallax particles; middle aurora; close light contours; foreground modal/panel. A 2.5D effect is not a faithful 360° view. Camera-offset amplitude monotonic with depth and bounded.
- /parallax remains strictly content/style-neutral when invoked alone. When /4629 explicitly adds this style AFTER /parallax invocation, put the new effect in separately controlled overlay layers; never mutate source pixels, geometry, colors or depth maps.
- Interaction: cursor/touch parallax, optional permission-based gyro on supported mobile browsers, calibrated motion damping, keyboard alternative, pause/toggle and no retained orientation telemetry.
- Default motion duration >= 8 seconds for large cycles, restrained luminance variance, no rapid flashes; respect prefers-reduced-motion and manual off controls, and avoid vestibular-discomfort-inducing drift.
- Performance budgets are targets, not claims: prioritize <=16.7ms/frame on capable devices, low-end fallback to static gradient, avoid layout thrash, memory growth, continuous heavy shaders, and excessive battery drain; measure actual FPS, long tasks and energy proxies before asserting compliance.

## Learning and optimization
Use /karma event fingerprints and tested regression rules for clipping, jank, glow-over-text, duplicate assets, contrast failures, reduced-motion regressions, visual monotony and mobile touch issues. Version design-token experiments and test on controlled screenshots; log objective performance and accessibility metrics and optional consented preference results. Selection may be deterministic; do not call it trained ML. Actual model training needs permissioned labeled data, holdout benchmarks, privacy safeguards and measured improvement. Never perform continuous unattended production changes without permitted tooling and approval.

## Release QA
Visual screenshots at mobile, tablet and desktop plus modal opened/closed/focus state; contrast, layout overlap, touch and keyboard, Escape, reduced motion, static fallback, gyro permission handling, frame-time and memory profiling, duplicate images, sensitive-data checks, final document QA. Two clean full passes if executable tooling supports them; otherwise NOT TESTED. Refer to canonical document-error-prevention standard for collision/truncation guarantees.
