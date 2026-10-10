# Composition contract

Use the user's stated spatial subject, author, scope, and publication constraints. Required source shape is defined by assets/schema/atlas.schema.json. The adapter validates that structural contract plus unique node IDs, connection endpoints, and the coordinate reference-system note. It preserves unknown source fields for handoff.

The PDF wrapper delegates typography, page construction, and footer drawing to the reviewed deep renderer. Read deep/assets/typography.py and the shared copyright policy rather than duplicating their values here. Use `--out` to choose the public PDF path. Adapted source JSON is written alongside the atlas source.

Structural validation does not establish research completeness, coordinate accuracy, source quality, or page quality. Verify those separately and report unresolved scope. Supplied notes must support the claims and coordinate values they accompany. Do not fabricate geography, references, figures, or audit results.
