# /extract_dir QA protocol

Run after every multi-document batch.

## Inventory checks

- manifest.json url count equals number of slugs
- each slug folder has exactly one PDF
- no Spanish twin folder when English exists
- no second PDF named monograph, folio, print, or clip in the same folder

## Text-duplication checks

Fingerprint the first 400 and last 400 normalized characters of each article.json paragraphs join. If two slugs share a fingerprint, drop the later slug and delete its PDF.

Inside one article.json, drop consecutive duplicate paragraphs and drop paragraphs that are exact title repeats.

Strip share crumbs, "Back to White Papers", "Claim the Deal", "Read Now", newsletter CTAs, and related-card blurbs before build.

## Render checks

```
pdftoppm -png -r 120 $PDF /tmp/extract-dir-<slug>
```

Inspect page 1, a middle page, and the last page.

Fail and rebuild if any appear:

- tofu or missing-glyph boxes
- baked checkerboard in a banner
- clipped title or overflowing image
- repeated identical page body (stuck loop)
- raw backslash LaTeX in body
- nav chrome that survived extract

## Footer checks

Page footers may carry source name + page number from article-clip. If a living copyright stamp is applied, it must read Web Development Corporation with an en dash year range and must not print a class letter A.

## Completeness checks

A PDF with fewer than 2 body paragraphs is incomplete. Re-extract or mark `status: incomplete` in the manifest. Do not pad with generated monograph prose.
