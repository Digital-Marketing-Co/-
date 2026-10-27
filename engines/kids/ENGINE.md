---
name: kids
description: Rewrite any supplied email, document, or text into a faithful professional version, a grade-7 hilarious thematic version, and an illustrated ATLAS-style educational presentation with copyright and source notes.
version: 1.0.0
---
# /kids — Clarity, Comedy & Illustrated Learning

## Invocation
`/kids [paste text or attach document]` with optional flags `--theme pirate`, `--swap privacy:piracy`, `--grade 7`, `--humor hilarious`, `--images`, `--banner`, `--atlas`, `--copyright`, `--wca-ivy-biblio`, `--format email|report|poster|pdf`.

## Goal
Replicate the full multi-stage workflow demonstrated in the DON CIO Privacy → Piracy example for any new input. Default to grade 7, lively but appropriate humor, and an illustrated banner/infographic when the user explicitly invokes /kids. Do not force a pirate theme or word substitution onto unrelated material: infer a context-appropriate theme or use a neutral funny approach. Ask one brief question only if an essential choice is missing.

## Workflow
1. **Read completely.** Extract an internal fidelity checklist of every factual claim, actor, acronym, deadline, date, contact, URL, eligibility condition, prohibition, sequence, submission channel, consequence, and expectation. Identify official legal names and potentially sensitive content.
2. **Professional reconstruction.** Produce a clear, polished, well-organized rewrite with headings, plain language, and numbered actions. Preserve every substantive detail. Do not imply the original is verified or endorsed.
3. **Kid-friendly adaptation.** Re-express at roughly U.S. grade 7 (short sentences, defined acronyms, concrete analogies). Keep all requirements and precise steps. Avoid condescension.
4. **Humor layer.** Make the kid-friendly version genuinely funny with playful metaphors, callbacks, surprising comparisons, and thematic wordplay; prioritize readability and fidelity over joke volume. Never invent instructions, policies, deadlines, permissions, or agency claims. Avoid jokes that trivialize abuse, violence, trauma, or urgent safety warnings.
5. **Optional word swaps.** Apply user-specified substitutions to parody labels and narrative; keep URLs, proper names, legally operative titles, and official terminology unchanged where necessary for correct action. Explain the real name once and clearly label parody. Do not silently alter quoted text.
6. **Action checklist.** Finish with a simple who/what/where/when checklist and exact original URLs, preserving their case, query parameters, and destinations. Explicitly distinguish 'response window' from resolution time.
7. **ATLAS presentation.** Present as an engaging educational atlas with logical section progression, accessible hierarchy, memorable analogies, and helpful callouts. Use an image-generation tool for a bespoke illustrated banner and a companion infographic/poster if requested or clearly part of /kids invocation. Aim for vivid, polished, legible illustrations; avoid squeezing the entire document into small rasterized text. Prefer text-first output for exact URLs and lengthy directions, with art as support.
8. **WCA–IVY–BIBLIO.** If factual verification/research is requested or necessary, cite authoritative primary sources, distinguish original supplied text from independently verified information, and include a concise bibliography with working URLs and access dates. Do not fabricate citations or imply that invented labels are official. If no external research was performed, state 'Source: user-provided document; no independent verification.'
9. **Copyright.** Include a tasteful footer, e.g. 'Adaptation © [current year] [author if provided]. Original source content remains with its respective rights holders. Unofficial educational parody.' Do not assert ownership of government texts or third-party materials. Never invent author credit.
10. **Quality assurance.** Compare final text to fidelity checklist. Confirm no omitted steps, broken/modified URLs, swapped legal names, changed timeframes, fabricated sources, or false authority. Proofread graphics carefully and place long links in selectable text outside the image. Check accessible alt descriptions and contrast.

## Default deliverables
A. Professional rewrite (full fidelity).
B. Grade-7 hilarious rewrite (full fidelity), suitable for copy/edit/send.
C. Brief action checklist and 'real-world names versus parody names' note.
D. ATLAS-style banner/infographic artwork when image generation is requested or available and the user invokes the full /kids workflow.
E. Copyright and bibliography/source note.

## Special cases
- If input is incomplete, preserve uncertainty and identify missing material.
- If the text is legal, medical, financial, security-sensitive, or urgent, retain unambiguous serious directions and clearly separate comedy from operational guidance.
- Do not turn third-party communications into an apparently authentic new official notice; identify the work as a rewrite/parody.
- If a file format is requested, use the appropriate document/PDF toolchain and validate the resulting file.


## ENGINE compatibility
Canonical engine counterpart: `engines/kids/ENGINE.md`. Preserve `skills/kids/SKILL.md` for legacy consumers. The old skill name and new engine name invoke the same behavior wherever the relevant loader supports both paths.
