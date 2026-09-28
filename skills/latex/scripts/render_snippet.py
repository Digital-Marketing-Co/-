#!/usr/bin/env python3
"""Compile one TeX or mathtext snippet to PNG, SVG, or PDF.

Preference: lualatex (Latin Modern) -> pdflatex -> matplotlib mathtext.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL = Path("/home/workdir/.grok/skills/latex")
PREAMBLE = SKILL / "assets" / "snippet-preamble.tex"


def _wrap(tex: str, mode: str) -> str:
    body = tex.strip()
    if mode == "display":
        if not body.startswith("\\["):
            body = "\\[\n" + body + "\n\\]"
    elif mode == "inline":
        if not body.startswith("\\("):
            body = "\\(" + body + "\\)"
    return body


def _compile_tex(body: str, work: Path, engine: str) -> Path | None:
    src = work / "snippet.tex"
    tmpl = PREAMBLE.read_text()
    src.write_text(tmpl.replace("BODY", body))
    cmd = [engine, "-interaction=nonstopmode", "-halt-on-error", "snippet.tex"]
    r = subprocess.run(cmd, cwd=work, capture_output=True, text=True)
    pdf = work / "snippet.pdf"
    if r.returncode != 0 or not pdf.exists():
        return None
    return pdf


def _pdf_to_png(pdf: Path, out: Path, dpi: int) -> None:
    subprocess.run(
        ["pdftoppm", "-png", "-singlefile", "-r", str(dpi), str(pdf), str(out.with_suffix(""))],
        check=True,
        capture_output=True,
    )
    if not out.exists():
        # pdftoppm writes <prefix>.png
        produced = out.with_suffix(".png")
        if produced.exists() and produced != out:
            produced.replace(out)


def _pdf_to_svg(pdf: Path, out: Path) -> bool:
    dvisvgm = shutil.which("dvisvgm")
    if not dvisvgm:
        return False
    r = subprocess.run(
        [dvisvgm, "--pdf", "--no-fonts", "-o", str(out), str(pdf)],
        capture_output=True,
        text=True,
    )
    return r.returncode == 0 and out.exists()


def _matplotlib_png(tex: str, out: Path, mode: str, dpi: int) -> bool:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return False
    fig = plt.figure(figsize=(8, 1.6) if mode == "display" else (6, 0.6))
    fig.patch.set_alpha(0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    wrapped = f"${tex}$" if not tex.strip().startswith("$") else tex
    try:
        ax.text(0.5, 0.5, wrapped, ha="center", va="center", fontsize=18 if mode == "display" else 12)
        fig.savefig(out, dpi=dpi, transparent=True)
    except Exception:
        plt.close(fig)
        return False
    plt.close(fig)
    return out.exists()


def render(tex: str, out: Path, mode: str, fmt: str, dpi: int) -> str:
    out.parent.mkdir(parents=True, exist_ok=True)
    body = _wrap(tex, mode)
    engines = [e for e in ("lualatex", "pdflatex") if shutil.which(e)]
    with tempfile.TemporaryDirectory(prefix="wca-latex-") as tmp:
        work = Path(tmp)
        pdf = None
        used = None
        for engine in engines:
            pdf = _compile_tex(body, work, engine)
            if pdf:
                used = engine
                break
        if pdf is None:
            if fmt == "png" and _matplotlib_png(tex, out, mode, dpi):
                return "matplotlib-mathtext"
            raise SystemExit("render_snippet: every engine failed, including matplotlib")
        if fmt == "pdf":
            shutil.copy(pdf, out)
            return used
        if fmt == "svg":
            if _pdf_to_svg(pdf, out):
                return used + "+dvisvgm"
            png = work / "snippet.png"
            _pdf_to_png(pdf, png, dpi)
            shutil.copy(png, out.with_suffix(".png"))
            raise SystemExit("svg conversion failed; wrote png sibling instead")
        _pdf_to_png(pdf, out, dpi)
        return used + "+pdftoppm"


def main() -> int:
    p = argparse.ArgumentParser(description="Compile a TeX snippet to an equation plate.")
    p.add_argument("--tex", help="TeX body (no documentclass)")
    p.add_argument("--file", help="Read TeX body from a file")
    p.add_argument("--mode", choices=("display", "inline", "text"), default="display")
    p.add_argument("--format", dest="fmt", choices=("png", "svg", "pdf"), default="png")
    p.add_argument("--dpi", type=int, default=300)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    if bool(args.tex) == bool(args.file):
        print("provide exactly one of --tex or --file", file=sys.stderr)
        return 2
    tex = args.tex if args.tex else Path(args.file).read_text()
    used = render(tex, Path(args.out), args.mode, args.fmt, args.dpi)
    print(f"wrote {args.out} via {used}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
