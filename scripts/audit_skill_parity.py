#!/usr/bin/env python3
"""Read-only repository-wide skill/engine consistency and QA evidence audit."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

REQUIRED = ("references/quality-profile.md", "evals/quality-cases.json")
STATUS = {"PASS", "FAIL", "BLOCKED", "NOT TESTED", "NOT APPLICABLE"}
ALIAS_ENGINES = {"disabled": "disability", "proceed": "disability"}
VISUAL_TERMS = ("visual", "image", "banner", "document", "pdf", "slide", "parallax", "4629", "textbook")

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def audit(root: Path) -> dict:
    results = []
    for skill in sorted((root / "skills").glob("*/SKILL.md")):
        name = skill.parent.name
        engine = root / "engines" / name / "ENGINE.md"
        checks, findings = {}, []
        text = skill.read_text(encoding="utf-8")
        checks["skill_present"] = "PASS"
        for relative in REQUIRED:
            p = skill.parent / relative
            checks[relative] = "PASS" if p.is_file() else "FAIL"
            if not p.is_file():
                findings.append(f"Missing required resource: {relative}")
        if name in ALIAS_ENGINES and engine.exists():
            etext = engine.read_text(encoding="utf-8")
            target = ALIAS_ENGINES[name]
            target_path = root / "engines" / target / "ENGINE.md"
            checks["engine_parity"] = "PASS" if target_path.is_file() and f"engines/{target}/ENGINE.md" in etext else "FAIL"
            if checks["engine_parity"] == "FAIL":
                findings.append("Alias engine missing or invalid target: " + target)
            missing, differing = [], []
        elif engine.exists():
            etext = engine.read_text(encoding="utf-8")
            # Engine copies may include an extra compatibility footer; compare all
            # normative canonical sections by heading and content, not just file hashes.
            def sections(value):
                matches = list(re.finditer(r"(?m)^## (.+)$", value))
                return {m.group(1).strip(): value[m.end():matches[i+1].start() if i+1<len(matches) else len(value)].strip()
                        for i,m in enumerate(matches)}
            canonical, legacy = sections(text), sections(etext)
            duplicate_canonical = len(re.findall(r"(?m)^## (.+)$", text)) != len(canonical)
            duplicate_legacy = len(re.findall(r"(?m)^## (.+)$", etext)) != len(legacy)
            missing = sorted(set(canonical) - set(legacy))
            differing = sorted(k for k in canonical.keys() & legacy.keys() if canonical[k] != legacy[k])
            checks["engine_parity"] = "FAIL" if missing or differing or duplicate_canonical or duplicate_legacy else "PASS"
            if duplicate_canonical or duplicate_legacy:
                findings.append("Duplicate level-two section headings in canonical skill or engine")
            if missing:
                findings.append("Engine missing canonical sections: " + ", ".join(missing))
            if differing:
                findings.append("Engine differs in canonical sections: " + ", ".join(differing))
        else:
            checks["engine_parity"] = "NOT APPLICABLE"
            missing, differing = [], []
        evaluation = skill.parent / "evals" / "quality-cases.json"
        if evaluation.is_file():
            try:
                data = json.loads(evaluation.read_text(encoding="utf-8"))
                cases = data.get("cases", [])
                declared = data.get("execution_status", "NOT TESTED")
                if declared not in STATUS:
                    findings.append("Unrecognized execution_status")
                    checks["evaluation_schema"] = "FAIL"
                elif data.get("skill") != name or not isinstance(cases, list) or not cases:
                    findings.append("Invalid or empty evaluation cases")
                    checks["evaluation_schema"] = "FAIL"
                else:
                    ids = [case.get("id") if isinstance(case, dict) else None for case in cases]
                    valid_ids = all(isinstance(x, str) and x.strip() for x in ids)
                    checks["evaluation_schema"] = "FAIL" if not valid_ids or len(ids) != len(set(ids)) else "PASS"
                    if checks["evaluation_schema"] == "FAIL":
                        findings.append("Missing or duplicate evaluation case IDs")
                checks["evaluation_execution"] = declared if declared in STATUS else "BLOCKED"
            except (ValueError, UnicodeError, AttributeError) as exc:
                checks["evaluation_schema"] = "FAIL"
                checks["evaluation_execution"] = "BLOCKED"
                findings.append("Evaluation parse failure: " + str(exc))
        else:
            checks["evaluation_schema"] = "FAIL"
            checks["evaluation_execution"] = "BLOCKED"
        checks["rendered_visual_qa"] = "NOT TESTED" if any(x in name.lower() for x in VISUAL_TERMS) else "NOT APPLICABLE"
        results.append({"skill": name, "canonical_path": str(skill.relative_to(root)),
                        "canonical_sha256": digest(skill),
                        "engine_path": str(engine.relative_to(root)) if engine.exists() else None,
                        "engine_sha256": digest(engine) if engine.exists() else None,
                        "checks": checks, "missing_sections": missing,
                        "differing_sections": differing, "findings": findings})
    failed = [r for r in results if "FAIL" in r["checks"].values()]
    return {"schema_version": 1, "scope": "all skills/*/SKILL.md",
            "skill_count": len(results), "structural_failures": len(failed),
            "status": "FAIL" if failed or not results else "PASS",
            "limitations": ["Static checks only; not a live loader, security or rendered-artifact test.",
                            "An untested evaluation or visual check never becomes PASS from this audit.",
                            "Missing optional legacy engines are NOT APPLICABLE, not failures.",
                            "Section-level parity is conservative and may flag intentional wording differences."],
            "skills": results}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out", type=Path, default=Path("skill-parity-report.json"))
    args = parser.parse_args()
    report = audit(args.root.resolve())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k!="skills"}, indent=2))
    raise SystemExit(1 if report["status"] == "FAIL" else 0)

if __name__ == "__main__":
    main()
