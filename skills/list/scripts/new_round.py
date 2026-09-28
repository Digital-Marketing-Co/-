#!/usr/bin/env python3
"""Stamp a /list research ledger and the next round file."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("workdir")
    parser.add_argument("--predicate", default="")
    parser.add_argument("--init", action="store_true")
    parser.add_argument("--empty", action="store_true", help="mark this round as adding zero keepers")
    parser.add_argument("--note", default="")
    args = parser.parse_args()

    root = Path(args.workdir)
    root.mkdir(parents=True, exist_ok=True)
    (root / "rounds").mkdir(exist_ok=True)
    (root / "items.jsonl").touch(exist_ok=True)
    (root / "sources.jsonl").touch(exist_ok=True)

    ledger_path = root / "ledger.json"
    ledger = load_json(
        ledger_path,
        {
            "predicate": args.predicate,
            "created": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "rounds": [],
            "consecutive_empty": 0,
            "gate_closed": False,
        },
    )
    if args.predicate:
        ledger["predicate"] = args.predicate

    if args.init and not ledger["rounds"]:
        write_json(ledger_path, ledger)
        (root / "scope.md").touch(exist_ok=True)
        (root / "gaps.md").write_text("# Gaps\n\nUnopened registers and thin classes.\n", encoding="utf-8")
        print(f"initialized {root}")
        return

    n = len(ledger["rounds"]) + 1
    keepers = count_jsonl(root / "items.jsonl")
    sources = count_jsonl(root / "sources.jsonl")
    empty = bool(args.empty)
    consecutive = ledger.get("consecutive_empty", 0) + 1 if empty else 0
    gate = (n >= 4 and consecutive >= 2) or n >= 12 or keepers >= 400

    row = {
        "n": n,
        "empty": empty,
        "keepers": keepers,
        "sources": sources,
        "note": args.note,
        "closed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    ledger["rounds"].append(row)
    ledger["consecutive_empty"] = consecutive
    ledger["gate_closed"] = gate
    ledger["keeper_count"] = keepers
    write_json(ledger_path, ledger)

    round_path = root / "rounds" / f"round-{n:02d}.md"
    round_path.write_text(
        f"# Round {n}\n\n"
        f"- empty: {empty}\n"
        f"- keepers: {keepers}\n"
        f"- sources: {sources}\n"
        f"- consecutive_empty: {consecutive}\n"
        f"- gate_closed: {gate}\n\n"
        f"{args.note}\n",
        encoding="utf-8",
    )
    print(f"round {n} empty={empty} keepers={keepers} gate_closed={gate}")


if __name__ == "__main__":
    main()
