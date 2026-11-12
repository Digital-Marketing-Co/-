# /Perfect Engine 13 — Optical Phenomena Gap Registry

Status: 12 proposed additions. Prior count 520; 532 proposed names before cross-version semantic deduplication. Optical demonstrations require scientific simulation or suitable hardware; this file implements neither.

## Nonlinear and ultrafast optics
- second_harmonic_generation_visualization: Second-Harmonic Generation Visualization [proposed]
- four_wave_mixing_visualization: Four-Wave Mixing Visualization [proposed]
- self_phase_modulation_visualization: Self-Phase Modulation Visualization [proposed]

## Diffractive and structured light
- airy_beam_propagation: Airy Beam Propagation [proposed]
- bessel_beam_self_healing: Bessel Beam Self-Healing [proposed]
- talbot_self_imaging: Talbot Self-Imaging [proposed]

## Polarization and topological light
- spin_orbit_light_coupling: Spin–Orbit Light Coupling [proposed]
- optical_skyrmion_field_visualization: Optical Skyrmion Field Visualization [proposed]
- cylindrical_vector_beam_rendering: Cylindrical Vector Beam Rendering [proposed]

## Advanced holographic materials
- photochromic_hologram_response: Photochromic Hologram Response [proposed]
- thermo_optic_hologram_tuning: Thermo-Optic Hologram Tuning [proposed]
- electrically_tunable_metasurface_holography: Electrically Tunable Metasurface Holography [proposed]

## Semantic merge review
- Second-Harmonic Generation, Four-Wave Mixing and Self-Phase Modulation are distinct nonlinear optical processes; do not merge them with generic plasma or glow effects.
- Airy and Bessel beams have different propagation properties; preserve both under structured-light family.
- Talbot Self-Imaging is a propagation/revival phenomenon, not generic diffraction patterns.
- Spin–Orbit Light Coupling relates to Pancharatnam–Berry Phase but is a broader interaction; retain a separate mechanism.
- Optical Skyrmion Field Visualization relates to polarization topology but is not synonymous with Vector Vortex Beams.
- Cylindrical Vector Beam Rendering overlaps Vector Vortex Beams in some configurations; classify as a variant where equivalent and preserve aliases.
- Photochromic, thermo-optic and electrically tunable metasurface holography use distinct material control mechanisms; do not merge.
- These are mostly scientific visualization or specialized optical hardware capabilities, not browser-native physical holograms.

## Quality and implementation contract
- Classify each item by mechanism, canonical family, variants, backend, optical hardware, evidence, accessibility fallback, performance and tests.
- Browser output must be labeled simulation when depicting physical coherent optics.
- Provide static accurate accessible scientific visualizations for document exports, preserving units and source provenance.
- Maintain canonical /Perfect and p, legacy /4629, existing /ITQE, /latex, /copyright, /QA, /VQA and anti-truncation requirements.
- Require real renderer tests and two actual QA/VQA passes before claiming production readiness.
- Do not assert that all 532 names are distinct or implemented; retrieve and deduplicate the complete earlier registry first.
