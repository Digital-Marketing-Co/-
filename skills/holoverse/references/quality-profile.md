# HOLOVERSE quality profile

## Execution and evidence
Treat `references/master-prompt.md` as the source of truth. Keep verified facts, assumptions, and open questions separate. Report results as `PASS`, `FAIL`, `BLOCKED`, or `NOT TESTED`, and back each one with evidence. Never claim a test pass, deployment, or live route you did not observe. Do not invoke paid inference at runtime or just to test the skill.

## Acceptance checks
- Six realms render with EN/ES copy: Nebular Forge, Ember Plateau, Abyssal Core, Photon Canopy, Temporal Rift, Crystalline Shore.
- Parallax responds to pointer, touch, and scroll. Gyroscope runs only after a user-gesture permission and falls back cleanly.
- `prefers-reduced-motion` disables animation with full content parity.
- Voxel mode uses real 3D geometry (three.js) and shows a text fallback without WebGL.
- `tsc` builds clean and vitest passes. Both `index.html` and `guide.html` return HTTP 200.

## Validation protocol
Run `npx tsc --noEmit && npx vitest run && npm run build`, serve the build, and check both pages. Use the master prompt §14 QA matrix for deeper audits.
