# Uniqueness

Every published still in one coffee-table book must be unique by path and by SHA-256 bytes.

Fail closed when

- two pages point at the same path
- two pages share a file hash
- a leaf is a crop, fade, or resize of another page
- the same prompt string is reused

Before delivery run

```bash
python3 /home/workdir/.grok/skills/coffee/scripts/audit_unique_images.py \
  /home/workdir/artifacts/<slug>/coffee.json
```

Exit 1 blocks the PDF.

Record every published path on the page object as `fitted`. Raw generates stay under `stills/raw-*.png` and are not printed.
