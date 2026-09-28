# Article extraction notes

Use `scripts/extract_article.py` first. Inspect `article.json` before building the PDF.

## What belongs in the clip

Keep:

- Headline (`h1` / `og:title`)
- Byline and published date
- Body paragraphs in source order
- Featured / hero image, only if it is not the same plate as an in-body figure
- In-body photographs and figures in source order (`blocks` in article.json)
- YouTube (or similar) embeds as their thumbnail plus the iframe `title` as caption

Drop:

- Site chrome (nav, menus, footers)
- Sidebars, trending, related, recirc cards
- Share / comment / newsletter widgets
- Ads, sponsor units, tracking pixels, logos, avatars
- Captions that are ads, "related", "trending", or "subscribe"
- Duplicate files of the same plate (og:image + hero, jpg + webp, srcset size variants)

## Caption rule

Keep a caption only when it is attached to that image in the article (figcaption, iframe title, or a short alt that names the subject). Never invent a photo credit. Empty caption is correct when the source had none.

## If the extractor misses

Common CMS hooks already tried: `article`, `[itemprop=articleBody]`, `.entry-content`, `.post-content`, `.article-body`, `.td-post-content`, Analyzing America `.aaee-article-copy-100`.

If paragraphs look like a homepage dump:

1. Re-open the saved `source.html` in the work dir
2. Find the real body class / id
3. Edit `article.json` by hand (delete junk paragraphs, drop leftover card images)
4. Then run `build_cm_pdf.py`

The builder prints every unique image at 100 percent page width (x = 0, no left or right margin or padding), LANCZOS-upscales when the source is narrower than 150 dpi at letter width, keeps source aspect, and walks `blocks` so each plate stays next to the paragraph it followed or preceded in the source. Edit `blocks` if a figure landed in the wrong slot.

YouTube embeds live in `<iframe src="https://www.youtube.com/embed/ID">`. Thumbnails:

- `https://img.youtube.com/vi/ID/maxresdefault.jpg`
- fallback `hqdefault.jpg`

## Visual QA (required)

After the PDF is written:

```bash
pdftoppm -png -r 150 output.pdf /tmp/clip-page
```

Open every page PNG. Fail the job if you see tofu (□), black boxes, clipped text, overlapping images, leftover sidebar copy, or any left/right gutter around a plate. Rebuild after fixing `article.json` or layout sizes. Latin Modern Roman is already bundled as TTF under `assets/fonts/` — do not register the TeX OTF files; reportlab rejects CFF outlines.
