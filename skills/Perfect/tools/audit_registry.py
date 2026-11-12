#!/usr/bin/env python3
"""Audit /Perfect candidate registry identifiers. Standard-library only.
Usage: python3 skills/Perfect/tools/audit_registry.py
Reads Engine 7–14 reference files from this repository.
"""
from pathlib import Path
import json
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "references"
PATTERN = re.compile(r"^[-]\s+(?:`([a-z0-9_]+)`\s*[—:]|([a-z0-9_]+):)\s*(.*?)\s*(?:\[proposed\]|\(proposed\))\s*$")
def norm(s):
    s = unicodedata.normalize("NFKD", s).casefold()
    return re.sub(r"[^a-z0-9]+", "_", "".join(c for c in s if not unicodedata.combining(c))).strip("_")

def audit():
    rows = []
    for path in sorted(REFS.glob("engine-*-candidates.md")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = PATTERN.match(line)
            if match:
                identifier = match.group(1) or match.group(2)
                name = match.group(3).strip()
                rows.append(dict(id=identifier, name=name, file=path.name, line=number, normalized_name=norm(name)))
    ids, names, duplicates = {}, {}, []
    for row in rows:
        for kind, key, index in (("id", row["id"], ids), ("normalized_name", row["normalized_name"], names)):
            if key in index:
                duplicates.append(dict(kind=kind, key=key, first=index[key], second=row))
            else:
                index[key] = row
    return dict(total_entries=len(rows), unique_identifiers=len(ids), exact_duplicate_findings=duplicates, entries=rows,
                warning="Exact normalized name/ID collisions only; semantic similarity and historical Engines 2–6 require separate human review.")

if __name__ == "__main__":
    result = audit()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(1 if result["exact_duplicate_findings"] else 0)
