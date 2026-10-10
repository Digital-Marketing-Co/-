#!/usr/bin/env python3
"""Replace a legacy duplicated footer section with a canonical reference."""
import argparse
import re
from pathlib import Path

REFERENCE='## Canonical footer\n\nRead `copyright/SKILL.md` and render its canonical notice helper once per page. Do not maintain independent legal text or year calculations.\n\n'


def strip_old_footer(text):
    # Replace only the old section, preserving all sections after it.
    return re.sub(r'(?ms)^## House copyright footer\n.*?(?=^## |\Z)',REFERENCE,text)


def apply(path):
    original=path.read_text(encoding='utf-8')
    rebuilt=strip_old_footer(original)
    if rebuilt==original:return 'unchanged'
    temp=path.with_name(path.name+'.footer-tmp')
    temp.write_text(rebuilt,encoding='utf-8');temp.replace(path)
    return 'updated'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files',nargs='+',type=Path)
    parser.add_argument('--apply',action='store_true',help='Write changes; default is a preview')
    args=parser.parse_args()
    for path in args.files:
        if not path.is_file():raise SystemExit(f'Missing file: {path}')
        if args.apply:status=apply(path)
        else:status='would update' if strip_old_footer(path.read_text())!=path.read_text() else 'unchanged'
        print(f'{status}\t{path}')
    return 0


if __name__=='__main__':raise SystemExit(main())
