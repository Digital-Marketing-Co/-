# Archives

## Transport vs package

Unpack `*.zip` backups. Do not flatten `docx xlsx pptx epub jar apk odt ods odp`.

## Extraction jail

Reject `..`, absolute paths, links that escape the work root, device nodes, FIFOs. Cap member count, declared uncompressed size, and nested archive depth (default 4).

## Collisions

Never overwrite. Prefix with source-archive name. Log every rename.

## Nesting

One intentional outer transport layer. Inner application packages stay packages.

## Security

Untrusted input. Decompression-bomb heuristic — if declared size exceeds a multiple of remaining disk, refuse and keep the archive as Class A.
