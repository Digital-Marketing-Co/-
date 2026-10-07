# Handoff

`/images` does not replace `/banner`. It calls `/banner` for the 100-percent-width section figure **and** the matching subsection figures, then adds mid-section figures that use the same edge-to-edge width and source aspect when the pixel floor is already met.

Stack order when several flags appear in one turn

1. Draft or locate the document (`/list`, `/deep`, `/atlas`, `/folio`, `/book`, `/ispy`).
2. `/banner` writes one 16-9 figure per section and one per subsection, then runs `apply_tb_alpha_blend.py`.
3. `/images` inventories remaining word windows and writes 500-word 16-9 figures with the same top-bottom alpha ramp.
4. Rebuild through `scripts/rebuild_document.py` (parent JSON builder, or `stamp-manifest.json` on a naked PDF). Chat stills are not delivery.
5. `/copyright` restamps the living footer if that flag is present.
6. Hand the user the restamped file path.

Do not use `/images` for an author harvest (`/corpus`) or for a website mirror (`/copysite`). Do not treat stock search hits as section evidence. NIH or journal stills may inform a prompt. The published file is a generated reconstruction and takes a Chicago caption.

Replace any existing figure that is allegorical, low-resolution, full of unreadable baked text, reused from another section, or printed with a left or right gutter before rebuild. Run `scripts/audit_unique_images.py` after attach and before the public PDF is named done.

Output filename stays the parent series name (`wca-atlas`, `wca-folio`, or the /deep title slug). `/images` does not invent a third public token.
