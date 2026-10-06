# Manifest

Write `compression-manifest.json` with one object per output path plus an `aggregate` object.

Per item — source_path, dest_path, detected_type, mime, class, original_bytes, final_bytes, saved_bytes, savings_percent, original_sha256, final_sha256, method, tool, params, metadata_policy, tests, result, warnings, collision, unchanged.

Aggregate — input_objects, output_objects, original_bytes, optimized_payload_bytes, packaged_bytes, archive_overhead, saved_bytes, savings_percent, optimized_count, unchanged_count, skipped_count, reverted_count, duplicate_count, container, method, validation.

Also write `compression-report.txt` as a human summary of the aggregate plus notable warnings.
