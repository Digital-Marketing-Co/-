# Raw lock

`raw.txt` is a diplomatic transcript. It is evidence. Later passes may explain it. They may not edit it.

## Reading order

1. Agency or letterhead line
2. Place line
3. Award or action sentence
4. Recipient block (rank, name, service)
5. Body citation paragraphs in print order
6. Signature name
7. Signature office
8. Devices with readable text (ribbon inscription, seal motto) last

If the photograph cuts a line, keep the visible fragment and write `[cut off]` at the lost edge. Do not complete the sentence from a later paragraph or from memory.

## Marks

| Mark | Meaning |
| --- | --- |
| `[illegible]` | glyphs present, not readable |
| `[cut off]` | paper or frame hides the rest of the line |
| `[word?]` | best guess, low confidence |
| `[sic]` | obvious printed error kept as printed |
| `(signed)` | after a handwritten name that also has a printed office line |

Do not use ellipses to hide uncertainty. Do not silently drop a clipped first letter.

## What stays

- Original line breaks that correspond to printed lines
- ALL CAPS names and medal titles
- Hyphenation at a printed line break (`naviga-` / `tional`)
- Office titles exactly as set
- Punctuation exactly as set

## What never enters raw.txt

- Expanded abbreviations (`United States Navy` when the line prints `UNITED STATES NAVY` is fine because that is the print; `USN` must stay `USN`)
- A gloss
- A date taken from the filename
- A family relationship
- A reconstructed missing word

## Lock procedure

```bash
python3 /home/workdir/.grok/skills/transcribe/scripts/init_workdir.py \
  --slug <slug> --source <path>
# after writing raw.txt
cp raw.txt raw.lock.txt
python3 /home/workdir/.grok/skills/transcribe/scripts/qa_transcript.py \
  /home/workdir/artifacts/transcribe-<slug>
```

`qa_transcript.py` hashes `raw.txt` against `raw.lock.txt`. A mismatch is a hard fail. Fix by restoring the lock, not by updating the lock to match a rewritten raw.
