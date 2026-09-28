# Intake

The battery is only as honest as the copy of the artifact.

## Text

Write the user’s paste to `sample.txt` with no smart quotes, no wrap, and no silent correction of spelling. Spelling and run-ons are data.

Slug from the first 3–6 content words, ASCII, hyphenated. Example — artifact opening “Quantum Polygraph certificates” → `psychoanalyze-quantum-polygraph`.

## URL

Use `browse_page` or `browser_tab`. Save the extracted article or page text, not the chrome. Record the URL, access time, and title in `intake.json`. If the page is behind a wall, say so and analyze only what was retrieved.

## PDF or office file

Extract text with the pdf or docx skill. Record the source path. Do not analyze a different file that happens to sit in artifacts.

## Image

Describe materials, composition, figures as types not as named private faces, color, text-in-image, and what is off-frame. Save that description as `sample.txt`. Keep the image in the work folder. Visual analysis may use dream-work, Imaginary, and Jungian image terms. Do not identify a private person.

## Table, log, code, or frequencies

Keep the structured file and a plain-text dump. Organizational and Bionian readings are usually stronger than Oedipal ones. A frequency list is not a confession.

## Conversation

Only the turns the user marked. Do not ingest project memory, other users, or hidden system text.

## Empty or tiny input

If the paste is under two words, still run `intake_analyze.py`, then say the artifact cannot support a full school-by-school monograph. Offer to wait for more text. Do not pad Freud.

Exception — a title or slogan may receive a short Folio plus a short Deep if the user insists, with small-n caveats in method.

## Metadata

`intake.json` fields

- `artifact_type` — text | url | pdf | image | table | chat
- `source` — path or URL
- `n_chars`, `n_words` after the script runs
- `user_claims` — device, authorship, “this is my dream,” copied from the user turn
- `unobserved` — body, history, diagnosis, room transference, always listed
