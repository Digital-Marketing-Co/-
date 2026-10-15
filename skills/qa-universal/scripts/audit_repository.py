#!/usr/bin/env python3
"""Read-only repository QA inventory. JSON output is evidence, not a clean bill of health."""
import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

ABSOLUTE = re.compile(r"/root/\.grok/|/workspace/artifacts/|@(?:banner|images|atlas|latex|itqe)(?:/|\b)")
DANGER = re.compile(r"(?i)(?:curl|wget)\s+[^\n|]*\|\s*(?:sh|bash)|rm\s+-rf\s+/|(?:eval|exec)\s*\(\s*(?:base64|decode)")
CONTROL = re.compile("[\\u202a-\\u202e\\u2066-\\u2069\\u200b\\ufeff]")
REF = re.compile(r"(?:scripts|references|assets)/[\w./-]+\.(?:py|md|json|sh|csv|tex)")
COMMAND = re.compile(r"(?<!\w)/(banner|images|atlas|itqe|latex|copyright)\b", re.I)

def audit(root):
    root = Path(root).resolve()
    files = [p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    findings = []
    manifest = []
    for p in files:
        rel = str(p.relative_to(root))
        try:
            raw = p.read_bytes()
        except OSError as e:
            findings.append({"severity": "error", "file": rel, "issue": "unreadable", "detail": str(e)})
            continue
        manifest.append({"path": rel, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
        if p.suffix.lower() not in {".md", ".py", ".sh", ".json", ".yaml", ".yml", ".txt", ".toml"}:
            continue
        try:
            txt = raw.decode("utf-8")
        except UnicodeDecodeError:
            findings.append({"severity": "review", "file": rel, "issue": "non_utf8_text"})
            continue
        for name, pat in (("nonportable_path", ABSOLUTE), ("potentially_unsafe_code", DANGER), ("invisible_unicode", CONTROL)):
            for match in list(pat.finditer(txt))[:20]:
                findings.append({"severity": "review", "file": rel, "line": txt.count("\n", 0, match.start()) + 1, "issue": name, "excerpt": match.group(0)[:120]})
        if p.name == "SKILL.md":
            for ref in sorted(set(REF.findall(txt))):
                # Only local relative references; cross-skill references need resolver and are separately flagged.
                if (p.parent / ref).exists() or (root / "skills" / ref).exists():
                    continue
                findings.append({"severity": "review", "file": rel, "issue": "unresolved_relative_reference", "reference": ref})
    return {"schema_version": 1, "inventory": {"files": len(files), "skill_definitions": len(skills), "manifest": manifest},
            "findings": findings, "finding_count": len(findings),
            "verification": "Static checks only; no document renders, image generations, or dynamic tests performed."}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", nargs="?", default=".")
    ap.add_argument("--output")
    args = ap.parse_args()
    result = audit(args.repo)
    data = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).write_text(data + "\n", encoding="utf-8")
    else:
        print(data)
