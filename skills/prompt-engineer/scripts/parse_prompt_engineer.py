#!/usr/bin/env python3
"""Parse /PromptEngineer remainder into mode, keys, and pseudoprompt."""
from __future__ import annotations

import argparse
import json
import re
import sys

MODES = {"spec", "build", "audit", "nav"}
KEY_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(\S+)$")


def parse(remainder: str) -> dict:
    raw = (remainder or "").strip()
    raw = re.sub(r"^/prompt-?engineer\b", "", raw, flags=re.I).strip()
    tokens = raw.split()
    mode = "build"
    keys: dict[str, str] = {}
    bag: list[str] = []
    i = 0
    if tokens and tokens[0].lower() in MODES:
        mode = tokens[0].lower()
        i = 1
    for tok in tokens[i:]:
        m = KEY_RE.match(tok)
        if m:
            keys[m.group(1).lower()] = m.group(2)
        else:
            bag.append(tok)
    pseudo = " ".join(bag).strip()
    apps = []
    if "apps" in keys:
        apps = [a for a in keys["apps"].split(",") if a]
    return {
        "mode": mode,
        "keys": keys,
        "slug": keys.get("slug") or infer_slug(pseudo),
        "stack": keys.get("stack", "html"),
        "brand": keys.get("brand", "Digital Marketing Co."),
        "auditor": keys.get("auditor", "https://DigitalMarketingCo.org/free-website-auditor"),
        "apps": apps,
        "pseudoprompt": pseudo,
        "needs_apps_sync": bool(
            re.search(r"\b(apps|mega\s*menu|404|footer|accordion|nav(igation)?)\b", pseudo, re.I)
        )
        or mode == "nav",
        "empty": not pseudo,
    }


def infer_slug(pseudo: str) -> str:
    if not pseudo:
        return "prompt-engineer-product"
    words = re.findall(r"[a-z0-9]+", pseudo.lower())
    stop = {
        "a", "an", "the", "and", "or", "for", "of", "to", "in", "on", "with",
        "make", "beautiful", "all", "that", "they", "are", "upon", "as", "well",
        "so", "it", "is", "be", "certain",
    }
    keep = [w for w in words if w not in stop][:6]
    return "-".join(keep) if keep else "prompt-engineer-product"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--remainder", default="")
    args = ap.parse_args()
    json.dump(parse(args.remainder), sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
