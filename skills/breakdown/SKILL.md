---
name: breakdown
description: After /breakdown, take every following word and split it into morphemes, prefixes, roots, suffixes, combining forms, and inflectional endings. Explain each piece, reassemble the sense, then give the current definition and the full etymology, history, and evolution of that word. Use when the user types /breakdown, breakdown the words, word-by-word morphology, morpheme split, or etymology of the list after the flag.
metadata:
  type: workflow
  version: "1.0"
  flag: /breakdown
  updatable: true
---

# /breakdown

After the skill flag fires, treat the remainder of the user message as a word list. For each token, decompose the word itself into component parts, explain every part, put the parts back together, then output the definition and the full etymology, history, and evolution of that word.

Skill path is /home/workdir/.grok/skills/breakdown

If the user only asked to create or revise this skill and supplied no word list, stop after the skill files exist. Do not invent sample words.
