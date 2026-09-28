#!/usr/bin/env python3
"""Sweep OpenAlex, Crossref, PubMed, and Semantic Scholar for one name."""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

UA = "WCA-Corpus/1.0 (mailto:research@digitalmarketingco.org)"
SLEEP = 0.25


def get(url: str) -> Any:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        raw = resp.read()
    if not raw:
        return {}
    return json.loads(raw.decode("utf-8"))


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def norm_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    doi = doi.strip()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi, flags=re.I)
    return doi.lower() or None


def openalex(name: str, mailto: str) -> list[dict]:
    rows: list[dict] = []
    cursor = "*"
    encoded = urllib.parse.quote(name)
    while cursor:
        url = (
            "https://api.openalex.org/works"
            f"?filter=author.search:{encoded}&per-page=200&cursor={urllib.parse.quote(cursor)}"
            f"&mailto={urllib.parse.quote(mailto)}"
        )
        data = get(url)
        for w in data.get("results") or []:
            authorships = w.get("authorships") or []
            authors = []
            for i, a in enumerate(authorships):
                author = a.get("author") or {}
                authors.append(
                    {
                        "family": (author.get("display_name") or "").split(" ")[-1],
                        "given": " ".join((author.get("display_name") or "").split(" ")[:-1]),
                        "role": "first" if i == 0 else "coauthor",
                        "id": author.get("id"),
                    }
                )
            loc = (w.get("primary_location") or {}).get("source") or {}
            rows.append(
                {
                    "id": "openalex-" + (w.get("id") or "").rsplit("/", 1)[-1],
                    "type": (w.get("type") or "article").replace("journal-article", "article"),
                    "title": w.get("display_name") or w.get("title") or "",
                    "authors": authors,
                    "year": w.get("publication_year"),
                    "venue": loc.get("display_name"),
                    "doi": norm_doi(w.get("doi")),
                    "pmid": None,
                    "url": (w.get("primary_location") or {}).get("landing_page_url") or w.get("id"),
                    "open_access": bool((w.get("open_access") or {}).get("is_oa")),
                    "source": "openalex",
                    "raw_id": w.get("id"),
                }
            )
        cursor = (data.get("meta") or {}).get("next_cursor")
        if not (data.get("results") or []):
            break
        time.sleep(SLEEP)
        if len(rows) >= 400:
            break
    return rows


def crossref(name: str) -> list[dict]:
    rows: list[dict] = []
    offset = 0
    encoded = urllib.parse.quote(name)
    while offset < 400:
        url = (
            "https://api.crossref.org/works"
            f"?query.author={encoded}&rows=100&offset={offset}"
        )
        data = get(url)
        items = ((data.get("message") or {}).get("items")) or []
        if not items:
            break
        for w in items:
            authors = []
            for i, a in enumerate(w.get("author") or []):
                authors.append(
                    {
                        "family": a.get("family") or "",
                        "given": a.get("given") or "",
                        "role": "first" if i == 0 else "coauthor",
                    }
                )
            pages = w.get("page")
            issued = ((w.get("issued") or {}).get("date-parts") or [[None]])[0]
            rows.append(
                {
                    "id": "doi-" + (norm_doi(w.get("DOI")) or f"crossref-{offset}"),
                    "type": (w.get("type") or "article").replace("journal-article", "article"),
                    "title": " ".join(w.get("title") or []),
                    "authors": authors,
                    "year": issued[0] if issued else None,
                    "venue": " ".join(w.get("container-title") or []),
                    "volume": (w.get("volume") or [None])[0] if isinstance(w.get("volume"), list) else w.get("volume"),
                    "issue": w.get("issue"),
                    "pages": pages,
                    "doi": norm_doi(w.get("DOI")),
                    "url": w.get("URL"),
                    "source": "crossref",
                }
            )
        offset += 100
        time.sleep(SLEEP)
    return rows


def pubmed(name: str) -> list[dict]:
    rows: list[dict] = []
    term = urllib.parse.quote(f"{name}[Author]")
    search = get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        f"?db=pubmed&retmode=json&retmax=400&term={term}"
    )
    ids = ((search.get("esearchresult") or {}).get("idlist")) or []
    if not ids:
        return rows
    for i in range(0, len(ids), 50):
        chunk = ",".join(ids[i : i + 50])
        summary = get(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
            f"?db=pubmed&retmode=json&id={chunk}"
        )
        result = summary.get("result") or {}
        for pmid in ids[i : i + 50]:
            w = result.get(pmid) or {}
            if not w:
                continue
            authors = []
            for j, a in enumerate(w.get("authors") or []):
                name_s = a.get("name") or ""
                authors.append(
                    {
                        "family": name_s.split(" ")[0] if name_s else "",
                        "given": " ".join(name_s.split(" ")[1:]),
                        "role": "first" if j == 0 else "coauthor",
                    }
                )
            aid = w.get("articleids") or []
            doi = None
            for item in aid:
                if item.get("idtype") == "doi":
                    doi = norm_doi(item.get("value"))
            rows.append(
                {
                    "id": f"pmid-{pmid}",
                    "type": "article",
                    "title": w.get("title") or "",
                    "authors": authors,
                    "year": int(str(w.get("pubdate") or "")[:4]) if str(w.get("pubdate") or "")[:4].isdigit() else None,
                    "venue": w.get("fulljournalname") or w.get("source"),
                    "volume": w.get("volume"),
                    "issue": w.get("issue"),
                    "pages": w.get("pages"),
                    "doi": doi,
                    "pmid": pmid,
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                    "source": "pubmed",
                }
            )
        time.sleep(SLEEP)
    return rows


def semantic_scholar(name: str) -> list[dict]:
    rows: list[dict] = []
    encoded = urllib.parse.quote(name)
    try:
        data = get(
            "https://api.semanticscholar.org/graph/v1/author/search"
            f"?query={encoded}&limit=10&fields=name,affiliations,paperCount,papers.title,papers.year,papers.externalIds,papers.authors"
        )
    except Exception:
        return rows
    for author in data.get("data") or []:
        for w in author.get("papers") or []:
            ext = w.get("externalIds") or {}
            authors = []
            for i, a in enumerate(w.get("authors") or []):
                display = a.get("name") or ""
                authors.append(
                    {
                        "family": display.split(" ")[-1],
                        "given": " ".join(display.split(" ")[:-1]),
                        "role": "first" if i == 0 else "coauthor",
                    }
                )
            rows.append(
                {
                    "id": "s2-" + (w.get("paperId") or ""),
                    "type": "article",
                    "title": w.get("title") or "",
                    "authors": authors,
                    "year": w.get("year"),
                    "doi": norm_doi(ext.get("DOI")),
                    "pmid": ext.get("PubMed"),
                    "source": "semantic_scholar",
                    "s2_author": author.get("authorId"),
                    "s2_author_name": author.get("name"),
                }
            )
        time.sleep(SLEEP)
    return rows


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--name", required=True)
    p.add_argument("--variants", nargs="*", default=[])
    p.add_argument("--out", required=True)
    p.add_argument("--mailto", default="research@digitalmarketingco.org")
    args = p.parse_args()
    out = Path(args.out)
    names = [args.name, *args.variants]
    seen_names = []
    for n in names:
        if n and n not in seen_names:
            seen_names.append(n)

    oa: list[dict] = []
    cr: list[dict] = []
    pm: list[dict] = []
    s2: list[dict] = []
    for n in seen_names:
        try:
            oa.extend(openalex(n, args.mailto))
        except Exception as exc:
            print(f"openalex fail {n}: {exc}")
        try:
            cr.extend(crossref(n))
        except Exception as exc:
            print(f"crossref fail {n}: {exc}")
        try:
            pm.extend(pubmed(n))
        except Exception as exc:
            print(f"pubmed fail {n}: {exc}")
        try:
            s2.extend(semantic_scholar(n))
        except Exception as exc:
            print(f"s2 fail {n}: {exc}")

    write_jsonl(out / "openalex.jsonl", oa)
    write_jsonl(out / "crossref.jsonl", cr)
    write_jsonl(out / "pubmed.jsonl", pm)
    write_jsonl(out / "semantic_scholar.jsonl", s2)
    print(json.dumps({"openalex": len(oa), "crossref": len(cr), "pubmed": len(pm), "semantic_scholar": len(s2)}))


if __name__ == "__main__":
    main()
