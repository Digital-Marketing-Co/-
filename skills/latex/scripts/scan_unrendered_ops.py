#!/usr/bin/env python3
"""Fail visible pages that still show unrendered math operators or operands."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SKIP_DIR = {".git", "__pycache__", "node_modules", "imagine_images"}
SKIP_SUFFIX = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".woff", ".woff2", ".ttf", ".otf", ".py"}
SOURCE_OK = {".tex", ".py", ".js", ".ts", ".tsx"}
ALLOWED_JSON_KEYS = {"tex", "latex", "source", "preamble", "prompt"}

URL = re.compile(r"https?://\S+|www\.\S+", re.I)
EMAIL = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
FENCE = re.compile(r"```[\s\S]*?```")
PROSE_SOLIDUS = re.compile(r"\b(?:and/or|n/a|w/o|I/O|PDF/A)\b", re.I)

UNDERSCORE = re.compile(r"_")
BACKSLASH = re.compile(r"\\")
CARET = re.compile(r"\^")
RELATION = re.compile(r"(?:<=|>=|!=|~=|->|<->)")
STAR = re.compile(r"(?<=[A-Za-z0-9\)\]])\s*\*\s*(?=[A-Za-z0-9\(\[])")
FRACTION = re.compile(
    r"(?<![:/\w])(?:[A-Za-z][A-Za-z0-9]*|\d+(?:\.\d+)?|\))\s*/\s*(?:[A-Za-z][A-Za-z0-9]*|\d+(?:\.\d+)?|\()"
)


def strip_allowed(text: str) -> str:
    text = FENCE.sub(" ", text)
    text = URL.sub(" ", text)
    text = EMAIL.sub(" ", text)
    text = PROSE_SOLIDUS.sub(" ", text)
    return text


def scan_text(label: str, text: str, allow_source: bool) -> list[str]:
    if not text or allow_source:
        return []
    cleaned = strip_allowed(text)
    hits: list[str] = []
    checks = (
        (UNDERSCORE, "unrendered subscript '_'"),
        (BACKSLASH, "unrendered backslash operator"),
        (CARET, "unrendered superscript '^'"),
        (RELATION, "unrendered relation operator"),
        (STAR, "unrendered multiplication '*'"),
        (FRACTION, "unrendered fraction or division '/'"),
    )
    for rx, reason in checks:
        m = rx.search(cleaned)
        if not m:
            continue
        start = max(0, m.start() - 24)
        end = min(len(cleaned), m.end() + 24)
        snippet = cleaned[start:end].replace("\n", " ")
        hits.append(f"{label}: {reason} in {snippet!r}")
    return hits


def walk_json_strings(obj, pointer: str, hits: list[str], file_label: str) -> None:
    if isinstance(obj, dict):
        for key, val in obj.items():
            if str(key).lower() in ALLOWED_JSON_KEYS:
                continue
            walk_json_strings(val, f"{pointer}/{key}", hits, file_label)
    elif isinstance(obj, list):
        for i, val in enumerate(obj):
            walk_json_strings(val, f"{pointer}/{i}", hits, file_label)
    elif isinstance(obj, str):
        hits.extend(scan_text(f"{file_label}{pointer}", obj, allow_source=False))


def scan_file(path: Path) -> list[str]:
    suffix = path.suffix.lower()
    if suffix in SKIP_SUFFIX or suffix in SOURCE_OK:
        return []
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    if suffix == ".json":
        try:
            data = json.loads(raw)
        except Exception:
            return scan_text(str(path), raw, allow_source=False)
        hits: list[str] = []
        walk_json_strings(data, "", hits, str(path))
        return hits
    if suffix == ".pdf":
        return scan_pdf_pages(path)
    return scan_text(str(path), raw, allow_source=False)


def page_count(pdf: Path) -> int:
    r = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True)
    for line in r.stdout.splitlines():
        if line.lower().startswith("pages:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except ValueError:
                return 0
    return 0


def scan_pdf_pages(pdf: Path) -> list[str]:
    hits: list[str] = []
    pages = page_count(pdf)
    if pages <= 0:
        r = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True)
        if r.returncode != 0:
            return [f"{pdf}: pdftotext failed"]
        return scan_text(str(pdf), r.stdout, allow_source=False)
    for n in range(1, pages + 1):
        r = subprocess.run(
            ["pdftotext", "-layout", "-f", str(n), "-l", str(n), str(pdf), "-"],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            hits.append(f"{pdf} p.{n}: pdftotext failed")
            continue
        hits.extend(scan_text(f"{pdf} p.{n}", r.stdout, allow_source=False))
    return hits


def walk(root: Path) -> list[str]:
    hits: list[str] = []
    paths = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file()]
    for p in paths:
        if any(part in SKIP_DIR for part in p.parts):
            continue
        hits.extend(scan_file(p))
    return hits


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("root", help="file or directory to scan")
    p.add_argument("--also-pdf", action="append", default=[])
    args = p.parse_args()
    hits = walk(Path(args.root))
    for pdf in args.also_pdf:
        hits.extend(scan_pdf_pages(Path(pdf)))
    if not hits:
        print("scan_unrendered_ops: clean")
        return 0
    print("scan_unrendered_ops: FAIL")
    for h in hits:
        print(" -", h)
    return 1


if __name__ == "__main__":
    sys.exit(main())
