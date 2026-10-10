---
name: output
description: Re-present requested files from this conversation or the user's Library for preview and download. Use when the user types /output followed by a filename, file type, topic, or reference to earlier deliverables.
---

# Output

## Quality and capability additions

Read [the task-specific quality profile](references/quality-profile.md) before execution. Use `evals/quality-cases.json` for regression scenarios; its assertions are acceptance criteria, not claims that tests have run. Shared path resolution and output rules live in `interop/SKILL.md`.


Use the words after `/output` to identify the requested existing deliverable or deliverables. If the user does not name one, use the most recent deliverables in the active task. Resolve ambiguous names against the conversation and Library; do not guess a file identity when several plausible files remain.

1. Locate the existing file. Use its known absolute path when still available. For a Library item, resolve its current version and materialize it only if the file is not already accessible locally. Preserve the existing Library identity and filename.
2. Confirm that the selected file exists and that its type matches the request. If it is missing, try the Library version or regenerate it from the available source when feasible. Never link to an absent file or claim that an uncreated file is ready.
3. Return a clickable sandbox link using the exact absolute path. For a PDF, explicitly label the link **Preview and download PDF**; the same link supports both actions in Work Mode. If several PDFs are requested, give one labeled link per file. Do not create a duplicate PDF merely to re-present it.
4. When the user requests a new format, convert and verify the new artifact first, save it according to the applicable file workflow, then link it. If a PDF is requested but only another format exists, generate the PDF only when source content and rendering tools are available.
5. Keep the response short. State any missing file or incomplete conversion plainly. Do not imply that a sandbox link itself saves a file to Library.

Never substitute a similarly titled draft without checking the requested version. Respect user access to private files and do not expose a file outside the user's requested scope.

## Delivery

Run the single delivery gate in `interop/SKILL.md` after task-specific validation. Preserve verified quotations and technical identifiers; report unresolved defects or blockers accurately.
