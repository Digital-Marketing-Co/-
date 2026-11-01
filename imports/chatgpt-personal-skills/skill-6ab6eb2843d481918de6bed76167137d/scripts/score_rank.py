#!/usr/bin/env python3
"""Score interpret inventory objects and write rank.json.

Usage:
  python3 score_rank.py /path/to/interpret-<slug>/inventory.jsonl --out /path/to/rank.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

WEIGHTS = {
    "data_fit": 0.40,
    "structural_load": 0.25,
    "identifiability": 0.20,
    "source_warrant": 0.15,
}


def clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def score_object(obj: dict) -> dict:
    raw_scores = obj.get("scores") or {}
    components = {
        key: clamp(raw_scores.get(key, 0.0)) for key in WEIGHTS
    }
    total = sum(components[key] * weight for key, weight in WEIGHTS.items())
    components["score"] = round(total, 4)
    obj = dict(obj)
    obj["scores"] = components
    return obj


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        text = line.strip()
        if not text or text.startswith("#"):
            continue
        try:
            rows.append(json.loads(text))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{line_no}: {exc}") from exc
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank interpret equation objects")
    parser.add_argument("inventory", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    objects = [score_object(obj) for obj in load_jsonl(args.inventory)]
    objects.sort(key=lambda obj: (-obj["scores"]["score"], obj.get("id", "")))

    payload = {
        "weights": WEIGHTS,
        "count": len(objects),
        "order": [obj.get("id") for obj in objects],
        "objects": objects,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {args.out} ({len(objects)} objects)")


if __name__ == "__main__":
    main()
