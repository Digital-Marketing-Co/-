#!/usr/bin/env python3
"""Fail-closed PDF inflation and hidden-instruction forensic scan.

Defensive gate only. It measures container bloat, incremental updates,
active content, and instruction-override strings inside streams. It does
not rewrite a file, does not emit an override, and does not describe how
to plant one.

Exit 0 when every tested file is within the house bounds.
Exit 1 when any inflation, active-content, or override marker is present.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import zlib
from pathlib import Path

# Bytes of declared stream payload per page above this, with little extracted
# text, is treated as inflation. Tuned for letter-size illustrated reports.
PAGE_BYTE_CEILING = 2_500_000
TEXT_RATIO_FLOOR = 0.004  # extracted text bytes / file bytes
PAD_RATIO = 0.85  # repeated-byte or whitespace share inside one stream
STREAM_PAD_FLOOR = 200_000

OVERRIDE_PATTERNS = (
    rb"ignore previous instructions",
    rb"ignore all prior instructions",
    rb"system prompt",
    rb"prompt override",
    rb"you are now",
    rb"disregard the above",
    rb"server-side interface",
    rb"jailbreak",
    rb"</?system>",
)

ACTIVE_MARKERS = (
    b"/JavaScript",
    b"/JS",
    b"/Launch",
    b"/EmbeddedFile",
    b"/RichMedia",
    b"/XFA",
)


def _streams(blob: bytes) -> list[bytes]:
    out = []
    for match in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", blob, re.S):
        raw = match.group(1)
        try:
            out.append(zlib.decompress(raw))
        except Exception:
            out.append(raw)
    return out


def _pad_ratio(buf: bytes) -> float:
    if not buf:
        return 0.0
    sample = buf[:2_000_000]
    counts: dict[int, int] = {}
    ws = 0
    for b in sample:
        counts[b] = counts.get(b, 0) + 1
        if b in (0, 9, 10, 13, 32):
            ws += 1
    top = max(counts.values()) / len(sample)
    return max(top, ws / len(sample))


def scan_pdf(path: Path) -> list[str]:
    hits: list[str] = []
    blob = path.read_bytes()
    size = len(blob)
    eof = blob.count(b"%%EOF")
    if eof > 1:
        hits.append(f"incremental-update: {eof} EOF markers (possible appended payload)")
    if eof == 0:
        hits.append("missing-eof: file does not end a normal PDF generation")
    structural = re.sub(rb"stream\r?\n.*?\r?\nendstream", b" ", blob, flags=re.S)
    for marker in ACTIVE_MARKERS:
        if marker in structural:
            hits.append(f"active-content: {marker.decode('ascii', 'replace')}")
    if b"/OpenAction" in structural and b"WCACopyrightYear" not in structural:
        hits.append("active-content: /OpenAction without the house year field")
    if b"/AA" in structural and b"/OpenAction" not in structural:
        hits.append("active-content: additional-actions dictionary")
    streams = _streams(blob)
    decoded = b"\n".join(streams)
    for pat in OVERRIDE_PATTERNS:
        if pat in structural.lower():
            hits.append(f"override-string: {pat.decode('ascii', 'replace')}")
        for stream in streams:
            if not stream:
                continue
            printable = sum(1 for b in stream[:4000] if 32 <= b < 127 or b in (9, 10, 13))
            if printable < 0.8 * min(len(stream), 4000):
                continue
            if pat in stream.lower():
                hits.append(f"override-string: {pat.decode('ascii', 'replace')}")
                break
    pages = 1
    info = subprocess.run(
        ["pdfinfo", str(path)],
        capture_output=True,
        text=True,
    )
    if info.returncode == 0:
        for line in info.stdout.splitlines():
            if line.startswith("Pages:"):
                pages = max(1, int(line.split()[1]))
                break
    else:
        pages = max(1, structural.count(b"/Type /Page") + structural.count(b"/Type/Page"))
        pages = max(1, pages - structural.count(b"/Type /Pages") - structural.count(b"/Type/Pages"))
    per_page = size / pages
    if per_page > PAGE_BYTE_CEILING:
        hits.append(
            f"size-inflation: {size} bytes over {pages} pages "
            f"({per_page:.0f} bytes/page > {PAGE_BYTE_CEILING})"
        )
    textish = sum(1 for b in decoded if 32 <= b < 127 or b in (9, 10, 13))
    image_objects = structural.count(b"/Image") + structural.count(b"/XObject")
    ratio = textish / size if size else 0
    if size > 400_000 and ratio < TEXT_RATIO_FLOOR and textish < 2_000 and image_objects == 0:
        hits.append(
            f"text-starvation: printable decoded bytes {textish} "
            f"against file {size} (ratio {ratio:.4f})"
        )
    for i, stream in enumerate(streams):
        if len(stream) >= STREAM_PAD_FLOOR and _pad_ratio(stream) >= PAD_RATIO:
            hits.append(
                f"stream-padding: stream {i} length {len(stream)} "
                f"pad-ratio {_pad_ratio(stream):.2f}"
            )
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan PDFs for inflation and override payloads")
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    failed = False
    for path in args.paths:
        if not path.is_file():
            print(f"MISSING {path}")
            failed = True
            continue
        hits = scan_pdf(path)
        if hits:
            failed = True
            print(f"FAIL {path}")
            for hit in hits:
                print(f"  {hit}")
        else:
            print(f"CLEAN {path} ({path.stat().st_size} bytes)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
