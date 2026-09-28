# Image non-repetition

Every published raster in a `/book` run must be a unique file and a unique picture.

## Two checks

1. Byte unique. SHA-256 of the published file is not shared with any other banner, figure, or raw source used in the same book.
2. Source unique. A mid-chapter figure may not be a copy, crop, fade, or resize of that book's section banner, and a banner may not reuse another chapter's raw generate.

## Fail closed

```bash
python3 /home/workdir/.grok/skills/book/scripts/audit_unique_images.py \
  /home/workdir/artifacts/<slug>/book.json
```

Exit code 1 blocks delivery.

## Also reject

- Two pages show the same picture
- Shared perceptual hash of near-duplicates
- Same remote URL normalized with query junk stripped
- U+FFFC, tofu, empty boxes, or broken-image icons
