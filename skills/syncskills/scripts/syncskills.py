#!/usr/bin/env python3
"""Deterministic, read-only-by-default SyncSkills inventory, manifest, and diff CLI."""
import argparse
import hashlib
import json
import os
import pathlib
import re
import sys
from datetime import datetime, timezone

VERSION = "1.0.0"
SKILL_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
SKIP = {".git", "__pycache__", ".pytest_cache", "node_modules", ".DS_Store"}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

def inventory(root):
    root = pathlib.Path(root).resolve()
    base = root / "skills"
    if not base.is_dir() or base.is_symlink():
        raise ValueError("skills/ directory missing or unsafe")
    skills = []
    for directory in sorted(base.iterdir()):
        if not directory.is_dir() or directory.is_symlink() or not SKILL_NAME.fullmatch(directory.name):
            continue
        if not (directory / "SKILL.md").is_file():
            continue
        entries = []
        for parent, dirs, files in os.walk(directory, followlinks=False):
            dirs[:] = sorted(d for d in dirs if d not in SKIP and not (pathlib.Path(parent) / d).is_symlink())
            for name in sorted(files):
                path = pathlib.Path(parent) / name
                if name in SKIP or path.is_symlink() or not path.is_file():
                    continue
                relative = path.relative_to(root).as_posix()
                entries.append({"path": relative, "sha256": digest(path.read_bytes())})
        skills.append({"name": directory.name, "files": entries,
                       "sha256": digest(canonical(entries))})
    return {"schema_version": "1.0.0", "skills": skills}

def validate(manifest):
    if manifest.get("schema_version") != "1.0.0" or not isinstance(manifest.get("skills"), list):
        raise ValueError("invalid manifest schema")
    names, paths = set(), set()
    for skill in manifest["skills"]:
        name = skill.get("name")
        if not isinstance(name, str) or not SKILL_NAME.fullmatch(name) or name in names:
            raise ValueError("invalid or duplicate skill")
        names.add(name)
        if not isinstance(skill.get("sha256"), str) or not re.fullmatch("[0-9a-f]{64}", skill["sha256"]):
            raise ValueError("invalid skill digest")
        files = skill.get("files")
        if not isinstance(files, list) or not files:
            raise ValueError("missing files")
        for entry in files:
            p, h = entry.get("path"), entry.get("sha256")
            if not isinstance(p, str) or not p.startswith("skills/" + name + "/") or ".." in pathlib.PurePosixPath(p).parts:
                raise ValueError("unsafe file path")
            if p in paths or not isinstance(h, str) or not re.fullmatch("[0-9a-f]{64}", h):
                raise ValueError("duplicate path or invalid digest")
            paths.add(p)
        if digest(canonical(files)) != skill["sha256"]:
            raise ValueError("skill digest mismatch")
    return True

def compare(base, canonical_release, consumer):
    """Three-way comparison. No implicit writes or unsafe auto-merges."""
    for obj in (base, canonical_release, consumer):
        validate(obj)
    def flatten(m):
        return {f["path"]: f["sha256"] for s in m["skills"] for f in s["files"]}
    b, c, u = map(flatten, (base, canonical_release, consumer))
    result = []
    for path in sorted(set(b) | set(c) | set(u)):
        old, target, actual = b.get(path), c.get(path), u.get(path)
        if target == actual:
            state = "IDENTICAL"
        elif actual == old and target != old:
            state = "OUTDATED"
        elif target == old and actual != old:
            state = "LOCAL_CUSTOMIZATION"
        elif old is None and target is None:
            state = "COMPATIBLE_EXTENSION"
        elif old is None and actual is None:
            state = "OUTDATED"
        else:
            state = "VERSION_CONFLICT"
        result.append({"path": path, "state": state, "baseline": old,
                       "canonical": target, "consumer": actual})
    return result

def main(argv=None):
    parser = argparse.ArgumentParser(description="SyncSkills safe manifest CLI")
    parser.add_argument("command", choices=["status", "scan", "diff", "plan", "verify", "doctor", "export", "audit", "sync", "rollback", "quarantine", "exhaustive"])
    parser.add_argument("--root", default=".")
    parser.add_argument("--baseline")
    parser.add_argument("--release")
    parser.add_argument("--consumer")
    parser.add_argument("--output")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command in ("diff", "plan") and all((args.baseline, args.release, args.consumer)):
            inputs = [json.loads(pathlib.Path(p).read_text(encoding="utf-8")) for p in (args.baseline, args.release, args.consumer)]
            data = {"command": args.command, "changes": compare(*inputs)}
        elif args.command in ("status", "scan", "verify", "doctor", "export", "exhaustive"):
            data = {"command": args.command, "inventory": inventory(args.root)}
            validate(data["inventory"])
            if args.command == "exhaustive":
                data["coverage"] = "LOCAL_ONLY_EXTERNAL_INTEGRATIONS_UNTESTED"
        else:
            data = {"command": args.command, "status": "BLOCKED",
                    "reason": "Requires authorized adapter, signed release, and external verification; no writes performed"}
        data["engine_version"] = VERSION
        data["mode"] = "READ_ONLY"
        output = json.dumps(data, indent=2, sort_keys=True) + "\n"
        if args.output:
            pathlib.Path(args.output).write_text(output, encoding="utf-8")
        else:
            sys.stdout.write(output)
        return 0 if data.get("status") != "BLOCKED" else 2
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}), file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
