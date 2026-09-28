# Emit the restamped file

`/banner` is unfinished until the document file contains one full-bleed still at every body section and every subsection.

Read `@images/references/emit-file.md` and follow it. Use `generate_image` to disk, `apply_tb_alpha_blend.py`, then

```bash
python3 @images/scripts/rebuild_document.py \
  ./artifacts/<slug>
```

Naked PDFs use `stamp-manifest.json` and `stamp_images_into_pdf.py`. Chat-only stills are not the deliverable.
