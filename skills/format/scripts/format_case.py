#!/usr/bin/env python3
"""Deterministic case reformatter for the /format skill.

Modes (aliases are case-insensitive):
  PC  Proper Case / ProperCase     first letter of each word upper, rest lower
  UC  UPPERCASE / AC / All Caps    every letter upper
  LC  lowercase                    every letter lower
  SC  smallcaps / SmallCaps        first letter of each word full capital,
                                   remaining letters of that word Unicode small caps

By default, separator characters (- _ • | ~ \\ / · – — etc.) are replaced with a single space.
Pass any of the keep flags to preserve them unchanged.

Usage:
  python3 format_case.py --mode PC "hello world"
  python3 format_case.py --mode SC --json "Digital Marketing Company"
  python3 format_case.py --mode SC --keep "e-mail subject"
  python3 format_case.py --self-test
"""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata

# Unicode small-capital map for a–z. Letters without a dedicated small-cap
# glyph keep a closest phonetic small-cap or the lowercase letter.
SMALL_CAPS = {
    "a": "ᴀ",  # U+1D00
    "b": "ʙ",  # U+0299
    "c": "ᴄ",  # U+1D04
    "d": "ᴅ",  # U+1D05
    "e": "ᴇ",  # U+1D07
    "f": "ꜰ",  # U+A730
    "g": "ɢ",  # U+0262
    "h": "ʜ",  # U+029C
    "i": "ɪ",  # U+026A
    "j": "ᴊ",  # U+1D0A
    "k": "ᴋ",  # U+1D0B
    "l": "ʟ",  # U+029F
    "m": "ᴍ",  # U+1D0D
    "n": "ɴ",  # U+0274
    "o": "ᴏ",  # U+1D0F
    "p": "ᴘ",  # U+1D18
    "q": "ǫ",  # U+01EB
    "r": "ʀ",  # U+0280
    "s": "ꜱ",  # U+A731
    "t": "ᴛ",  # U+1D1B
    "u": "ᴜ",  # U+1D1C
    "v": "ᴠ",  # U+1D20
    "w": "ᴡ",  # U+1D21
    "x": "x",  # no dedicated small-cap x
    "y": "ʏ",  # U+028F
    "z": "ᴢ",  # U+1D22
}

MODE_ALIASES = {
    "pc": "pc",
    "propercase": "pc",
    "proper-case": "pc",
    "proper_case": "pc",
    "proper case": "pc",
    "proper": "pc",
    "uc": "uc",
    "uppercase": "uc",
    "upper-case": "uc",
    "upper_case": "uc",
    "upper case": "uc",
    "upper": "uc",
    "ac": "uc",
    "allcaps": "uc",
    "all-caps": "uc",
    "all_caps": "uc",
    "all caps": "uc",
    "caps": "uc",
    "lc": "lc",
    "lowercase": "lc",
    "lower-case": "lc",
    "lower_case": "lc",
    "lower case": "lc",
    "lower": "lc",
    "sc": "sc",
    "smallcaps": "sc",
    "small-caps": "sc",
    "small_caps": "sc",
    "small caps": "sc",
    "smallcap": "sc",
    "small cap": "sc",
}

MODE_LABELS = {
    "pc": "Proper Case",
    "uc": "UPPERCASE",
    "lc": "lowercase",
    "sc": "Small Caps",
}


def normalize_mode(raw: str | None) -> str | None:
    if raw is None:
        return None
    key = " ".join(raw.strip().lower().replace("–", "-").replace("—", "-").split())
    key_compact = key.replace(" ", "").replace("-", "").replace("_", "")
    if key in MODE_ALIASES:
        return MODE_ALIASES[key]
    if key_compact in MODE_ALIASES:
        return MODE_ALIASES[key_compact]
    return None


def is_letter(ch: str) -> bool:
    return unicodedata.category(ch).startswith("L")


def is_emoji(ch: str) -> bool:
    """Heuristic: Symbol, other (So) or common emoji ranges. Preserve these."""
    cat = unicodedata.category(ch)
    if cat == "So":
        return True
    # Common emoji blocks (rough but sufficient for preservation).
    cp = ord(ch)
    return (
        0x1F300 <= cp <= 0x1F5FF
        or 0x1F600 <= cp <= 0x1F64F
        or 0x1F680 <= cp <= 0x1F6FF
        or 0x1F900 <= cp <= 0x1F9FF
        or 0x2600 <= cp <= 0x26FF
        or 0x2700 <= cp <= 0x27BF
    )


def is_separator(ch: str) -> bool:
    """Separator characters that should become spaces by default."""
    if ch in "-_•|~\\/·–—−‐‑‒―|•·":
        return True
    # Common punctuation that often acts as a word separator.
    if ch in ",.;:!?\"'`()[]{}":
        return True
    cat = unicodedata.category(ch)
    if cat.startswith("P") or (cat.startswith("S") and not is_emoji(ch)):
        return True
    return False


def replace_separators(text: str) -> str:
    """Replace separator characters with a single space. Keep letters, digits, whitespace, emoji."""
    return "".join(" " if is_separator(ch) else ch for ch in text)


def to_small_cap(ch: str) -> str:
    folded = ch.casefold()
    if len(folded) == 1 and folded in SMALL_CAPS:
        return SMALL_CAPS[folded]
    # Latin letters outside a–z stay lower; everything else is unchanged.
    if is_letter(ch):
        return ch.lower()
    return ch


def transform_word(word: str, mode: str) -> str:
    if mode == "uc":
        return word.upper()
    if mode == "lc":
        return word.lower()

    out: list[str] = []
    seen_letter = False
    for ch in word:
        if not is_letter(ch):
            out.append(ch)
            continue
        if not seen_letter:
            out.append(ch.upper())
            seen_letter = True
            continue
        if mode == "pc":
            out.append(ch.lower())
        else:  # sc
            out.append(to_small_cap(ch))
    return "".join(out)


def transform_text(text: str, mode: str, keep_separators: bool = False) -> str:
    """Apply the mode. By default replace separators with spaces first."""
    if mode not in MODE_LABELS:
        raise ValueError(f"unknown mode: {mode}")

    if not keep_separators:
        text = replace_separators(text)

    parts: list[str] = []
    buf: list[str] = []

    def flush_word() -> None:
        if buf:
            parts.append(transform_word("".join(buf), mode))
            buf.clear()

    for ch in text:
        # A "word" is a maximal run that is not whitespace.
        if ch.isspace():
            flush_word()
            parts.append(ch)
        else:
            buf.append(ch)
    flush_word()
    return "".join(parts)


def self_test() -> int:
    cases = [
        # default: replace separators with space
        ("pc", "hello world", False, "Hello World"),
        ("pc", "HELLO WORLD", False, "Hello World"),
        ("pc", "don't stop", False, "Don T Stop"),
        ("pc", "e-mail subject", False, "E Mail Subject"),
        ("pc", "  spaced   out  ", False, "  Spaced   Out  "),
        ("uc", "Hello World", False, "HELLO WORLD"),
        ("ac", "Hello World", False, "HELLO WORLD"),
        ("lc", "Hello World", False, "hello world"),
        ("sc", "Hello", False, "Hᴇʟʟᴏ"),
        ("sc", "Digital Marketing Company", False, "Dɪɢɪᴛᴀʟ Mᴀʀᴋᴇᴛɪɴɢ Cᴏᴍᴘᴀɴʏ"),
        ("ProperCase", "a b", False, "A B"),
        ("ALL CAPS", "mix", False, "MIX"),
        ("small caps", "Qa", False, "Qᴀ"),
        ("sc", "2026-spatial-semiotics", False, "2026 Sᴘᴀᴛɪᴀʟ Sᴇᴍɪᴏᴛɪᴄꜱ"),
        ("pc", "file_name-test|one", False, "File Name Test One"),
        # keep behavior
        ("pc", "e-mail subject", True, "E-mail Subject"),
        ("pc", "don't stop", True, "Don't Stop"),
        ("sc", "hello, world!", True, "Hᴇʟʟᴏ, Wᴏʀʟᴅ!"),
    ]
    failed = 0
    for raw_mode, src, keep, expected in cases:
        mode = normalize_mode(raw_mode)
        got = transform_text(src, mode, keep_separators=keep)  # type: ignore[arg-type]
        if got != expected:
            failed += 1
            print(f"FAIL {raw_mode!r} keep={keep} {src!r}\n  got {got!r}\n  exp {expected!r}", file=sys.stderr)
    if failed:
        print(f"{failed} failed", file=sys.stderr)
        return 1
    print("ok", len(cases), "cases")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Reformat text by /format mode.")
    parser.add_argument("--mode", "-m", required=False, help="PC, UC, AC, LC, SC, or a long alias")
    parser.add_argument("--json", action="store_true", help="print a JSON object")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--keep",
        "--nstrips",
        "--strip",
        "--rmsprtrs",
        "--remove",
        "--rmsprtr",
        action="store_true",
        dest="keep",
        help="Do not replace separators with spaces (preserve them).",
    )
    parser.add_argument("text", nargs="*", help="text to reformat (joins with a single space)")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    mode = normalize_mode(args.mode)
    if mode is None:
        print(
            json.dumps({"error": "unknown_or_missing_mode", "mode": args.mode})
            if args.json
            else "error: unknown or missing mode (use PC, UC, AC, LC, SC, or a listed alias)",
            file=sys.stderr,
        )
        return 2

    if not args.text:
        raw = sys.stdin.read()
    else:
        raw = " ".join(args.text)

    out = transform_text(raw, mode, keep_separators=args.keep)
    if args.json:
        print(
            json.dumps(
                {
                    "mode": mode,
                    "label": MODE_LABELS[mode],
                    "source": raw,
                    "text": out,
                    "kept_separators": args.keep,
                },
                ensure_ascii=False,
            )
        )
    else:
        sys.stdout.write(out)
        if not out.endswith("\n"):
            sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
