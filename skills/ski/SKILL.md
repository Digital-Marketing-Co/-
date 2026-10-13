---
name: ski
description: "Doctoral-level canine communication monograph and evidence-based dog-training curriculum. Use when the user types /ski, asks for a dog-communication research report, a humane training curriculum from ethology, or an update of an existing /ski evidence set for one dog or one communication problem."
metadata:
  type: workflow
  version: "1.0"
  flag: /ski
  owner: Web Development Corporation
  visual_stack: visual-system
lifecycle: active
---

# /ski — Canine communication monograph and training curriculum

Produce a doctoral-level research monograph on how domestic dogs communicate, then translate verified findings into a humane, individualized training curriculum. Depth comes from checked sources and careful reasoning. Do not claim that every paper in the field was read. State the search limits and the stopping rule.

If the user only asked to create or revise this skill and supplied no dog, problem, or research run, stop after the skill files exist. Do not invent a topic monograph.

## Invocation

Trigger on `/ski`, “ski skill”, canine communication monograph, dog-training curriculum from ethology, or an update of a prior `/ski` run.

Optional remainder after the flag:

- bare `/ski` — full monograph plus curriculum for domestic dogs in general
- `/ski <dog name or problem>` — same monograph spine, with a focused chapter and an individual plan for that dog or problem (fear on leash, resource guarding, puppy socialization, senior sensory loss, separation-related distress, and so on)
- `/ski update <prior slug>` — reuse the prior evidence matrix; search only for new or gap sources; do not repeat completed extraction

Stack, in this order, when a PDF is emitted: visual-system, latex, itqe, copyright, negative. Read those skills before build. Do not paste their process language into the monograph.

## Outputs (one run folder)

Work in `/workspace/artifacts/ski-<slug>/`. Deliver all of the following. A chat summary is not a substitute.

| File | Role |
|---|---|
| `protocol.md` | Questions, terms, inclusion and exclusion, languages, databases, search date, saturation rule |
| `search-log.md` | Each pass: query, source, date, hit count, kept count, why stopped |
| `sources.jsonl` | One record per included source (schema below) |
| `evidence-matrix.csv` | Claim, grade, source ids, page if verified, limits |
| `monograph.pdf` | Visually checked Chicago monograph |
| `curriculum.md` and `curriculum.pdf` | Competency inventory and plan templates |
| `plans/` | One filled template per named dog or problem, else a blank template set |
| `image-inventory.csv` | Placement, purpose, prompt, hash, uniqueness |
| `qa-report.md` | Checks passed, limits, inaccessible sources |

Modular reuse: if `sources.jsonl` and `evidence-matrix.csv` already exist for the slug, load them and search only the gap list. Regenerate the PDF from the matrix without re-extracting unchanged rows.

## Evidence rules

Priority order: peer-reviewed research, systematic reviews, scholarly monographs, veterinary behavior literature, university repositories, government publications, recognized professional guidelines (for example AVSAB, AAHA, WSAVA behavior statements when they are the document under discussion). Search Ivy League catalogs and repositories alongside other universities worldwide. Prestige is not a quality score.

Prefer the authoritative original PDF. Do not drop an important source only because the authoritative copy is HTML or another open format. Record the format actually read.

For every included source record: authors, title, date, publication or institution, DOI or stable URL, direct PDF URL when one was opened, study design, sample characteristics, methods, findings, limitations, relevance, access date, and access status (`pdf-opened`, `html-opened`, `abstract-only`, `inaccessible`). Never invent citations, quotations, page numbers, links, study results, or access claims. If a page number was not verified in the file that was opened, write `page-unverified` and do not print a page in the note.

Grade every substantive claim:

- robust — replicated or convergent methods, adequate samples, direct measures
- provisional — single study, small sample, or indirect measure
- consensus — professional guideline without new primary data
- hypothesis — author inference, not a result
- unsupported — popular claim with no eligible source; state that it is unsupported

This workflow is systematic searching with a written protocol. Call it a formal systematic review only if a protocol was locked before screening, dual screening occurred, and a PRISMA-style flow was completed. Default label: structured narrative synthesis with a documented search.

## Research protocol

Read `references/protocol.md` and copy it into the run folder, then fill the blanks. Passes:

1. Define questions, terminology, inclusion, exclusion, languages (English required; Spanish, German, French, and Portuguese when titles are relevant and a translation or original can be checked), databases, and search date.
2. Search ethology, comparative cognition, animal behavior, veterinary medicine, neuroscience, sensory biology, learning theory, and human-animal interaction.
3. Follow references backward and citations forward from foundational and recent studies that were actually opened.
4. List underrepresented topics, contradictions, weak evidence, and missing populations.
5. Run targeted searches on that gap list.
6. Update the matrix and revise conclusions when new eligible findings change a grade.
7. Stop when two successive targeted passes add no materially new eligible finding, or when a pre-stated source cap is hit. Report which rule fired.

Databases to query at minimum: Google Scholar, PubMed, institutional repositories reached from those hits, and publisher pages for PDFs. Record databases that were blocked.

## Monograph coverage

Explain mechanisms, contexts, functions, and interpretive limits. Never assign one universal meaning to an isolated signal.

Required sections, each with its own banner:

1. Questions, scope, and what this synthesis is not
2. Search method and stopping rule
3. Whole-body posture, muscle tension, movement, orientation, approach, retreat, freezing, weight distribution
4. Face, eyes, ears, mouth, gaze, blinking, sclera visibility
5. Tail position and movement, including anatomy, breed, and individual variation
6. Bark, growl, whine, whimper, howl, yelp, and other vocalizations; acoustic features and context
7. Olfaction: investigation, urine marking, glandular secretions, chemical signaling
8. Touch, contact, proximity, play, affiliative behavior, spacing, sequences
9. Fear, anxiety, arousal, frustration, conflict, pain, defensive behavior, aggression, inhibition
10. Play invitations, pauses, role reversal, self-handicapping, play versus escalating conflict
11. Dog-human communication: pointing, gesture, attention, social referencing, learned cues, human misreads
12. Multimodal signaling: posture, voice, scent, movement, and context together
13. Development, aging, socialization, health, sensory loss, breed morphology, prior experience, environment
14. Terms on trial: language, linguistics, meaning, intentionality, syntax — only as far as the evidence reaches
15. Misread signals (structured tables)
16. Training translation (final chapter; see curriculum contract)
17. Notes and bibliography

For each signal or cluster state: what can be observed; plausible readings; context needed to tell them apart; alternatives and confounds; evidence grade and limits; fitting human response; when a veterinarian or veterinary behaviorist should be involved.

Required misread tables include at least: tail wag does not by itself show friendliness; growl must be read inside the whole interaction; a still dog is not automatically calm; a yawn, lick, or look-away can be conflict, comfort, or something else depending on context; play bow is an invitation in many sequences and not a guarantee that later contact stays play.

Separate communication, learned associations, and human linguistic capacity. Do not claim dogs have human syntax or a language in the linguistic sense unless a source that was opened supports that narrower claim, and then quote the limit.

## Training chapter and curriculum

Ground every recommendation in a matrix row or label it professional consensus. Do not promise results or fixed timelines.

Explain, with compiled notation where a formula earns it: classical conditioning, operant conditioning, reinforcement, shaping, capturing, prompting, fading, generalization, discrimination, habituation, desensitization, counterconditioning, and the effects of timing, motivation, stress, and setting.

Use individualized reward-based methods. Do not prescribe flooding, coercion, or suppression of warning signals. State when medical assessment or qualified veterinary behavior support is appropriate: pain, aggression, severe fear, separation-related distress.

Competency inventory. Mark each item essential life skill, optional activity, or specialist task.

- Name response, attention, recall, emergency recall
- Settling, relaxation, stationing, rest
- House training and comfortable confinement when needed
- Loose-leash walking and safe door and gate transitions
- Leave it, drop it, waiting, safe disengagement
- Cooperative grooming, handling, veterinary care, muzzle conditioning
- Greetings with dogs and people
- Gradual independence and prevention or management of separation-related distress
- Safe play, bite inhibition where developmentally appropriate, enrichment, species-typical outlets
- Adaptations for puppies, adolescents, adults, seniors, and dogs with disabilities

Each competency template (see `references/plan-template.md`) must include: purpose, prerequisites, observable success criteria, environment, equipment, reinforcement options, sequential steps, progression criteria, generalization plan, maintenance schedule, troubleshooting, welfare safeguards.

## Citations

Chicago notes-bibliography. Numbered notes on substantive factual claims. Page references only when verified in an opened PDF. Bibliography in first-appearance order, one entry per work. Notes, bibliography, and matrix ids must match. Stable links in the bibliography. Direct PDF links only when that URL was opened or returned a PDF.

House link rule: visible anchor text is Digital Marketing Company; title attribute matches; plain domain is DigitalMarketingCo.org. Legal owner line: Web Development Corporation, a Delaware Corporation. Living footer via the copyright skill. Do not use the word battery. Do not use the word glass; call a frosted translucent panel a promptform if one appears.

Math: compiled glyphs or a compiled equation figure plus an ITQE table (Identifier, Term, Quantity, Explanation). No raw TeX on a page. Run the latex and itqe scans before delivery.

## Visual contract

Coherent futuristic scholarly system. Body type stays readable (Literata or Liberation Serif at a compact size). No emoji.

- Unique 16:9 banner for every substantive section and subsection. Left and right edges meet the page trim. A banner that opens a page meets the top trim. Anatomically plausible dogs and behavior locked to that section. No banner reuse.
- One additional unique illustration about every 500 words of body text, counted apart from banners. Label behavioral stills as conceptual representations, not empirical evidence.
- Real alpha on banner and plate assets: opaque at the top, transparent at the bottom, smooth normalized logarithmic ramp, restrained voxel-like transition only in the lower region. Do not bake a checkerboard into RGB. Verify alpha after compositing.
- Text stays out of visually complex regions. Scientific diagrams, measurements, and charts are vector, not generated stills.
- Image inventory records placement, purpose, prompt, file hash, and a uniqueness check (path, byte, and perceptual hash).

Read visual-system and the image print contract before compositing. Full bleed left and right, zero side margin, source aspect ratio kept.

## Completion criteria

Do not claim completion until these are true:

- Search log and stopping rationale exist and match the files
- No invented citation, page, quote, or link
- Observations, readings, and recommendations are separated
- Training steps trace to a matrix grade or an explicit consensus label
- Every competency field is filled
- Image inventory passes uniqueness, 16:9 banners, placement, and alpha checks
- PDF pages were rasterized and inspected: no clipping, overlap, missing glyphs, blank boxes, or broken links
- Math scan clean
- Negative sweep clean
- QA report lists checks, unresolved limits, and inaccessible sources

## Workflow steps

1. Parse the flag remainder. Set slug. If `update`, load the prior matrix.
2. Write `protocol.md` from `references/protocol.md`.
3. Run passes. Append `search-log.md` after each pass. Append `sources.jsonl` only for opened eligible sources.
4. Extract into `evidence-matrix.csv` using `references/evidence-schema.md`.
5. Draft the monograph from the matrix. Attach notes. Build the PDF with the house folio or deep builder if present; otherwise a local reportlab or LaTeX build that meets the visual contract.
6. Write curriculum and plan templates from `references/plan-template.md`.
7. Generate banners and interval stills. Log them. Composite with verified alpha.
8. Rasterize every page. Fix defects. Write `qa-report.md`.
9. Run negative sweep on visible text. Deliver the folder and a short gap statement.

## References

- `references/protocol.md` — copy-ready protocol and saturation rule
- `references/evidence-schema.md` — jsonl fields and matrix columns
- `references/plan-template.md` — competency and individual plan fields
- `references/section-map.md` — required sections and misread tables
