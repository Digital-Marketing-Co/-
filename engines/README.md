# Engines

**Engine** is the preferred name for the repository's reusable AI instructions. **Skill** is a backwards-compatible alias. `ENGINE.md` is the preferred engine filename; `SKILL.md` remains a compatibility entry for systems that require it.

Routing convention: `skills/<name>/SKILL.md` → `engines/<name>/ENGINE.md` when an engine counterpart exists. Both names must remain usable; do not delete old paths until consumers have been migrated and tested. Case variants SKILL, skill, SKILLS, skills, ENGINE, engine, ENGINES, engines are terminology aliases, not necessarily filesystem aliases on case-sensitive systems.

Current migrated engine: `engines/disability/ENGINE.md` (also accepts disabled, proceed, P, D). Other skills remain at their existing paths until individually migrated and verified. Avoid global text replacement of code identifiers or external API names.
