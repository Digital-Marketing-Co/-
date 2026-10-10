# Supplied visual assets

Use a section's `banner` object with `path`, `caption`, `prompt`, and `href` for supplied imagery supported by the deep renderer. Resolve relative image paths from the source JSON directory. The adapter preserves these fields and makes visual `path` fields absolute in its output. It does not generate an image or add banners to generated inventory sections.

Apply `interop/references/image-print-contract.md` for fit and print geometry. Fit scripts reside in the reviewed images skill; optional top and bottom blending resides in banner/scripts/apply_tb_alpha_blend.py. Follow the current user's opacity and transparency instructions. Inspect the actual rendered page for trim, aspect ratio, clipping, legible labels, caption placement, and source correspondence.

Use exact plotting or cartographic tools for measured maps, scales, coordinates, and network relations. Clearly identify conceptual illustrations as such. Confirm source date, coordinate reference system, boundaries, legend, and geographic coverage before treating a map as evidence. The atlas adapter cannot validate those properties.
