#!/usr/bin/env python3
"""Resolve a skill by frontmatter identity, preferring the current checkout."""
from __future__ import annotations
import argparse
import os
import re
import sys
from pathlib import Path


def skill_name(directory: Path) -> str | None:
    path = directory / 'SKILL.md'
    if not path.is_file():
        return None
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        return None
    frontmatter = text.split('---', 2)[1]
    match = re.search(r'^name:\s*[\"\']?([a-z0-9-]+)[\"\']?\s*$', frontmatter, re.M)
    return match.group(1) if match else None


def resolve(name: str, roots: list[Path] | None = None) -> Path:
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        raise ValueError('Require a canonical lowercase skill name')
    if roots is None:
        roots = [Path(__file__).resolve().parents[2]]
        if os.environ.get('SKILL_ROOT'):
            roots.append(Path(os.environ['SKILL_ROOT']).expanduser())
        for ancestor in [Path.cwd(), *Path.cwd().parents]:
            if (ancestor / 'skills').is_dir():
                roots.append(ancestor / 'skills')
                break
        if os.environ.get('CODEX_HOME'):
            roots.append(Path(os.environ['CODEX_HOME']) / 'skills')
        roots += [Path('/root/.codex/skills/remote-skills'), Path.home() / '.codex/skills',
                  Path('/root/.grok/server-skills'), Path('/home/workdir/.grok/skills')]
    seen = set()
    for root in roots:
        root = root.resolve()
        if root in seen or not root.is_dir():
            continue
        seen.add(root)
        direct = root / name
        if skill_name(direct) == name:
            return direct
        matches = [p for p in root.iterdir() if p.is_dir() and skill_name(p) == name]
        if len(matches) > 1:
            raise ValueError(f'Ambiguous installed skill identity: {name}')
        if matches:
            return matches[0]
    raise FileNotFoundError(f'Missing skill: {name}')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name')
    parser.add_argument('--root', action='append', type=Path)
    args = parser.parse_args()
    try:
        print(resolve(args.name, args.root))
        return 0
    except (ValueError, FileNotFoundError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
