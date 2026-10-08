#!/usr/bin/env python3
"""Print the first existing artifacts directory."""
from pathlib import Path

candidates = [
    Path("/workspace/artifacts"),
    Path("/home/workdir/artifacts"),
    Path("/tmp/artifacts"),
]
for path in candidates:
    if path.is_dir():
        print(path)
        raise SystemExit(0)
print("missing artifacts directory", file=__import__("sys").stderr)
raise SystemExit(1)
