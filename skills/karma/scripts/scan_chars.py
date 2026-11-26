#!/usr/bin/env python3
"""
scan_chars.py — Character integrity scanner for /karma gate.
Fail closed on mojibake, replacement characters, or anomalous glyphs.
Usage: python3 scan_chars.py <file_or_dir>
"""
import sys
import os
import re
from pathlib import Path

REPLACEMENT = '\ufffd'
ANOMALOUS = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')
MOJIBAKE_HINTS = re.compile(r'(Ã.|Â.|â.|ð.|ï¿½|ï»¿)')

def scan_file(path: Path) -> list:
    findings = []
    try:
        text = path.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        findings.append(f"READ_ERROR {path}: {e}")
        return findings
    if REPLACEMENT in text:
        findings.append(f"REPLACEMENT_CHAR {path}")
    if ANOMALOUS.search(text):
        findings.append(f"ANOMALOUS_CTRL {path}")
    if MOJIBAKE_HINTS.search(text):
        findings.append(f"MOJIBAKE_HINT {path}")
    return findings

def main():
    if len(sys.argv) < 2:
        print("Usage: scan_chars.py <path>")
        sys.exit(2)
    target = Path(sys.argv[1])
    all_findings = []
    if target.is_file():
        all_findings.extend(scan_file(target))
    elif target.is_dir():
        for p in target.rglob('*'):
            if p.is_file() and p.suffix.lower() in {'.md', '.txt', '.py', '.html', '.json', '.pdf'}:
                all_findings.extend(scan_file(p))
    else:
        print(f"Path not found: {target}")
        sys.exit(2)
    if all_findings:
        print("FAIL")
        for f in all_findings:
            print(f)
        sys.exit(1)
    else:
        print("PASS")
        sys.exit(0)

if __name__ == "__main__":
    main()
