#!/usr/bin/env python3
"""Drop chrome crumbs and consecutive duplicate paragraphs from article.json."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

DROP_RE = re.compile(
    r"(back to white papers|claim the deal|read now|skip to main content|"
    r"launch offer|save 30%|follow us on social|service areas|"
    r"subscribe|newsletter|share:\s*|print as pdf|about the author\s*↓|"
    r"digital marketing agency & digital marketing company|"
    r"our expert team of developers is ready|"
    r"from seo to custom web applications|"
    r"elite ai prompt engineering consulting|"
    r"ready to transform your vision|"
    r"start your project|get a quote|claim the|"
    r"https://validator\.w3\.org/feed|"
    r"tap any symbol to expand)",
    re.I,
)


def clean(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    paras = []
    seen_last = None
    title = (data.get("title") or "").strip()
    for raw in data.get("paragraphs") or []:
        p = re.sub(r"\s+", " ", str(raw)).strip()
        if not p or len(p) < 3:
            continue
        if DROP_RE.search(p):
            continue
        if title and p.lower() == title.lower():
            continue
        if seen_last and p == seen_last:
            continue
        paras.append(p)
        seen_last = p
    data["paragraphs"] = paras
    # Drop images that failed to download or point at missing files.
    keep_imgs = []
    for im in data.get("images") or []:
        fp = im.get("file")
        if fp and Path(fp).is_file():
            keep_imgs.append(im)
    data["images"] = keep_imgs
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return data


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("article_json")
    args = ap.parse_args()
    data = clean(Path(args.article_json))
    print(f"paragraphs={len(data.get('paragraphs') or [])} images={len(data.get('images') or [])}")


if __name__ == "__main__":
    main()
