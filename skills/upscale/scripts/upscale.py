#!/usr/bin/env python3
"""Lanczos tiled upscale to a vector/tensor baseline raster."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

SCALE_CANDIDATES = (2.0, 1.5, 1.25)
MAX_MP = 80.0
MAX_LONG_EDGE = 12000
RAM_FRACTION = 0.45
OVERHEAD_BYTES = 150 * 1024 * 1024
TILE_SRC_H = 360
OVERLAP_SRC = 12


def available_ram_bytes() -> int:
    try:
        with open("/proc/meminfo", encoding="utf-8") as fh:
            for line in fh:
                if line.startswith("MemAvailable:"):
                    return int(line.split()[1]) * 1024
    except OSError:
        pass
    return 512 * 1024 * 1024


def choose_scale(w: int, h: int) -> float:
    avail = available_ram_bytes()
    budget = max(int(avail * RAM_FRACTION) - OVERHEAD_BYTES, 64 * 1024 * 1024)
    src_mp = (w * h) / 1e6
    for scale in SCALE_CANDIDATES:
        nw = max(1, int(round(w * scale)))
        nh = max(1, int(round(h * scale)))
        dest_mp = (nw * nh) / 1e6
        rgb_bytes = nw * nh * 3
        if dest_mp <= MAX_MP and max(nw, nh) <= MAX_LONG_EDGE and rgb_bytes <= budget:
            return scale
    if src_mp <= MAX_MP and max(w, h) <= MAX_LONG_EDGE:
        return 1.0
    return 1.0


def parse_formats(raw: str) -> list[str]:
    allowed = {"png", "tiff", "tif", "webp", "npy", "pt", "svg", "pdf"}
    out: list[str] = []
    for token in raw.replace(";", ",").split(","):
        key = token.strip().lower().lstrip(".")
        if not key:
            continue
        if key == "tif":
            key = "tiff"
        if key not in allowed:
            raise SystemExit(f"unsupported format: {key}")
        if key not in out:
            out.append(key)
    if "png" not in out:
        out.insert(0, "png")
    return out


def resize_tiled(src: Image.Image, scale: float) -> Image.Image:
    w, h = src.size
    nw = max(1, int(round(w * scale)))
    nh = max(1, int(round(h * scale)))
    if scale == 1.0:
        return src.copy()

    dst_mode = src.mode if src.mode in {"RGB", "RGBA", "L"} else "RGB"
    if src.mode != dst_mode:
        work = src.convert(dst_mode)
    else:
        work = src

    dest = Image.new(dst_mode, (nw, nh))
    y = 0
    while y < h:
        y1 = min(h, y + TILE_SRC_H)
        top = max(0, y - OVERLAP_SRC)
        bot = min(h, y1 + OVERLAP_SRC)
        strip = work.crop((0, top, w, bot))
        tw = nw
        th = max(1, int(round(strip.size[1] * scale)))
        resized = strip.resize((tw, th), Image.Resampling.LANCZOS)
        src_top_off = y - top
        dst_y = int(round(y * scale))
        dst_h = int(round(y1 * scale)) - dst_y
        crop_top = int(round(src_top_off * scale))
        crop_bot = crop_top + dst_h
        if crop_bot > resized.size[1]:
            crop_bot = resized.size[1]
            dst_h = crop_bot - crop_top
        piece = resized.crop((0, crop_top, tw, crop_bot))
        dest.paste(piece, (0, dst_y))
        y = y1
        del strip, resized, piece
    return dest


def save_png(im: Image.Image, path: Path) -> None:
    params = {"optimize": True, "compress_level": 6}
    if "dpi" in im.info:
        params["dpi"] = im.info["dpi"]
    else:
        params["dpi"] = (300, 300)
    im.save(path, format="PNG", **params)


def save_tiff(im: Image.Image, path: Path) -> None:
    im.save(path, format="TIFF", compression="tiff_lzw", dpi=im.info.get("dpi", (300, 300)))


def save_webp(im: Image.Image, path: Path) -> None:
    im.save(path, format="WEBP", lossless=True, quality=100, method=4)


def save_npy(im: Image.Image, path: Path) -> None:
    arr = np.asarray(im)
    np.save(path, arr)


def save_pt(im: Image.Image, path: Path) -> None:
    try:
        import torch
    except ImportError as exc:
        raise SystemExit("torch is not available for --formats pt") from exc
    arr = np.asarray(im)
    tensor = torch.from_numpy(arr)
    torch.save(tensor, path)


def save_svg_quantized(im: Image.Image, path: Path, colors: int = 16) -> None:
    """Coarse color-layer SVG. Not a substitute for a hand vector."""
    work = im.convert("RGB")
    max_edge = 2400
    w, h = work.size
    if max(w, h) > max_edge:
        scale = max_edge / float(max(w, h))
        work = work.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.Resampling.BOX)
    pal = work.quantize(colors=colors, method=Image.Quantize.MEDIANCUT)
    pw, ph = pal.size
    palette = pal.getpalette()[: colors * 3]
    px = list(pal.getdata())
    # Build one path-less SVG with an embedded PNG so the file is a valid
    # vector container that still holds the upscaled raster as the object.
    # Callers who need true outlines should run a dedicated tracer on the PNG.
    from io import BytesIO
    import base64

    buf = BytesIO()
    work.save(buf, format="PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    svg = (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{pw}" height="{ph}" viewBox="0 0 {pw} {ph}">\n'
        f'  <title>Upscaled raster baseline ({colors}-color preview container)</title>\n'
        f'  <image width="{pw}" height="{ph}" '
        f'xlink:href="data:image/png;base64,{b64}"/>\n'
        f"</svg>\n"
    )
    path.write_text(svg, encoding="utf-8")
    del palette, px


def save_pdf(im: Image.Image, path: Path) -> None:
    page = im.convert("RGB")
    page.save(path, format="PDF", resolution=300.0)


def main() -> int:
    parser = argparse.ArgumentParser(description="Upscale a raster to a vector/tensor baseline.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--outdir", default="/home/workdir/artifacts")
    parser.add_argument("--formats", default="png")
    parser.add_argument("--scale", type=float, default=0.0, help="Override auto scale.")
    args = parser.parse_args()

    src_path = Path(args.input).expanduser().resolve()
    if not src_path.is_file():
        raise SystemExit(f"input not found: {src_path}")

    outdir = Path(args.outdir).expanduser().resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    formats = parse_formats(args.formats)
    src = Image.open(src_path)
    src.load()
    w, h = src.size
    scale = float(args.scale) if args.scale and args.scale > 0 else choose_scale(w, h)
    nw = max(1, int(round(w * scale)))
    nh = max(1, int(round(h * scale)))

    dest = resize_tiled(src, scale)
    if src.info.get("dpi"):
        dest.info["dpi"] = src.info["dpi"]
    else:
        dest.info["dpi"] = (300, 300)

    stem = src_path.stem
    written: dict[str, str] = {}
    base = outdir / f"{stem}-upscale-{nw}x{nh}"

    for fmt in formats:
        if fmt == "png":
            path = base.with_suffix(".png")
            save_png(dest, path)
        elif fmt == "tiff":
            path = base.with_suffix(".tiff")
            save_tiff(dest, path)
        elif fmt == "webp":
            path = base.with_suffix(".webp")
            save_webp(dest, path)
        elif fmt == "npy":
            path = base.with_suffix(".npy")
            save_npy(dest, path)
        elif fmt == "pt":
            path = base.with_suffix(".pt")
            save_pt(dest, path)
        elif fmt == "svg":
            path = base.with_suffix(".svg")
            save_svg_quantized(dest, path)
        elif fmt == "pdf":
            path = base.with_suffix(".pdf")
            save_pdf(dest, path)
        else:
            continue
        written[fmt] = str(path)

    report = {
        "source": str(src_path),
        "source_size": [w, h],
        "source_mode": src.mode,
        "scale": scale,
        "dest_size": [nw, nh],
        "dest_mode": dest.mode,
        "dest_mp": round((nw * nh) / 1e6, 3),
        "available_ram_mb": round(available_ram_bytes() / (1024 * 1024), 1),
        "outputs": {k: {"path": v, "bytes": os.path.getsize(v)} for k, v in written.items()},
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
