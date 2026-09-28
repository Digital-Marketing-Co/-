#!/usr/bin/env python3
"""Pick a visual-system genre palette for a calling skill and topic."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = json.loads((ROOT / "assets" / "palettes.json").read_text())

TOPIC_HINTS = (
    (("ocean", "marine", "navy", "harbor", "reef", "chart", "map", "coast"), "atlas-marine"),
    (("country", "nation", "flag", "capital", "sovereign"), "nation-dusk"),
    (("cipher", "decode", "token", "inventory", "catalog", "list"), "list-phosphor"),
    (("book", "chapter", "volume", "reprint"), "book-spine"),
    (("article", "clip", "blog", "news", "printout"), "clip-paper"),
    (("freud", "jung", "lacan", "klein", "psyche", "dream"), "psyche-plum"),
    (("corpus", "bibliography", "orcid", "author harvest"), "corpus-slate"),
    (("folio", "phd", "ivy", "monograph", "dissertation"), "ivy-ink"),
)


def pick(skill: str, topic: str = "") -> dict:
    defaults = TABLE["defaults"]
    key = defaults.get(skill, "ivy-ink")
    if key == "inherit":
        key = "ivy-ink"
    blob = (topic or "").lower()
    for words, hinted in TOPIC_HINTS:
        if any(w in blob for w in words):
            key = hinted
            break
    palette = TABLE["palettes"][key]
    return {"genre": key, "skill": skill, "palette": palette}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--skill", required=True)
    p.add_argument("--topic", default="")
    args = p.parse_args()
    print(json.dumps(pick(args.skill, args.topic), indent=2))


if __name__ == "__main__":
    main()
