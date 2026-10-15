#!/usr/bin/env python3
"""Safe, deterministic slash-skill planning; never executes skill content."""
import argparse
import json
import re
from pathlib import Path

TOKEN = re.compile(r"(?<![\w/@])/(?!/)([A-Za-z][A-Za-z0-9_-]*)(?![\w/-])")
URL = re.compile(r"https?://\S+")
INLINE = re.compile(r"`[^`\n]*`")
FENCE = re.compile(r"```[\s\S]*?```")
ALIASES = {"banners": "banner", "image": "images", "wca": "wca-ivy-biblio", "qa": "qa-universal"}
DEPENDENCIES = {"images": ["banner"], "atlas": ["banner"], "itqe": ["latex"], "qa-universal": []}
STAGES = ["atlas", "banner", "images", "latex", "itqe", "copyright", "compression", "qa-universal"]

def strip_inert(text):
    text = FENCE.sub(lambda m: " " * len(m.group()), text)
    text = INLINE.sub(lambda m: " " * len(m.group()), text)
    text = URL.sub(lambda m: " " * len(m.group()), text)
    return "\n".join(" " * len(line) if line.lstrip().startswith(">") else line for line in text.split("\n"))

def plan(text, available=None):
    found = [ALIASES.get(m.group(1).lower(), m.group(1).lower()) for m in TOKEN.finditer(strip_inert(text))]
    selected = list(dict.fromkeys(found))
    if available is not None:
        unknown = [x for x in selected if x not in available]
        selected = [x for x in selected if x in available]
    else:
        unknown = []
    edges = {}
    def add(name, stack=()):
        if name in stack:
            raise ValueError("cycle: " + " -> ".join((*stack, name)))
        if name in edges:
            return
        deps = [x for x in DEPENDENCIES.get(name, []) if available is None or x in available]
        for dep in deps:
            add(dep, (*stack, name))
        edges[name] = deps
    for name in selected:
        add(name)
    # Topological ordering with fixed tie-break, not prompt position.
    ordered = []
    pending = set(edges)
    while pending:
        ready = [x for x in pending if all(y in ordered for y in edges[x])]
        if not ready:
            raise ValueError("unresolved dependency cycle")
        ready.sort(key=lambda x: (STAGES.index(x) if x in STAGES else len(STAGES), x))
        chosen = ready[0]
        ordered.append(chosen)
        pending.remove(chosen)
    return {"requested": selected, "execution_order": ordered, "unknown": unknown,
            "dependencies": edges, "banner_owner": "banner" if "banner" in edges else None,
            "supplementary_figures_owner": "images" if "images" in edges else None}

def available_skills(root):
    return {p.parent.name.lower() for p in (Path(root) / "skills").glob("*/SKILL.md")}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("--repo-root", type=Path)
    args = ap.parse_args()
    available = available_skills(args.repo_root) if args.repo_root else None
    print(json.dumps(plan(args.prompt, available), indent=2))

if __name__ == "__main__":
    main()
