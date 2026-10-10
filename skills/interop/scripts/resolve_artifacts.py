#!/usr/bin/env python3
"""Resolve a writable staging directory, creating it when needed."""
import argparse
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--path', type=Path)
    args = parser.parse_args()
    path = args.path or Path(os.environ.get('SKILL_ARTIFACTS_DIR', str(Path.cwd() / 'artifacts')))
    path = path.expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    if not path.is_dir() or not os.access(path, os.W_OK):
        raise SystemExit('Artifact staging directory is not writable')
    print(path)


if __name__ == '__main__':
    main()
