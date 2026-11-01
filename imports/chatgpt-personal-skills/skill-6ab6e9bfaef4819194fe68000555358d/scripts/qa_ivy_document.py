#!/usr/bin/env python3
"""QA a WCA Ivy folio/deep JSON for citation order and ITQE completeness."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Reuse remapper helpers
sys.path.insert(0, str(Path(__file__).resolve().parent))
from inject_itqe import REQUIRED, is_equation, walk_equations  # noqa: E402
from reorder_citations import collect_first_seen, extract_ns, iter_text_targets, read_text  # noqa: E402

RAW_TEX = re.compile(r"(\$\$|\\\[|\\\(|\\frac|\\sum|\\int|\\mathrm)")
AUTHORDATE = re.compile(r"\(([A-Z][A-Za-z.\-]+(?:\s+(?:and|&)\s+[A-Z][A-Za-z.\-]+)?)\s+\d{4}[a-z]?\)")


def qa(data: dict) -> list[str]:
    errors: list[str] = []
    first_seen = collect_first_seen(data)
    notes = data.get("notes") or []
    notes_by_n = {}
    for note in notes:
        if "n" not in note:
            errors.append("note object missing n")
            continue
        n = int(note["n"])
        if n in notes_by_n:
            errors.append(f"duplicate notes[].n = {n}")
        notes_by_n[n] = note

    if first_seen:
        expected = list(range(1, len(first_seen) + 1))
        if first_seen != expected:
            errors.append(f"first-appearance note numbers are {first_seen}, expected {expected}")
        for n in first_seen:
            if n not in notes_by_n:
                errors.append(f"cited note {n} has no notes[].n entry")
        note_ns = sorted(notes_by_n)
        if note_ns and note_ns != list(range(1, note_ns[-1] + 1)):
            errors.append(f"notes[].n not contiguous: {note_ns}")

    cited = set(first_seen)
    unused = [n for n in notes_by_n if n not in cited]
    if unused:
        errors.append(f"uncited notes remain: {unused}")

    biblio = data.get("bibliography") or []
    work_order_from_notes: list[str] = []
    seen_works: set[str] = set()
    for n in first_seen:
        note = notes_by_n.get(n) or {}
        wid = None
        if note.get("work_id"):
            wid = str(note["work_id"])
        elif isinstance(note.get("biblio"), int):
            wid = f"biblio:{note['biblio']}"
        if wid and wid not in seen_works:
            seen_works.add(wid)
            work_order_from_notes.append(wid)

    index_chain = []
    for n in first_seen:
        note = notes_by_n.get(n) or {}
        if isinstance(note.get("biblio"), int):
            idx = note["biblio"]
            if idx not in index_chain:
                index_chain.append(idx)
    if index_chain and index_chain != sorted(index_chain):
        # first-appearance biblio indices should be nondecreasing unique sequence 0..k
        if index_chain != list(range(len(index_chain))):
            errors.append(
                f"bibliography indices by first appearance are {index_chain}, "
                "expected 0..k in first-citation order"
            )

    if biblio and not work_order_from_notes and not index_chain:
        errors.append("bibliography present but notes do not identify works (add work_id or biblio)")

    for container, key in iter_text_targets(data):
        text = read_text(container, key)
        if RAW_TEX.search(text or ""):
            errors.append(f"raw TeX in {key!r}: {text[:80]}")
        if AUTHORDATE.search(text or ""):
            errors.append(f"author-date parenthetical in {key!r}: {text[:80]}")

    eqs = walk_equations(data)
    for eq in eqs:
        rows = eq.get("itqe") or []
        if not rows:
            errors.append(f"{eq.get('id', 'equation')} missing ITQE table")
            continue
        for i, row in enumerate(rows, start=1):
            if not isinstance(row, dict):
                errors.append(f"{eq.get('id', 'equation')} ITQE row {i} is not an object")
                continue
            missing = [k for k in REQUIRED if not str(row.get(k) or "").strip()]
            if missing:
                errors.append(f"{eq.get('id', 'equation')} ITQE row {i} missing {', '.join(missing)}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="QA WCA Ivy citation order and ITQE tables.")
    parser.add_argument("json_path")
    args = parser.parse_args()
    data = json.loads(Path(args.json_path).read_text(encoding="utf-8"))
    errors = qa(data)
    if errors:
        print("FAIL")
        for err in errors:
            print(f"  - {err}")
        return 1
    notes = len(data.get("notes") or [])
    works = len(data.get("bibliography") or [])
    eqs = len(walk_equations(data))
    print(f"PASS  notes={notes}  works={works}  equations={eqs}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
