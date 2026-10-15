# Document validation matrix

Each check is an acceptance requirement, not proof of execution.

| Format | Structural validation | Visual validation |
| --- | --- | --- |
| PDF | Reopen, font and glyph coverage, text extraction, link and mathematical table integrity | Rasterize and inspect every page for clipping, missing symbols and overlaps |
| DOCX | Validate package, styles, relationships, alt text and tables | Render and inspect every page in a compatible engine |
| PPTX | Validate slides, notes, relationships and shape bounds | Render and inspect every slide |
| XLSX | Validate formulas, totals, data types, chart sources and sheet integrity | Inspect printable ranges, column widths and visible data |
| HTML | Check semantics, links, accessibility, responsive structure | Desktop, mobile and print screenshots |
| PNG, JPEG, WebP | Decode, dimension and aspect validation, duplicate hashing | Full-resolution visual inspection |
| SVG | Parse XML, verify viewBox and assets | Rasterize and inspect |
| CSV, TXT, MD, RTF, ODS, ODT, ODP | Verify encoding, structure and native format validity | Render where supported; report blocked where not |

Record actual tool availability, checks executed, pass/fail/blocked, artifact hashes and reproducible evidence. Do not mark an unexecuted visual inspection as passed.
