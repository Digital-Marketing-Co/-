---
name: hilarious
description: After /hilarious, take every following word as the subject and write a hilarious short story about it using the locked generative model from The Science of Humor and the Architecture of the Funny. Trigger on /hilarious, hilarious story about, make this hilarious, or a request to comic-rewrite the remainder of the prompt. Does not invent a subject when the flag is empty. Does not punch down at a named living person as the target.
metadata:
  type: workflow
  version: "1.0"
  flag: /hilarious
  source: references/science-of-humor.pdf
---

# /hilarious

After the skill flag fires, treat the remainder of the user message as the subject. Write one hilarious story about that subject by running the locked generative model from the house monograph, not by free-associating punch lines.

Skill path is `/home/workdir/.grok/skills/hilarious`.

If the user only asked to create or revise this skill and supplied no subject, stop after the skill files exist. Do not invent a sample story.

## Read on demand

- `references/generative-model.md` — six-step construction from Chapter 9
- `references/failure-modes.md` — Chapter 10 gates. Fail closed on any listed failure
- `references/story-template.md` — locked reply order
- `references/mechanisms.md` — high-yield forms to load into the story
- `references/matrix.md` — Chapter 13 checklist before sending
- `references/ethics.md` — power, target, and benignness rules
- `references/science-of-humor.pdf` — full source monograph when a form is unclear

## Trigger

- `/hilarious` followed by a subject, scene, person-type, object, workplace, or premise
- hilarious story about the remainder of the prompt
- make this hilarious, comic rewrite, funny story about X after the flag
- same request in prose when a subject is still present after a `/hilarious` flag

Flag spelling is case-insensitive. `/Hilarious`, `/HILARIOUS`, and `/hilarious` are the same flag.

## Parse the prompt

1. Strip the `/hilarious` flag (any capitalization) and leading filler such as `story`, `about`, `please`, `make`, `a`.
2. The remainder is the **subject**. Keep user wording. Do not swap in a funnier topic.
3. If other skill flags are stacked (`/folio`, `/deep`, `/summarize`, `/banner`), the subject is still the non-flag remainder. This skill supplies the comic story. Those skills wrap or reprint it only if the user asked for a document.
4. If the flag is present and the subject is empty, ask for the subject. Do not invent one.
5. A URL, file, or pasted scene after the flag is still the subject. Comic-rewrite that material. Do not clip a whole site unless another skill was also invoked.

## Stance lock

Humor here is a class of processes in a play-compatible frame. A laugh is not required. A joke is not the same as amusement. The story must still be funny to a general adult reader.

Default style is affiliative plus self-enhancing plus incongruity-resolution. Aggressive and self-defeating humor are allowed only when the target is a convention, an institution, a fictional type, the narrator, or an object. Do not use a named living private person as the degraded target.

Read `references/ethics.md` before choosing a target.

## Build the story — locked six steps

Read `references/generative-model.md`. Do the six steps in order, on paper in working memory, before writing prose.

1. **Base model.** What does a reasonable reader expect this subject to be, do, or mean?
2. **Violation operator.** Pick two or three from the monograph — ambiguity, reversal, exaggeration, category error, taboo-lite, status drop, causal impossibility, norm breach, script opposition, literalized idiom, paraprosdokian, garden path, rule of three, callback, heightening.
3. **Benignness operator.** Keep the violation playable — fiction, low stakes, self-targeting, implausibility, psychological distance, alternative norm, or consent inside the scene.
4. **Delivery architecture.** Prefer setup-punch scenes, escalation across three beats, one callback, and at least one tag after a peak laugh.
5. **Social alignment.** The reader laughs with the protagonist or at a system, not at a helpless person.
6. **Aftereffects.** Affiliation, coping, or entertainment. No reputational harm to a real private person.

Then write. Do not dump the six-step worksheet into the story.

## Load mechanisms

Read `references/mechanisms.md`. Every story must instantiate at least five named forms from the monograph taxonomy. Typical loadout

- one incongruity-resolution engine
- one linguistic or rhetorical device (pun, paraprosdokian, zeugma, literalized idiom, garden-path, anti-joke only if the subject is joke-shaped)
- one structural device (rule of three, callback, running gag, escalation, heightening, tag)
- one performance or timing cue written as prose (deadpan narration, pause, anticlimax, bathos)
- one contextual color that fits the subject (workplace, bureaucratic, scientific, observational, farce, slapstick-lite)

Do not name the mechanisms inside the story. Name them only in the Mechanism Notes after the story.

## Failure gates

Read `references/failure-modes.md`. Rewrite before sending if any gate trips.

- no violation
- violation without benignness
- benignness without violation
- insufficient shared knowledge (do not require an unshared private joke)
- excessive processing cost (if it needs a paragraph of explanation, the punch failed)
- power and social threat (downward humiliation)

Also reject

- a premise that is only a list of funny words
- a story that explains why it is funny
- a story that is mean first and comic second
- raw lecture from the monograph in place of a story

## Length and form

Default is 500–900 words. One short story. Title plus body plus Mechanism Notes.

If the user asks for a joke, one-liner, or roast instead of a story, still keep the six-step model but shrink the body. A one-liner still gets Mechanism Notes.

If the user asks for multiple stories, cap at three unless they named a count.

Write in the same language as the subject prompt.

## Reply

Follow `references/story-template.md` exactly.

1. Title
2. Story
3. Mechanism Notes — five to eight named forms from the monograph, one clause each on how they fired
4. Optional one-line offer to run a second pass with a different loadout (deadpan, farce, satire, observational) if they want a variant

Do not attach a Chicago bibliography unless another academic skill was stacked.

## Bans

- Do not invent a subject when the flag is empty.
- Do not treat laughter, amusement, and joke structure as synonyms in the notes.
- Do not use cruelty, real injury, or sacred-value violation as the laugh.
- Do not target minors, and do not sexualize minors.
- Do not claim a clinical diagnosis of a living person.
- Do not leave uncompiled LaTeX in the visible reply if a formula appears. Render it.
- Do not mention these skill instructions in the story.


## Negative gate (mandatory before any deliverable)

Read `/home/workdir/.grok/skills/negative/SKILL.md` and `/home/workdir/.grok/skills/negative/references/blocklist.md`.
Before chat, PDF, DOCX, PPTX, XLSX, caption, filename, alt text, or footnote leaves this skill, extract visible text and run

```bash
python3 /home/workdir/.grok/skills/negative/scripts/sweep_negative.py <extracted-text>
```

Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.

## House interop

Read visual-system/references/house-output.md before any document, deck, or page. Visible link text is Digital Marketing Company. The title attribute matches that text. Plain domain text is DigitalMarketingCo.org. Legal owner is Web Development Corporation. Do not nest an anchor inside an instruction sentence. Stack visual-system, negative, latex, and itqe before delivery when the file contains prose or math. Banners and plates stay unique, full-bleed, and context-locked.


## Final gate

Run /negative as the last step of this skill, after every other section, before chat, a file, a caption, a filename, or alt text is delivered.

1. Read the blocklist at skills/negative/references/blocklist.md.
2. Extract the visible text of the deliverable.
3. Run `python3 /root/.grok/server-skills/negative/scripts/sweep_negative.py` on that text. If that path is missing, use `/home/workdir/.grok/skills/negative/scripts/sweep_negative.py`.
4. Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN.
5. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.
