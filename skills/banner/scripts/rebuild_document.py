#!/usr/bin/env python3
"""Banner-side wrapper using the reviewed adjacent images skill."""
from __future__ import annotations

import runpy
from pathlib import Path


def resolve_images() -> Path:
    adjacent = Path(__file__).resolve().parents[2] / "images"
    if (adjacent / "scripts/rebuild_document.py").is_file():
        return adjacent
    base = Path('/root/.codex/skills/remote-skills')
    for file in sorted(base.glob('*/SKILL.md')):
        head = file.read_text(encoding='utf-8', errors='replace').splitlines()[:20]
        if any(line.strip() == 'name: images' for line in head):
            return file.parent
    raise FileNotFoundError('Images skill rebuild script is unavailable')


if __name__ == "__main__":
    runpy.run_path(str(resolve_images() / 'scripts/rebuild_document.py'), run_name='__main__')
