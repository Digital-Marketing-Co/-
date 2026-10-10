---
name: copyright
description: Apply one centered canonical copyright notice per page, preserve the body, and verify legal and brand links. Use for /copyright, /copyright YYYY, footer replacement, owner changes, or paginated document creation.
---

# Canonical copyright footer

Read [the quality profile](references/quality-profile.md) and `evals/quality-cases.json`. This directory is the sole source of legal footer text and year logic.

`scripts/notice.py` supplies the default notice: © 2012–CURRENT_YEAR Web Development Corporation. All rights reserved. Use a closed-up en dash; when the current year is not later than the start year, show only the start year. Honor an explicit owner or start year without inventing a jurisdiction or founding date.

## Native document creation

Import the canonical notice helper, reserve a footer band, and render one notice per page. Portable standalone builders may bundle an identical generated copy; validate copy equality whenever this source changes. Build-time current-year text is universally readable. Never describe it as a viewer-updated field unless that behavior was implemented and tested separately.

## Existing PDF replacement

Resolve the user-named file or current requested deliverable. Do not choose an unrelated recent PDF. Inspect page geometry, current notices, footer content, and signatures before modifying. Preserve source files unless replacement is explicitly requested.

Run `scripts/stamp_copyright.py INPUT --start YEAR --owner OWNER --legal LEGAL --out OUTPUT`. The stamp replaces old standalone notices, removes prior footer brand labels and annotations, and adds a single readable form-field fallback plus local viewer-dependent year-update code. Viewers that do not run document JavaScript retain the build year. The footer band must not conceal body content; rebuild the document with reserved space if necessary.

Upper legal label Web Development Corporation uses the exact target https://WebDevelopment.tv used by the lower Web Development, Inc. label. The lower brand labels use Digital Marketing Co. linked to https://DigitalMarketingCo.org and Web Development, Inc. linked to https://WebDevelopment.tv. Keep links legible, centered within their intended cells, and unobscured. Apply user-directed brand placement overrides explicitly.

## Verification

Check every page for one notice, intended owner/year, readable fallback, original body preservation, and correct URI annotations. Stamp twice on a disposable fixture to prove idempotence. Verify year formatting with a future-year fixture. A field with JavaScript is not proof that an actual viewer updated it. Do not claim a notice registers rights or creates copyright that applicable law withholds.

Do not copy legal text or year calculations into other skills or append repeated legal blobs. `scripts/append_prompt_appendix.py` can migrate a legacy footer section to a canonical reference with an explicit file argument; it does not rewrite global instructions. Follow `interop/SKILL.md` for the single delivery gate.
