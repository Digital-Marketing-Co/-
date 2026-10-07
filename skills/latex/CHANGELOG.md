# Changelog

## 2026-10-06

- Version 1.10. Output documents must pass the /negative skill before delivery (`scripts/run_negative_gate.py`). Figurative AI nouns swap to atlas, gazette, or plate.
- Version 1.9. Orphan headings that are not followed by paragraph text must move to the next page (`references/heading-keep.md`, `scripts/scan_orphan_headings.py`).
- Unrendered operators and operands fail the gate: visible `_`, `\`, fraction `/`, `^`, relation ASCII, and multiplication `*` (`references/unrendered-ops.md`, `scripts/scan_unrendered_ops.py`).
- Skill root path corrected to `/root/.grok/server-skills/latex`.
