# Uniqueness

Every published still in one book must be unique by path, by SHA-256 bytes, and by prompt string.

Fail closed when:

- two pages point at the same path
- two pages share a file hash
- two pages share a prompt
- a leaf is a crop or resize of another page

Before delivery:

```bash
python3 /root/.grok/server-skills/coffee/scripts/audit_unique_images.py \
  /workspace/artifacts/<slug>/coffee.json
```

Exit 1 blocks the PDF.

Record the printed file on the page object as `fitted`. Raw generates stay under `stills/raw-*.png` and are not the audit key.
