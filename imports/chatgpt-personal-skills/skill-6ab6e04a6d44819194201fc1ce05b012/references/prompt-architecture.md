# Locked prompt architecture

Write every visual or motion prompt as one paragraph in this order. Do not number the clauses inside the prompt.

1. Subject lock — two to five concrete nouns. Prefer the rarest proper noun in the spec.
2. Spatial lock — one setting the spec actually names. Invent no extra skyline.
3. Material lock — real surfaces those objects have.
4. Camera lock — aspect, scale, plane of focus.
5. Light lock — photometric, volumetric, rim only as rim.
6. Beauty lock — awe-inspiring, publication-grade, futuristic cinematic still or shot. Razor-sharp named subject. Shallow falloff behind it. No soft muddy toy-like collage or stock-generic lab.
7. Depth lock — visible volume in air, layered planes, physically based materials.
8. Motion lock (video only) — one camera move, one subject move, duration, easing.
9. Audio lock (video or audio only) — room tone, score bed, or spoken line if requested.
10. Negative lock — no caption text, no watermark, no logo unless the spec demands a brand mark as an object, no photoreal portrait of a private living person, no allegory, no readable paragraphs, no maker names, no skill flags.

Stills request 3300 × 1856 when aspect is 16:9. Do not write fade, transparent, alpha, or checkerboard into a generate prompt.

## Web-app prompts

A web-app "prompt" is a build spec, not a picture paragraph. Order

1. Product one-liner
2. Audience and job-to-be-done
3. Information architecture (routes)
4. Visual system (palette, type, depth)
5. Component inventory
6. Interaction and empty states
7. Policy and age gates when the brand is Aether
8. Acceptance checks

## Academic document prompts

Hand off to `/folio` or `/deep`. The generate prompt here is the mandate paragraph plus the section list, not a fake paper.

## Differentiation

A new prompt must differ from every earlier prompt in the same pack on at least three axes — primary object, camera scale, key material, setting, key light, or motion.
