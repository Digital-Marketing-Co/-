# Release evidence format

Run `python scripts/quality_gate.py MANIFEST.json` using the resolved doc skill path. Keep the manifest/evidence with the working output; final QA is evidence, not an automatic guarantee. Relative paths resolve against the manifest directory. Compute SHA-256 from real final bytes. Each check and visual-unit record must also carry artifact_sha256 matching the final artifact; a matching revision string alone is insufficient. Never invent evidence or observations to satisfy this validator.

Required top-level fields:

- `schema_version`: 1; nonempty `run_id` and string `revision`.
- `output_kind`: document, app, dataset, text, image or media. Use the ACTUAL target's kind for check/grow/publish/translate; validate each delivered artifact separately.
- `artifact`: `{ "path": "final.pdf", "sha256": "ACTUAL_DIGEST" }`. For an app use the immutable source/build snapshot being inspected and record deployment version in notes; this validator cannot independently query live deployments.
- `required_checks`: list of requirement IDs including the baseline IDs in quality_gate.py; add all user-specific acceptance checks. Never remove a required user check to get a pass.
- `checks`: records `{ "id": "content", "revision": "r2", "artifact_sha256": "ACTUAL_FINAL_ARTIFACT_DIGEST", "status": "PASS", "note": "Actual result and method", "evidence": [{ "path": "check.log", "sha256": "ACTUAL_DIGEST" }] }`. Failed/blocked/untested required items block a finished release. N/A needs an explicit reason in note and must not excuse a requested requirement. N/A applicability needs human judgment; the script cannot prove it.
- `expected_visual_units`: complete inventory such as `["page:1", "page:2"]` or route/state/viewport/locale IDs. For a final PDF pdfinfo independently checks that all final pages are included. Other formats require inventory from the actual renderer/exporter or app route/state map; this gate cannot discover omitted routes or locale combinations.
- `visual_units`: records `{ "id": "page:1", "revision": "r2", "artifact_sha256": "ACTUAL_FINAL_ARTIFACT_DIGEST", "status": "PASS", "observation": "Actual detailed visual inspection", "reviewer": "agent or person identifier", "evidence": { "path": "page-1.png", "sha256": "ACTUAL_DIGEST" } }`. Inspect the image, not just its existence. Use private evidence; do not automatically save screenshots as user-facing files.
- `unresolved_defects`: array; must be empty for a finished release. Preserve defects in working/draft manifests instead of deleting them to pass.

Baseline check IDs:

| Kind | Required IDs |
| --- | --- |
| document | requirements, content, sources, links, accessibility, visual |
| app | requirements, functional, persistence, security, accessibility, visual, build |
| dataset | requirements, schema, counts, exports, accessibility, visual |
| text | requirements, content, readability, visual |
| image/media | requirements, integrity, visual |

Only a dataset marked `machine_readable_only: true` may mark visual N/A. Plain text uses direct structure/readability inspection with text-file evidence. Missing browser, renderer or reader must be represented as BLOCKED/NOT TESTED, never invented passes. The gate reports PASS for validated recorded evidence only; actual correctness and visual inspection still require their respective tools and observations. A marked draft may be delivered with a BLOCKED report and clear limitations. No execution of this script is needed for a one-line utility reply or ordinary conversation.
