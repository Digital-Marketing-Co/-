#!/usr/bin/env python3
"""Banner-side wrapper: delegate to the images document builder."""
from __future__ import annotations

import runpy
from pathlib import Path


def _resolve_skill(name: str) -> Path:
    root = Path(__file__).resolve().parents[2]
    local = root / name
    if (local / "SKILL.md").is_file():
        return local
    for base in (Path.home() / ".local/share/dmc-skills", Path("/root/.codex/skills/remote-skills")):
        if (base / name / "SKILL.md").is_file():
            return base / name
        for file in base.glob("skill-*/SKILL.md"):
            head = file.read_text(encoding="utf-8", errors="replace").splitlines()[:8]
            if any(line.strip() == f"name: {name}" for line in head):
                return file.parent
    raise FileNotFoundError(f"Required skill not found: {name}")


def resolve_images() -> Path:
    """Resolve the canonical images skill without side effects."""
    return _resolve_skill("images")


if __name__ == "__main__":
    runpy.run_path(str(_resolve_skill("images") / "scripts/rebuild_document.py"), run_name="__main__")
