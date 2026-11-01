#!/usr/bin/env python3
"""Stamp an /iterate ledger folder and append one iteration record."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


LEDGER_NAME = "ledger.json"


def load_ledger(root: Path) -> dict:
    path = root / LEDGER_NAME
    if not path.exists():
        return {
            "topic": "",
            "created": date.today().isoformat(),
            "iteration": 0,
            "status": "open",
            "emit_target": "folio",
            "open_questions": [],
            "iterations": [],
        }
    return json.loads(path.read_text(encoding="utf-8"))


def save_ledger(root: Path, ledger: dict) -> None:
    (root / LEDGER_NAME).write_text(
        json.dumps(ledger, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def init_folder(root: Path, topic: str, emit_target: str) -> dict:
    root.mkdir(parents=True, exist_ok=True)
    (root / "rounds").mkdir(exist_ok=True)
    (root / "iterations").mkdir(exist_ok=True)
    (root / "sources.jsonl").touch(exist_ok=True)
    (root / "nodes.jsonl").touch(exist_ok=True)
    ledger = load_ledger(root)
    if not ledger.get("topic"):
        ledger["topic"] = topic
    ledger["emit_target"] = emit_target or ledger.get("emit_target") or "folio"
    save_ledger(root, ledger)
    scope = root / "scope.md"
    if not scope.exists():
        scope.write_text(
            f"# Scope\n\nWorking title: {topic}\n\n"
            "Research questions:\n\n- \n\n"
            f"Emit target: {ledger['emit_target']}\n",
            encoding="utf-8",
        )
    return ledger


def append_iteration(
    root: Path,
    hole: str,
    keepers_added: int,
    claims_added: int,
    empty: bool,
) -> dict:
    ledger = load_ledger(root)
    n = int(ledger.get("iteration") or 0) + 1
    rec = {
        "n": n,
        "date": date.today().isoformat(),
        "hole": hole,
        "keepers_added": keepers_added,
        "claims_added": claims_added,
        "empty": bool(empty),
        "restamp": "pending",
    }
    ledger["iteration"] = n
    ledger.setdefault("iterations", []).append(rec)
    save_ledger(root, ledger)

    round_path = root / "rounds" / f"round-{n:02d}.md"
    if not round_path.exists():
        round_path.write_text(
            f"# Round {n:02d}\n\n"
            f"Hole: {hole}\n\n"
            "## Queries\n\n## Keepers added\n\n## Claims\n\n"
            "## Equation ids\n\n## Temporary notes\n\n"
            "## Dissent\n\n## Open questions\n",
            encoding="utf-8",
        )
    iter_path = root / "iterations" / f"iter-{n:02d}.json"
    iter_path.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    return ledger


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("root", type=Path, help="Work folder iterate-<slug>")
    p.add_argument("--topic", default="", help="Working title (init)")
    p.add_argument("--emit-target", default="folio", choices=("folio", "deep"))
    p.add_argument("--init", action="store_true")
    p.add_argument("--hole", default="", help="Hole this iteration fills")
    p.add_argument("--keepers-added", type=int, default=0)
    p.add_argument("--claims-added", type=int, default=0)
    p.add_argument("--empty", action="store_true")
    args = p.parse_args()

    root = args.root
    if args.init:
        ledger = init_folder(root, args.topic, args.emit_target)
        print(json.dumps({"ok": True, "action": "init", "iteration": ledger.get("iteration", 0)}))
        return

    if not (root / LEDGER_NAME).exists():
        raise SystemExit(f"missing {root / LEDGER_NAME}; run with --init first")

    ledger = append_iteration(
        root,
        hole=args.hole or "(unspecified)",
        keepers_added=args.keepers_added,
        claims_added=args.claims_added,
        empty=args.empty,
    )
    print(json.dumps({"ok": True, "action": "append", "iteration": ledger["iteration"]}))


if __name__ == "__main__":
    main()
