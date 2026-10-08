#!/usr/bin/env python3
"""Fetch a URL as HTML and extract a print.json block stream. Ads stripped."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from html import unescape
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, Comment, NavigableString, Tag

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

JUNK_CLASS_RE = re.compile(
    r"(site-header|page-header|global-header|masthead-nav|site-footer|"
    r"site-nav|navbar|menu-bar|sidebar|related|recirc|keep-reading|"
    r"recommend|trending|popular-posts|share-buttons|social-share|"
    r"comments-area|comment-list|newsletter|subscribe-box|"
    r"promo|sponsor|advert|adsense|ad-slot|ad-unit|advertisement|"
    r"breadcrumb|pagination|tag-list|cookie-banner|paywall|modal|popup|"
    r"card-image|card-grid|outbrain|taboola|google-auto-placed|"
    r"social-bar|follow-us|promoted)",
    re.I,
)

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
    "main",
]

BANNER_RE = re.compile(
    r"(hero|banner|overlay|cover|masthead|featured|splash|lead-art|full-bleed)",
    re.I,
)

CAPTION_JUNK_RE = re.compile(
    r"(advert|sponsor|promoted|related|trending|subscribe|"
    r"newsletter|click here|read more|photo illustration)",
    re.I,
)

SKIP_P_RE = re.compile(
    r"^(share|comment|subscribe|advertisement|read more|advertisment)\b",
    re.I,
)

EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002700-\U000027BF"
    "\U0001F000-\U0001F2FF"
    "\ufe0f"
    "]+"
)


def class_blob(el: Tag) -> str:
    if not isinstance(el, Tag) or el.attrs is None:
        return ""
    cls = el.get("class") or []
    if isinstance(cls, str):
        cls = [cls]
    return " ".join(str(c) for c in cls) + " " + str(el.get("id") or "")


def is_junk_container(el: Tag) -> bool:
    return bool(JUNK_CLASS_RE.search(class_blob(el)))


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
        return soup.body or soup
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]


def clean_tree(root: Tag) -> None:
    for tag in list(root.find_all(["script", "style", "noscript", "form", "svg", "button", "iframe"])):
        src = (tag.get("src") or "") if isinstance(tag, Tag) else ""
        if tag.name == "iframe" and ("youtube" in src or "youtu.be" in src or "vimeo" in src):
            continue
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
        if el.name in {"p", "h1", "h2", "h3", "h4", "img", "figure", "li", "blockquote", "iframe"}:
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
    src = unescape(src.strip())
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
    m = re.search(r"(?:youtube\.com/embed/|youtu\.be/)([A-Za-z0-9_-]{6,})", src or "")
    return m.group(1) if m else None


def img_src(base: str, img: Tag) -> str | None:
    return best_from_srcset(base, img.get("srcset") or img.get("data-srcset")) or abs_url(
        base,
        img.get("src")
        or img.get("data-src")
        or img.get("data-lazy-src")
        or img.get("data-original"),
    )


def looks_like_ad_url(url: str) -> bool:
    low = url.lower()
    needles = (
        "doubleclick",
        "googlesyndication",
        "adservice",
        "/ads/",
        "adserver",
        "taboola",
        "outbrain",
        "1x1",
        "pixel.gif",
        "sprite",
        "gravatar",
    )
    return any(n in low for n in needles)


def looks_like_chrome_image(url: str, alt: str, blob: str) -> bool:
    low = (url + " " + alt + " " + blob).lower()
    if any(x in low for x in ("logo", "icon", "emoji", "badge", "avatar", "sprite")):
        return True
    return False


def is_banner_context(el: Tag, index: int, before_first_p: bool) -> bool:
    blob = class_blob(el)
    for p in el.parents:
        if isinstance(p, Tag):
            blob += " " + class_blob(p)
    if BANNER_RE.search(blob):
        return True
    if index == 0 and before_first_p:
        return True
    return False


def strip_emoji(text: str) -> str:
    return re.sub(r"\s+", " ", EMOJI_RE.sub("", text or "")).strip()


def extract_title(soup: BeautifulSoup) -> str:
    for h1 in soup.find_all("h1"):
        t = strip_emoji(h1.get_text(" ", strip=True))
        if 8 <= len(t) <= 220:
            if not re.match(r"^(join|sign in|welcome|menu|search)\b", t, re.I):
                return t
    og = meta(soup, "og:title", "twitter:title")
    if og:
        return re.sub(r"\s+[—|\-]\s+.*$", "", strip_emoji(og)).strip() or strip_emoji(og)
    if soup.title:
        return re.sub(r"\s+[—|\-]\s+.*$", "", strip_emoji(soup.title.get_text(strip=True))).strip()
    return ""


def extract_author(soup: BeautifulSoup) -> str:
    a = meta(soup, "author", "article:author", "og:article:author")
    if a and not a.startswith("http"):
        return strip_emoji(a)
    for sel in [".author", ".byline", "[rel='author']", "[itemprop='author']"]:
        el = soup.select_one(sel)
        if el:
            t = strip_emoji(el.get_text(" ", strip=True))
            t = re.sub(r"^by\s+", "", t, flags=re.I)
            if 2 < len(t) < 80:
                return t
    return ""


def extract_date(soup: BeautifulSoup) -> str:
    return meta(soup, "article:published_time", "og:published_time", "pubdate", "date") or ""


def extract_site(soup: BeautifulSoup, url: str) -> str:
    site = meta(soup, "og:site_name")
    if site:
        return strip_emoji(site)
    host = urlparse(url).netloc
    return host.removeprefix("www.")


def walk_blocks(container: Tag, base: str) -> list[dict]:
    blocks: list[dict] = []
    seen_img: set[str] = set()
    saw_paragraph = False
    img_index = 0

    def add_image(img: Tag) -> None:
        nonlocal img_index
        parent_blob = " ".join(class_blob(p) for p in img.parents if isinstance(p, Tag))
        if JUNK_CLASS_RE.search(parent_blob):
            return
        src = img_src(base, img)
        if not src or src in seen_img or looks_like_ad_url(src):
            return
        alt = strip_emoji(img.get("alt") or "")
        if looks_like_chrome_image(src, alt, parent_blob + " " + class_blob(img)):
            return
        seen_img.add(src)
        cap = strip_emoji(nearby_caption(img))
        if cap and CAPTION_JUNK_RE.search(cap):
            cap = ""
        role = "banner" if is_banner_context(img, img_index, not saw_paragraph) else "figure"
        img_index += 1
        blocks.append({"type": role, "url": src, "caption": cap, "alt": alt})

    interesting = container.find_all(
        ["h1", "h2", "h3", "h4", "p", "li", "blockquote", "img", "figure", "iframe"]
    )
    for el in interesting:
        if not isinstance(el, Tag):
            continue
        parent_blob = " ".join(class_blob(p) for p in el.parents if isinstance(p, Tag))
        if JUNK_CLASS_RE.search(parent_blob) or is_junk_container(el):
            continue
        if el.name in {"h2", "h3", "h4"} or (el.name == "h1" and container.find("h1") is not el):
            text = strip_emoji(el.get_text(" ", strip=True))
            if 2 <= len(text) <= 220:
                blocks.append({"type": "heading", "level": int(el.name[1]), "text": text})
            continue
        if el.name == "p":
            if el.find_parent("blockquote") or el.find_parent("li") or el.find_parent("figcaption"):
                continue
            for img in el.find_all("img"):
                add_image(img)
            text = strip_emoji(el.get_text(" ", strip=True))
            if not text:
                continue
            if len(text) < 40 and SKIP_P_RE.search(text):
                continue
            low = text.lower()
            if low in {"share", "share share comment", "comment"}:
                continue
            if re.search(r"share your perspective|leave a comment|join the conversation|subscribe to", low):
                continue
            blocks.append({"type": "paragraph", "text": text})
            saw_paragraph = True
            continue
        if el.name == "li":
            if el.find_parent("nav"):
                continue
            text = strip_emoji(el.get_text(" ", strip=True))
            if text:
                blocks.append({"type": "list_item", "text": text})
            continue
        if el.name == "blockquote":
            text = strip_emoji(el.get_text(" ", strip=True))
            if text:
                blocks.append({"type": "quote", "text": text})
            continue
        if el.name == "img":
            if el.find_parent("p") or el.find_parent("figure"):
                continue
            add_image(el)
            continue
        if el.name == "figure":
            img = el.find("img")
            if img:
                add_image(img)
            continue
        if el.name == "iframe":
            yid = youtube_id(el.get("src") or "")
            if yid:
                url = f"https://img.youtube.com/vi/{yid}/maxresdefault.jpg"
                if url not in seen_img:
                    seen_img.add(url)
                    blocks.append(
                        {
                            "type": "figure",
                            "url": url,
                            "caption": strip_emoji(el.get("title") or ""),
                            "alt": strip_emoji(el.get("title") or ""),
                        }
                    )
    return blocks


def download_image(url: str, dest_dir: Path, session: requests.Session) -> str | None:
    try:
        r = session.get(url, timeout=25, stream=True)
        r.raise_for_status()
        data = r.content
        if len(data) < 800:
            return None
        ext = ".jpg"
        ctype = (r.headers.get("content-type") or "").lower()
        if "png" in ctype:
            ext = ".png"
        elif "webp" in ctype:
            ext = ".webp"
        elif "gif" in ctype:
            ext = ".gif"
        name = hashlib.sha1(url.encode("utf-8")).hexdigest()[:16] + ext
        path = dest_dir / name
        path.write_bytes(data)
        return str(path)
    except Exception:
        return None


def slugify(title: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", (title or "print").lower()).strip("-")
    return "-".join([w for w in text.split("-") if w])[:60] or "print"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("url")
    p.add_argument("--out", required=True)
    args = p.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    img_dir = out / "images"
    img_dir.mkdir(exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"})
    resp = session.get(args.url, timeout=30)
    resp.raise_for_status()
    html = resp.text
    (out / "source.html").write_text(html, encoding="utf-8")

    soup = BeautifulSoup(html, "lxml")
    container = pick_container(soup)
    clean_tree(container)

    title = extract_title(soup)
    blocks = walk_blocks(container, args.url)

    og = meta(soup, "og:image", "og:image:url", "twitter:image")
    og_url = abs_url(args.url, og) if og else None
    has_banner = any(b.get("type") == "banner" for b in blocks)
    if og_url and not has_banner and not looks_like_ad_url(og_url):
        blocks.insert(0, {"type": "banner", "url": og_url, "caption": "", "alt": ""})

    for b in blocks:
        if b.get("type") in {"banner", "figure"} and b.get("url"):
            local = download_image(b["url"], img_dir, session)
            b["path"] = local or ""

    payload = {
        "source_url": args.url,
        "title": title,
        "author": extract_author(soup),
        "date": extract_date(soup),
        "site": extract_site(soup, args.url),
        "slug": slugify(title),
        "blocks": blocks,
        "house": {
            "anchor": "Digital Marketing Company",
            "href": "https://digitalmarketingco.org",
            "domain_plain": "DigitalMarketingCo.org",
        },
        "owner": {
            "legal": "Web Development Corporation, a Delaware Corporation",
            "short": "Web Development Corporation",
            "founded": 2012,
        },
    }
    (out / "print.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {out / 'print.json'} blocks={len(blocks)} title={title!r}")


if __name__ == "__main__":
    main()
