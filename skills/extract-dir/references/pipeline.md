# /extract_dir locked pipeline

## Discover

Parse the sitemap first (`/sitemap.xml` or a path-specific sitemap). Keep `<loc>` values whose path matches the requested directory (default `/white-papers/`).

If the sitemap is incomplete, also collect unique hrefs from the directory index page. Union the two sets, then dedupe.

## Dedupe keys

For each URL compute:

- scheme+host+path with trailing slash stripped
- language: drop `/es/` and `/libros-blancos/` when an English twin exists
- slug: last path segment

Keep one record per slug. Prefer the shorter canonical sitemap loc over a marketing-length slug if both 200.

## Extract

```
python3 <clip>/scripts/extract_article.py "URL" --out $ROOT/<slug>
```

article.json must contain title, url, paragraphs (article only), images (hero + in-body).

Copysite fallback (page mode only) when paragraphs < 3 after extract:

```
python3 <copy>/scripts/copysite.py "URL" --out $ROOT/<slug>/mirror --zip /tmp/unused-extract-dir.zip --mode page
```

Then re-run extract against the local mirror index.html via file URL or a repaired JSON edit. Delete the zip if it was only a fallback; do not deliver a second artifact.

## Banner

One plate per document. Prompt or compose from the title plus three concrete nouns in the first two paragraphs. Fade with apply_banner_fade.py. Insert the faded PNG as images[0] in article.json only when the extract has no usable hero. If a hero already exists, keep the hero and store the banner under banners/ without embedding it a second time in the body.

## Build

```
python3 <clip>/scripts/build_cm_pdf.py $ROOT/<slug>/article.json --out $ROOT/<slug>/<Title_Slug>.pdf
```

Optional post-stamp of the living house footer is allowed. Do not generate a second PDF.

## Monograph gate

Run phd-ivy-monograph only when ALL of these are true:

- user explicitly asked for a new monograph, not a reprint
- the source page is a stub, outline, or abstract rather than a finished paper
- no article.json paragraphs would be copied into monograph.json body

Otherwise skip. Record `monograph: skipped-anti-duplication` in manifest.json.
