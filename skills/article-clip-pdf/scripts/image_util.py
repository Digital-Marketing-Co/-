#!/usr/bin/env python3
"""Dedupe, hash, and LANCZOS upscale helpers for article-clip-pdf."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from PIL import Image as PILImage

TRACKING_QS = {
    "w", "h", "width", "height", "fit", "crop", "quality", "auto",
    "fm", "q", "dpr", "s", "ixlib", "ixid", "resize", "format",
}


def norm_url(url: str) -> str:
    if not url:
        return ""
    p = urlparse(url.strip())
    host = (p.netloc or "").lower()
    if host.startswith("www."):
        host = host[4:]
    path = re.sub(r"/+", "/", p.path or "")
    path = re.sub(r"-(?:\d+x\d+|scaled|rotated)\.(jpe?g|png|webp|gif)$", r".\1", path, flags=re.I)
    qs = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True) if k.lower() not in TRACKING_QS]
    query = urlencode(qs)
    return urlunparse(("", host, path.rstrip("/"), "", query, ""))


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def percept_bits(path: Path, size: int = 8) -> str:
    """8x8 average-hash bitstring. Near-identical plates collide even across jpg/webp."""
    try:
        im = PILImage.open(path)
        im = im.convert("L").resize((size, size), PILImage.Resampling.BILINEAR)
        pixels = list(im.getdata())
        avg = sum(pixels) / max(1, len(pixels))
        return "".join("1" if px >= avg else "0" for px in pixels)
    except Exception:
        return ""


def percept_key(path: Path, size: int = 8) -> str:
    bits = percept_bits(path, size=size)
    if not bits:
        return ""
    return hashlib.sha256(bits.encode()).hexdigest()[:16]


def hamming(a: str, b: str) -> int:
    if not a or not b or len(a) != len(b):
        return 64
    return sum(ch1 != ch2 for ch1, ch2 in zip(a, b))


def is_duplicate(path: Path, seen_hash: set[str], seen_phash: set[str]) -> bool:
    digest = file_sha256(path)
    if digest in seen_hash:
        return True
    bits = percept_bits(path)
    if bits:
        for prev in seen_phash:
            if hamming(bits, prev) <= 1:
                return True
    seen_hash.add(digest)
    if bits:
        seen_phash.add(bits)
    return False


def upscale_to_width(path: Path, target_px: int) -> Path:
    """LANCZOS-upscale so the bitmap is at least target_px wide. Never change aspect."""
    im = PILImage.open(path)
    if im.mode not in {"RGB", "L"}:
        if "A" in im.getbands():
            bg = PILImage.new("RGB", im.size, (255, 255, 255))
            bg.paste(im.convert("RGBA"), mask=im.convert("RGBA").split()[-1])
            im = bg
        else:
            im = im.convert("RGB")
    else:
        im = im.convert("RGB")
    w, h = im.size
    if w <= 0 or h <= 0:
        raise ValueError(f"bad image size {path}")
    if w < target_px:
        nh = max(1, int(round(h * (target_px / w))))
        im = im.resize((target_px, nh), PILImage.Resampling.LANCZOS)
        out = path.with_name(path.stem + f"_w{target_px}.jpg")
        im.save(out, "JPEG", quality=90, optimize=True)
        return out
    return path
