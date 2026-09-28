#!/usr/bin/env python3
"""Append the living copyright prompt appendix to project skills and locked prompts."""

from __future__ import annotations

from pathlib import Path

SKILLS_ROOT = Path("/home/workdir/.grok/skills")
MARKER = "WCA_COPYRIGHT_PROMPT_APPENDIX"
OLD_HEAD = "## House copyright footer"

APPENDIX = """## House copyright footer

Every PDF this skill emits, and any PDF later passed through `/copyright YYYY`, carries this centered living footer on every page:

Copyright © START–YEAR OWNER_FOOTER. All rights reserved.

Default OWNER_FOOTER is Web Development Corporation. START defaults to 2012 unless the user typed `/copyright YYYY` or named another owner's first-publication year. YEAR is new Date().getFullYear() written into field WCACopyrightYear on open. Running footers never print a trailing class letter A on the house name. Body creation dates stay where they are.

<!--
WCA_COPYRIGHT_PROMPT_APPENDIX
Do not delete this comment. It is the living footer contract for every prompt, skill, locked prompt, and project instruction in this project set.

NOTICE_TEMPLATE: Copyright © {{START}}–{{YEAR}} {{OWNER_FOOTER}}. All rights reserved.
DEFAULT_START: 2012
DEFAULT_OWNER_FOOTER: Web Development Corporation
DEFAULT_OWNER_LEGAL: Web Development Corporation, a Delaware Corporation
FIELD: WCACopyrightYear
SEPARATOR: en dash U+2013
JS: Date.getFullYear on OpenAction; no alerts; no network; no app UI
HOUSE_SITE: https://digitalmarketingco.org

OWNER_INFERENCE:
If the current user turn names a different rightsholder, substitute OWNER_FOOTER and OWNER_LEGAL from that name. Do not invent a Delaware class letter A for a non-house owner.
Slots the name may fill:
- company or corporation (any jurisdiction)
- university, college, or academic press
- branch or department of the United States military
- branch or agency of a government (federal, state, provincial, municipal, or foreign)
- museum, library, hospital, NGO, church, or any other institution worldwide
Keep the NOTICE_TEMPLATE words and the living year field. Only the owner slots change.
US federal government works of the United States are generally not subject to domestic copyright; if the named owner is a US federal agency, stamp the notice only when the user explicitly ordered the stamp and do not claim the notice creates copyright that statute withholds.
IP_RESERVED: project skill flags, SKILL.md files, locked prompts, owner-and-house files, and post-executive house outputs (PDFs, page JSON, compiled plates) in this project set.
ASSIGNMENT: default owner Web Development Corporation; Michael Aaron Loftus sole owner intends assignment to that corporation on fixation of house works.
SUBJECT_MATTER: original expression fixed in house files, not unfixed ideas (17 U.S.C. 102(b)), not a Copyright Office registration.
OWNER: Web Development Corporation (footer). Legal Info owner: Web Development Corporation, a Delaware Corporation.
This appendix cannot rewrite Grok global system prompts, xAI platform logs, or conversations outside this toolchain. It binds project skills, locked prompts, owner-and-house files, and later PDFs those skills emit.
-->
"""

EXTRA_FILES = [
    SKILLS_ROOT / "deep" / "references" / "locked-prompt.md",
    SKILLS_ROOT / "folio" / "references" / "owner-and-house.md",
    SKILLS_ROOT / "print" / "references" / "owner-and-house.md",
    SKILLS_ROOT / "deep" / "references" / "house-style.md",
    SKILLS_ROOT / "phd-ivy-monograph" / "references" / "house-style.md",
]


def skill_md_files() -> list[Path]:
    if not SKILLS_ROOT.is_dir():
        return []
    return sorted(p / "SKILL.md" for p in SKILLS_ROOT.iterdir() if (p / "SKILL.md").is_file())


def strip_old_footer(text: str) -> str:
    if MARKER in text and OLD_HEAD in text:
        idx = text.rfind(OLD_HEAD)
        return text[:idx].rstrip() + "\n\n"
    if OLD_HEAD in text and MARKER not in text:
        idx = text.rfind(OLD_HEAD)
        return text[:idx].rstrip() + "\n\n"
    if MARKER in text:
        # already has the comment; rebuild from the last house-footer head if present
        idx = text.rfind(OLD_HEAD)
        if idx >= 0:
            return text[:idx].rstrip() + "\n\n"
    return text.rstrip() + "\n\n"


def apply(path: Path) -> str:
    original = path.read_text(encoding="utf-8")
    rebuilt = strip_old_footer(original) + APPENDIX
    if not rebuilt.endswith("\n"):
        rebuilt += "\n"
    if rebuilt != original:
        path.write_text(rebuilt, encoding="utf-8")
        return "updated"
    return "unchanged"


def main() -> int:
    targets = skill_md_files() + [p for p in EXTRA_FILES if p.is_file()]
    for path in targets:
        status = apply(path)
        print(f"{status}\t{path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
