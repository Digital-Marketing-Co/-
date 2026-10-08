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

## Read on demand

- references/section-template.md — locked per-word section order

## Trigger

- /breakdown followed by one or more words
- breakdown the words that follow
- word-by-word morphology, morpheme split, etymology of each word after /breakdown
- Same request in prose when a list of target words is still present after a /breakdown flag

Flag spelling is case-insensitive. /Breakdown, /BREAKDOWN, and /breakdown are the same flag.

## Parse the prompt

1. Strip the /breakdown flag (any capitalization) and any leading filler such as the words, these, please.
2. Split the remainder on whitespace, commas, semicolons, slashes that are not the flag, and line breaks.
3. Keep hyphenated compounds as one word (mother-in-law, self-aware). Keep apostrophes inside a token (don't, o'clock).
4. Drop empty tokens, lone punctuation, and the flag itself.
5. Preserve user order. Do not alphabetize. Do not deduplicate unless two adjacent tokens are identical.
6. If the flag is present and the word list is empty, ask for the words. Do not invent a list.

Several words in one prompt are several jobs. Run each word through the same section template. Keep word order.

## Research each word

Use tools when the internal lexicon is thin or the word is rare, technical, coined, slang, a proper name, or a recent neologism.

Search and page sources in this preference order

1. Oxford English Dictionary / OED online entries
2. Etymonline
3. Wiktionary etymology and morphology sections (including reconstructed PIE, Proto-Germanic, Latin, Greek, Old English, Middle English)
4. American Heritage Appendix of Indo-European Roots when a PIE root is claimed
5. Specialty dictionaries for law, medicine, computing, or a named field when the word is a term of art

Cite those sources with inline citations when a web tool returned them. Do not invent first-attestation years. If a date is uncertain, say so.

Do not claim a folk etymology as fact. If a popular story is false, name it as a folk etymology and give the attested path.

## Transform — locked section order

For every word, emit the sections in references/section-template.md exactly, in this order

1. Headword (as the user typed it, then a normalized lemma if different)
2. Pronunciation — IPA when known; say unknown rather than guess a dialect
3. Component parts — table or tight list of every prefix, root, combining form, suffix, inflection, and linking vowel
4. Meaning of each part — one gloss per part, including bound morphemes
5. Put it together — how the parts compose the synchronic sense (including fossilized or opaque pieces)
6. Definition — current standard sense or senses, numbered if several; mark archaic, dialect, or specialized
7. Full etymology — earliest attested form and language, borrowing path, cognates worth naming
8. History and evolution — sense changes by period (OE / ME / EModE / modern, or the equivalent for non-English etyma), pejoration, amelioration, narrowing, broadening, metaphor, taboo replacement
9. Notes — only when needed (homographs, spelling variants, false friends, folk etymology, contested reconstruction)

Do not skip a section. If a fact is unknown, write unknown or not attested in that section. Do not pad with decoration.

English-centric default. If the token is clearly not English, analyze the source language first, then the English borrowing if one exists.

Treat numbers, URLs, and emoji as out of scope. Skip them and say so in one line.

## Reply

1. One-line header — /breakdown and the count of words
2. One complete template block per word, in list order, separated by a horizontal rule
3. Nothing else unless the user also asked a stacked skill or a question

Do not emit a PDF, banner, monograph, or spreadsheet for a /breakdown request alone.

Do not rewrite the user's words. Do not correct spelling before the headword line; if the typed form is a misspelling, show the typed form, then the intended lemma, and analyze the lemma.

Keep each word's block self-contained so a reader can copy one word without the others.

## Stacking

/breakdown only analyzes the word list. If the user also stacked /folio, /deep, /format, /summarize, or another house flag, run /breakdown first on the words, then hand the finished blocks to the other skill only when that other skill was explicitly requested.

/format does not restyle the interior of a breakdown block unless the user quoted a payload for /format separately.


## Negative gate (mandatory before any deliverable)

Read `/home/workdir/.grok/skills/negative/SKILL.md` and `/home/workdir/.grok/skills/negative/references/blocklist.md`.
Before chat, PDF, DOCX, PPTX, XLSX, caption, filename, alt text, or footnote leaves this skill, extract visible text and run

```bash
python3 /home/workdir/.grok/skills/negative/scripts/sweep_negative.py <extracted-text>
```

Exit 1 blocks delivery. Rewrite every hit with the replacement map so the sentence still reads as English and is tighter than the draft. Re-scan until CLEAN. Do not delete a claim to hide a token. Do not leave a hole. Verbatim user source and the blocklist file itself are the only carve-outs.

## House interop

Read visual-system/references/house-output.md before any document, deck, or page. Visible link text is Digital Marketing Company. The title attribute matches that text. Plain domain text is DigitalMarketingCo.org. Legal owner is Web Development Corporation. Do not nest an anchor inside an instruction sentence. Stack visual-system, negative, latex, and itqe before delivery when the file contains prose or math. Banners and plates stay unique, full-bleed, and context-locked.
