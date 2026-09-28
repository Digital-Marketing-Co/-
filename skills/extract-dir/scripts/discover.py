#!/usr/bin/env python3
"""Discover unique document URLs from a sitemap + optional index page."""

from __future__ import annotations

import argparse
import json
import re
import sys
from html import unescape
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree as ET

import requests

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


def fetch(url: str) -> str:
    r = requests.get(url, headers={"User-Agent": UA}, timeout=90)
    r.raise_for_status()
    r.encoding = r.apparent_encoding or "utf-8"
    return r.text


def locs_from_sitemap(xml_text: str) -> list[str]:
    # Strip default namespaces so loc tags match.
    xml_text = re.sub(r'\sxmlns="[^"]+"', "", xml_text, count=1)
    xml_text = re.sub(r'\sxmlns:\w+="[^"]+"', "", xml_text)
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return re.findall(r"<loc>\s*(https?://[^<]+)\s*</loc>", xml_text)
    out = []
    for el in root.iter():
        tag = el.tag.split("}")[-1]
        if tag == "loc" and el.text:
            out.append(el.text.strip())
    return out


def locs_from_index(html: str, base: str, prefix: str) -> list[str]:
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', html, re.I)
    out = []
    for h in hrefs:
        absu = urljoin(base, unescape(h))
        if prefix in urlparse(absu).path:
            out.append(absu.split("#")[0])
    return out


def slug_of(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    return (path.split("/")[-1] or "index").lower()


def is_mirror(url: str) -> bool:
    p = urlparse(url).path.lower()
    return p.startswith("/es/") or "/libros-blancos/" in p


def discover(sitemap: str, directory: str, path_prefix: str) -> dict:
    urls = []
    try:
        urls.extend(locs_from_sitemap(fetch(sitemap)))
    except Exception as exc:
        print(f"[warn] sitemap fetch failed: {exc}", file=sys.stderr)
    try:
        urls.extend(locs_from_index(fetch(directory), directory, path_prefix))
    except Exception as exc:
        print(f"[warn] index fetch failed: {exc}", file=sys.stderr)

    filtered = []
    for u in urls:
        path = urlparse(u).path
        if path_prefix.rstrip("/") in path.rstrip("/"):
            if path.rstrip("/") == path_prefix.rstrip("/"):
                continue  # directory index itself
            low = path.lower()
            if low.endswith((".xml", ".rss", ".atom", ".json", ".txt")):
                continue
            filtered.append(u.split("?")[0].rstrip("/"))

    by_slug: dict[str, str] = {}
    dropped = []
    for u in filtered:
        if is_mirror(u):
            dropped.append({"url": u, "reason": "hreflang-or-es-mirror"})
            continue
        sl = slug_of(u)
        prev = by_slug.get(sl)
        if prev is None:
            by_slug[sl] = u
        elif len(u) < len(prev):
            dropped.append({"url": prev, "reason": "longer-twin"})
            by_slug[sl] = u
        elif u != prev:
            dropped.append({"url": u, "reason": "duplicate-slug"})

    records = [{"slug": sl, "url": u} for sl, u in sorted(by_slug.items())]
    return {
        "sitemap": sitemap,
        "directory": directory,
        "path_prefix": path_prefix,
        "count": len(records),
        "documents": records,
        "dropped": dropped,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sitemap", required=True)
    ap.add_argument("--directory", required=True)
    ap.add_argument("--prefix", default="/white-papers/")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    data = discover(args.sitemap, args.directory, args.prefix)
    from pathlib import Path

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Wrote {args.out} ({data['count']} unique documents)")


if __name__ == "__main__":
    main()
