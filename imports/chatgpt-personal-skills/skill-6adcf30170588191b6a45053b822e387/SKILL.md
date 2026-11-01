---
name: data
description: "Build verified datasets, spreadsheets and quantitative inventories with interactive scope selection and presentation QA. Use /data for research tables, rankings, CSV, JSON or spreadsheet outputs."
---

# Data

Resolve the installed personal skill named `doc` and read its `references/output-contract.md` once per run. Read it as a reference; do not invoke doc or restart its intake.

## Interactive start

Show the proposed output plan and reuse prior choices. Ask at most two useful questions only for missing material context: Dataset universe/time range and required fields or export format. Honor explicit no-questions/bypass settings. Use the shared 4629 style phase for a new designed output, once across handoffs.

## Execution

Build the requested dataset and its usable presentation. Define the schema, units, source provenance, scope, retrieval dates, normalization, deduplication and update rules. Distinguish observed values from estimates and unknowns. Sort by the stated variable, descending when appropriate to the brief. Provide the requested machine-readable or spreadsheet output; keep schema/data-dictionary details internal when the user requests a single data-only file, otherwise include a useful data dictionary, with interactive tables only when requested or useful. Verify counts, formulas, completeness claims, constraints and exports. Never replace a requested large dataset with invented records or an unverified count.

## Specialist routing

Use Spreadsheets for workbooks and charts; relevant research sources for records; app only for a requested working interface.

## Required QA and visual QA

Verify source provenance, schema/types, units, nulls, row/unique counts, deduplication, ranking ties, formulas and round-trip exports. Check human-readable tables/charts for label collisions, number/date formats, legends, contrast and narrow-screen readability. Pure machine-readable data may mark visual QA not applicable with a concrete reason; any preview or workbook still needs inspection. Follow the shared repair and release gates. Never mark unexecuted checks passed.

Read [the endpoint quality profile](references/quality-profile.md) for requirements and tests.
