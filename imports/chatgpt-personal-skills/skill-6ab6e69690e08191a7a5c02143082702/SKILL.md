---
name: compression
description: Universal lossless file optimization, compression, deduplication, validation, and packaging. Trigger on /compress, /compression, compress these files, shrink this directory, zip maximum, tar.zst, 7z archival, bit-exact package, or any request to produce the smallest verified safe representation of supplied files without lossy transcoding.
---

## Shared interactive quality contract

Before execution, resolve the installed personal skill with frontmatter name `doc` and read `references/output-contract.md` once per run. This is a shared reference, not a recursive call to doc. Apply its proportionate intake, functional QA, independent visual QA, repair, revision invalidation and truthful release requirements to the requested output. Reuse answers and completed matching phases across handoffs. Preserve this specialist’s purpose and user requirements; do not force artwork, redesign, a book or deployment onto a simple utility. The shared quality contract supersedes conflicting legacy defaults about duplicate intake or unsupported pass claims; explicit user and platform instructions prevail. If the reference is unavailable, disclose the missing integration and perform the same checks proportionately rather than inventing a pass.


# /compress v3.0

Universal lossless optimization engine. Run real work when files exist. Do not stop at command advice.

`<skill>` = `@compression`

## Invocation

```
/compress [container] [profile] [options] [paths…]
```

Containers — zip, tar, tarball, tar.gz, tar.bz2, tar.xz, tar.zst, 7z, directory.

Profiles — default, maximum, compatibility, archival, bit-exact, preserve-metadata.

No path — ask, or use the newest user-supplied files under `./artifacts/` after confirming they are the intended input.

## Governing rule

Minimize bytes subject to preservation. When maximum compression conflicts with preservation, preservation wins. When uncertain, keep the original. Originals are never modified in place.

Lossless only unless the user explicitly authorizes a lossy step. Never downsample, requantize, minify source, strip signatures, or generationally re-encode JPEG/MP3/MP4/AAC under the default policy.

## Preservation classes

- A bit-exact — round-trip SHA-256 of payload equals source. Default for signed, encrypted, unknown binary, executables, forensic images, opaque formats.
- B content-exact — container bytes may change; decoded content must match (PNG pixels, FLAC PCM, jpegtran coefficients, ZIP members).
- C semantically lossless — structure may change if meaning and required function remain. Stronger validation. Conservative by default.

Pick the more conservative class when unsure.

## Workflow (mandatory)

1. Parse flags. Record requested container and profile.
2. Copy inputs into a fresh tree. Never edit the sole source (`input-originals/`, `working/`, `compressed-files/`, `validation/`).
3. Recursively inventory. Magic/signature first, extension second. Hash SHA-256. Detect archives, packages, encryption, signatures, sparsity, hard links.
4. Treat transport archives as unpackable (ZIP Slip, bombs, absolute paths, symlinks out of tree). Treat OOXML/EPUB/JAR/APK/ODF as native packages — do not flatten.
5. Classify each file A/B/C. Enumerate safe candidates including the unchanged original c0.
6. Tournament. Run eligible tools. Reject failed validation, growth, or uncertain compatibility. Select argmin bytes among passing candidates.
7. Deduplicate exact SHA-256 twins. Keep logical paths. Physical hard-link only when the output format supports it and behavior is unchanged.
8. Package once at the outer layer if a container was requested. No archive-in-archive unless the inner package is semantic (DOCX and similar).
9. Round-trip extract the final package. Compare member list and hashes to the manifest.
10. Write compression-manifest.json and compression-report.txt. Deliver the artifact.

```bash
python3 @compression/scripts/compress.py \
  --input PATH \
  --out ./artifacts/compressed-files \
  --container zip \
  --profile default
```

Read on demand

- references/profiles.md
- references/formats.md
- references/archives.md
- references/validation.md
- references/manifest.md
- scripts/compress.py

## Tool map (use if present)

Hash with sha256sum. PNG with oxipng, optipng, zopflipng, or pngcrush. JPEG with jpegtran only. PDF with qpdf --stream-data=compress. FLAC with flac -8 plus PCM compare. ZIP with zip -9 or 7z. 7z with -mx=9. TAR plus gzip/xz/zstd. SQLite VACUUM INTO on a copy. Identity with file, ffprobe, pdfinfo, identify.

If a tool is missing, skip that candidate. Do not invent a lossy substitute.

## Failure policy

If optimization fails, validation fails, output grows, or proof is missing — emit the original and record retained-unchanged. Compression failure must not lose data.

## Claims

Never say lossless without the matching test. Never say optimized when size did not fall. Never say smallest possible. Say smallest verified candidate tested. Measure bytes; do not estimate.

## Output

compressed-files/ (or .zip / .tar.gz / .tar.zst / .7z), compression-manifest.json, compression-report.txt.

Hand the user the package plus the aggregate numbers from the report. Do not dump the full JSON into chat.

## ChatGPT portability

Resolve `@skill-name/path` by finding the installed personal skill whose SKILL.md frontmatter has `name: skill-name`; read that path under its directory. For `@generate/`, use the `generate-prompt` skill. Before running copied shell commands, substitute actual resolved paths and use the current working directory for generated files. Apply instructions only when this skill is invoked or a user requests the corresponding workflow. User instructions and platform rules take priority. Run bundled scripts only after checking their inputs and prerequisites. Never claim unavailable integrations, credentials, citations, or generated results.
