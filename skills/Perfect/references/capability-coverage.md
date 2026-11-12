# Perfect holographic capability coverage — v1

This file is an implementation-status ledger, not a declaration that all 541 proposed capabilities are implemented. Statuses must be based on reviewed source and execution evidence.

## Status vocabulary

- `coded-unverified`: code exists, but runtime and visual QA have not been demonstrated.
- `browser-verified`: automated browser run passed with traceable run identifier.
- `visual-verified`: reviewed screenshots and two documented visual QA passes.
- `hardware-dependent`: requires an optical display, capture device, or calibrated physical apparatus.
- `research-only`: conceptual, mathematical, or algorithmic item not yet offered as a product effect.
- `unmapped`: candidate not yet deduplicated or classified.

## Coded screen-based effects

The following 24 names correspond to selectable controls in `examples/holographic-lab-v4.html`. All are currently `coded-unverified`.

| ID | UI label | Implementation |
| --- | --- | --- |
| glow | Neon glow | CSS box shadow |
| prism | Prismatic foil | CSS conic gradient |
| orbit | Orbital rings | CSS animation |
| aurora | Aurora shift | CSS hue animation |
| fresnel | Fresnel rim | CSS outline approximation |
| shimmer | Shimmer sweep | CSS gradient animation |
| scan | Scanline field | CSS repeating gradient |
| depth | Spatial shadow | CSS drop shadow |
| caustics | Caustic light | Stylized radial gradient |
| haze | Volumetric haze | CSS glow approximation, not volumetric rendering |
| chromatic | Chromatic edges | Text shadow color separation |
| fringes | Interference fringes | Stylized radial bands |
| particles | Particle constellation | Fixed gradient points |
| grid | Holographic grid | CSS line lattice |
| glass | Glass reflection | CSS highlight overlay |
| energy | Energy rings | Animated circular border |
| halo | Soft halo | CSS outline |
| diffraction | Diffraction grating | Stylized line pattern |
| moire | Moiré pattern | Crossed line patterns |
| filaments | Plasma filaments | Blurred conic gradient |
| facets | Crystal facets | Conic gradient overlay |
| lattice | Light lattice | Repeating line lattice |
| radar | Radar sweep | Rotating conic gradient |
| vortex | Optical vortex | Rotating conic pattern |

## Not yet equivalent to implemented visual effects

Examples of `hardware-dependent` or `research-only` catalog items:

- Computer-generated holography, phase-only holography, wavefront propagation and spatial light modulation: require optical simulation or specialized output for physically meaningful results.
- Digital holographic data storage and shift-multiplexed recording: recording systems, not CSS appearance toggles.
- Neural radiance fields and Gaussian splatting: rendering architectures requiring datasets and appropriate rendering engines.
- Eye-tracked multiview perspective and light-field refocusing: require compatible input, scene data and/or displays.
- Camera intrinsic calibration, depth-sensor fusion and physical surface anchoring: require camera or depth hardware and calibration.
- Audio-reactive visuals: require an authorized audio source and a separate audio-processing implementation.

## Acceptance criteria

1. Reconcile and semantically deduplicate all 541 proposals against authoritative source files; preserve provenance and aliases.
2. Assign each candidate one primary category and a truthful status.
3. Verify effect activation, deactivation, combinations, keyboard operation, numeric inputs and reduced-motion behavior in a real browser.
4. Capture and review desktop/mobile screenshots; record two clean QA/VQA passes with evidence.
5. Do not claim physical holography, calibrated optics, production deployment or universal completeness from CSS approximations.
