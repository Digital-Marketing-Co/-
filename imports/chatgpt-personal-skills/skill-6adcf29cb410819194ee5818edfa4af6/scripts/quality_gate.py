#!/usr/bin/env python3
"""Validate declared release evidence; does not inspect pixels or run functional tests."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

BASELINES = {
    'document': {'requirements', 'content', 'sources', 'links', 'accessibility', 'visual'},
    'app': {'requirements', 'functional', 'persistence', 'security', 'accessibility', 'visual', 'build'},
    'dataset': {'requirements', 'schema', 'counts', 'exports', 'accessibility', 'visual'},
    'text': {'requirements', 'content', 'readability', 'visual'},
    'image': {'requirements', 'integrity', 'visual'},
    'media': {'requirements', 'integrity', 'visual'},
}
STATES = {'PASS', 'FAIL', 'BLOCKED', 'NOT TESTED', 'NOT APPLICABLE'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(data, base):
    errors = []
    def require(condition, message):
        if not condition:
            errors.append(message)
    def nonempty(v):
        return isinstance(v, str) and bool(v.strip())
    def file_record(item, label):
        if not isinstance(item, dict):
            errors.append(label + ': expected file record')
            return None
        if not nonempty(item.get('path')):
            errors.append(label + ': missing path')
            return None
        p = Path(item['path'])
        if not p.is_absolute():
            p = base / p
        if not p.is_file():
            errors.append(label + ': missing file')
            return None
        require(nonempty(item.get('sha256')) and digest(p) == item.get('sha256'), label + ': stale or missing SHA-256')
        return p
    if not isinstance(data, dict):
        return ['manifest must be an object']
    require(data.get('schema_version') == 1, 'unsupported schema_version')
    require(nonempty(data.get('run_id')), 'missing run_id')
    require(nonempty(data.get('revision')), 'missing revision')
    kind = data.get('output_kind')
    require(kind in BASELINES, 'unknown output_kind')
    artifact = file_record(data.get('artifact'), 'artifact')
    artifact_hash = data.get('artifact', {}).get('sha256') if isinstance(data.get('artifact'), dict) else None
    required = data.get('required_checks')
    require(isinstance(required, list) and all(nonempty(x) for x in required), 'required_checks must be a string list')
    required = required if isinstance(required, list) and all(isinstance(x, str) for x in required) else []
    require(len(set(required)) == len(required), 'duplicate required check IDs')
    require(BASELINES.get(kind, set()).issubset(required), 'missing baseline required checks')
    units = data.get('expected_visual_units')
    require(isinstance(units, list) and all(nonempty(x) for x in units), 'expected_visual_units must be a string list')
    units = units if isinstance(units, list) and all(isinstance(x, str) for x in units) else []
    require(len(set(units)) == len(units), 'duplicate expected visual units')
    checks = data.get('checks')
    require(isinstance(checks, list), 'checks must be an array')
    checks = checks if isinstance(checks, list) else []
    by_id = {}
    for check in checks:
        if not isinstance(check, dict):
            errors.append('invalid check record')
            continue
        ident = check.get('id')
        require(nonempty(ident), 'check missing id')
        if not isinstance(ident, str):
            continue
        require(ident not in by_id, 'duplicate check: ' + ident)
        by_id[ident] = check
        status = check.get('status')
        require(status in STATES, ident + ': invalid status')
        require(check.get('revision') == data.get('revision'), ident + ': stale revision')
        require(nonempty(artifact_hash) and check.get('artifact_sha256') == artifact_hash, ident + ': evidence bound to different artifact')
        require(nonempty(check.get('note')), ident + ': missing actual observation/reason')
        if status == 'PASS':
            evidence = check.get('evidence')
            require(isinstance(evidence, list) and bool(evidence), ident + ': PASS lacks evidence')
            for i, item in enumerate(evidence if isinstance(evidence, list) else []):
                file_record(item, f'{ident} evidence {i}')
        if ident in required:
            require(status in {'PASS', 'NOT APPLICABLE'}, ident + ': release blocked by ' + str(status))
    for ident in required:
        require(ident in by_id, 'missing required result: ' + ident)
    visual = by_id.get('visual', {})
    visual_na = visual.get('status') == 'NOT APPLICABLE'
    require(not visual_na or kind == 'dataset' and data.get('machine_readable_only') is True,
            'visual N/A only allowed for a machine-readable-only dataset')
    if not visual_na:
        require(bool(units), 'missing expected visual unit inventory')
    if kind == 'document' and artifact and artifact.suffix.lower() == '.pdf':
        try:
            info = subprocess.run(['pdfinfo', str(artifact)], capture_output=True, text=True, timeout=30)
            count = re.search(r'^Pages:\s*(\d+)', info.stdout, re.M)
            require(info.returncode == 0 and count is not None, 'could not independently count final PDF pages')
            if count:
                require(set(units) == {f'page:{i}' for i in range(1, int(count[1]) + 1)}, 'visual inventory must cover every final PDF page')
        except (OSError, subprocess.TimeoutExpired):
            errors.append('PDF page count blocked: pdfinfo unavailable or timed out')
    inspected = data.get('visual_units', [])
    require(isinstance(inspected, list), 'visual_units must be an array')
    seen = set()
    for unit in inspected if isinstance(inspected, list) else []:
        if not isinstance(unit, dict):
            errors.append('invalid visual unit')
            continue
        ident = unit.get('id')
        if not isinstance(ident, str):
            errors.append('visual unit lacks id')
            continue
        require(ident not in seen, 'duplicate visual result: ' + ident)
        seen.add(ident)
        require(ident in units, 'visual result outside scope: ' + ident)
        require(unit.get('revision') == data.get('revision'), ident + ': stale visual revision')
        require(nonempty(artifact_hash) and unit.get('artifact_sha256') == artifact_hash, ident + ': visual evidence bound to different artifact')
        require(unit.get('status') == 'PASS', ident + ': visual inspection incomplete')
        require(nonempty(unit.get('observation')), ident + ': missing visual observation')
        require(nonempty(unit.get('reviewer')), ident + ': missing reviewer')
        proof = file_record(unit.get('evidence'), ident + ' visual evidence')
        if kind in {'document', 'app', 'image', 'media'} and proof:
            require(proof.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg'}, ident + ': rendered visual evidence required')
    if not visual_na:
        require(seen == set(units), 'visual results do not cover the declared scope')
    defects = data.get('unresolved_defects')
    require(isinstance(defects, list), 'unresolved_defects must be an array')
    require(defects == [], 'unresolved defects prevent a finished release')
    return errors


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('manifest', type=Path)
    args = p.parse_args()
    try:
        data = json.loads(args.manifest.read_text())
        errors = validate(data, args.manifest.resolve().parent)
    except (OSError, ValueError, TypeError) as exc:
        errors = [str(exc)]
    print(json.dumps({'evidence_gate': 'BLOCKED' if errors else 'PASS', 'errors': errors,
                      'limitation': 'Validates recorded evidence; does not judge pixels, truthfulness or functional correctness.'}, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
