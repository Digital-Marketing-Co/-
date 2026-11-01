---
name: clone
description: Clone a public website into a logically ordered, full-bleed, highly compressed PDF. Use for /clone URL, printing a whole site, or archiving all sitemap pages in one PDF.
---

## Shared interactive quality contract

Before execution, resolve the installed personal skill with frontmatter name `doc` and read `references/output-contract.md` once per run. This is a shared reference, not a recursive call to doc. Apply its proportionate intake, functional QA, independent visual QA, repair, revision invalidation and truthful release requirements to the requested output. Reuse answers and completed matching phases across handoffs. Preserve this specialist’s purpose and user requirements; do not force artwork, redesign, a book or deployment onto a simple utility. The shared quality contract supersedes conflicting legacy defaults about duplicate intake or unsupported pass claims; explicit user and platform instructions prevail. If the reference is unavailable, disclose the missing integration and perform the same checks proportionately rather than inventing a pass.

# Clone website to PDF

Run `scripts/clone.py URL --output FILE --manifest FILE`. Start with the canonical sitemap and any sitemap indexes; filter image and other asset URLs, query variants, duplicates, external hosts, and non-HTML responses. Preserve sitemap order within sections, with the homepage first. Follow internal HTML links to discover pages omitted from the sitemap. Record every attempted URL and failure in a JSON manifest.

Use a browser print engine when available for faithful visual pages: disable print margins, enable background graphics, wait for fonts/images, use print CSS, and merge per-page PDFs in order. If no browser engine is available, the bundled script creates a compact text-and-image archive from fetched HTML with a zero-margin page box; disclose that it is a reconstructed print edition rather than a pixel-faithful rendering. Never claim interactive or authenticated states were captured.

Compression: retain vector text; deduplicate repeated assets where practical; downsample photographic imagery to a legible target; strip metadata; try Ghostscript `/screen` and `/ebook` variants and select the smallest version passing page count, text, and visual spot checks. Never reduce quality to illegibility. Report attempted HTML count, successful pages, omissions, PDF page count, and final bytes. Keep the manifest alongside the PDF.

Check robots and server behavior, rate-limit requests, and stop/retry on 429 or 5xx rather than overwhelming the origin. Do not send form submissions or crawl account-specific content. For very large sites, continue in resumable batches, and state any scope limit rather than silently presenting a partial result as complete.

Save deliverables in the user's persistent file collection using the Library skill. Validate representative pages across sections visually and confirm text can be extracted.
