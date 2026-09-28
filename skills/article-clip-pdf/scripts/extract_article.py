#!/usr/bin/env python3
"""Fetch a URL and extract article-only text + in-article images.

Writes article.json and downloaded images into --out.
Does not keep nav, ads, sidebars, related cards, comments, or share widgets.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html import unescape
from pathlib import Path
from urllib.parse import urljoin, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

import requests
from bs4 import BeautifulSoup, Comment, NavigableString, Tag

from image_util import file_sha256, is_duplicate, norm_url, percept_key

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

JUNK_CLASS_RE = re.compile(
    r"(site-header|page-header|global-header|masthead|site-footer|"
    r"site-nav|navbar|menu-bar|sidebar|related|recirc|keep-reading|"
    r"recommend|trending|popular-posts|share-buttons|social-share|"
    r"comments-area|comment-list|newsletter|subscribe-box|"
    r"promo|sponsor|advert|adsense|breadcrumb|pagination|"
    r"tag-list|cookie-banner|paywall|modal|popup|card-image|card-grid)",
    re.I,
)
JUNK_ID_RE = JUNK_CLASS_RE

KEEP_SELECTORS = [
    "article",
    "[itemprop='articleBody']",
    ".entry-content",
    ".post-content",
    ".article-content",
    ".article-body",
    ".story-body",
    ".post-body",
    ".td-post-content",
    ".elementor-widget-theme-post-content",
    ".aaee-article-copy-100",
    ".aas-content-article",
    "main",
]

CAPTION_JUNK_RE = re.compile(
    r"(advert|sponsor|promoted|related|trending|subscribe|"
    r"newsletter|click here|read more|photo illustration)",
    re.I,
)


def class_blob(el: Tag) -> str:
    if not isinstance(el, Tag) or el.attrs is None:
        return ""
    cls = el.get("class") or []
    if isinstance(cls, str):
        cls = [cls]
    return " ".join(str(c) for c in cls) + " " + str(el.get("id") or "")


def is_junk_container(el: Tag) -> bool:
    blob = class_blob(el)
    return bool(JUNK_CLASS_RE.search(blob))


def meta(soup: BeautifulSoup, *keys: str) -> str:
    for key in keys:
        tag = soup.find("meta", property=key) or soup.find("meta", attrs={"name": key})
        if tag and tag.get("content"):
            return tag["content"].strip()
    return ""


def pick_container(soup: BeautifulSoup) -> Tag:
    scored: list[tuple[int, Tag]] = []
    seen: set[int] = set()
    for sel in KEEP_SELECTORS:
        for el in soup.select(sel):
            if id(el) in seen:
                continue
            seen.add(id(el))
            text = el.get_text(" ", strip=True)
            paras = el.find_all("p")
            score = len(text) + 80 * len(paras)
            if is_junk_container(el):
                score //= 4
            scored.append((score, el))
    if not scored:
        body = soup.body or soup
        return body
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]


def clean_tree(root: Tag) -> None:
    for tag in list(root.find_all(["script", "style", "noscript", "form", "svg", "button"])):
        try:
            tag.decompose()
        except Exception:
            pass
    for c in list(root.find_all(string=lambda t: isinstance(t, Comment))):
        try:
            c.extract()
        except Exception:
            pass
    doomed = []
    for el in list(root.find_all(True)):
        if not isinstance(el, Tag) or el is root:
            continue
        if el.name in {"p", "h1", "h2", "img", "figure", "iframe"}:
            continue
        if is_junk_container(el):
            doomed.append(el)
    for el in doomed:
        try:
            el.decompose()
        except Exception:
            pass


def abs_url(base: str, src: str | None) -> str | None:
    if not src:
        return None
    src = src.strip()
    if src.startswith("data:"):
        return None
    return urljoin(base, src)


def best_from_srcset(base: str, srcset: str | None) -> str | None:
    if not srcset:
        return None
    parts = []
    for chunk in srcset.split(","):
        bits = chunk.strip().split()
        if not bits:
            continue
        url = bits[0]
        w = 0
        if len(bits) > 1 and bits[1].endswith("w"):
            try:
                w = int(bits[1][:-1])
            except ValueError:
                w = 0
        parts.append((w, url))
    if not parts:
        return None
    parts.sort()
    return abs_url(base, parts[-1][1])


def nearby_caption(img: Tag) -> str:
    fig = img.find_parent("figure")
    if fig:
        cap = fig.find("figcaption")
        if cap:
            return cap.get_text(" ", strip=True)
    parent = img.parent
    if parent:
        nxt = parent.find_next_sibling(["figcaption", "p", "small", "em"])
        if nxt and nxt.name in {"figcaption", "small"}:
            return nxt.get_text(" ", strip=True)
    return (img.get("alt") or "").strip()


def youtube_id(src: str) -> str | None:
    m = re.search(r"(?:youtube\.com/embed/|youtu\.be/)([A-Za-z0-9_-]{6,})", src)
    return m.group(1) if m else None


def skip_image_url(url: str, role: str) -> bool:
    low = url.lower()
    crumbs = (
        "1x1", "pixel", "sprite", "icon", "logo", "emoji", "gravatar",
        "badge", "flag", "avatar", "social-icons", "favicon",
    )
    if any(x in low for x in crumbs) and role != "featured":
        return True
    return False


def img_src(img: Tag, base: str) -> str | None:
    return best_from_srcset(base, img.get("srcset") or img.get("data-srcset")) or abs_url(
        base, img.get("src") or img.get("data-src") or img.get("data-lazy-src")
    )


def collect_images(soup: BeautifulSoup, container: Tag, base: str) -> list[dict]:
    """Collect unique in-article images in document order. Never emit the same plate twice."""
    found: list[dict] = []
    seen_url: set[str] = set()

    def add(url: str | None, role: str, caption: str = "", alt: str = "") -> dict | None:
        if not url:
            return None
        if skip_image_url(url, role):
            return None
        key = norm_url(url) or url
        if key in seen_url:
            return None
        seen_url.add(key)
        rec = {
            "url": url,
            "role": role,
            "caption": caption if caption and not CAPTION_JUNK_RE.search(caption) else "",
            "alt": alt or "",
        }
        found.append(rec)
        return rec

    search_root = container
    for img in search_root.find_all("img"):
        parent_blob = " ".join(class_blob(p) for p in img.parents if isinstance(p, Tag))
        if JUNK_CLASS_RE.search(parent_blob):
            continue
        if img.find_parent(class_=JUNK_CLASS_RE):
            continue
        src = img_src(img, base)
        add(src, "inline", nearby_caption(img), img.get("alt") or "")

    for iframe in search_root.find_all("iframe"):
        src = iframe.get("src") or ""
        yid = youtube_id(src)
        if yid:
            add(
                f"https://img.youtube.com/vi/{yid}/maxresdefault.jpg",
                "embed",
                (iframe.get("title") or "").strip(),
                iframe.get("title") or "",
            )

    # Hero / OG only if it is not the same plate as an in-body figure.
    og = meta(soup, "og:image", "og:image:url", "twitter:image")
    og_url = abs_url(base, og) if og else None
    if og_url and (norm_url(og_url) or og_url) not in seen_url:
        for wrap_sel in [".aas-content-featured", ".post-thumbnail", ".featured-image", ".wp-post-image"]:
            wrap = soup.select_one(wrap_sel)
            if not wrap:
                continue
            img = wrap if wrap.name == "img" else wrap.find("img")
            if img:
                src = img_src(img, base)
                rec = add(src, "featured", nearby_caption(img), img.get("alt") or "")
                if rec:
                    found.insert(0, found.pop())
                    return found
        rec = add(og_url, "featured")
        if rec:
            found.insert(0, found.pop())
    return found


def extract_blocks(container: Tag, base: str) -> list[dict]:
    """Walk the article DOM in source order. Paragraphs and figures stay interleaved."""
    blocks: list[dict] = []
    seen_url: set[str] = set()
    skip_re = re.compile(r"^(share|comment|subscribe|advertisement|read more)\b", re.I)

    def emit_image(img: Tag) -> None:
        parent_blob = " ".join(class_blob(p) for p in img.parents if isinstance(p, Tag))
        if JUNK_CLASS_RE.search(parent_blob):
            return
        src = img_src(img, base)
        if not src or skip_image_url(src, "inline"):
            return
        key = norm_url(src) or src
        if key in seen_url:
            return
        seen_url.add(key)
        blocks.append(
            {
                "type": "image",
                "url": src,
                "caption": nearby_caption(img),
                "alt": img.get("alt") or "",
                "role": "inline",
            }
        )

    def emit_para(text: str, kind: str = "para") -> None:
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            return
        if len(text) < 40 and skip_re.search(text):
            return
        low = text.lower()
        if low in {"share", "share share comment", "comment"}:
            return
        if re.search(r"share your perspective|reply to other readers|leave a comment|join the conversation", low):
            return
        blocks.append({"type": kind, "text": text})

    seen_nodes: set[int] = set()
    for el in container.descendants:
        if not isinstance(el, Tag) or id(el) in seen_nodes:
            continue
        if el.name in {"script", "style", "noscript"}:
            continue
        if el.name == "figure":
            img = el.find("img")
            if img:
                emit_image(img)
                seen_nodes.add(id(img))
            continue
        if el.name == "img":
            emit_image(el)
            continue
        if el.name == "iframe":
            src = el.get("src") or ""
            yid = youtube_id(src)
            if yid:
                thumb = f"https://img.youtube.com/vi/{yid}/maxresdefault.jpg"
                key = norm_url(thumb)
                if key not in seen_url:
                    seen_url.add(key)
                    blocks.append(
                        {
                            "type": "image",
                            "url": thumb,
                            "caption": (el.get("title") or "").strip(),
                            "alt": el.get("title") or "",
                            "role": "embed",
                        }
                    )
            continue
        if el.name in {"h2", "h3", "h4"}:
            emit_para(el.get_text(" ", strip=True), "heading")
            continue
        if el.name == "p":
            if el.find_parent("figure"):
                continue
            emit_para(el.get_text(" ", strip=True), "para")
            continue
    return blocks


def extract_paragraphs(container: Tag) -> list[str]:
    paras: list[str] = []
    # prefer explicit <p> in reading order, skip empty / share crumbs
    skip_re = re.compile(r"^(share|comment|subscribe|advertisement|read more)\b", re.I)
    for p in container.find_all("p"):
        if p.find_parent(["blockquote"]) and p.find_parent("blockquote") is not None:
            text = p.get_text(" ", strip=True)
        else:
            text = p.get_text(" ", strip=True)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) < 40 and skip_re.search(text):
            continue
        if not text:
            continue
        low = text.lower()
        if low in {"share", "share share comment", "comment"}:
            continue
        if re.search(r"share your perspective|reply to other readers|leave a comment|join the conversation", low):
            continue
        paras.append(text)

    if len(paras) >= 2:
        return paras

    # fallback: split text blocks
    raw = container.get_text("\n", strip=True)
    chunks = [re.sub(r"\s+", " ", c).strip() for c in raw.split("\n") if c.strip()]
    return [c for c in chunks if len(c) > 40]


EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002700-\U000027BF"
    "\U0001F000-\U0001F0FF"
    "\U0001F100-\U0001F1FF"
    "\U0001F200-\U0001F2FF"
    "\ufe0f"
    "]+"
)


def strip_emoji(text: str) -> str:
    return re.sub(r"\s+", " ", EMOJI_RE.sub("", text)).strip()


def extract_title(soup: BeautifulSoup, container: Tag) -> str:
    candidates = []
    for h1 in soup.find_all("h1"):
        t = re.sub(r"\s+", " ", h1.get_text(" ", strip=True)).strip()
        t = strip_emoji(t)
        if 8 <= len(t) <= 200:
            candidates.append(t)
    # Prefer a real headline over social-share og:title clickbait
    if candidates:
        # skip generic UI headings
        ui = re.compile(r"^(join|sign in|welcome|menu|search)\b", re.I)
        good = [t for t in candidates if not ui.search(t)]
        if good:
            return good[0]
        return candidates[0]
    og = meta(soup, "og:title", "twitter:title")
    if og:
        return re.sub(r"\s+[—|\-]\s+.*$", "", og).strip() or og
    if soup.title:
        return re.sub(r"\s+[—|\-]\s+.*$", "", soup.title.get_text(strip=True)).strip()
    return ""


def extract_author(soup: BeautifulSoup) -> str:
    a = meta(soup, "author", "article:author", "og:article:author")
    if a:
        return re.sub(r"^https?://.*", "", a).strip() or a
    for sel in [".author", ".byline", "[rel='author']", "[itemprop='author']"]:
        el = soup.select_one(sel)
        if el:
            t = el.get_text(" ", strip=True)
            t = re.sub(r"^by\s+", "", t, flags=re.I)
            if 2 < len(t) < 80:
                return t
    return ""


def extract_date(soup: BeautifulSoup) -> str:
    d = meta(soup, "article:published_time", "og:published_time", "pubdate", "date")
    if d:
        return d[:10] if len(d) >= 10 and d[4] == "-" else d
    t = soup.find("time")
    if t:
        return (t.get("datetime") or t.get_text(strip=True))[:16]
    return ""


def download(url: str, dest: Path) -> bool:
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
        r.raise_for_status()
        ctype = r.headers.get("content-type", "")
        if "html" in ctype and len(r.content) < 2000:
            return False
        dest.write_bytes(r.content)
        return dest.stat().st_size > 800
    except Exception as exc:
        print(f"[warn] image failed {url}: {exc}", file=sys.stderr)
        return False


def run(url: str, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    img_dir = out_dir / "images"
    img_dir.mkdir(exist_ok=True)

    r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    html = r.text
    (out_dir / "source.html").write_text(html, encoding="utf-8", errors="replace")

    soup = BeautifulSoup(html, "html.parser")
    title = extract_title(soup, soup)
    author = extract_author(soup)
    date = extract_date(soup)
    source_name = meta(soup, "og:site_name") or urlparse(url).netloc.replace("www.", "")

    container = pick_container(soup)
    clean_tree(container)
    blocks = extract_blocks(container, url)
    paragraphs = [b["text"] for b in blocks if b.get("type") in {"para", "heading"}]
    if len(paragraphs) < 2:
        paragraphs = extract_paragraphs(container)
    images = collect_images(soup, container, url)

    # Merge any block-level images missing from collect_images (order already in blocks).
    by_url = {norm_url(im["url"]): im for im in images}
    for b in blocks:
        if b.get("type") != "image":
            continue
        key = norm_url(b.get("url") or "")
        if key and key not in by_url:
            images.append(
                {
                    "url": b["url"],
                    "role": b.get("role") or "inline",
                    "caption": b.get("caption") or "",
                    "alt": b.get("alt") or "",
                }
            )
            by_url[key] = images[-1]

    saved = []
    seen_hash: set[str] = set()
    seen_phash: set[str] = set()
    url_to_file: dict[str, str] = {}
    for i, im in enumerate(images):
        ext = Path(urlparse(im["url"]).path).suffix.lower() or ".jpg"
        if ext not in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
            ext = ".jpg"
        fname = f"{i:02d}_{im['role']}{ext}"
        dest = img_dir / fname
        ok = download(im["url"], dest)
        if not ok and im["role"] == "embed" and "maxresdefault" in im["url"]:
            fallback = im["url"].replace("maxresdefault", "hqdefault")
            if download(fallback, dest):
                im = dict(im)
                im["url"] = fallback
                ok = True
        if not ok:
            continue
        if is_duplicate(dest, seen_hash, seen_phash):
            dest.unlink(missing_ok=True)
            continue
        rec = dict(im)
        rec["file"] = str(dest)
        rec["sha256"] = file_sha256(dest)
        rec["phash"] = percept_key(dest)
        saved.append(rec)
        url_to_file[norm_url(rec["url"])] = str(dest)

    placed_blocks = []
    used_files: set[str] = set()
    for b in blocks:
        if b.get("type") != "image":
            placed_blocks.append(b)
            continue
        fpath = url_to_file.get(norm_url(b.get("url") or ""))
        if not fpath or fpath in used_files:
            continue
        used_files.add(fpath)
        nb = dict(b)
        nb["file"] = fpath
        placed_blocks.append(nb)

    data = {
        "url": url,
        "title": title,
        "author": author,
        "date": date,
        "source_name": source_name,
        "paragraphs": paragraphs,
        "images": saved,
        "blocks": placed_blocks,
    }
    (out_dir / "article.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: (len(v) if k in {"paragraphs", "images"} else v) for k, v in data.items()}, ensure_ascii=False, indent=2))
    return data


def main() -> None:
    ap = argparse.ArgumentParser(description="Extract article text + images from a URL")
    ap.add_argument("url")
    ap.add_argument("--out", required=True, help="Output directory")
    args = ap.parse_args()
    run(args.url, Path(args.out))


if __name__ == "__main__":
    main()
