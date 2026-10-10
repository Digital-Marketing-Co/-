#!/usr/bin/env python3
"""Deterministic case reformatter for the /format skill.

Modes (aliases are case-insensitive):
  PC  Proper Case / ProperCase     first letter of each word upper, rest lower
  UC  UPPERCASE / AC / All Caps    every letter upper
  LC  lowercase                    every letter lower
  SC  smallcaps / SmallCaps        first letter of each word full capital,
                                   remaining letters of that word Unicode small caps

Usage:
  python3 format_case.py --mode PC "hello world"
  python3 format_case.py --mode SC --json "Digital Marketing Co."
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


def transform_text(text: str, mode: str) -> str:
    """Apply the mode while preserving whitespace runs and non-word gaps."""
    if mode not in MODE_LABELS:
        raise ValueError(f"unknown mode: {mode}")
    parts: list[str] = []
    buf: list[str] = []
    in_word = False

    def flush_word() -> None:
        if buf:
            parts.append(transform_word("".join(buf), mode))
            buf.clear()

    for ch in text:
        # A "word" is a maximal run that is not whitespace. Punctuation
        # stays glued to the adjacent letters so "hello," becomes "Hello,".
        if ch.isspace():
            flush_word()
            parts.append(ch)
            in_word = False
        else:
            buf.append(ch)
            in_word = True
    flush_word()
    return "".join(parts)


def self_test() -> int:
    cases = [
        ("pc", "hello world", "Hello World"),
        ("pc", "HELLO WORLD", "Hello World"),
        ("pc", "don't stop", "Don't Stop"),
        ("pc", "e-mail subject", "E-mail Subject"),
        ("pc", "  spaced   out  ", "  Spaced   Out  "),
        ("uc", "Hello World", "HELLO WORLD"),
        ("ac", "Hello World", "HELLO WORLD"),
        ("lc", "Hello World", "hello world"),
        ("sc", "Hello", "Hᴇʟʟᴏ"),
        ("sc", "Digital Marketing Co.", "Dɪɢɪᴛᴀʟ Mᴀʀᴋᴇᴛɪɴɢ Cᴏᴍᴘᴀɴʏ"),
        ("ProperCase", "a b", "A B"),
        ("ALL CAPS", "mix", "MIX"),
        ("small caps", "Qa", "Qᴀ"),
    ]
    failed = 0
    for raw_mode, src, expected in cases:
        mode = normalize_mode(raw_mode)
        got = transform_text(src, mode)  # type: ignore[arg-type]
        if got != expected:
            failed += 1
            print(f"FAIL {raw_mode!r} {src!r}\n  got {got!r}\n  exp {expected!r}", file=sys.stderr)
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

    out = transform_text(raw, mode)
    if args.json:
        print(
            json.dumps(
                {
                    "mode": mode,
                    "label": MODE_LABELS[mode],
                    "source": raw,
                    "text": out,
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
