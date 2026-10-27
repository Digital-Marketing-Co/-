# Parallax depth quality profile

## Execution and evidence

Preserve the source image, subject identity, geometry, and photographic realism unless the user explicitly requests an edit. Record source provenance, output type, device constraints, pixel dimensions, and evidence for every reported QA outcome. Never claim an ordinary still image contains working gyroscope motion, a depth map, a segmented layer stack, or verified Apple Spatial Scene eligibility unless independently demonstrated.

For visual artifacts follow `visual-system/references/quality-design.md`; for shared composition follow `interop/SKILL.md`. These references are shared contracts, not a substitute for task-specific tests.

## Depth and layer-order contract

Use a continuous inverse-depth estimate (0 farthest, 1 nearest), preserve uncertain regions, and split semantic groups only when evidence and performance justify more layers. Every exported layer must have a stable persistent ID and a distinct, contiguous integer display index from 0 to N-1. Sort by physical depth before rendering, exporting, and QA; compose far-to-near in ascending index. Verify monotone depth centroids and bounded, generally monotone transform amplitude, with documented physical exceptions for refractive or reflective surfaces. Check masks, alpha compositing, inpainting, edge overscan, and occlusion. Never equate an interpolated depth slice with a verified distinct physical object.

## Acceptance checks

Check (1) input fidelity and absence of duplicated imagery, (2) stable horizon, plausible light and water optics, (3) contiguous unique layer indices and consistent depth order, (4) silhouette halos and disocclusion gaps, (5) no clipped edges during maximal displacement, (6) motion smoothing, permission fallback, reduced-motion behavior, and performance for interactive outputs, and (7) native iOS still-image limitations and clock-safe crop. Report actual layer count and unverified assumptions; do not assert 60 fps or real-device testing without measurements.

## Validation protocol

Run representative, boundary, and presentation cases in `evals/quality-cases.json` against produced artifacts. Record input hashes, tool versions, layer manifest, observed render order, test conditions, failures, and whether device QA was performed. Use PASS, FAIL, BLOCKED, or NOT TESTED; do not convert structural validation into visual or device certification.