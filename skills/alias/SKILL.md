---
name: alias
description: Register, resolve, inspect, and safely remove persistent aliases for existing named skills. Usage /alias EXISTING_SKILL NEW_ALIAS.
metadata:
  type: workflow
  version: "1.0.0"
  flag: /alias
  owner: Web Development Corporation
---

# /alias — Skill Alias Registry

## Syntax and argument order

`/alias EXISTING_SKILL NEW_ALIAS`

The FIRST argument is the name of an existing, resolvable skill to invoke. The SECOND argument is the new alias that invokes it. Both accept an optional leading slash. Example: `/alias academy-ivy phd` registers `/phd` → `/academy-ivy`. Do not reverse arguments.

## Registration procedure

1. Parse exactly two whitespace-separated names; reject missing/extra arguments, malformed names, flags, path traversal, and shell metacharacters. Normalize by stripping a single leading slash, retaining the case policy of the skill registry. Allow `[A-Za-z0-9][A-Za-z0-9_-]*`.
2. Resolve the FIRST name against the canonical `skills/<name>/SKILL.md` registry and existing aliases. Do not invent a missing skill. Resolve alias chains to the canonical target, with a visited set and depth limit (32).
3. Reject self-aliasing, cycles, shadowing any real skill name, reserved commands, or overwriting an alias mapped to a different target unless the user explicitly requests reassignment. An identical existing mapping is an idempotent success.
4. Persist mapping in `skills/alias/aliases.json` with schema `{"schema_version":1,"aliases":{"alias-name":"canonical-skill-name"}}`. Keep keys sorted, preserve unrelated mappings, and validate that every target exists. Write atomically where possible.
5. Validate JSON parsing, uniqueness, no cycles, all targets resolvable, and that alias invocation forwards the entire remainder of arguments unchanged to the canonical skill.
6. Commit the registry update to the canonical GitHub repository `Digital-Marketing-Co/-`, then synchronize the same file to `Digital-Marketing-Co/Digital-Marketing-Co` with hash verification. Never claim cross-repository sync unless verified. Respect repository branch protection and conflict checks.
7. When a compatible runtime dispatcher or loader exists, register aliases there or generate the required alias entrypoint and test invocation. A JSON registry by itself does NOT cause ChatGPT, Grok, or other runtimes to recognize a new slash command automatically. Clearly report whether runtime activation is verified.

## Invocation semantics

When a command begins with a registered alias, resolve it to the canonical skill, load that skill's current instructions, and pass through all trailing text, flags, and input unchanged. Resolve before execution and never execute the alias definition as the target. Changes to the canonical skill apply automatically because aliases are references, not duplicated skill text.

## Administrative operations

- `/alias list`: show all registered mappings and their resolution status.
- `/alias inspect NEW_ALIAS`: show its canonical target and whether runtime registration is active.
- `/alias remove NEW_ALIAS`: remove only the named mapping after confirming it exists; do not delete the target skill.
- `/alias help`: show syntax and examples.

## Safety and QA

Do not overwrite canonical skills, run arbitrary commands from alias names, silently change existing mappings, or claim successful installation from a GitHub commit alone. On any error, preserve the prior registry and report the blocking condition. Use the canonical repository as source of truth and treat any secondary copy as a verified mirror.
