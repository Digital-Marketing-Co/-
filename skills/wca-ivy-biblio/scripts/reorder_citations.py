#!/usr/bin/env python3
"""Remap WCA Ivy note numbers into reading order and sort the bibliography."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NOTE_RUN = re.compile(r"\{\{\s*(\d+(?:\s*,\s*\d+)*)\s*\}\}")
TITLE_KEY = re.compile(r"<i>(.*?)</i>", re.I)


def extract_ns(text: str) -> list[int]:
    nums: list[int] = []
    for inner in NOTE_RUN.findall(text or ""):
        for part in inner.split(","):
            part = part.strip()
            if part.isdigit():
                n = int(part)
                if n not in nums:
                    nums.append(n)
    return nums


def rewrite_markers(text: str, mapping: dict[int, int]) -> str:
    if not text:
        return text

    def repl(match: re.Match) -> str:
        nums = []
        for part in match.group(1).split(","):
            part = part.strip()
            if part.isdigit():
                old = int(part)
                nums.append(str(mapping.get(old, old)))
        return "{{" + ", ".join(nums) + "}}"

    return NOTE_RUN.sub(repl, text)


def iter_text_targets(data: dict) -> list[tuple[object, str]]:
    """Return (container, key) pairs whose values are strings that may hold markers."""
    targets: list[tuple[object, str]] = []
    if isinstance(data.get("abstract"), str):
        targets.append((data, "abstract"))
    for section in data.get("sections") or []:
        kind = (section.get("kind") or "body").lower()
        if kind in {"notes", "bibliography"}:
            continue
        paras = section.get("paragraphs") or []
        for i, item in enumerate(paras):
            if isinstance(item, str):
                targets.append((paras, i))
            elif isinstance(item, dict):
                if isinstance(item.get("caption"), str):
                    targets.append((item, "caption"))
                if isinstance(item.get("text"), str):
                    targets.append((item, "text"))
        fig = section.get("figure") or {}
        if isinstance(fig, dict) and isinstance(fig.get("caption"), str):
            targets.append((fig, "caption"))
        for eq in section.get("equations") or []:
            if isinstance(eq, dict) and isinstance(eq.get("caption"), str):
                targets.append((eq, "caption"))
    return targets


def read_text(container, key) -> str:
    return container[key] or ""


def write_text(container, key, value: str) -> None:
    container[key] = value


def collect_first_seen(data: dict) -> list[int]:
    seen: list[int] = []
    for container, key in iter_text_targets(data):
        for n in extract_ns(read_text(container, key)):
            if n not in seen:
                seen.append(n)
    return seen


def title_key_from_note(text: str) -> str:
    m = TITLE_KEY.search(text or "")
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip().lower()
    compact = re.sub(r"<[^>]+>", "", text or "")
    compact = re.sub(r"\s+", " ", compact).strip().lower()
    return compact[:80]


def work_id_for_note(note: dict, biblio: list) -> str:
    if note.get("work_id"):
        return str(note["work_id"])
    if "biblio" in note and note["biblio"] is not None:
        try:
            idx = int(note["biblio"])
            if 0 <= idx < len(biblio):
                entry = biblio[idx]
                if isinstance(entry, dict) and entry.get("work_id"):
                    return str(entry["work_id"])
                return f"biblio:{idx}"
        except (TypeError, ValueError):
            pass
    return "title:" + title_key_from_note(note.get("text") or "")


def biblio_text(entry) -> str:
    if isinstance(entry, dict):
        return entry.get("text") or ""
    return str(entry)


def reorder(data: dict, keep_unused: bool = False) -> dict[int, int]:
    first_seen = collect_first_seen(data)
    mapping = {old: i + 1 for i, old in enumerate(first_seen)}

    notes = list(data.get("notes") or [])
    notes_by_old = {}
    for note in notes:
        if "n" not in note:
            continue
        notes_by_old[int(note["n"])] = note

    unused = [n for n in notes if "n" in n and int(n["n"]) not in mapping]
    if keep_unused and unused:
        next_n = len(mapping) + 1
        for note in unused:
            mapping[int(note["n"])] = next_n
            next_n += 1

    for container, key in iter_text_targets(data):
        write_text(container, key, rewrite_markers(read_text(container, key), mapping))

    new_notes = []
    for old, new in sorted(mapping.items(), key=lambda kv: kv[1]):
        note = notes_by_old.get(old)
        if note is None:
            note = {"n": new, "text": f"[Note {old} missing after remap.]"}
        else:
            note = dict(note)
            note["n"] = new
        new_notes.append(note)

    biblio = list(data.get("bibliography") or [])
    work_first: dict[str, int] = {}
    work_entry: dict[str, object] = {}
    work_order: list[str] = []

    for note in new_notes:
        wid = work_id_for_note(note, biblio)
        n = int(note["n"])
        if wid not in work_first:
            work_first[wid] = n
            work_order.append(wid)
            if "biblio" in note and note["biblio"] is not None:
                try:
                    idx = int(note["biblio"])
                    if 0 <= idx < len(biblio):
                        work_entry[wid] = biblio[idx]
                except (TypeError, ValueError):
                    pass
            if wid not in work_entry and wid.startswith("title:"):
                # leave a hole; filled from leftover biblio below
                work_entry.setdefault(wid, None)

    used_indices = set()
    for note in new_notes:
        if "biblio" in note and note["biblio"] is not None:
            try:
                used_indices.add(int(note["biblio"]))
            except (TypeError, ValueError):
                pass

    leftovers = [entry for i, entry in enumerate(biblio) if i not in used_indices]
    new_biblio: list = []
    seen_texts = set()
    for wid in work_order:
        entry = work_entry.get(wid)
        if entry is None:
            continue
        text = biblio_text(entry)
        key = re.sub(r"\s+", " ", text).strip().lower()
        if key and key in seen_texts:
            continue
        if key:
            seen_texts.add(key)
        new_biblio.append(entry)

    for entry in leftovers:
        text = biblio_text(entry)
        key = re.sub(r"\s+", " ", text).strip().lower()
        if key and key in seen_texts:
            continue
        if key:
            seen_texts.add(key)
        new_biblio.append(entry)

    index_by_id = {}
    for i, entry in enumerate(new_biblio):
        if isinstance(entry, dict) and entry.get("work_id"):
            index_by_id[str(entry["work_id"])] = i
        normalized_text = re.sub(r'\s+', ' ', biblio_text(entry)).strip().lower()
        index_by_id[f"biblio-text:{normalized_text}"] = i

    old_to_new_biblio = {}
    for old_i, entry in enumerate(biblio):
        normalized_text = re.sub(r'\s+', ' ', biblio_text(entry)).strip().lower()
        text_key = f"biblio-text:{normalized_text}"
        if text_key in index_by_id:
            old_to_new_biblio[old_i] = index_by_id[text_key]
        elif isinstance(entry, dict) and entry.get("work_id") and str(entry["work_id"]) in index_by_id:
            old_to_new_biblio[old_i] = index_by_id[str(entry["work_id"])]

    for note in new_notes:
        wid = work_id_for_note(note, biblio)
        if isinstance(note.get("biblio"), int) and note["biblio"] in old_to_new_biblio:
            note["biblio"] = old_to_new_biblio[note["biblio"]]
        elif wid in index_by_id:
            note["biblio"] = index_by_id[wid]

    data["notes"] = new_notes
    data["bibliography"] = new_biblio
    data["citation_order"] = "first-appearance"
    return mapping


def main() -> int:
    parser = argparse.ArgumentParser(description="Remap WCA Ivy citations into reading order.")
    parser.add_argument("json_path")
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--out")
    parser.add_argument("--keep-unused", action="store_true")
    args = parser.parse_args()

    path = Path(args.json_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    mapping = reorder(data, keep_unused=args.keep_unused)

    out_path = Path(args.out) if args.out else path
    if not args.in_place and not args.out:
        print(json.dumps({str(k): v for k, v in mapping.items()}, indent=2))
        return 0

    out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    map_path = out_path.with_name("citation-map.json")
    map_path.write_text(
        json.dumps({str(k): v for k, v in sorted(mapping.items())}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"rewrote {out_path} ({len(mapping)} note numbers)")
    print(f"map {map_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
