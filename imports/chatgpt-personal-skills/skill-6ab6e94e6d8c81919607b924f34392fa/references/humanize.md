# Voice rules

Humanize means a person who knows the subject wrote it on purpose. It does not mean friendly. It does not mean casual slang unless the source already talks that way.

## Do

- Lead with the thing, not with a weather report about the topic.
- Prefer verbs that name an act (`stamp`, `fade`, `tokenize`, `refuse`) over verbs that name a vibe (`enhance`, `elevate`, `empower`).
- Keep one odd concrete noun when the source has one. That is how writing stays attached to the world.
- Let a sentence be short after a long one.
- Keep the house names the house already uses.

## Do not

These strings are automatic rejects at level 4 and 5. Rewrite the sentence.

- In today's rapidly evolving landscape
- In the ever-changing world of
- It is important to note that
- It is worth mentioning
- At the end of the day
- When it comes to
- plays a crucial role
- serves as a testament
- stands as a beacon
- a rich tapestry
- delve / dive deep / take a deep dive
- underscore (as a verb of emphasis)
- leverage (as a synonym for use)
- robust, seamless, cutting-edge, groundbreaking, innovative used as decoration
- not only X but also Y as a reflex
- Let's explore / Let's dive in / Without further ado

Also reject

- a first-person anecdote the source does not contain
- a moral the source did not draw
- a metaphor that introduces a new domain (sports, war, family) the source did not use

## Skill files

When the source is a house skill, humanize only the connective tissue.

Keep byte-stable

- flag names (`/deep`, `/folio`, `/banner`, `/summarize`, `/copyright`)
- paths under `/home/workdir/`
- owner strings and the OpenAction field name
- point sizes, fade inches, page size, filename patterns
- the commented `WCA_COPYRIGHT_PROMPT_APPENDIX` block

A skill file after level 4 should still read as orders to an agent, not as a blog post about the skill.
