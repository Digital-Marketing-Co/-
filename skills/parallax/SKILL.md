---
name: parallax
description: Style-neutral, source-preserving vector contour depth decomposition, up to 256 indexed layers, gyroscope-sensitive parallax, and coverage-aware spherical navigation.
version: 2.1.0
---

# /parallax — Style-Neutral Depth Engine

## Invocation
/parallax [source] [target: interactive web | layered assets | iOS wallpaper | video] [depth_layers: up to 256] [gyro sensitivity]. Default to the most recent user-supplied image. Never claim a static image is sensor-responsive.

## Mandatory style and source preservation
Never add artistic styles, objects, scenery, lighting effects, color transformations, or decorative elements WITHOUT EXPLICIT POST SKILL INVOCATION PROMPT. Preserve the original image.

Keep the original input immutable. Any explicit post-invocation edit applies only to a derived copy and only within the user's stated scope. Do not infer authorization from earlier examples, presets, the skill name, or aesthetic preferences. No automatic theme, lighting, color grading, object addition, or stylistic embellishment.

## Geometry-only processing
1. Analyze source coverage, pixel dimensions, depth evidence, uncertainty, and target viewport. Preserve original colors, composition, subjects, textures, and exposure.
2. Estimate continuous normalized inverse depth d(x,y) in [0,1], where 0 is farthest and 1 nearest. Record uncertainty. Trace subpixel-aware vector contours and alpha masks using actual source boundaries, not predetermined object or scenery categories.
3. Build an adaptive depth hierarchy with at most 256 distinct useful contour layers. Split only when improving depth fidelity, silhouette/occlusion accuracy, or motion. Prefer continuous mesh warps over redundant slices; never claim that 256 layers are necessarily optimal.
4. Assign contiguous integer indices 0..N-1, ordered farthest to nearest, with stable IDs separate from indices. Reindex atomically on splits/merges. Store index, depth bounds, centroid, parent ID, mask, vector contour, alpha, transform coefficient, uncertainty, and QA status in an ordered manifest.
5. Ensure monotonically increasing depth centroids and, for comparable camera shifts, nondecreasing bounded displacement amplitude from far to near. Composite back to front; validate topology, exclusivity/alpha handling, and correct occlusion.
6. Interpolate missing pixels only where justified by existing image evidence. Do not invent unseen objects, scenery, or geometry. If reconstruction is uncertain, constrain the camera motion or reveal a transparent/neutral boundary rather than fabricate source content.
7. Optimize gyro-responsive parallax with user-gesture deviceorientation permission on supported mobile browsers, HTTPS, calibration, sensor filtering, capped transforms, orientation recalibration, touch fallback, and no sensor retention. Respect reduced-motion, disable/intensity controls, and battery/frame budgets. Target smooth performance where feasible; report actual measured results.
8. Offer 360-degree horizontal and 180-degree vertical camera navigation only if source coverage or verified multi-view geometry supports it. A single flat image cannot supply faithful unseen reverse views. Constrain rotation to covered angles rather than synthesizing unauthorized scenery. Never imply that interactive web gyro behavior works as a live iOS system wallpaper.
9. Iterate contour → depth → split/merge → index → render → inspect → optimize until two consecutive QA passes show no material improvement. Check halos, tears, disocclusions, duplicated pixels, geometry, ordering, crop safety, performance, permissions, accessibility, and source fidelity.

## Output
- Immutable source and derived render or interactive preview as actually generated.
- Depth map, ordered vector masks/layers, and machine-readable manifest when actually generated.
- Actual layer count, coverage limits, sensor implementation status, QA evidence, unresolved uncertainties, and explicit distinction between working assets and specifications.
- Do not claim files, real-device tests, commits, deployment, or native spatial wallpaper compatibility unless verified.

## References
- https://developer.mozilla.org/en-US/docs/Web/API/Device_orientation_events/Detecting_device_orientation
- https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
