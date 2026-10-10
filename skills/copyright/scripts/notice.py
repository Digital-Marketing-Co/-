"""Pure publication copyright policy shared by PDF builders."""
from datetime import date

DEFAULT_OWNER = "Web Development Corporation"
DEFAULT_START = 2012

def notice_text(start=DEFAULT_START, year=None, owner=DEFAULT_OWNER):
    start = int(start)
    year = date.today().year if year is None else int(year)
    span = f"{start}–{year}" if year > start else str(start)
    return f"© {span} {owner}. All rights reserved."

def notice_for(data=None):
    data = data or {}
    owner = data.get("owner") or {}
    if isinstance(owner, str):
        name, start = owner, data.get("copyright_start", DEFAULT_START)
    else:
        name = owner.get("short") or owner.get("legal") or DEFAULT_OWNER
        start = data.get("copyright_start", owner.get("founded", DEFAULT_START))
    return notice_text(start=start, owner=name)
