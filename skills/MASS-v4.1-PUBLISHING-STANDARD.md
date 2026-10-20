# MASS v4.1 Universal Publishing Standard

Version: 4.1.0
Date: 2026-10-20
Scope: All output-producing skills, including atlas, banner, images, copyright, latex, deep, research, textbook, and related workflows.

## Inheritance
Retain all MASS v3.0 and v4.0 requirements. This standard augments existing skills; it does not replace their domain-specific instructions.

## Visual assets
- Produce contextually relevant, distinct 16:9 section and subsection banners.
- Target one additional relevant supporting image per 500 substantive body words.
- Use horizontal full bleed when the destination format supports it; preserve body-text safe margins.
- Avoid duplicates, distortion, clipping, invented sources, and inaccessible text overlays.
- Optimize images for delivery without compromising legibility.

## Pagination and tables
- Keep headings with their first substantive paragraph or associated content block; move heading to the next page if necessary.
- Keep a complete table on one page whenever it fits within the usable page area.
- Split a table across pages only if its full height exceeds a usable page; prefer row boundaries and repeat column headings.
- Validate page rendering for clipping, blank pages, orphan headings, overflow, and footer collisions.

## Output formats
- Accept an optional document format specification, such as --formats=pdf,docx,html.
- PDF remains the primary output and is always produced, accompanied by supported requested additional formats.
- Validate per-format compatibility and report unsupported or lossy conversions rather than silently substituting outputs.
- Preserve citations, bibliography, mathematical expressions, tables, copyright, and accessibility to the extent supported by each format.

## Quality and efficiency
- Use deterministic rendering, reusable assets, and local tests when possible.
- Minimize Abacus.ai credits without sacrificing accuracy, security, accessibility, or required QA.
- Distinguish planned implementation from executed, tested, and deployed changes.
- Do not claim skill installation or production synchronization until the target environment confirms it.
