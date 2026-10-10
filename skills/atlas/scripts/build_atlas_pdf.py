#!/usr/bin/env python3
"""Adapt atlas JSON, then invoke the adjacent reviewed deep PDF renderer."""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys

from atlas_to_deep import convert


def resolve_deep() -> Path:
    skills = Path(__file__).resolve().parents[2]
    direct = skills / 'deep' / 'scripts/build_deep_pdf.py'
    if direct.is_file():
        return direct
    resolver = skills / 'interop/scripts/resolve_root.py'
    if not resolver.is_file():
        raise FileNotFoundError('Deep renderer and shared skill resolver are unavailable')
    spec = importlib.util.spec_from_file_location('atlas_skill_resolver', resolver)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    root = module.resolve('deep')
    script = root / 'scripts/build_deep_pdf.py'
    if not script.is_file():
        raise FileNotFoundError(script)
    return script


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('atlas_json', type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    source = args.atlas_json.expanduser().resolve()
    output = args.out.expanduser().resolve()
    if output.suffix.lower() != '.pdf':
        raise ValueError('--out must name a PDF file')
    if output == source or output == source.with_name('deep.json'):
        raise ValueError('PDF output must differ from source and adapter JSON')
    renderer = resolve_deep()
    adapted = convert(source)
    subprocess.run([sys.executable, str(renderer), str(adapted), '--out', str(output)], check=True)
    print(output)


if __name__ == '__main__':
    main()
