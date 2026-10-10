#!/usr/bin/env python3
"""Pick the parent builder, or fall back to stamp_images_into_pdf.py.

Usage
  python3 rebuild_document.py /path/to/slug-or-pdf
      [--manifest stamp-manifest.json]
      [--out /path/to/out.pdf]

Looks in the directory (or the PDF parent) for folio.json, monograph.json,
deep.json, atlas.json, book.json, list.json. Runs that builder when found.
Otherwise requires --manifest and writes a stamped PDF.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

IMAGES = Path(__file__).resolve().parents[1]
SKILLS = IMAGES.parent
STAMP = IMAGES / "scripts" / "stamp_images_into_pdf.py"

BUILDERS = [
    ("folio.json", SKILLS / "folio" / "scripts" / "build_folio_pdf.py"),
    ("monograph.json", SKILLS / "folio" / "scripts" / "build_monograph_pdf.py"),
    ("deep.json", SKILLS / "deep" / "scripts" / "build_deep_pdf.py"),
    ("atlas.json", SKILLS / "atlas" / "scripts" / "build_atlas_pdf.py"),
    ("book.json", SKILLS / "book" / "scripts" / "build_book_pdf.py"),
    ("list.json", SKILLS / "list" / "scripts" / "build_list_pdf.py"),
]


def find_root(target: Path) -> Path:
    if target.is_dir():
        return target
    return target.parent


def find_builder(root: Path) -> tuple[Path, Path] | None:
    for name, script in BUILDERS:
        js = root / name
        if js.is_file() and script.is_file():
            return js, script
    return None


def run(cmd: list[str]) -> None:
    print("+", " ".join(str(c) for c in cmd))
    subprocess.check_call(cmd)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("target")
    p.add_argument("--manifest", default="")
    p.add_argument("--out", default="")
    args = p.parse_args()
    target = Path(args.target).expanduser().resolve()
    root = find_root(target)
    hit = find_builder(root)
    if hit:
        js, script = hit
        cmd = [sys.executable, str(script), str(js)]
        if args.out:
            cmd.extend(["--out", str(Path(args.out).expanduser().resolve())])
        elif js.name == "deep.json":
            cmd.extend(["--out", str(target if target.suffix.lower() == ".pdf" else root / "deep.pdf")])
        run(cmd)
        return
    manifest = Path(args.manifest).expanduser() if args.manifest else root / "stamp-manifest.json"
    if not manifest.is_file():
        raise SystemExit(
            "No parent JSON builder and no stamp-manifest.json. "
            "Write the manifest, then rerun with --manifest."
        )
    cmd = [sys.executable, str(STAMP), str(manifest)]
    if args.out:
        cmd.extend(["--out", str(Path(args.out).expanduser().resolve())])
    run(cmd)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
    except Exception as exc:
        print(f"rebuild_document: {exc}", file=sys.stderr)
        sys.exit(1)
