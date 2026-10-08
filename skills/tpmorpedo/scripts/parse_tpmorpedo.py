#!/usr/bin/env python3
"""Parse a /tpmorpedo remainder into two dataset lanes and a view filter."""

import argparse
import json
import re
import sys

MODES = ("prompt", "mine", "pages", "all")
STRATA = ("stats", "images", "motion", "holo")
RUN_VERBS = ("run", "mine", "gather", "procure", "build")


def split_lanes(text: str) -> tuple[str, str, str]:
    marker = re.search(r"#1\b|#2\b", text)
    if not marker:
        return text.strip(), "", ""
    pre = text[: marker.start()].strip()
    rest = text[marker.start() :]
    one = re.search(r"#1\b(.*?)(?=#2\b|$)", rest, flags=re.S)
    two = re.search(r"#2\b(.*)$", rest, flags=re.S)
    d1 = one.group(1).strip() if one else ""
    d2 = two.group(1).strip() if two else ""
    return pre, d1, d2


def parse(remainder: str) -> dict:
    raw = (remainder or "").strip()
    pre, d1, d2 = split_lanes(raw)
    tokens = pre.split()
    mode = "prompt"
    keys: dict[str, str] = {}
    free: list[str] = []
    current_key = ""
    for token in tokens:
        if token in MODES and not current_key:
            mode = token
            continue
        if ":" in token and not token.startswith("http"):
            k, v = token.split(":", 1)
            current_key = k.strip().lower()
            keys[current_key] = v.strip().strip('"')
            continue
        if current_key in ("set", "slug", "geo", "pages"):
            keys[current_key] = (keys[current_key] + " " + token).strip()
            continue
        current_key = ""
        free.append(token)
    subject = " ".join(free).strip()
    view = keys.get("view") or keys.get("filter") or "all-types"
    if not d1:
        d1 = keys.get("set") or subject
    if not d2:
        d2 = f"{view} of {d1}".strip() if d1 else ""
    if any(v in subject.lower().split() for v in RUN_VERBS) and mode == "prompt":
        mode = "mine"
    if "upgrade" in subject.lower() and "page" in subject.lower() and mode == "prompt":
        mode = "pages"
    strata = list(STRATA)
    if view != "all-types":
        asked = [p.strip() for p in view.split(",") if p.strip()]
        strata = [p for p in asked if p in STRATA] or list(STRATA)
    return {
        "mode": mode,
        "dataset_1": d1,
        "dataset_2": d2,
        "view": view,
        "strata": strata,
        "slug": keys.get("slug") or re.sub(r"[^a-z0-9]+", "-", d1.lower()).strip("-")[:48],
        "pages": [p for p in (keys.get("pages") or "").split(",") if p],
        "geo": keys.get("geo") or "unspecified",
        "since": keys.get("since") or "",
        "until": keys.get("until") or "",
        "subject_bag": subject,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--remainder", default="")
    args = parser.parse_args()
    json.dump(parse(args.remainder), sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
