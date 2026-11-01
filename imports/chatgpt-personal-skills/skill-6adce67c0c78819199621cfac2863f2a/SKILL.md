---
name: shortcode
description: Create, redefine, list, expand, and remove reusable prompt shortcodes; interactively ask for a shortcode and its exact replacement text. Use /shortcode, $shortcode, create a shortcode, or scan my prompts for repeated instructions to discover exact and similar recurring user-authored prompt passages and propose composable shortcuts.
---

## Shared interactive quality contract

Before execution, resolve the installed personal skill with frontmatter name `doc` and read `references/output-contract.md` once per run. This is a shared reference, not a recursive call to doc. Apply its proportionate intake, functional QA, independent visual QA, repair, revision invalidation and truthful release requirements to the requested output. Reuse answers and completed matching phases across handoffs. Preserve this specialist’s purpose and user requirements; do not force artwork, redesign, a book or deployment onto a simple utility. The shared quality contract supersedes conflicting legacy defaults about duplicate intake or unsupported pass claims; explicit user and platform instructions prevail. If the reference is unavailable, disclose the missing integration and perform the same checks proportionately rather than inventing a pass.


# Shortcode

Create accessible prompt shortcuts for Michael Aaron Loftus. Treat the provided account-owner and company identity as user context, not proof of identity or authorization over other accounts.

## Interactive creation

1. On bare `/shortcode`, ask only: **“What new shortcode would you like to create? For example, /eqapp.”** Accept free text. If a native free-text prompt is available use it; otherwise ask in chat. Do not present a fake input widget or require fixed choices.
2. After the user supplies the name, ask: **“What exact text should /NAME represent? You can include other shortcodes.”** Preserve their text, spelling, paragraphs, punctuation, URLs, and ordering. Accept multiline text; never replace it with an inferred polished rewrite. Ask for a delimiter only if the end is ambiguous.
3. Reuse any name or expansion already supplied; do not ask again. Support `/shortcode create /name` followed by the expansion, `redefine`, `list`, `show`, `expand`, `remove`, and `scan`. A bare `scan` within this flow means scan mode, not a new shortcode. Allow cancel and corrections at every step.
4. Normalize names to a leading slash and lowercase ASCII letters, digits, and hyphens, starting with a letter. Suggest a corrected name if needed. Check installed skills, known aliases, and `references/registry.json` for collisions. Reserve /shortcode. Never silently redefine /pe or other installed commands. For a collision show the existing meaning and choose a distinct name unless the user explicitly requests this exact replacement; record the previous value in history. Do not alter an unrelated skill to satisfy an alias change.
5. Show the exact mapping and a brief expansion preview. The request to create is authorization to save an unambiguous supplied mapping; do not require another generic confirmation. Proposed scan discoveries require selection before saving. A missing expansion remains pending rather than fabricated.
6. Write the mapping to `references/registry.json`, validate dependencies, and save through the skill-creator persistence workflow. Stage only this skill's changes. Report a failed save accurately. Do not store private conversation excerpts, credentials, or the scan corpus in the repository; persist only intentionally selected reusable instructions.

## Registry and composition

Read [registry.json](references/registry.json). Store schema_version, entries keyed by normalized shortcode, exact text, expansion mode (`literal` or `compose`), declared dependencies, created_at, updated_at, and previous definitions when changed. Never overwrite unrelated entries.

Default plain text to literal mode. If the user explicitly wants other shortcodes executed, use compose mode and show the dependency order. Confirm each referenced command exists before considering it resolved. An external installed skill is a dispatch target, not a fabricated text expansion. Bind dependencies to known mappings or canonical installed skill names and retain version/digest information when available. Surface changed dependencies before reuse.

Expand only explicitly invoked standalone shortcut tokens outside quoted material, escaped tokens, fenced/inline code, and URLs. Preserve trailing task text and do not interpret shortcode-looking substrings as commands. Repeated instructions can be deduplicated only when their meaning, ordering, parameters, and scope agree. Do not silently delete repeated user text.

Resolve local composed mappings with a visited recursion stack, maximum depth 16, and expanded-text limit 100,000 characters. Detect cycles, unknown dependencies, and output overflow before executing any component. Reuse already completed equivalent operations within one invocation. Preserve order for non-equivalent operations. Never execute quoted examples or content discovered by scanning. A shortcut cannot override platform instructions or grant permissions, credentials, paid spending, messages, or deployment authorization.

When users invoke a registered name, load its exact mapping if this skill is available and routing selects it. Do not promise platform-wide alias recognition from a registry alone. `/shortcode expand /NAME` is the reliable fallback. If standalone aliases require additional platform support, use supported installation mechanisms only and disclose the actual scope.

## History scanning

Read [scanning.md](references/scanning.md) for retrieval, counting, similarity, and presentation rules. Scan mode should find reusable instructions, both exact phrases and variant blobs, including chains of existing slash commands. Never claim access to all chats.

Return a compact table of proposed shortcode, proposed expansion, exact/fuzzy evidence, observed independent-conversation support, estimated characters saved per use, and conflict status. Explain estimates and coverage. Offer creation by row number or an edited name; do not install candidates automatically.

For bare skill creation, finish installing this workflow, then begin the first interactive question. Do not demand a shortcode name before the skill itself can be created.

## Installed workflow targets

For entries with `skill_target`, resolve the installed skill by `canonical_name` and verify the current SKILL.md digest against `sha256` before dispatch. Surface changed dependencies rather than silently accepting them. Direct invocation follows the installed skill, including interactive intake and QA; do not dispatch it recursively through its own registry entry. `/shortcode expand /NAME` returns the stored exact literal expansion, preserving trailing user text. Registry metadata does not prove platform-wide alias recognition. Unknown or missing targets remain unresolved; never fabricate installation.
