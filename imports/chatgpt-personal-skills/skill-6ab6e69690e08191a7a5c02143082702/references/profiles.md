# Profiles

## default

Integrity, quality, function, compatibility, recoverability, then size. Strong but practical settings. Stop when extra CPU saves a negligible number of bytes.

## maximum

Evaluate every available safe encoder and high setting. Compare byte counts. Keep the smallest passing candidate. Time may be large. Quality may not be traded.

## compatibility

Prefer ZIP, gzip, widely installed decoders. Avoid zstd ultra, 7z solid archives that old tools cannot open, unless the user named them.

## archival

Keep metadata, timestamps, permissions, open formats, checksums, self-description. Do not strip EXIF, ICC, licenses, or provenance for a few bytes.

## bit-exact

Force Class A on every payload. Only outer-container compression of unmodified members.

## preserve-metadata

Treat all metadata as REQUIRED. No chunk/tag stripping even when technically dispensable.
