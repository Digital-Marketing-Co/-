# /Perfect Engine 8 — Gap-Focused Candidates

Status: 24 proposed candidates, not implemented. Prior catalog: 456 named proposals (not verified unique). These additions are engineering capabilities, not all visual effects. Review against prior registry before treating as unique.

## Computational holography
- `gerchberg_saxton_phase_retrieval` — Gerchberg–Saxton Phase Retrieval [proposed]
- `wirtinger_hologram_optimization` — Wirtinger Hologram Optimization [proposed]
- `multi_wavelength_phase_encoding` — Multi-Wavelength Phase Encoding [proposed]
- `phase_quantization_error_visualization` — Phase Quantization Error Visualization [proposed]

## Optical system diagnostics
- `modulation_transfer_function_mapping` — Modulation Transfer Function Mapping [proposed]
- `point_spread_function_field_map` — Point Spread Function Field Map [proposed]
- `stray_light_ghost_analysis` — Stray-Light Ghost Analysis [proposed]
- `speckle_contrast_reduction` — Speckle Contrast Reduction [proposed]

## Display engineering
- `waveguide_exit_pupil_replication` — Waveguide Exit-Pupil Replication [proposed]
- `vergence_accommodation_mitigation` — Vergence–Accommodation Mitigation [proposed]
- `pupil_swim_correction` — Pupil Swim Correction [proposed]
- `display_uniformity_compensation` — Display Uniformity Compensation [proposed]

## Scene reconstruction
- `neural_surface_reconstruction` — Neural Surface Reconstruction [proposed]
- `multi_view_stereo_consistency` — Multi-View Stereo Consistency [proposed]
- `reflectance_field_capture` — Reflectance Field Capture [proposed]
- `polarimetric_surface_normal_estimation` — Polarimetric Surface Normal Estimation [proposed]

## Interactive rendering
- `late_stage_reprojection` — Late-Stage Reprojection [proposed]
- `asynchronous_timewarp` — Asynchronous Timewarp [proposed]
- `gaze_contingent_detail_allocation` — Gaze-Contingent Detail Allocation [proposed]
- `hand_occlusion_compositing` — Hand-Occlusion Compositing [proposed]

## Publication verification
- `pdf_transparency_flattening_preview` — PDF Transparency Flattening Preview [proposed]
- `font_embedding_integrity_scan` — Font Embedding Integrity Scan [proposed]
- `color_separation_plate_inspection` — Color Separation Plate Inspection [proposed]
- `rasterization_resolution_audit` — Rasterization Resolution Audit [proposed]

## Preliminary semantic review
- Gerchberg–Saxton Phase Retrieval is a specific algorithm within Phase Retrieval Visualization; retain as algorithmic variant, not a new family.
- Wirtinger Hologram Optimization is a distinct numerical optimization approach; relate to computer-generated holography, do not merge its algorithm with Gerchberg–Saxton.
- Multi-Wavelength Phase Encoding relates to phase-only holography but adds wavelength multiplexing; retain variant.
- Phase Quantization Error Visualization is a diagnostic, not equivalent to wavefront propagation.
- Modulation Transfer Function Mapping and Point Spread Function Field Map are linked by Fourier optics but represent different measurements.
- Speckle Contrast Reduction is a mitigation technique; distinct from Coherent Speckle depiction.
- Waveguide Exit-Pupil Replication is display optics, not equivalent to Eye-Box Expansion's general objective.
- Vergence–Accommodation Mitigation relates to Accommodation–Vergence Conflict Preview but is mitigation rather than diagnosis.
- Neural Surface Reconstruction is not identical to Neural Radiance Field Rendering or Gaussian Splat Rendering.
- Late-Stage Reprojection and Asynchronous Timewarp are related latency-compensation techniques; retain implementation distinctions.
- Gaze-Contingent Detail Allocation is an optimization variant of Foveated Light-Field Rendering; preserve alias and scope.
- PDF Transparency Flattening Preview and Rasterization Resolution Audit are export-validation capabilities, not holographic effects.

## Required semantic deduplication pipeline
1. Collect all prior source manifests and record provenance; do not infer complete earlier 408 entries from summary counts.
2. Normalize Unicode, names, identifiers and definitions; detect exact collisions.
3. Compare physical mechanism, algorithm, visual appearance, input requirements and output behavior; group families and variants.
4. Preserve all prior aliases, separate optical phenomena from algorithms, UI interactions and QA checks.
5. Produce machine-readable decision ledger with old_id, canonical_id, relation, rationale and evidence.
6. Build/test supported renderers and export fallbacks before changing status from proposed.
7. Validate contrast, motion, optical claims, math, copyright, image uniqueness and two actual QA/VQA passes.
8. Keep changes on a review branch until acceptance checks pass.

## Design compatibility
Canonical intended /Perfect with p alias; legacy /4629. Do not overwrite skills/4629/SKILL.md. Preserve linked /ITQE, /latex, /images, /banner, /copyright, /QA, /VQA and anti-truncation rules. Holographic binary tiles must be accessible without traditional radio/checkbox visuals.
