#!/usr/bin/env python3
"""Merge works.jsonl lines onto durable identifiers."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path


NOISE = re.compile(
    r"\b(accepted manuscript|author manuscript|preprint|version of record)\b",
    re.I,
)


def norm_title(title: str | None) -> str:
    if not title:
        return ""
    t = unicodedata.normalize("NFKD", title)
    t = "".join(ch for ch in t if not unicodedata.combining(ch))
    t = t.lower()
    t = NOISE.sub(" ", t)
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def norm_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", str(doi), flags=re.I)
    doi = doi.strip().lower()
    return doi or None


def first_family(work: dict) -> str:
    authors = work.get("authors") or []
    if not authors:
        return ""
    return (authors[0].get("family") or "").lower()


def keys_for(work: dict) -> list[str]:
    out: list[str] = []
    doi = norm_doi(work.get("doi"))
    if doi:
        out.append(f"doi:{doi}")
    pmid = work.get("pmid")
    if pmid:
        out.append(f"pmid:{pmid}")
    pmcid = work.get("pmcid")
    if pmcid:
        out.append(f"pmcid:{str(pmcid).upper()}")
    isbn = work.get("isbn")
    if isbn:
        out.append("isbn:" + re.sub(r"[^0-9Xx]", "", str(isbn)))
    patent = work.get("patent_number")
    if patent:
        out.append("patent:" + re.sub(r"[^A-Z0-9]", "", str(patent).upper()))
    nct = work.get("nct_id")
    if nct:
        out.append("nct:" + str(nct).upper())
    grant = work.get("grant_id")
    if grant:
        out.append("grant:" + str(grant).upper().replace(" ", ""))
    fp = f"fp:{norm_title(work.get('title'))}|{work.get('year')}|{first_family(work)}"
    if norm_title(work.get("title")) and work.get("year"):
        out.append(fp)
    return out


def richness(work: dict) -> tuple:
    return (
        1 if norm_doi(work.get("doi")) else 0,
        1 if work.get("pmid") else 0,
        1 if work.get("pages") else 0,
        1 if work.get("volume") else 0,
        1 if work.get("url") else 0,
        len(json.dumps(work)),
    )


def merge(a: dict, b: dict) -> dict:
    winner, loser = (a, b) if richness(a) >= richness(b) else (b, a)
    out = dict(winner)
    for key in ("doi", "pmid", "pmcid", "isbn", "patent_number", "nct_id", "grant_id", "url", "pdf_url", "venue", "volume", "issue", "pages"):
        if not out.get(key) and b.get(key):
            out[key] = b.get(key)
        if not out.get(key) and a.get(key):
            out[key] = a.get(key)
    sources = []
    for item in (a, b):
        src = item.get("source")
        if isinstance(src, list):
            sources.extend(src)
        elif src:
            sources.append(src)
    out["source"] = sorted(set(sources))
    also = list(out.get("also") or [])
    for item in (a, b):
        if item.get("id") and item.get("id") != out.get("id"):
            also.append(item["id"])
        also.extend(item.get("also") or [])
    out["also"] = sorted(set(also))
    return out


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("--out", required=True)
    p.add_argument("--report", required=True)
    args = p.parse_args()
    works = load_jsonl(Path(args.input))

    parent: dict[int, int] = {}

    def find(i: int) -> int:
        parent.setdefault(i, i)
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[rj] = ri

    index: dict[str, int] = {}
    for i, work in enumerate(works):
        parent.setdefault(i, i)
        for key in keys_for(work):
            if key in index:
                union(i, index[key])
            else:
                index[key] = i

    groups: dict[int, list[int]] = defaultdict(list)
    for i in range(len(works)):
        groups[find(i)].append(i)

    keepers = []
    report_lines = ["# Dedup report", ""]
    for root, members in sorted(groups.items(), key=lambda kv: min(kv[1])):
        merged = works[members[0]]
        for idx in members[1:]:
            merged = merge(merged, works[idx])
        keepers.append(merged)
        if len(members) > 1:
            ids = [works[m].get("id") for m in members]
            report_lines.append(f"- winner `{merged.get('id')}` from {ids}")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        for work in keepers:
            fh.write(json.dumps(work, ensure_ascii=False) + "\n")
    Path(args.report).write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(json.dumps({"in": len(works), "out": len(keepers), "merges": len(works) - len(keepers)}))


if __name__ == "__main__":
    main()
