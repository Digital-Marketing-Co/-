# Perfect vNext — cross-skill design and QA contract

Status: review-branch implementation overlay; not deployed.

## Design
- Design tokens: midnight navy `#08172C`, cyan `#00C9ED`, ink `#17283B`; body contrast >= 4.5:1 and large text >= 3:1.
- PDFs use static holographic effects: luminous rims, subtle gradients, layered vector geometry and opaque content panels. Never imply motion in PDFs.
- Interactive formats may use volumetric lighting, gyroscopic depth, responsive glass, animated aurora, luminous focus outlines and reduced-motion alternatives.
- Preserve caller typography, factual meaning, citations, source images and /parallax style neutrality.
- Maintain native searchable text, readable tables, print-safe fallback and accessible alternatives.

## QA matrix
1. Inventory all skills/*/SKILL.md and engines; record source ref and SHA-256.
2. Validate frontmatter, links, aliases, dependency cycles, recursive calls and paths.
3. Check prompt-injection boundaries, secrets, Unicode controls/confusables, least privilege and provenance.
4. Run skill-specific functional, negative and deterministic replay tests.
5. Documents: reopen, extract text, inspect glyphs, clipping, bookmarks, contrast, images, footers and links.
6. Math: symbol/operator/index/unit census, dimensional checks, ITQE adjacency and LaTeX render checks.
7. Interactive: keyboard, touch, screen reader, reduced motion, contrast, mobile and performance.
8. Require two actually executed clean full passes. Blocked means NOT_RUN, never PASS.
9. Keep sanitized findings, diffs, hashes, rollback and explicit release status.

## Usage
`python3 tools/perfect-qa/verify_skills.py . --out perfect-qa.json`
`python3 -m unittest discover -s tools/perfect-qa -p 'test_*.py' -v`

Read-only auditor. Findings are review leads, not confirmed defects. No automatic modification of skills.
