#!/usr/bin/env python3
"""Mirror a start URL plus linked assets and zip the tree."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import posixpath
import re
import sys
import zipfile
from collections import deque
from html import unescape
from pathlib import Path
from typing import Iterable
from urllib.parse import urldefrag, urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

SKIP_HOST_PARTS = (
    "google-analytics.com",
    "googletagmanager.com",
    "googlesyndication.com",
    "doubleclick.net",
    "googleadservices.com",
    "facebook.net",
    "facebook.com",
    "scorecardresearch.com",
    "quantserve.com",
    "hotjar.com",
    "disqus.com",
    "disquscdn.com",
    "amazon-adsystem.com",
    "criteo.com",
    "taboola.com",
    "outbrain.com",
    "casalemedia.com",
    "pubmatic.com",
    "openx.net",
    "rubiconproject.com",
    "deployads.com",
    "carbonads.com",
    "ads.linkedin",
    "googletagservices.com",
    "btloader.com",
    "pagead2.googlesyndication",
    "adservice.google",
    "fundingchoicesmessages.google",
    "google.com/ads",
    "googletag",
)

ASSET_EXT = {
    ".css",
    ".js",
    ".mjs",
    ".map",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".svg",
    ".ico",
    ".bmp",
    ".avif",
    ".woff",
    ".woff2",
    ".ttf",
    ".otf",
    ".eot",
    ".mp3",
    ".mp4",
    ".webm",
    ".ogg",
    ".wav",
    ".json",
    ".txt",
    ".xml",
    ".pdf",
}

HTML_EXT = {".html", ".htm", ".xhtml", ".php", ".asp", ".aspx", ""}

URL_IN_CSS = re.compile(
    r"""(?P<prefix>url\(\s*['"]?)(?P<url>[^'")\s]+)(?P<suffix>['"]?\s*\))""",
    re.I,
)
IMPORT_IN_CSS = re.compile(
    r"""@import\s+(?:url\()?['"](?P<url>[^'"]+)['"]\)?""",
    re.I,
)
URL_IN_JS = re.compile(
    r"""['"](?P<url>(?:https?:)?//[^'"]+?\.(?:css|js|mjs|png|jpe?g|gif|webp|svg|ico|woff2?|ttf|otf|json)|(?:\.\./|\./|/)[^'"]+?\.(?:css|js|mjs|png|jpe?g|gif|webp|svg|ico|woff2?|ttf|otf))['"]""",
    re.I,
)
SRCSET_SPLIT = re.compile(r"\s*,\s*")


def skip_host(host: str) -> bool:
    h = (host or "").lower()
    return any(part in h for part in SKIP_HOST_PARTS)


def normalize_url(url: str) -> str:
    url, _frag = urldefrag(url.strip())
    p = urlparse(url)
    path = posixpath.normpath(p.path or "/")
    if p.path.endswith("/") and not path.endswith("/"):
        path += "/"
    return urlunparse((p.scheme, p.netloc.lower(), path, "", p.query, ""))


def ext_of(url: str) -> str:
    path = urlparse(url).path
    return posixpath.splitext(path)[1].lower()


def is_html_url(url: str, content_type: str = "") -> bool:
    ct = (content_type or "").split(";")[0].strip().lower()
    if ct in {"text/html", "application/xhtml+xml"}:
        return True
    return ext_of(url) in HTML_EXT and ct.startswith("text/") or ext_of(url) in {".html", ".htm", ".xhtml"}


def is_asset_url(url: str) -> bool:
    return ext_of(url) in ASSET_EXT


def _safe_seg(seg: str) -> str:
    out = re.sub(r"[^A-Za-z0-9._-]+", "-", seg).strip(".-")
    return out or "file"


def local_relpath(url: str, content_type: str = "") -> str:
    p = urlparse(url)
    path = p.path or "/"
    ext = posixpath.splitext(path)[1].lower()
    ct = (content_type or "").split(";")[0].strip().lower()
    if path.endswith("/"):
        path += "index.html"
    elif not ext:
        if ct == "text/css" or "family=" in (p.query or ""):
            path = path.rstrip("/") + ".css"
        elif ct in {"application/javascript", "text/javascript"}:
            path = path.rstrip("/") + ".js"
        elif ct.startswith("image/"):
            subtype = ct.split("/", 1)[-1].split("+")[0]
            path = path.rstrip("/") + "." + (subtype if subtype != "jpeg" else "jpg")
        elif ct.startswith("font/") or ct in {"application/font-woff", "application/font-woff2"}:
            path = path.rstrip("/") + (".woff2" if "woff2" in ct else ".woff")
        elif ct in {"text/html", "application/xhtml+xml"} or not ct:
            path = path.rstrip("/") + ".html"
        else:
            path = path.rstrip("/") + ".bin"
    path = path.lstrip("/")
    if not path:
        path = "index.html"
    if p.query:
        stem, ext2 = posixpath.splitext(path)
        q = _safe_seg(p.query)[:80]
        path = f"{stem}-{q}{ext2}"
    host = _safe_seg(p.netloc.lower())
    parts = [host] + [_safe_seg(x) for x in path.split("/") if x]
    return "/".join(parts)


def safe_join(root: Path, rel: str) -> Path:
    dest = (root / rel).resolve()
    if not str(dest).startswith(str(root.resolve())):
        raise ValueError(f"path escape: {rel}")
    return dest


def rel_href(from_rel: str, to_rel: str) -> str:
    return posixpath.relpath(to_rel, start=posixpath.dirname(from_rel) or ".")


class Mirror:
    def __init__(
        self,
        start: str,
        out: Path,
        mode: str = "page",
        max_pages: int = 80,
        max_depth: int = 2,
        max_files: int = 400,
        max_bytes: int = 80 * 1024 * 1024,
    ) -> None:
        self.start = normalize_url(start)
        parsed = urlparse(self.start)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise SystemExit(f"Need an http(s) URL, got: {start}")
        self.origin = f"{parsed.scheme}://{parsed.netloc.lower()}"
        self.host = parsed.netloc.lower()
        self.out = out
        self.mode = mode
        self.max_pages = 1 if mode == "page" else max_pages
        self.max_depth = 0 if mode == "page" else max_depth
        self.max_files = max_files if mode == "page" else max(max_files, 800)
        self.max_bytes = max_bytes if mode == "page" else max(max_bytes, 160 * 1024 * 1024)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": UA,
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
            }
        )
        self.queue: deque[tuple[str, int, str]] = deque()  # url, depth, kind
        self.seen: set[str] = set()
        self.files: dict[str, dict] = {}  # url -> meta
        self.url_to_rel: dict[str, str] = {}
        self.bytes = 0
        self.pages = 0
        self.errors: list[str] = []

    def enqueue(self, url: str, depth: int, kind: str) -> None:
        if not url or url.startswith(("data:", "javascript:", "mailto:", "tel:", "#")):
            return
        try:
            absu = normalize_url(urljoin(self.start if kind == "start" else url, url) if False else url)
        except Exception:
            return
        if not absu.startswith("http"):
            return
        host = urlparse(absu).netloc.lower()
        if skip_host(host):
            return
        same = host == self.host
        asset = is_asset_url(absu) or kind in {"css", "js", "img", "font", "asset"}
        htmlish = kind == "html" or (not asset and ext_of(absu) in HTML_EXT)
        if not same:
            if htmlish and kind == "html":
                return
            if not asset and kind not in {"css", "js", "img", "font", "asset"}:
                # allow bare CDN paths without extension if kind is asset-like
                if kind == "html":
                    return
        if htmlish and not asset:
            if depth > self.max_depth:
                return
            if self.pages + sum(1 for _, _, k in self.queue if k == "html") >= self.max_pages:
                return
        if absu in self.seen:
            return
        if len(self.files) + len(self.queue) >= self.max_files:
            return
        self.seen.add(absu)
        self.queue.append((absu, depth, "html" if htmlish and not asset else (kind if kind != "start" else "html")))

    def fetch(self, url: str) -> tuple[bytes, str, int] | None:
        try:
            r = self.session.get(url, timeout=25, allow_redirects=True)
        except requests.RequestException as e:
            self.errors.append(f"{url} :: {e}")
            return None
        if r.status_code >= 400:
            self.errors.append(f"{url} :: HTTP {r.status_code}")
            return None
        data = r.content or b""
        if self.bytes + len(data) > self.max_bytes:
            self.errors.append(f"{url} :: skipped, size cap")
            return None
        ct = r.headers.get("Content-Type", "")
        final = normalize_url(str(r.url))
        return data, ct, r.status_code

    def save(self, url: str, data: bytes, content_type: str) -> str:
        rel = local_relpath(url, content_type)
        ct = (content_type or "").split(";")[0].strip().lower()
        dest = safe_join(self.out, rel)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        self.bytes += len(data)
        self.url_to_rel[url] = rel
        self.files[url] = {
            "rel": rel,
            "bytes": len(data),
            "content_type": ct,
        }
        return rel

    def extract_html(self, url: str, data: bytes, depth: int) -> None:
        soup = BeautifulSoup(data, "lxml")
        for tag in soup.find_all("link"):
            rels = " ".join(tag.get("rel") or []).lower()
            href = tag.get("href")
            if not href:
                continue
            absu = urljoin(url, href)
            if "stylesheet" in rels or (tag.get("as") or "").lower() in {"style", "font", "image", "script"}:
                kind = "css" if "stylesheet" in rels or tag.get("as") == "style" else "asset"
                if tag.get("as") == "font":
                    kind = "font"
                if tag.get("as") == "image":
                    kind = "img"
                if tag.get("as") == "script":
                    kind = "js"
                self.enqueue(absu, depth, kind)
            elif "icon" in rels or "apple-touch-icon" in rels or "shortcut" in rels:
                self.enqueue(absu, depth, "img")
            elif "preload" in rels or "prefetch" in rels or "modulepreload" in rels:
                self.enqueue(absu, depth, "asset")
        for tag in soup.find_all("script"):
            src = tag.get("src")
            if src:
                self.enqueue(urljoin(url, src), depth, "js")
        for attr in ("src", "data-src", "data-original", "poster"):
            for tag in soup.find_all(attrs={attr: True}):
                if tag.name == "script":
                    continue
                val = tag.get(attr)
                if not val:
                    continue
                kind = "img" if tag.name in {"img", "source", "image"} else "asset"
                self.enqueue(urljoin(url, val), depth, kind)
        for tag in soup.find_all(attrs={"srcset": True}):
            self._srcset(url, tag.get("srcset") or "", depth)
        for tag in soup.find_all(attrs={"data-srcset": True}):
            self._srcset(url, tag.get("data-srcset") or "", depth)
        for tag in soup.find_all(style=True):
            self._css_urls(url, tag.get("style") or "", depth)
        for tag in soup.find_all("style"):
            self._css_urls(url, tag.string or "", depth)
        if self.mode == "site":
            for tag in soup.find_all("a", href=True):
                href = tag.get("href")
                absu = urljoin(url, href)
                if urlparse(absu).netloc.lower() == self.host:
                    self.enqueue(absu, depth + 1, "html")

    def _srcset(self, base: str, srcset: str, depth: int) -> None:
        for part in SRCSET_SPLIT.split(srcset.strip()):
            if not part:
                continue
            u = part.strip().split()[0]
            self.enqueue(urljoin(base, u), depth, "img")

    def _css_urls(self, base: str, text: str, depth: int) -> None:
        if not text:
            return
        for m in URL_IN_CSS.finditer(text):
            raw = unescape(m.group("url"))
            if raw.startswith("data:"):
                continue
            absu = urljoin(base, raw)
            kind = "font" if ext_of(absu) in {".woff", ".woff2", ".ttf", ".otf", ".eot"} else "asset"
            if ext_of(absu) in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico"}:
                kind = "img"
            if ext_of(absu) == ".css":
                kind = "css"
            self.enqueue(absu, depth, kind)
        for m in IMPORT_IN_CSS.finditer(text):
            self.enqueue(urljoin(base, unescape(m.group("url"))), depth, "css")

    def extract_css(self, url: str, data: bytes, depth: int) -> None:
        try:
            text = data.decode("utf-8", "replace")
        except Exception:
            return
        self._css_urls(url, text, depth)

    def extract_js(self, url: str, data: bytes, depth: int) -> None:
        try:
            text = data.decode("utf-8", "replace")
        except Exception:
            return
        for m in URL_IN_JS.finditer(text):
            raw = m.group("url")
            absu = urljoin(url, raw)
            kind = "js" if ext_of(absu) in {".js", ".mjs"} else "asset"
            if ext_of(absu) == ".css":
                kind = "css"
            self.enqueue(absu, depth, kind)

    def rewrite_html(self, url: str, data: bytes) -> bytes:
        soup = BeautifulSoup(data, "lxml")
        from_rel = self.url_to_rel[url]

        def rewrite_attr(val: str) -> str | None:
            if not val or val.startswith(("data:", "javascript:", "mailto:", "tel:", "#")):
                return None
            absu = normalize_url(urljoin(url, val))
            if absu in self.url_to_rel:
                return rel_href(from_rel, self.url_to_rel[absu])
            return None

        for tag in soup.find_all(True):
            for attr in ("href", "src", "data-src", "data-original", "poster"):
                if tag.has_attr(attr):
                    neu = rewrite_attr(tag.get(attr))
                    if neu is not None:
                        tag[attr] = neu
            if tag.has_attr("srcset"):
                tag["srcset"] = self._rewrite_srcset(url, from_rel, tag.get("srcset") or "")
            if tag.has_attr("data-srcset"):
                tag["data-srcset"] = self._rewrite_srcset(url, from_rel, tag.get("data-srcset") or "")
            if tag.has_attr("style"):
                tag["style"] = self._rewrite_css_text(url, from_rel, tag.get("style") or "")
        for tag in soup.find_all("style"):
            if tag.string:
                tag.string.replace_with(self._rewrite_css_text(url, from_rel, tag.string))
        # base tag would break relative links
        for tag in soup.find_all("base"):
            tag.decompose()
        return str(soup).encode("utf-8")

    def _rewrite_srcset(self, base: str, from_rel: str, srcset: str) -> str:
        out = []
        for part in SRCSET_SPLIT.split(srcset.strip()):
            if not part:
                continue
            bits = part.strip().split()
            absu = normalize_url(urljoin(base, bits[0]))
            if absu in self.url_to_rel:
                bits[0] = rel_href(from_rel, self.url_to_rel[absu])
            out.append(" ".join(bits))
        return ", ".join(out)

    def _rewrite_css_text(self, base: str, from_rel: str, text: str) -> str:
        def repl(m: re.Match) -> str:
            raw = unescape(m.group("url"))
            if raw.startswith("data:"):
                return m.group(0)
            absu = normalize_url(urljoin(base, raw))
            if absu in self.url_to_rel:
                return f"{m.group('prefix')}{rel_href(from_rel, self.url_to_rel[absu])}{m.group('suffix')}"
            return m.group(0)

        text = URL_IN_CSS.sub(repl, text)

        def repl_imp(m: re.Match) -> str:
            absu = normalize_url(urljoin(base, unescape(m.group("url"))))
            if absu in self.url_to_rel:
                return m.group(0).replace(m.group("url"), rel_href(from_rel, self.url_to_rel[absu]))
            return m.group(0)

        return IMPORT_IN_CSS.sub(repl_imp, text)

    def rewrite_css(self, url: str, data: bytes) -> bytes:
        text = data.decode("utf-8", "replace")
        return self._rewrite_css_text(url, self.url_to_rel[url], text).encode("utf-8")

    def run(self) -> dict:
        self.out.mkdir(parents=True, exist_ok=True)
        self.enqueue(self.start, 0, "html")
        # force start even if classified oddly
        if self.start not in self.seen:
            self.seen.add(self.start)
            self.queue.appendleft((self.start, 0, "html"))

        while self.queue:
            url, depth, kind = self.queue.popleft()
            got = self.fetch(url)
            if not got:
                continue
            data, ct, _status = got
            final = url
            rel = self.save(final, data, ct)
            ct0 = (ct or "").split(";")[0].strip().lower()
            if kind == "html" or ct0 in {"text/html", "application/xhtml+xml"}:
                self.pages += 1
                self.extract_html(final, data, depth)
            elif kind == "css" or ct0 == "text/css" or rel.endswith(".css"):
                self.extract_css(final, data, depth)
            elif kind == "js" or ct0 in {"application/javascript", "text/javascript"} or rel.endswith((".js", ".mjs")):
                self.extract_js(final, data, depth)

        # second pass rewrite
        for url, meta in list(self.files.items()):
            path = safe_join(self.out, meta["rel"])
            raw = path.read_bytes()
            ct = meta.get("content_type") or ""
            if meta["rel"].endswith((".html", ".htm", ".xhtml")) or ct in {"text/html", "application/xhtml+xml"}:
                path.write_bytes(self.rewrite_html(url, raw))
            elif meta["rel"].endswith(".css") or ct == "text/css":
                path.write_bytes(self.rewrite_css(url, raw))

        start_rel = self.url_to_rel.get(self.start)
        manifest = {
            "ok": bool(self.files) and start_rel is not None,
            "start_url": self.start,
            "start_file": start_rel,
            "mode": self.mode,
            "host": self.host,
            "file_count": len(self.files),
            "page_count": self.pages,
            "bytes": self.bytes,
            "errors": self.errors[:50],
            "files": [
                {"url": u, **m}
                for u, m in sorted(self.files.items(), key=lambda kv: kv[1]["rel"])
            ],
        }
        (self.out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        # convenience opener
        if start_rel:
            (self.out / "OPEN_ME.html").write_text(
                f"""<!DOCTYPE html><meta charset="utf-8">
<title>Copied site</title>
<meta http-equiv="refresh" content="0; url={start_rel}">
<p><a href="{start_rel}">Open copied page</a></p>
""",
                encoding="utf-8",
            )
        return manifest


def zip_tree(src: Path, zip_path: Path) -> int:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in src.rglob("*"):
            if path.is_file():
                zf.write(path, arcname=str(path.relative_to(src)))
                count += 1
    return count


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Copy a website plus assets and zip it.")
    ap.add_argument("url")
    ap.add_argument("--out", required=True)
    ap.add_argument("--zip", required=True)
    ap.add_argument("--mode", choices=("page", "site"), default="page")
    ap.add_argument("--max-pages", type=int, default=80)
    ap.add_argument("--max-depth", type=int, default=2)
    ap.add_argument("--max-files", type=int, default=400)
    args = ap.parse_args(argv)

    out = Path(args.out)
    if out.exists():
        # fresh tree
        import shutil

        shutil.rmtree(out)
    mirror = Mirror(
        args.url,
        out,
        mode=args.mode,
        max_pages=args.max_pages,
        max_depth=args.max_depth,
        max_files=args.max_files,
    )
    manifest = mirror.run()
    zipped = zip_tree(out, Path(args.zip))
    manifest["zip"] = str(Path(args.zip))
    manifest["zip_members"] = zipped
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    # refresh zip with updated manifest
    zip_tree(out, Path(args.zip))
    print(json.dumps({k: manifest[k] for k in ("ok", "start_url", "start_file", "mode", "file_count", "page_count", "bytes", "zip", "zip_members") if k in manifest}, indent=2))
    if manifest.get("errors"):
        print("errors:", len(manifest["errors"]), file=sys.stderr)
        for e in manifest["errors"][:12]:
            print(" ", e, file=sys.stderr)
    return 0 if manifest.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
