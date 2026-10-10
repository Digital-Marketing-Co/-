#!/usr/bin/env python3
"""Plan /images banners and 500-word mid-section figure slots.

Usage:
  python3 plan_image_slots.py path/to/atlas.json
  python3 plan_image_slots.py path/to/deep.json
  python3 plan_image_slots.py --pdf path/to/file.pdf
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SKIP_KIND = {"notes", "bibliography"}
SKIP_TITLE_RE = re.compile(
    r"^(notes|bibliography|contents|title|colophon|acknowledg)",
    re.I,
)
TAG_RE = re.compile(r"<[^>]+>")
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")


def words(text: str) -> list[str]:
    clean = TAG_RE.sub(" ", text or "")
    clean = clean.replace("{{", " ").replace("}}", " ")
    return WORD_RE.findall(clean)


def word_count(text: str) -> int:
    return len(words(text))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def paragraphs_of(section: dict) -> list[str]:
    raw = section.get("paragraphs") or []
    out: list[str] = []
    for item in raw:
        if isinstance(item, str):
            out.append(item)
        elif isinstance(item, dict):
            if item.get("type") in {"equation", "figure", "table"}:
                continue
            out.append(item.get("text") or item.get("html") or "")
    return [p for p in out if p.strip()]


def plan_section(section: dict) -> dict:
    title = section.get("title") or section.get("id") or ""
    kind = (section.get("kind") or "body").lower()
    sid = section.get("id") or ""
    if kind in SKIP_KIND or SKIP_TITLE_RE.match(title.strip()):
        return {
            "id": sid,
            "title": title,
            "kind": kind,
            "skip": True,
            "banner": False,
            "words_blurb": 0,
            "words_after": 0,
            "slots": 0,
            "anchors": [],
        }
    paras = paragraphs_of(section)
    if not paras:
        blurb, rest = [], []
    elif len(paras) == 1:
        blurb, rest = paras[:1], []
    else:
        blurb, rest = paras[:2], paras[2:]
    n_blurb = sum(word_count(p) for p in blurb)
    counts = [word_count(p) for p in rest]
    n_after = sum(counts)
    slots = n_after // 500
    if slots == 0 and n_after >= 350:
        slots = 1
    anchors = []
    running = 0
    needed = min(500, n_after)
    k = 1
    for i, c in enumerate(counts):
        running += c
        while k <= slots and running >= needed:
            anchors.append(
                {
                    "slot": k,
                    "after_paragraph_index": i + len(blurb),
                    "cumulative_words": running,
                }
            )
            k += 1
            needed = k * 500
    banner = section.get("banner") or {}
    return {
        "id": sid,
        "title": title,
        "kind": kind,
        "skip": False,
        "banner": True,
        "banner_path": banner.get("path") or "",
        "words_blurb": n_blurb,
        "words_after": n_after,
        "slots": slots,
        "anchors": anchors,
    }


def plan_json(data: dict) -> list[dict]:
    sections = data.get("sections") or []
    return [plan_section(s) for s in sections]


def plan_pdf(path: Path) -> list[dict]:
    try:
        import subprocess

        text = subprocess.check_output(
            ["pdftotext", "-layout", str(path), "-"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"pdftotext failed: {exc}") from exc
    blocks = re.split(r"\n(?=[IVX]+\.\s|[A-Z][A-Za-z].{8,80}\n)", text)
    fake_sections = []
    for i, block in enumerate(blocks):
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if not lines:
            continue
        title = lines[0][:120]
        body = " ".join(lines[1:])
        fake_sections.append(
            {
                "id": f"pdf-{i:02d}",
                "title": title,
                "kind": "body",
                "paragraphs": [body[:800], body[800:1600], body[1600:]],
            }
        )
    return [plan_section(s) for s in fake_sections]


def main() -> None:
    parser = argparse.ArgumentParser(description="Plan /images slots")
    parser.add_argument("json_path", nargs="?")
    parser.add_argument("--pdf", default="")
    args = parser.parse_args()
    if args.pdf:
        rows = plan_pdf(Path(args.pdf))
    elif args.json_path:
        rows = plan_json(load_json(Path(args.json_path)))
    else:
        raise SystemExit("pass a JSON path or --pdf")
    print(json.dumps({"sections": rows}, indent=2))
    body = [r for r in rows if not r.get("skip")]
    print(
        f"# body={len(body)} banners={sum(1 for r in body if r['banner'])} "
        f"figures={sum(r['slots'] for r in body)}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
