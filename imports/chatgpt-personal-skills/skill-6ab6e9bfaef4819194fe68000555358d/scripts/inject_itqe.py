#!/usr/bin/env python3
"""Attach ITQE tables to display-equation objects. Does not invent explanations."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED = ("identifier", "term", "quantity", "explanation")


def is_equation(item: object) -> bool:
    if not isinstance(item, dict):
        return False
    kind = (item.get("type") or item.get("kind") or "").lower()
    return kind == "equation"


def rows_from_symbols(eq: dict) -> list[dict]:
    rows = []
    for sym in eq.get("symbols") or []:
        if not isinstance(sym, dict):
            continue
        row = {
            "identifier": str(sym.get("identifier") or "").strip(),
            "term": str(sym.get("term") or "").strip(),
            "quantity": str(sym.get("quantity") or "").strip(),
            "explanation": str(sym.get("explanation") or "").strip(),
        }
        if any(row[k] for k in REQUIRED):
            rows.append(row)
    return rows


def merge_itqe(eq: dict) -> list[dict]:
    existing = [r for r in (eq.get("itqe") or []) if isinstance(r, dict)]
    if existing:
        cleaned = []
        for row in existing:
            cleaned.append(
                {
                    "identifier": str(row.get("identifier") or "").strip(),
                    "term": str(row.get("term") or "").strip(),
                    "quantity": str(row.get("quantity") or "").strip(),
                    "explanation": str(row.get("explanation") or "").strip(),
                }
            )
        return cleaned
    return rows_from_symbols(eq)


def walk_equations(data: dict) -> list[dict]:
    found: list[dict] = []
    for section in data.get("sections") or []:
        for item in section.get("paragraphs") or []:
            if is_equation(item):
                found.append(item)
        for item in section.get("equations") or []:
            if is_equation(item) or isinstance(item, dict):
                item.setdefault("type", "equation")
                found.append(item)
    return found


def inject(data: dict, require_complete: bool = False) -> tuple[int, list[str]]:
    errors: list[str] = []
    count = 0
    for eq in walk_equations(data):
        eq["type"] = "equation"
        eq["itqe"] = merge_itqe(eq)
        count += 1
        if not eq["itqe"]:
            errors.append(f"{eq.get('id', 'equation')} has no ITQE rows")
            continue
        for i, row in enumerate(eq["itqe"], start=1):
            missing = [k for k in REQUIRED if not row.get(k)]
            if missing:
                errors.append(
                    f"{eq.get('id', 'equation')} row {i} missing {', '.join(missing)}"
                )
    if require_complete and errors:
        raise SystemExit("ITQE incomplete:\n  " + "\n  ".join(errors))
    data["itqe_attached"] = count
    return count, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Attach ITQE tables to equation objects.")
    parser.add_argument("json_path")
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--out")
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()

    path = Path(args.json_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    count, errors = inject(data, require_complete=args.require_complete)

    if args.in_place or args.out:
        out_path = Path(args.out) if args.out else path
        out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"attached ITQE on {count} equation object(s) → {out_path}")
    else:
        print(json.dumps({"count": count, "errors": errors}, indent=2))

    if errors and not args.require_complete:
        print("warnings:", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
