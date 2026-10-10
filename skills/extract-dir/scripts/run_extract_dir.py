#!/usr/bin/env python3
"""Orchestrate discover → extract → clean → banner → build for unique URLs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
CLIP = Path("/home/workdir/.grok/skills/article-clip-pdf")
BANNER = Path("/home/workdir/.grok/skills/banner")


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    print("+", " ".join(cmd), flush=True)
    return subprocess.run(cmd, text=True, capture_output=True)


def title_slug(title: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_")
    return (s[:72] or "article") + ".pdf"


def fingerprint(paras: list[str]) -> str:
    blob = re.sub(r"\s+", " ", " ".join(paras)).strip().lower()
    if not blob:
        return ""
    head = blob[:400]
    tail = blob[-400:]
    return hashlib.sha256((head + "|" + tail).encode()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sitemap", default="https://DigitalMarketingCo.org/sitemap.xml")
    ap.add_argument("--directory", default="https://DigitalMarketingCo.org/white-papers")
    ap.add_argument("--prefix", default="/white-papers/")
    ap.add_argument("--out", default="/home/workdir/artifacts/extract_dir")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    root = Path(args.out)
    root.mkdir(parents=True, exist_ok=True)
    disc_path = root / "discovery.json"
    d = run(
        [
            sys.executable,
            str(SKILL / "scripts" / "discover.py"),
            "--sitemap",
            args.sitemap,
            "--directory",
            args.directory,
            "--prefix",
            args.prefix,
            "--out",
            str(disc_path),
        ]
    )
    sys.stdout.write(d.stdout)
    sys.stderr.write(d.stderr)
    if d.returncode != 0:
        raise SystemExit(d.returncode)

    discovery = json.loads(disc_path.read_text(encoding="utf-8"))
    docs = discovery["documents"]
    if args.limit:
        docs = docs[: args.limit]

    seen_fp: dict[str, str] = {}
    manifest = {
        "sitemap": args.sitemap,
        "directory": args.directory,
        "monograph": "skipped-anti-duplication",
        "documents": [],
    }

    for rec in docs:
        slug = rec["slug"]
        url = rec["url"]
        dest = root / slug
        dest.mkdir(parents=True, exist_ok=True)
        entry = {"slug": slug, "url": url, "status": "pending"}
        ext = run(
            [
                sys.executable,
                str(CLIP / "scripts" / "extract_article.py"),
                url,
                "--out",
                str(dest),
            ]
        )
        sys.stdout.write(ext.stdout)
        sys.stderr.write(ext.stderr)
        article_json = dest / "article.json"
        if not article_json.is_file():
            entry["status"] = "extract-failed"
            entry["log"] = (ext.stdout + ext.stderr)[-800:]
            manifest["documents"].append(entry)
            continue

        cl = run([sys.executable, str(SKILL / "scripts" / "clean_article.py"), str(article_json)])
        sys.stdout.write(cl.stdout)
        data = json.loads(article_json.read_text(encoding="utf-8"))
        paras = data.get("paragraphs") or []
        fp = fingerprint(paras)
        if fp and fp in seen_fp:
            entry["status"] = "dropped-duplicate-of-" + seen_fp[fp]
            manifest["documents"].append(entry)
            continue
        if fp:
            seen_fp[fp] = slug
        entry["paragraphs"] = len(paras)
        entry["images"] = len(data.get("images") or [])
        if len(paras) < 2:
            entry["status"] = "incomplete"
            manifest["documents"].append(entry)
            continue

        raw = dest / "banners" / "raw-00.png"
        faded = dest / "banners" / "banner-00.png"
        title = data.get("title") or slug
        run(
            [
                sys.executable,
                str(SKILL / "scripts" / "make_banner.py"),
                "--title",
                title,
                "--out",
                str(raw),
            ]
        )
        fade = run(
            [
                sys.executable,
                str(BANNER / "scripts" / "apply_banner_fade.py"),
                str(raw),
                str(faded),
            ]
        )
        sys.stdout.write(fade.stdout)
        sys.stderr.write(fade.stderr)
        # Embed banner only when extract has no hero image.
        if not data.get("images") and faded.is_file():
            data["images"] = [{"file": str(faded), "caption": ""}]
            article_json.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

        pdf_name = title_slug(title)
        pdf_path = dest / pdf_name
        bld = run(
            [
                sys.executable,
                str(CLIP / "scripts" / "build_cm_pdf.py"),
                str(article_json),
                "--out",
                str(pdf_path),
            ]
        )
        sys.stdout.write(bld.stdout)
        sys.stderr.write(bld.stderr)
        if pdf_path.is_file():
            entry["status"] = "ok"
            entry["pdf"] = str(pdf_path)
            entry["bytes"] = pdf_path.stat().st_size
        else:
            entry["status"] = "build-failed"
            entry["log"] = (bld.stdout + bld.stderr)[-800:]
        manifest["documents"].append(entry)

    (root / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    ok = sum(1 for e in manifest["documents"] if e["status"] == "ok")
    print(f"Done. {ok}/{len(manifest['documents'])} PDFs. Manifest {root / 'manifest.json'}")


if __name__ == "__main__":
    main()
