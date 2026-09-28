#!/usr/bin/env python3
"""Insert the locked render-gate section into every project SKILL.md once."""
from __future__ import annotations

from pathlib import Path

ROOT = Path("/home/workdir/.grok/skills")
MARKER = "## Render gate (mandatory with /itqe and /latex)"
BLOCK = """
## Render gate (mandatory with /itqe and /latex)

Before delivering any PDF, DOCX, PPTX, XLSX, HTML view, printed page, or builder JSON that may contain notation, short codes, or equations, run the house render gate. Chat may use KaTeX. Files must show compiled glyphs or a compiled plate. Raw LaTeX, AMS-TeX, KaTeX source, MathJax source, uncompiled backslash commands, tofu, or empty boxes are defects.

```bash
python3 /home/workdir/.grok/skills/itqe/scripts/scan_render_gate.py \\
  /home/workdir/artifacts/<slug> \\
  --also-pdf /home/workdir/artifacts/<file>.pdf
python3 /home/workdir/.grok/skills/latex/scripts/scan_raw_tex.py \\
  /home/workdir/artifacts/<slug> \\
  --also-pdf /home/workdir/artifacts/<file>.pdf --pages
```

Exit code 1 blocks delivery. Repair with `/latex` plates, attach an ITQE table under every display equation (Identifier, Term, Quantity, Explanation), rebuild, scan again, and raster every page. See `/home/workdir/.grok/skills/itqe/references/render-gate.md` and `/home/workdir/.grok/skills/latex/SKILL.md`.
"""

ANCHORS = (
    "## House copyright footer",
    "<!--\nWCA_COPYRIGHT_PROMPT_APPENDIX",
    "<!--WCA_COPYRIGHT_PROMPT_APPENDIX",
)


def patch(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return "skip"
    insert_at = None
    for anc in ANCHORS:
        i = text.find(anc)
        if i != -1:
            insert_at = i
            break
    blob = "\n" + BLOCK.strip() + "\n\n"
    if insert_at is None:
        text = text.rstrip() + "\n" + blob
    else:
        text = text[:insert_at] + blob + text[insert_at:]
    path.write_text(text, encoding="utf-8")
    return "patched"


def main() -> None:
    for skill_md in sorted(ROOT.glob("*/SKILL.md")):
        status = patch(skill_md)
        print(f"{status}\t{skill_md.parent.name}")


if __name__ == "__main__":
    main()
