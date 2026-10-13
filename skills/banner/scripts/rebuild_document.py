#!/usr/bin/env python3

from pathlib import Path as _SkillPath
def _resolve_skill(name):
    base = _SkillPath('/root/.codex/skills/remote-skills')
    for file in base.glob('skill-*/SKILL.md'):
        head = file.read_text(encoding='utf-8', errors='replace').splitlines()[:6]
        if any(line.strip() == f'name: {name}' for line in head):
            return file.parent
    raise FileNotFoundError(f'Personal skill not installed: {name}')
"""Banner-side wrapper. Same rebuild as /images."""
from __future__ import annotations

import runpy
from pathlib import Path

runpy.run_path(
    str((_resolve_skill("images") / "scripts/rebuild_document.py")),
    run_name="__main__",
)
