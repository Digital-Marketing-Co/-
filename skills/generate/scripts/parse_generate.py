#!/usr/bin/env python3
"""Parse /generate remainder into a JSON spec."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TYPES_PATH = ROOT / "assets" / "output-types.json"

KNOWN = {
    "type",
    "subject",
    "brand",
    "use",
    "audience",
    "tone",
    "aspect",
    "duration",
    "camera",
    "light",
    "material",
    "setting",
    "motion",
    "count",
    "pages",
    "stack",
    "length",
    "run",
    "mode",
    "cast",
    "policy",
    "studio",
}

SLUG_ALIASES = {
    "webapp": "web-app",
    "web": "web-app",
    "app": "web-app",
    "application": "web-app",
    "film": "video",
    "motion": "video",
    "cinema": "video",
    "image": "still",
    "images": "still",
    "hero": "still",
    "pptx": "deck",
    "slides": "deck",
    "presentation": "deck",
    "pdf": "folio",
    "report": "folio",
    "monograph": "deep",
    "xlsx": "sheet",
    "excel": "sheet",
    "spreadsheet": "sheet",
    "docx": "letter",
    "proposal": "letter",
    "svg": "vector",
    "ringtone": "audio",
    "voice": "audio",
    "catalog": "catalog",
    "list": "catalog",
}


def load_types() -> list[dict]:
    if TYPES_PATH.exists():
        return json.loads(TYPES_PATH.read_text()).get("types", [])
    return []


def tokenize(remainder: str) -> tuple[dict[str, str], list[str]]:
    keys: dict[str, str] = {}
    free: list[str] = []
    token_re = re.compile(r'(\w+):(".*?"|\S+)')
    used_spans: list[tuple[int, int]] = []
    for m in token_re.finditer(remainder):
        k = m.group(1).lower()
        v = m.group(2)
        if v.startswith('"') and v.endswith('"'):
            v = v[1:-1]
        if k in KNOWN:
            keys[k] = v
            used_spans.append(m.span())
    mask = remainder
    for start, end in reversed(used_spans):
        mask = mask[:start] + " " * (end - start) + mask[end:]
    free = [p for p in mask.split() if p]
    return keys, free


def infer_type(keys: dict[str, str], free: list[str], slugs: set[str]) -> str | None:
    if keys.get("type"):
        raw = keys["type"].lower().strip()
        return SLUG_ALIASES.get(raw, raw)
    if not free:
        return None
    first = free[0].lower().strip(",")
    if first in slugs or first in SLUG_ALIASES:
        return SLUG_ALIASES.get(first, first)
    blob = " ".join(free).lower()
    for needle, slug in (
        ("web app", "web-app"),
        ("webapp", "web-app"),
        ("coffee table", "coffee"),
        ("video", "video"),
        ("banner", "banner"),
        ("folio", "folio"),
        ("dashboard", "dashboard"),
    ):
        if needle in blob:
            return slug
    return None


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--remainder", default="")
    args = p.parse_args()
    remainder = args.remainder.strip()
    types = load_types()
    slugs = {t["slug"] for t in types} | {"catalog"}
    keys, free = tokenize(remainder)
    inferred = infer_type(keys, free, slugs)
    if inferred and free and free[0].lower().strip(",") in {inferred, *SLUG_ALIASES}:
        free = free[1:]
    if keys.get("subject"):
        extra = " ".join(free).strip()
        subject = (keys["subject"] + (" " + extra if extra else "")).strip()
    else:
        subject = " ".join(free).strip()
    brand = keys.get("brand")
    if not brand and (inferred == "video" or "gnitekram" in remainder.lower() or "aether" in remainder.lower()):
        brand = "aether"
    spec = {
        "remainder": remainder,
        "type": inferred or "catalog",
        "subject": subject,
        "brand": brand or "",
        "keys": keys,
        "free": free,
        "run": str(keys.get("run", "false")).lower() in {"1", "true", "yes", "run"},
        "studio": keys.get("studio", "https://gnitekram.org/"),
    }
    json.dump(spec, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
