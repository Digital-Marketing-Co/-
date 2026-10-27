---
name: parallax
description: Maximize physically plausible 3D parallax for images, iPhone spatial wallpapers, banners, and interactive scenes with depth segmentation, QA, and accessibility.
---
# /parallax — Immersive Depth Engineering

## Invocation
/ parallax [source image or scene] [target: iOS Spatial Scene | interactive web | video | layered assets]. Aliases: /parallax /depth /gyro-parallax. Default to the last supplied image and iPhone 9:16 wallpaper when context indicates it. Never claim a still image is gyroscope-responsive.

## Prompt-engineering pipeline
1. Identify the original image and preserve photographic identity and geometry; do not substitute a newly imagined image unless explicitly requested. Determine target aspect ratio, output pixel dimensions, cropping safety, and clock/widget safe area.
2. Optimize physically credible depth cues: occlusion, relative scale, perspective, atmospheric haze, shadow consistency, water refraction, fine texture and lens characteristics. Never invent incompatible lighting or impossible reflections.
3. Separate nonduplicated semantic planes: (a) near foliage/shells, (b) beach, (c) shallow water/coral, (d) distant palms/islands, (e) horizon/sky. Refine with instance masks and continuous depth map; feather boundaries only where physically appropriate; inpaint disoccluded areas rather than stretching pixels.
4. For iOS 26 native wallpaper: prioritize clear subject/background separation, good lighting, recognizable depth, uncluttered clock area, and safe edge padding. Output an ordinary photographic image for Apple's on-device Spatial Scene eligibility evaluation. Do not assert that eligibility or strength can be guaranteed, and do not claim access to Apple's private depth processing. Guide user to Settings > Wallpaper > Add New Wallpaper > Photos, select eligible image, enable Spatial Scene if available. Native effect is Lock Screen only.
5. For custom interactive web/PWA: require user-gesture motion permission where needed, secure HTTPS, deviceorientation feature detection, no sensor data retention, low-pass smoothing, neutral orientation calibration, capped displacement, CSS transform or WebGL layer translation, perspective scale from depth, interpolation, visibility pause, orientation-change recalibration, and touch fallback. Device sensors work only while the app is active; do not claim arbitrary live iOS system wallpaper integration.
6. Apply displacement inversely with depth, constrained by inpainted overscan. Starting guidance only: near layer ±22px, beach ±14px, lagoon ±8px, distant islands ±3px, sky 0–1px on a ~400 CSS-pixel-wide preview; tune based on image resolution and edge coverage. Never sacrifice naturalism for amplitude. Use a subtle rotational component only when horizon remains level.
7. Respect prefers-reduced-motion; provide disable and intensity controls; avoid vestibular triggers. Aim for smooth 60fps when feasible, degrade gracefully, throttle offscreen work, and avoid paid inference at runtime.
8. Iteratively /expound: diagnose each defect, revise geometry/masks/occlusion, rerender, and run technical, photographic, mobile crop, accessibility, and visual QA until two consecutive review passes yield no material improvements. Stop rather than claim unverified exhaustive perfection.

## Deliverables
- Native: pristine 9:16 still image optimized for iOS Spatial Scenes; explicit limitation that Apple's conversion and motion are device-dependent.
- Interactive: original/extended image, nonduplicated transparent layers, masks, depth map, preview, and source implementation when requested; report which assets actually exist.
- QA report: crop coverage, silhouette halos, disocclusion gaps, horizon stability, shadow/reflection coherence, perceived depth, performance, permission handling, reduced-motion, and real-device verification status.
- Do not claim generated depth maps, layers, real-device QA, commits, or deployments without producing/verifying them.

## References
Apple Support https://support.apple.com/en-us/102638
MDN https://developer.mozilla.org/en-US/docs/Web/API/Device_orientation_events/Detecting_device_orientation
MDN https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/prefers-reduced-motion


## Adaptive maximum-layer interpolation (mandatory)
Replace the fixed five-layer ceiling with an adaptive, depth-ordered hierarchy. The original five semantic groups are starting anchors only; subdivide each into as many independently useful and visually coherent depth slices as image evidence and performance permit. Do not fabricate depth certainty from a single image.

### Iterative layer construction
1. Estimate a continuous normalized inverse-depth map d(x,y) in [0,1], where 0 is farthest and 1 is nearest; separately preserve instance boundaries, translucency, water/refraction, and uncertainty.
2. Initialize the five anchor groups; split high-depth-variance groups by adaptive quantiles or edge-aware clustering. Prefer boundaries at real occlusion discontinuities. Within smoothly varying surfaces, use depth interpolation and a mesh/depth warp instead of thousands of hard-cut sprites.
3. On each iteration, propose additional slices only where the split improves motion fidelity, silhouette quality, or perceptible depth. Maintain parent-child provenance, mask exclusivity or explicitly documented alpha compositing, and reconstruct newly exposed pixels.
4. Assign every layer a unique integer index, contiguous and monotonically increasing from 0000 (farthest background) to N-1 (nearest foreground). Sort by physical depth before EVERY render, serialization, export, and QA pass. Higher index must be nearer to the viewer. Never rely on filesystem order or lexicographic string ordering without zero padding.
5. For each indexed layer, record: index, semantic group, depth_min, depth_max, centroid_depth, parent_index, mask reference, alpha, occlusion relationships, transform coefficient, and QA status. Reindex atomically after splits/merges; keep stable persistent IDs distinct from display indices.
6. Interpolate transform strength continuously with depth, using bounded monotone easing; farther layers never translate more than nearer layers for the same camera shift. Treat sky as nearly stationary, horizon as stable, and refractive water as a special physically constrained case.
7. Enforce compositing back-to-front (ascending index); validate that occluders appear in front of occluded objects and no layer is skipped or duplicated. Export an ordered manifest and deterministic render test.
8. Increase layer count until marginal depth-quality gain is negligible or memory, battery, framerate, edge-coverage, and artifact budgets would be exceeded. Do not assert a universal optimal count: use adaptive budgets (e.g., 8–32 useful semantic/sprite planes on capable devices as a starting experiment, with continuous depth meshes where superior), benchmark real hardware, and lower count when necessary.
9. Iteratively /expound with split → index → interpolate → inpaint → render → measure → QA. Repeat until two consecutive complete passes produce no material gain in perceived depth or occlusion correctness and no regressions. Never claim actual tests without executing them.

### Layer-order invariants
- Indices are exactly [0, 1, ..., N-1], without gaps or duplicates.
- depth_centroid[i] <= depth_centroid[i+1] (far-to-near convention).
- transform_amplitude[i] <= transform_amplitude[i+1], subject to explicit physical exceptions for reflective/refractive surfaces.
- Render order follows ascending indices; foreground covers background.
- A split or merge MUST regenerate indices, depth ranges, masks, and manifest before the next iteration.
- The final report includes actual layer count, indexed manifest, split/merge history, benchmark conditions, and any unverified assumptions.



## Vector-contour semantic depth and 360° panorama (v3 specification)
1. Detect and label every distinguishable object and material region, including overlapping palm leaflets, trunks, hibiscus, shells, foam, sand, water, reef, mountains, clouds, and sky. Assign stable object IDs, semantic class, confidence, occlusion relationships, and contour geometry. Maximize useful recall while suppressing hallucinated objects and duplicated instances.
2. Trace subpixel-aware vector contours (SVG paths or equivalent) from masks, with adaptive sampling, topology checks, and antialiased alpha boundaries. Preserve holes, thin structures, translucent foliage, soft foam, and motion blur. Never claim exact object identification without verification.
3. Estimate depth from perspective, occlusion, relative scale, texture, and learned monocular cues where available. Fuse object-level relative depth with intra-object depth gradients and continuous mesh/depth fields. Treat inferred depth as uncertain, not measured physical distance. Interpolate intra-object depth adaptively; avoid horizontal slicing as a substitute for true object contours.
4. Generate candidate extra layers by subdividing vector-bounded objects and depth discontinuities, ordered numerically from farthest 0000 to nearest N-1. Rebuild manifests atomically after every split or merge. Prefer continuous depth meshes for curved surfaces over needless duplicate sprite layers.
5. For every novel camera pose, compute visibility and disocclusions, reconstruct newly exposed backgrounds, and reject inconsistent anatomy/botany, lighting, shadows, shorelines, reflection directions, and island geometry. AI regeneration is optional and only when explicitly authorized and available; maintain original image as immutable reference.
6. A single image does not contain the complete rear/side geometry required for a faithful 360° scene. To deliver 360° azimuth by 180° elevation, either acquire multi-view imagery or synthesize explicitly labeled speculative unseen views; enforce equirectangular seam closure, pole handling, horizon stability, and cross-view object identity. Never present invented reverse views as documentary photography.
7. Interpret celestial-axis spin as a clearly selectable camera yaw around the local vertical axis or a sky-sphere rotation; keep real-world horizon and gravity physically coherent. If astronomical motion is requested, use a separately specified time/location model rather than arbitrary star motion.
8. Optimize for realistic parallax, not the largest number of layers. Profile device memory, frame pacing, GPU overdraw, battery use, texture budgets, and quality; reduce or merge layers where extra complexity harms realism.
9. Iterate /expound: detect → contour → estimate depth → interpolate → index → regenerate disocclusions → render multi-view → compare → QA. Stop after two consecutive passes with no material improvements, and report actual implementation, tests, inferred versus measured depth, and unresolved artifacts.
