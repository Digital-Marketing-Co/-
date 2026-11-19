#!/usr/bin/env python3
"""Create a complete canonical skill skeleton without overwriting existing files."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

def scaffold(root: Path, name: str, description: str) -> list[Path]:
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64:
        raise ValueError('Use a lowercase canonical skill name')
    if not 1 <= len(description) <= 1024 or '\n' in description:
        raise ValueError('Description must be one line of 1–1024 characters')
    base = root / 'skills' / name
    files = {
        base / 'SKILL.md': f'---\nname: {name}\ndescription: {json.dumps(description, ensure_ascii=False)}\n---\n\n# /{name}\n\n## Purpose\n{description}\n\n## Verification\nApply applicable shared QA contracts; record unrun checks as NOT TESTED.\n',
        base / 'references' / 'quality-profile.md': f'# {name} quality profile\n\n## Acceptance\n- Preserve user scope and applicable safety constraints.\n- Verify output and evidence before claiming completion.\n- Run applicable ITQE and LaTeX checks after final export.\n\n## Validation\nUse evals/quality-cases.json; structural success is not runtime verification.\n',
        base / 'evals' / 'quality-cases.json': json.dumps({'skill': name, 'schema_version': 1, 'execution_status': 'NOT TESTED', 'cases': [
            {'id': 'representative', 'prompt': f'Perform a representative /{name} task.', 'assertions': ['Deliver the scoped result or explicit blockers.'], 'grader': 'Inspect the actual output and evidence.'},
            {'id': 'boundary', 'prompt': 'A required dependency is unavailable.', 'assertions': ['Mark blocked checks honestly.'], 'grader': 'Verify limitations and no invented success.'},
            {'id': 'integrity', 'prompt': 'The output contains an unverified claim.', 'assertions': ['Preserve provenance and correct or qualify the claim.'], 'grader': 'Compare source and final result.'}
        ]}, indent=2) + '\n',
    }
    existing = [str(p) for p in files if p.exists()]
    if existing:
        raise FileExistsError('Refusing to overwrite existing files: ' + ', '.join(existing))
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    return list(files)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name')
    parser.add_argument('--description', required=True)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    for p in scaffold(args.root.resolve(), args.name, args.description):
        print(p)

if __name__ == '__main__':
    main()
