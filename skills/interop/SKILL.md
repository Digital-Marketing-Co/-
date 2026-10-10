---
name: interop
description: Resolve skill dependencies and coordinate shared evidence, visual, mathematical, copyright, and delivery checks across repository and installed skill trees. Use when composing skills or delivering their artifacts.
---

# Shared skill contract

Read [the quality profile](references/quality-profile.md) before execution. Regression scenarios live in `evals/quality-cases.json`; they are criteria, not executed results.

## Resolve one reviewed revision

Run this checkout's `scripts/resolve_root.py NAME`. It prefers adjacent canonical skill directories, then configured and installed roots, matching frontmatter identity even when the installed directory has a generated identifier. Set `SKILL_ROOT` or pass `--root` to select an explicit verified tree. Do not mix dependencies from different revisions. Reject invalid names, ambiguous identities, and missing dependencies. Resolve legacy command paths before running them.

Use `scripts/resolve_artifacts.py` for writable staging; `--path` or `SKILL_ARTIFACTS_DIR` controls its destination. Follow the host's persistence workflow for final artifacts. A staging path or preview link is not proof of successful persistent saving.

## Composition and precedence

Apply user instructions and platform rules first, then the calling skill's explicit format and fidelity requirements, then shared defaults. Honor deep's all-section full-opacity banners, transparent product imagery, no-shadow requests, raw transcription, and archive fidelity. Do not force visual decoration onto code, audio, link shortening, or simple file retrieval.

Keep the calling procedure, visual design, substantive mathematics, quantitative element tables, paginated copyright, and final delivery checks in that order. Detect recursive dependencies and run each shared gate once. Read `references/evidence-method.md` for research and `visual-system/references/quality-design.md` for visual outputs. Use genuine math rendering for substantive equations; preserve legitimate code syntax, paths, URLs, and unit strings.

## Canonical identity and footer

The house domain is DigitalMarketingCo.org. Preserve the requested brand label and existing verified target. The sole notice owner and year logic live in `copyright/SKILL.md` and `copyright/scripts/notice.py`. Other skills import or render that output; they do not maintain competing legal text. Inspect one notice per page, clickable labels, and original body preservation. A viewer-dependent year update requires a readable build-time fallback and explicit viewer limitations.

Do not overwrite bundled host docx, pdf, xlsx, pptx, or ffmpeg skills. The custom repository pdf guidance can be read without replacing the host tool.

## Single delivery gate

1. Finish task-specific checks; open and inspect the actual final output. Check text, images, equations, notes, links, page geometry, and applicable accessibility requirements.
2. Resolve `negative`; scan generated visible prose, captions, filenames, and alt text once. Preserve verified quotations, technical identifiers, executable source, source URLs, and actual proper names when changing them would falsify information. Report wording conflicts rather than corrupting data.
3. Correct generated prose hits and repeat the scan. A failed or unrun required check must be reported. Do not label untested flows passed.
4. Save using the host workflow, verify availability, and provide the final file or revision link with remaining limits. Never claim a GitHub push installed a skill on another host.

## After a skill edit

Preserve complete directories, validate changed behavior, record the base revision and per-skill provenance, commit, and update GitHub with a checked branch head. Update editable installations separately and verify their saved revision. Report independent repository and installation results.
