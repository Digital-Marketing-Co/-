#!/usr/bin/env python3
"""Print the first existing skill directory for a name."""
import sys
from pathlib import Path

name = sys.argv[1] if len(sys.argv) > 1 else ""
candidates = [
    Path(f"/root/.grok/server-skills/{name}"),
    Path(f"/home/workdir/.grok/skills/{name}"),
    Path(f"/workspace/skills/{name}"),
    Path(f"/opt/skills/{name}"),
]
for path in candidates:
    if path.is_dir():
        print(path)
        raise SystemExit(0)
print(f"missing skill directory: {name}", file=sys.stderr)
raise SystemExit(1)
