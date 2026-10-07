# File-inflation forensic gate

Defensive scan only. `scripts/scan_file_inflation.py` reads a finished PDF and exits 1 when the container shows bloat or a hidden instruction. It does not rewrite the file and it does not describe how to plant a payload.

## What it flags

- More than one `%%EOF` marker (incremental update that can hide an appended object).
- A missing `%%EOF`.
- `/JavaScript`, `/JS`, `/Launch`, `/EmbeddedFile`, `/RichMedia`, `/XFA`.
- `/OpenAction` unless the house year field `WCACopyrightYear` is also present.
- An additional-actions dictionary `/AA` outside that house year action.
- Decoded or raw streams containing instruction-override phrases (`ignore previous instructions`, `system prompt`, `prompt override`, `jailbreak`, and the same family).
- File size above 2,500,000 bytes per page.
- A large file whose decoded printable text is under 0.4 percent of the container and under 2,000 printable bytes.
- A stream of at least 200,000 bytes whose repeated-byte or whitespace share is at least 0.85.

## What it does not do

It does not attribute a file to any person, service, or military office. A hit is a container defect. A clean result is not a proof of authorship. The house year action is the only OpenAction carve-out.

## Command

```bash
python3 /root/.grok/server-skills/latex/scripts/scan_file_inflation.py \
  /home/workdir/artifacts/<file>.pdf
```

Exit 1 blocks delivery. Rebuild from source. Do not strip a signed original in place. Lossless size reduction, when requested, is a separate `qpdf` stream recompress after this scan is clean.
