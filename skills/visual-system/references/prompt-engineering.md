# PhD-level generate-prompt contract

Load this file whenever `/banner` or `/images` writes a generate prompt, and whenever `/latex` compiles a decorative or section figure that will print as a still. Body type, point size, and math compile rules stay with the calling skill.

The job is not "make a pretty science picture." The job is one irreplaceable still per node — context-locked, byte-unique, perceptually unique, and beautiful enough to hold a full-bleed letter page.

## Non-negotiable outcomes

1. Contextual. Name only objects, settings, materials, and instruments that already exist in that section (banner) or in that 500-word window (mid-text). If the caption were covered, a domain reader would still know which node the still belongs to.
2. One still per node. Every body section and every subsection gets its own banner. Mid-text stills follow the 500-word cadence. A parent banner never covers a child heading.
3. No duplicates. No shared path, no shared SHA-256, no shared perceptual hash, no crop, no recolor, no resize of another published file in the same document.
4. Beauty floor. Awe-inspiring, publication-grade, futuristic cinematic still. Reject soft, muddy, toy-like, collage, clip-art, stock-generic lab, and metaphor architecture.
5. Fail closed. Three generate attempts per slot. A fourth collision or a generic still blocks delivery of that slot.

## Prompt architecture (locked order)

Write the prompt as one paragraph in this order. Do not number the clauses in the prompt itself.

1. Subject lock — two to five concrete nouns from the node (molecule, instrument, tissue, vessel, landform, document, device). Prefer the rarest proper noun in that node.
2. Spatial lock — one setting the node actually names (dental operatory tray, dentin slab in cross-section, patch-clamp rig, clove-bud still, zinc-oxide powder bed). Invent no skyline.
3. Material lock — real surfaces those objects have (phenolic oil meniscus, zinc-oxide powder, gold electrode glass, wet dentin tubules, borosilicate).
4. Camera lock — 16-9 landscape, 3300 × 1856 px request, three-quarter or macro as the object scale demands, razor-sharp plane on the named object, shallow falloff behind it.
5. Light lock — photoreal volumetric lighting, physically based materials, visible depth in air, controlled gold and violet rim only as rim, not as neon wash.
6. Beauty lock — append the exact clause in `beauty-lock.md`.
7. Depth lock — append the exact clause in `depth.md`.
8. Negative lock — no caption text, no watermark, no logo, no agency seal, no photoreal portrait of a private person, no allegory, no metaphor architecture, no readable paragraphs, no burned-in numerals unless that exact string is already in the node text.

Do not write figure, gazette, atlas, folio, deep, exhaustive, AI, xAI, or ChatGPT into the prompt. Do not write fade, transparent, alpha, or checkerboard into the prompt. Top-bottom alpha is applied after generate by `apply_tb_alpha_blend.py`.

## Differentiation rule (anti-duplicate prompts)

Before the generate call, list every prompt already used in this document. The new prompt must differ in at least three of these axes

- primary named object
- camera scale (macro / three-quarter / interior still-life)
- key material
- setting
- time-of-day or key light direction

If two nodes share a molecule, change the instrument or the cut-plane. Eugenol in a section on partition chemistry is a meniscus in octanol–water glassware. Eugenol in a section on dentinal diffusion is a cross-section of wet dentin tubules under a zinc-oxide pack. Those are different stills. Same bottle on two pages is a defect.

Store `prompt` on the banner or figure object. Never send an identical prompt string twice.

## Beauty rejection list

Regenerate when any of these appear in the raw PNG

- generic white bench that could illustrate any chapter
- glowing abstract blobs standing in for a named molecule
- unreadable baked captions or mirrored letters
- soft focus on the subject
- stretched or letterboxed frame
- collage or split-screen
- repeated composition from an earlier slot (same bottle angle, same glove, same skyline)
- neon grid or hologram UI the node text does not name
- a compiled equation plate reused as a banner

## /latex stack

Compiled math plates from `render_snippet.py` are equation figures. They may not be copied into a banner slot or a 500-word mid-text slot. Each equation plate is unique to that equation id. Banner and mid-text stills never contain raw TeX and never display an equation unless that exact compiled relation already sits in the node and has its own ITQE table.
