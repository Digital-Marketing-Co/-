# Format rules

## Class A (leave bytes; outer-pack only)

Signed PDF/OOXML/PE/JAR; encrypted blobs; unknown magic; disk images; model weights; executables; installers.

## PNG

Class B. optipng/oxipng/zopflipng. Compare decoded RGBA. Keep ICC, alpha, APNG frames.

## JPEG

Class B only via jpegtran (Huffman / progressive). Never cjpeg/imagemagick quality rewrite.

## GIF / lossless WebP / APNG

Lossless only. Validate every frame, delay, loop, disposal.

## Audio

Lossy codecs — remux only. FLAC/ALAC/WAV — recompress and PCM-compare.

## Video

Stream copy / remux. No generational encode.

## PDF

qpdf structural compress. No downsample, no JPEG requantize, no font drop, no tag drop. Signed PDF stays Class A.

## OOXML / ODF / EPUB / JAR / APK

Native packages. Rezip members only when spec allows. Do not flatten. Signed packages stay Class A.

## Text / SVG / source

Do not minify unless authorized. Outer compressor exploits redundancy.

## SQLite

VACUUM INTO a copy. Integrity check + row counts.

## Fonts

No outline edits. WOFF2 only when use-case and license allow; keep the original unless conversion was requested.

## Sparse files

Do not expand holes. Record logical vs allocated size.
