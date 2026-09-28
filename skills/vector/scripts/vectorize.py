#!/usr/bin/env python3
"""Raster or PDF page -> SVG with traced outlines plus high-confidence live text."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

VTRACER_DEFAULTS = dict(
    colormode="color",
    hierarchical="stacked",
    mode="spline",
    filter_speckle=1,
    color_precision=8,
    layer_difference=8,
    corner_threshold=30,
    length_threshold=3.0,
    max_iterations=10,
    splice_threshold=30,
    path_precision=3,
)

CONF_MIN = 85
MIN_TEXT_H = 14
MAX_WORK_EDGE = 5400


def ensure_vtracer():
    try:
        import vtracer  # noqa: F401
    except ImportError:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "vtracer", "cairosvg", "-i", "https://pypi.org/simple"],
            check=True,
        )


def parse_formats(raw: str) -> list[str]:
    allowed = {"svg", "png", "pdf"}
    out: list[str] = []
    for token in raw.replace(";", ",").split(","):
        key = token.strip().lower().lstrip(".")
        if not key:
            continue
        if key not in allowed:
            raise SystemExit(f"unsupported format: {key}")
        if key not in out:
            out.append(key)
    if "svg" not in out:
        out.insert(0, "svg")
    return out


def rasterize_pdf_page(pdf_path: Path, dest_png: Path, page: int = 1, dpi: int = 300) -> Path:
    prefix = dest_png.with_suffix("")
    subprocess.run(
        ["pdftoppm", "-png", "-r", str(dpi), "-f", str(page), "-l", str(page), str(pdf_path), str(prefix)],
        check=True,
    )
    produced = Path(f"{prefix}-{page}.png")
    if not produced.exists():
        candidates = list(prefix.parent.glob(prefix.name + "*.png"))
        if not candidates:
            raise SystemExit("pdftoppm produced no PNG")
        produced = candidates[0]
    produced.replace(dest_png)
    return dest_png


def choose_work_image(src: Image.Image, fullres: bool) -> Image.Image:
    w, h = src.size
    long_edge = max(w, h)
    work = src if src.mode in {"RGB", "RGBA"} else src.convert("RGB")
    if fullres or long_edge <= MAX_WORK_EDGE:
        return work
    scale = MAX_WORK_EDGE / float(long_edge)
    nw, nh = max(1, int(round(w * scale))), max(1, int(round(h * scale)))
    return work.resize((nw, nh), Image.Resampling.BOX)


def run_vtracer(png_path: Path, svg_path: Path) -> None:
    ensure_vtracer()
    import vtracer

    vtracer.convert_image_to_svg_py(str(png_path), str(svg_path), **VTRACER_DEFAULTS)


def _ocr_data(im: Image.Image, psm: int, ox: int = 0, oy: int = 0) -> list[dict]:
    import pytesseract

    data = pytesseract.image_to_data(
        im, config=f"--oem 3 --psm {psm}", output_type=pytesseract.Output.DICT
    )
    rows = []
    for i, raw in enumerate(data["text"]):
        text = (raw or "").strip()
        if not text or not re.search(r"[A-Za-z0-9]", text):
            continue
        try:
            conf = float(data["conf"][i])
        except (TypeError, ValueError):
            continue
        if conf < CONF_MIN:
            continue
        w, h = int(data["width"][i]), int(data["height"][i])
        if h < MIN_TEXT_H or w < 8:
            continue
        rows.append(
            {
                "text": text,
                "conf": conf,
                "left": int(data["left"][i]) + ox,
                "top": int(data["top"][i]) + oy,
                "width": w,
                "height": h,
            }
        )
    return rows


def ocr_words(im: Image.Image) -> list[dict]:
    w, h = im.size
    left_w = max(200, int(w * 0.16))
    right0 = min(w - 200, int(w * 0.84))
    regions = [
        (0, int(h * 0.03), left_w, h, 6),
        (right0, 0, w, h, 6),
        (int(w * 0.12), 0, int(w * 0.88), max(120, int(h * 0.045)), 7),
    ]
    words: list[dict] = []
    for x0, y0, x1, y1, psm in regions:
        y = y0
        while y < y1:
            yb = min(y1, y + 900)
            crop = im.crop((x0, y, x1, yb))
            words.extend(_ocr_data(crop, psm, ox=x0, oy=y))
            y = yb

    def iou(a, b) -> float:
        ax2, ay2 = a["left"] + a["width"], a["top"] + a["height"]
        bx2, by2 = b["left"] + b["width"], b["top"] + b["height"]
        ix1, iy1 = max(a["left"], b["left"]), max(a["top"], b["top"])
        ix2, iy2 = min(ax2, bx2), min(ay2, by2)
        iw, ih = max(0, ix2 - ix1), max(0, iy2 - iy1)
        inter = iw * ih
        if inter <= 0:
            return 0.0
        union = a["width"] * a["height"] + b["width"] * b["height"] - inter
        return inter / union if union else 0.0

    words.sort(key=lambda r: (-r["conf"], -r["height"]))
    kept: list[dict] = []
    for row in words:
        if any(iou(row, k) > 0.45 for k in kept):
            continue
        kept.append(row)
    return kept


def sample_colors(im: Image.Image, box: dict) -> tuple[str, str]:
    x, y, w, h = box["left"], box["top"], box["width"], box["height"]
    pad = 2
    x0, y0 = max(0, x - pad), max(0, y - pad)
    x1, y1 = min(im.size[0], x + w + pad), min(im.size[1], y + h + pad)
    crop = np.asarray(im.convert("RGB").crop((x0, y0, x1, y1)))
    if crop.size == 0:
        return "#ffffff", "#000000"
    frame = np.concatenate(
        [crop[0, :, :], crop[-1, :, :], crop[:, 0, :], crop[:, -1, :]], axis=0
    ).astype(np.float32)
    backdrop = np.median(frame, axis=0)
    flat = crop.reshape(-1, 3).astype(np.float32)
    dist = np.linalg.norm(flat - backdrop, axis=1)
    far = flat[dist >= max(18.0, np.percentile(dist, 70))]
    if len(far) == 0:
        far = flat

    def hexify(rgb) -> str:
        r, g, b = [int(max(0, min(255, round(v)))) for v in rgb]
        return f"#{r:02x}{g:02x}{b:02x}"

    return hexify(far.mean(axis=0)), hexify(backdrop)


def inject_live_text(svg_text: str, words: list[dict], im: Image.Image) -> tuple[str, int]:
    idx = svg_text.rfind("</svg>")
    if idx < 0:
        raise SystemExit("VTracer SVG missing </svg>")
    parts = ['  <g id="live-text">']
    count = 0
    for box in words:
        fill, back = sample_colors(im, box)
        h = box["height"]
        family = (
            "Liberation Serif, Times New Roman, Times, serif"
            if h >= 28
            else "Liberation Sans, Arial, Helvetica, sans-serif"
        )
        size = max(8, int(round(h * 0.86)))
        x, y, w = box["left"], box["top"], box["width"]
        parts.append(
            f'    <rect x="{x - 1}" y="{y - 1}" width="{w + 2}" height="{h + 2}" fill="{back}"/>'
        )
        parts.append(
            f'    <text x="{x}" y="{y + int(round(h * 0.82))}" font-family="{family}" '
            f'font-size="{size}" fill="{fill}">{escape(box["text"])}</text>'
        )
        count += 1
    parts.append("  </g>")
    return svg_text[:idx] + "\n" + "\n".join(parts) + "\n" + svg_text[idx:], count


def path_count(svg_text: str) -> int:
    return len(re.findall(r"<path\b", svg_text))


def render_with_cairo(svg_path: Path, dest: Path, kind: str, preview_w: int = 1200) -> None:
    try:
        import cairosvg
    except ImportError:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "cairosvg", "-i", "https://pypi.org/simple"],
            check=True,
        )
        import cairosvg

    if kind == "png":
        cairosvg.svg2png(url=str(svg_path), write_to=str(dest), output_width=preview_w)
    elif kind == "pdf":
        cairosvg.svg2pdf(url=str(svg_path), write_to=str(dest))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--outdir", default="/home/workdir/artifacts")
    parser.add_argument("--formats", default="svg,png,pdf")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--fullres", action="store_true")
    parser.add_argument("--skip-ocr", action="store_true")
    args = parser.parse_args()

    src_path = Path(args.input).expanduser().resolve()
    if not src_path.is_file():
        raise SystemExit(f"input not found: {src_path}")
    outdir = Path(args.outdir).expanduser().resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    formats = parse_formats(args.formats)
    stem = re.sub(r"-upscale-\d+x\d+$", "", src_path.stem)

    tmp = Path(tempfile.mkdtemp(prefix="vectorize-"))
    try:
        work_png = tmp / "work.png"
        if src_path.suffix.lower() == ".pdf":
            rasterize_pdf_page(src_path, work_png, page=args.page)
            raw = Image.open(work_png)
        else:
            raw = Image.open(src_path)
            raw.load()
        src_size = raw.size
        work = choose_work_image(raw, fullres=args.fullres)
        work.convert("RGB").save(work_png, "PNG")

        raw_svg = tmp / "trace.svg"
        run_vtracer(work_png, raw_svg)
        svg_text = raw_svg.read_text(encoding="utf-8")

        live_count = 0
        if not args.skip_ocr:
            words = ocr_words(work.convert("RGB"))
            svg_text, live_count = inject_live_text(svg_text, words, work.convert("RGB"))

        svg_path = outdir / f"{stem}-vector.svg"
        svg_path.write_text(svg_text, encoding="utf-8")
        written = {"svg": {"path": str(svg_path), "bytes": svg_path.stat().st_size}}

        preview = outdir / f"{stem}-vector-preview.png"
        pdf_path = outdir / f"{stem}-vector.pdf"
        if "png" in formats:
            render_with_cairo(svg_path, preview, "png")
            written["png"] = {"path": str(preview), "bytes": preview.stat().st_size}
        if "pdf" in formats:
            render_with_cairo(svg_path, pdf_path, "pdf")
            written["pdf"] = {"path": str(pdf_path), "bytes": pdf_path.stat().st_size}

        report = {
            "source": str(src_path),
            "source_size": list(src_size),
            "work_size": list(work.size),
            "path_count": path_count(svg_text),
            "live_text_count": live_count,
            "outputs": written,
        }
        print(json.dumps(report, indent=2))
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
