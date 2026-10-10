#!/usr/bin/env python3
"""Audit every canonical skill without executing untrusted skill scripts."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
import yaml


def audit(root: Path) -> dict:
    errors, warnings, entries = [], [], []
    skills = root / 'skills'
    files = sorted(skills.glob('*/SKILL.md'))
    if not files:
        errors.append('No canonical skills found')
    names = set()
    for path in files:
        relative = str(path.relative_to(root))
        text = path.read_text(encoding='utf-8')
        try:
            if not text.startswith('---\n') or len(text.split('---', 2)) != 3:
                raise ValueError('Missing frontmatter delimiters')
            data = yaml.safe_load(text.split('---', 2)[1])
            if not isinstance(data, dict):
                raise ValueError('Frontmatter must be a mapping')
            name, description = data.get('name'), data.get('description')
            if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name)>64:
                raise ValueError('Invalid canonical name')
            if name != path.parent.name or name in names:
                raise ValueError('Name differs from directory or repeats an identity')
            names.add(name)
            if not isinstance(description, str) or not 1 <= len(description) <= 1024:
                raise ValueError('Description must be 1–1024 characters')
            if len(text.splitlines()) > 500:
                warnings.append(f'{relative}: move optional details into references')
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
                if '://' in target or target.startswith('#'):
                    continue
                target = target.split('#')[0]
                if target and not (path.parent / target).is_file():
                    errors.append(f'{relative}: missing linked resource {target}')
            for resource in ('references/quality-profile.md', 'evals/quality-cases.json'):
                if not (path.parent / resource).is_file():
                    errors.append(f'{relative}: missing {resource}')
            entries.append({'skill':name,'files':sum(p.is_file() for p in path.parent.rglob('*') if '__pycache__' not in p.parts),
                            'skill_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        except (ValueError, yaml.YAMLError) as exc:
            errors.append(f'{relative}: {exc}')
    scripts = sorted(skills.rglob('*.py'))
    for path in scripts:
        try:
            compile(path.read_text(encoding='utf-8'), str(path), 'exec')
        except (SyntaxError, UnicodeError) as exc:
            errors.append(f'{path.relative_to(root)}: {exc}')
    json_count = 0
    for path in skills.rglob('*.json'):
        json_count += 1
        try:
            data = json.loads(path.read_text(encoding='utf-8'), parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
            if path.name == 'quality-cases.json':
                if data.get('skill') != path.parent.parent.name or not data.get('cases'):
                    raise ValueError('Invalid per-skill case identity or empty cases')
                for case in data['cases']:
                    if not case.get('prompt') or not case.get('assertions') or not case.get('grader'):
                        raise ValueError('Case lacks prompt, assertions, or evidence grader')
        except (ValueError, UnicodeError) as exc:
            errors.append(f'{path.relative_to(root)}: {exc}')
    return {'status':'FAIL' if errors else 'PASS','skill_count':len(files),'python_files_compiled':len(scripts),
            'json_files_parsed':json_count,'errors':errors,'warnings':warnings,'skills':entries,
            'limitations':['Structural validation does not prove live integrations, rendered quality, or all scenario behavior.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    report = audit(args.root.resolve())
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='skills'},indent=2))
    raise SystemExit(0 if report['status']=='PASS' else 1)


if __name__ == '__main__':
    main()
