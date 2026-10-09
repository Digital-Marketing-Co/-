#!/usr/bin/env python3
"""QA checklist for a /pepe widget folder. Exit 0 on PASS, 1 on any fail."""

import re
import sys
from pathlib import Path

LIMITS = {"pepe-promptform.js": 40_000, "pepe-promptform.css": 24_000}


def main() -> int:
    folder = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    js = folder / "pepe-promptform.js"
    css = folder / "pepe-promptform.css"
    html = folder / "index.html"
    fails = []

    if not js.is_file():
        fails.append("Q1 missing pepe-promptform.js")
    else:
        text = js.read_text(encoding="utf-8")
        if "customElements.define" not in text:
            fails.append("Q2 missing customElements.define")
        if "PepePromptform" not in text:
            fails.append("Q2 missing PepePromptform")
        if "attachShadow" not in text:
            fails.append("Q3 missing attachShadow")
        if "pepe-ready" not in text:
            fails.append("Q7 missing pepe-ready")
        if "pepe-action" not in text:
            fails.append("Q7 missing pepe-action")
        if "mount" not in text or "unmount" not in text:
            fails.append("Q8 missing mount or unmount")
        if re.search(r"document\.body\.style", text):
            fails.append("Q9 document.body.style write")
        if js.stat().st_size > LIMITS["pepe-promptform.js"]:
            fails.append("Q10 js over 40 KB")
    if not css.is_file():
        fails.append("Q4 missing css")
    else:
        ctext = css.read_text(encoding="utf-8")
        if "prefers-reduced-motion" not in ctext:
            fails.append("Q4 missing prefers-reduced-motion")
        if ":focus-visible" not in ctext:
            fails.append("Q5 missing focus-visible")
        if css.stat().st_size > LIMITS["pepe-promptform.css"]:
            fails.append("Q10 css over 24 KB")
    if not html.is_file() or "pepe-promptform" not in html.read_text(encoding="utf-8"):
        fails.append("Q11 host page missing custom element")
    joined = ""
    for name in ("pepe-promptform.js", "pepe-promptform.css", "index.html"):
        path = folder / name
        if path.is_file():
            joined += path.read_text(encoding="utf-8")
    if not re.search(r"aria-label|aria-labelledby", joined):
        fails.append("Q6 missing accessible name")

    report = folder / "QA.md"
    lines = ["# QA report", "", f"Folder: `{folder.name}`", ""]
    if fails:
        lines.append("Status: FAIL")
        lines.append("")
        for item in fails:
            lines.append(f"- {item}")
        report.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("FAIL")
        for item in fails:
            print(item)
        return 1
    lines.append("Status: PASS")
    lines.append("")
    lines.append("Q1-Q12 structural checks cleared. Syntax check is recorded by the caller.")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
