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
