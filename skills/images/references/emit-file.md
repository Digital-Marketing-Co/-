# Emit the restamped file

`/images` and `/banner` are unfinished until a real file exists with the stills in reading order.

## Deliverable

The public object is the rebuilt document, not a chat carousel.

- PDF sources → one PDF under `./artifacts/` using the parent series filename (`…-wca-folio.pdf`, `…-wca-atlas.pdf`, the /deep slug, or the source stem plus nothing invented).
- DOCX / PPTX sources → restamp through those skills and emit that file.
- Chat-only `Render Generated Image` stills with no file on disk are a defect.

## Generate to disk

Use the house `generate_image` tool so each still lands on disk. Copy or move it into the slug folder.

- Section banner raw → `<slug>/banners/raw-NN.png`
- Section banner published → `<slug>/banners/banner-NN.png` after `apply_tb_alpha_blend.py`
- Subsection banner → `<slug>/banners/banner-NN-SS.png`
- Mid-text plate → `<slug>/figures/fig-{section}-{k}.png`

Do not leave the only copy under `artifacts/imagine_images/`. Do not treat a streamed chat image as the published raster.

## Attach then rebuild

1. Set `banner.path` (and caption, prompt, href, source_note) on every body section and subsection.
2. Set each mid-text `figures[]` object with path, caption, prompt, after_paragraph or after_page.
3. Rebuild

```bash
python3 @images/scripts/rebuild_document.py \
  ./artifacts/<slug>
```

That script runs `build_folio_pdf.py`, `build_deep_pdf.py`, `build_atlas_pdf.py`, `build_book_pdf.py`, or `build_list_pdf.py` when the matching JSON exists.

4. Naked PDF with no JSON → write `<slug>/stamp-manifest.json` and run

```bash
python3 @images/scripts/rebuild_document.py \
  /path/to/source.pdf \
  --manifest ./artifacts/<slug>/stamp-manifest.json
```

`stamp_images_into_pdf.py` inserts one full-bleed letter page (`x = 0`, 16-9 height from page width) immediately after each `after_page`. Heading pages stay intact. The plate opens the next page.

## Manifest shape

```json
{
  "source_pdf": "/home/workdir/attachments/source.pdf",
  "output_pdf": "./artifacts/<slug>/<stem>.pdf",
  "items": [
    {
      "kind": "banner",
      "path": "banners/banner-01.png",
      "after_page": 2,
      "heading": "I. Introduction",
      "href": "https://digitalmarketingco.org/r/?src=images-banner&section=intro"
    }
  ]
}
```

`after_page` is 1-indexed on the source PDF. Place a section banner after the page that prints that heading. Place a mid-text plate after the page that closes its 500-word window.

## Fail closed

- No output path printed to the user → job is not done.
- Builder JSON present but `banner.path` missing on a printed body heading → regenerate, do not crop a parent banner.
- Stamped PDF page count must equal source pages plus the number of manifest items.
- Then run uniqueness audit, render gate, and negative sweep on the output file.
