# Compiled plates versus section stills

`/latex` compiles mathematics and listings. `/banner` and `/images` generate context-locked stills. Those jobs do not share files.

## Rules

- One `render_snippet.py` output belongs to one equation id. Do not copy that PNG into a second equation, a banner slot, or a 500-word mid-text slot.
- A banner or mid-text still must not contain raw TeX and must not display an equation unless that exact compiled relation already sits in the node with an ITQE table of its own.
- When `/latex` is stacked with `/banner` or `/images`, run `images/scripts/audit_unique_images.py` on the document JSON before delivery so a snippet plate cannot collide with a section still by path or bytes.
- Beauty and context for photographic stills live in `visual-system/references/prompt-engineering.md`. This skill does not relax that contract.
