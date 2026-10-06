# Source types

Ingest the first readable target in this order and stop.

1. An attached raster (JPG, PNG, TIFF, HEIC, WEBP) in the current turn
2. An attached PDF or text file
3. A path the user named under `/home/workdir/`
4. A URL (clip the article or scan first; then transcribe the clipped body)
5. Pasted text in the same turn after the `/transcribe` flag
6. The newest `source.*` already sitting in `/home/workdir/artifacts/transcribe-<slug>/`

## Rasters of printed documents

Treat framed citations, commissions, diplomas, letters, plaques, and caption cards as documents, not as I-Spy scenes.

Read the full frame first. Then, only if a line is clipped or glared

- Crop to the paper, not the wall
- Rotate to the printed baseline
- Lanczos-upscale a line crop at 1.5x or 2x when the glyph height is under about 12 source pixels
- Cap destination at 80 MP

Never generative-inpaint paper. Never invent a word hidden by the frame rabbet.

Also inventory non-text devices that belong to the document

- letterhead
- seal or flag device
- ribbon bar or medal miniature
- wet signature versus printed name
- mat, glaze, and frame (physical-object section only)

Those devices go in `transcript.json` under `devices`, not inside `raw.txt`, unless they carry readable text.

## PDFs

Extract text with pdftotext when the page is born-digital. If the page is a scan, rasterize at 200 dpi and treat it as a document raster.

## Recordings

If the user points at audio or video and asks for a transcript, write timed lines in `raw.txt` as `[mm:ss] text`. Mark uncertain speech `[word?]`. Do not clean filler until pass-1.

## Pasted text

The paste is already raw. Copy it unchanged into `raw.txt`. Still write the lock file.

## What is not a source

- A skill file the user did not name
- A prior folio on a different topic
- Memory about a family member when the pixels do not print that relationship
