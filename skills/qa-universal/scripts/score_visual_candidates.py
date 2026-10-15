#!/usr/bin/env python3
"""Rank evidenced visual candidates; critical failures always disqualify."""
import argparse
import json
from pathlib import Path

WEIGHTS = {"fidelity": .25, "readability": .25, "composition": .20, "hierarchy": .15, "realism": .10, "performance": .05}

def evaluate(candidates):
    results = []
    for c in candidates:
        scores = c.get("scores", {})
        missing = [k for k in WEIGHTS if k not in scores]
        invalid = [k for k in WEIGHTS if k in scores and (type(scores[k]) not in (int, float) or not 0 <= scores[k] <= 10)]
        if missing or invalid:
            results.append({"id": c.get("id"), "status": "NOT_TESTED", "missing": missing, "invalid": invalid})
            continue
        value = round(sum(scores[k] * w for k, w in WEIGHTS.items()), 3)
        failures = c.get("critical_failures", [])
        results.append({"id": c.get("id"), "status": "REJECTED" if failures else "ELIGIBLE", "score": value, "critical_failures": failures})
    eligible = [r for r in results if r["status"] == "ELIGIBLE"]
    winner = max(eligible, key=lambda r: (r["score"], str(r["id"])))["id"] if eligible else None
    return {"winner": winner, "results": results, "weights": WEIGHTS}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("input", type=Path)
    p.add_argument("--out", type=Path)
    a = p.parse_args()
    result = json.dumps(evaluate(json.loads(a.input.read_text(encoding="utf-8"))), indent=2) + "\n"
    if a.out:
        a.out.write_text(result, encoding="utf-8")
    else:
        print(result)
