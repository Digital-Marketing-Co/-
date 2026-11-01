#!/usr/bin/env python3
"""/Q A1Z26 + duovigesimal battery with +/* window operators."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from itertools import combinations
from typing import Iterable

DIGITS22 = "0123456789ABCDEFGHIJKL"
assert len(DIGITS22) == 22

ORD = {chr(64 + i): i for i in range(1, 27)}
REV = {i: chr(64 + i) for i in range(1, 27)}

PRESIDENTS = [
    "Washington", "Adams", "Jefferson", "Madison", "Monroe",
    "Jackson", "VanBuren", "Harrison", "Tyler", "Polk", "Taylor",
    "Fillmore", "Pierce", "Buchanan", "Lincoln", "Johnson", "Grant",
    "Hayes", "Garfield", "Arthur", "Cleveland", "McKinley",
    "Roosevelt", "Taft", "Wilson", "Harding", "Coolidge", "Hoover",
    "Truman", "Eisenhower", "Kennedy", "Nixon", "Ford", "Carter",
    "Reagan", "Bush", "Clinton", "Obama", "Trump", "Biden",
]

JFK_TERMS = [
    "Kennedy", "JFK", "John", "Fitzgerald", "Jackie", "Jacqueline", "Bouvier",
    "Caroline", "JohnJohn", "Oswald", "Lee", "Harvey", "Marina", "Ruby", "Jacob",
    "Rubenstein", "Knoll", "Grassy", "Dealey", "Plaza", "Dallas", "Texas",
    "Houston", "Elm", "Street", "Stemmons", "Triple", "Underpass",
    "Warren", "Commission", "Earl", "Ford", "McCloy", "Dulles", "Russell",
    "Cooper", "Boggs", "Specter", "Belin", "Rankin",
    "HSCA", "Blakey", "Sprague", "Stokes",
    "Zapruder", "Abraham", "Nix", "Muchmore", "Hughes", "Bronson",
    "Tippit", "JDtippit", "Connally", "Nellie", "Hill", "Clint", "Ready",
    "Greer", "Kellerman", "Lawson", "Sorrels", "Rowley",
    "Johnson", "LBJ", "Ladybird", "Hoover", "Edgar", "Tolson",
    "Angleton", "Helms", "McCone", "Harvey", "Morales", "Phillips",
    "CIA", "FBI", "Secret", "Service", "ONI", "Military",
    "Motorcade", "Limousine", "Lincoln", "SS100X", "Lancer",
    "Book", "Depository", "TSBD", "Sixth", "Floor", "Sniper", "Nest",
    "Rifle", "Mannlicher", "Carcano", "C2766", "Pistol", "Revolver",
    "Magic", "Bullet", "CE399", "Single", "Bullet", "Pristine",
    "Shooter", "Conspiracy", "Lone", "Nut", "Patsy",
    "Garrison", "Jim", "Shaw", "Clay", "Ferrie", "David", "Bannister",
    "Mongoose", "JMWAVE", "Cuba", "Castro", "Fidel", "Bay", "Pigs",
    "Mafia", "Marcello", "Trafficante", "Giancana", "Roselli", "Traffic",
    "Onassis", "Airforce", "One", "AF1", "Parkland", "Bethesda", "Autopsy",
    "Humes", "Boswell", "Finck", "Burkley",
    "Umbrella", "Man", "Badge", "Man", "Tramp", "Tramps",
    "Nixon", "Nixon", "Watergate",
    "Loftus", "NOLE", "NOEL",
    "Backyard", "Photo", "Walker", "General", "Odio", "Sylvia",
    "Mexico", "City", "Embassy", "Kostikov",
    "Fair", "Play", "Cuba", "Committee", "FPCC",
    "New", "Orleans", "Camp", "Street",
    "Irving", "Paine", "Ruth", "Michael", "MichaelPaine",
    "Wesley", "Frazier", "Truly", "Roy", "Brennan", "Howard",
    "Arnold", "Newman", "Moorman", "Mary", "Jean", "Hill",
    "Altgens", "James", "Hudson", "Bowers", "Lee", "Simmons",
    "Railroad", "Overpass", "Daltex", "County", "Records",
    "Parkland", "Trauma", "Room", "One",
    "Torbitt", "Document", "Hunt", "EHoward", "Sturgis", "Frank",
    "Phillips", "DavidAtlee", "Veciana", "Antonio", "Alpha",
    "Lansdale", "Edward", "Krulak", "Operation", "Northwoods",
    "Chicago", "Tampa", "Plot", "Vallee", "Thomas",
]

LEX = {
    "A","I","AN","AS","AT","BE","BY","DO","GO","HE","IF","IN","IS","IT",
    "ME","MY","NO","OF","ON","OR","SO","TO","UP","US","WE","AND","THE",
    "FOR","BUT","NOT","YOU","ALL","CAN","HER","WAS","ONE","OUR","OUT",
    "DAY","GET","HAS","HIM","HIS","HOW","MAN","NEW","NOW","OLD","SEE",
    "TWO","WAY","WHO","CIA","FBI","NSA","JFK","LBJ","RFK","DEA","DOD",
    "USA","KGB","OSS","CA","AI","AL","EL","LA","LE","LI","LO","NE","OL",
    "AA","BB","FC","SFC","Q","K","V","EG","BF","Z","JH","AH","BE","DO",
    "SHE","HE","OR","TO","UP","OF","NO","US","ON","IN","CODE","FILE",
    "SHOT","DEAL","PLOT","PLAN","BOOK","HILL","WALL","WARD","WEST",
    "EAST","PARK","POST","SEAL","SIGN","STAR","TIME","VOTE","YEAR",
    "ZERO","ACE","BOND","CELL","COLD","DOOR","FIRE","FLAG","IRON",
    "KING","LAND","LEAD","LEFT","LINE","LIST","LOCK","LONG","LORD",
    "LOSS","MAIL","MARK","NAME","NAVY","NEED","NONE","NOTE","NULL",
    "OATH","OPEN","OVAL","PASS","POLE","POLL","PORT","RACE","RAIL",
    "READ","REST","RISE","ROAD","ROCK","ROLE","ROOM","ROSE","SAFE",
    "SALE","SEED","SITE","SOLE","TALE","TALK","TEAM","TELL","TOLL",
    "TONE","TOOL","TREE","TURN","UNIT","WIND","WIRE","WOLF","WOOD",
    "WORD","WORK","YARD","KNOLL","KENNEDY","OSWALD","RUBY","WARREN",
    "DALLAS","TEXAS","JOHNSON","NIXON","FORD","CARTER","BUSH",
    "CLINTON","OBAMA","TRUMP","BIDEN","LOFTUS","HOOVER","DULLES","CE","HSCA","TSBD","ELM","NEST","LONE","PATSY","HO","HOE","H","O",
}


def clean(s: str) -> str:
    return re.sub(r"[^A-Za-z]", "", s).upper()


def to_base22(n: int) -> str:
    if n < 0:
        raise ValueError("negative")
    if n == 0:
        return "0"
    out = []
    x = n
    while x:
        x, r = divmod(x, 22)
        out.append(DIGITS22[r])
    return "".join(reversed(out))


def a1z26_digits(word: str) -> str:
    return "".join(f"{ORD[ch]:02d}" if ORD[ch] >= 10 else str(ORD[ch]) for ch in word)


def a1z26_padded(word: str) -> str:
    return "".join(f"{ORD[ch]:02d}" for ch in word)


def int_to_letters_mixed(n: int) -> list[str]:
    """Map an integer to A1Z26 letter bundles (17=Q, 26=Z and BF, 108=JH/AH/J8)."""
    out = []
    if 1 <= n <= 26:
        out.append(REV[n])
    s = str(n)
    # two-digit chunks
    if len(s) == 2 and 1 <= n <= 26:
        out.append(REV[n])
    if len(s) >= 2:
        a, b = int(s[0]), int(s[1:]) if s[1:] else 0
        pair = ""
        if 1 <= int(s[0]) <= 26:
            pair += REV[int(s[0])]
        if len(s) == 2 and 1 <= int(s[1]) <= 9:
            pair += REV[int(s[1])]
        if pair:
            out.append(pair)
        # 26 => BF (2,6)
        if len(s) == 2:
            x, y = int(s[0]), int(s[1])
            if 1 <= x <= 26 and 1 <= y <= 26:
                out.append(REV[x] + REV[y])
    if len(s) == 3:
        # 108 => J=10 H=8, A=1 H=08, J8
        if 1 <= int(s[:2]) <= 26:
            out.append(REV[int(s[:2])] + (REV[int(s[2])] if 1 <= int(s[2]) <= 26 else s[2]))
        if 1 <= int(s[0]) <= 26 and 1 <= int(s[1:]) <= 26:
            out.append(REV[int(s[0])] + REV[int(s[1:])])
        out.append(REV[int(s[:2])] + s[2] if 1 <= int(s[:2]) <= 26 else s)
    # unique preserve order
    seen = []
    for x in out:
        if x and x not in seen:
            seen.append(x)
    return seen or [s]


def apply_pairs(text: str) -> list[tuple[str, str]]:
    """K||AA, V||BB, FC||SFC and inverses as literal substitutions."""
    rows = [("id", text)]
    fwd = text
    fwd2 = fwd.replace("K", "AA").replace("V", "BB").replace("FC", "SFC")
    if fwd2 != text:
        rows.append(("expand_KAA_VBB_FC", fwd2))
    rev = text
    rev2 = rev.replace("AA", "K").replace("BB", "V").replace("SFC", "FC")
    if rev2 != text:
        rows.append(("collapse_AAK_BBV_SFC", rev2))
    return rows



def a1z26_letter(n: int) -> str:
    """Single-letter A1Z26 if 1..26, else empty."""
    if 1 <= n <= 26:
        return REV[n]
    return ""


def furthermore_pair(a: int, b: int) -> list[tuple[str, int, str]]:
    """Second-generation +/* on two child results.

    Locked ABC example: 1+2=3, 2+3=5, then 3+5=8=H and 3*5=15=O, so HO ≈ HOE.
    """
    rows = []
    s, pr = a + b, a * b
    ls, lp = a1z26_letter(s), a1z26_letter(pr)
    rows.append(("furthermore_sum", s, ls or str(s)))
    rows.append(("furthermore_prod", pr, lp or str(pr)))
    if ls and lp:
        concat = ls + lp
        rows.append(("furthermore_concat", s * 100 + (pr % 100), concat))
        if concat == "HO":
            rows.append(("furthermore_approx_HOE", s * 100 + (pr % 100), "HOE"))
    return rows



def chunk_letter(n: int) -> str | None:
    """1..26 → A..Z. 10=J, 11=K, 22=V, 26=Z. 0 skipped."""
    if n == 0:
        return ""
    if 1 <= n <= 26:
        return REV[n]
    return None


def partitions_1_2(digits: str) -> list[list[int]]:
    """All compositions of the digit string into parts of length 1 or 2."""
    digits = "".join(ch for ch in digits if ch.isdigit())
    out: list[list[int]] = []

    def rec(i: int, acc: list[int]) -> None:
        if i == len(digits):
            out.append(acc[:])
            return
        # length 1
        n1 = int(digits[i])
        acc.append(n1)
        rec(i + 1, acc)
        acc.pop()
        # length 2
        if i + 1 < len(digits):
            n2 = int(digits[i : i + 2])
            acc.append(n2)
            rec(i + 2, acc)
            acc.pop()

    if digits:
        rec(0, [])
    return out


def letterize_chunks(chunks: list[int]) -> str | None:
    letters = []
    for n in chunks:
        lab = chunk_letter(n)
        if lab is None:
            return None  # 27..99 invalid as a single A1Z26 cell
        letters.append(lab)
    return "".join(letters)


def reduce_to_one_or_two(letters: str, depth: int = 0, seen: set[str] | None = None) -> list[str]:
    """Reduce a letter string to length 1 or 2 via ordinal sum and 1-2 partitions of that sum."""
    if seen is None:
        seen = set()
    letters = re.sub(r"[^A-Z]", "", letters.upper())
    if not letters or letters in seen or depth > 6:
        return []
    seen.add(letters)
    leaves = []
    if 1 <= len(letters) <= 2:
        leaves.append(letters)
    total = sum(ORD[ch] for ch in letters)
    # one letter if 1..26
    if 1 <= total <= 26:
        leaves.append(REV[total])
    # two-digit reading of the total
    ds = str(total)
    for part in partitions_1_2(ds):
        lab = letterize_chunks(part)
        if lab:
            if 1 <= len(lab) <= 2:
                leaves.append(lab)
            elif depth < 5:
                leaves.extend(reduce_to_one_or_two(lab, depth + 1, seen))
    # unique preserve
    out = []
    for x in leaves:
        if x and x not in out:
            out.append(x)
    return out


def decode_tree(label: str, digits: str) -> dict:
    """Hierarchical 1-2 digit partition tree plus 1-2 letter reductions."""
    parts = partitions_1_2(digits)
    branches = []
    leaf_count: dict[str, int] = {}
    full_count: dict[str, int] = {}
    for ch in parts:
        lab = letterize_chunks(ch)
        row = {
            "chunks": ch,
            "valid": lab is not None,
            "letters": lab,
            "leaves": [],
        }
        if lab:
            full_count[lab] = full_count.get(lab, 0) + 1
            leaves = reduce_to_one_or_two(lab)
            row["leaves"] = leaves
            for lf in leaves:
                leaf_count[lf] = leaf_count.get(lf, 0) + 1
        branches.append(row)
    connected = sorted(
        ({"node": k, "branches": v} for k, v in leaf_count.items() if v >= 2),
        key=lambda r: (-r["branches"], r["node"]),
    )
    return {
        "label": label,
        "digits": digits,
        "n_partitions": len(parts),
        "n_valid": sum(1 for b in branches if b["valid"]),
        "branches": branches,
        "full_string_freq": dict(sorted(full_count.items(), key=lambda kv: (-kv[1], kv[0]))),
        "leaf_freq": dict(sorted(leaf_count.items(), key=lambda kv: (-kv[1], kv[0]))),
        "connected_duplicate_leaves": connected,
    }

def window_ops(nums: list[int]) -> list[tuple[str, int]]:
    """Adjacent and prefix/suffix + and * on the A1Z26 number list."""
    rows = []
    n = len(nums)
    if not nums:
        return rows
    rows.append(("sum_all", sum(nums)))
    prod = 1
    for v in nums:
        prod *= v
    rows.append(("prod_all", prod))
    for i in range(n - 1):
        rows.append((f"sum_{i}_{i+1}", nums[i] + nums[i + 1]))
        rows.append((f"prod_{i}_{i+1}", nums[i] * nums[i + 1]))
    # join first-two digits as a number plus last, etc. (user 19+34, 193+4)
    s = "".join(str(v) for v in nums)
    # all split points
    for k in range(1, len(s)):
        left, right = s[:k], s[k:]
        if left.startswith("0") or right.startswith("0"):
            # still allow if user dropped zeros already
            pass
        try:
            a, b = int(left), int(right)
        except ValueError:
            continue
        rows.append((f"split_sum_{k}", a + b))
        rows.append((f"split_prod_{k}", a * b))
    return rows


def encode_furthermore(word: str, vals: list[int]) -> list[tuple[str, int, str]]:
    """Chain adjacent + and * children, then letterize."""
    out = []
    n = len(vals)
    if n < 3:
        return out
    # first two adjacent sums (the locked ABC pattern)
    s0, s1 = vals[0] + vals[1], vals[1] + vals[2]
    out.extend(("sumchain_" + tag, num, let) for tag, num, let in furthermore_pair(s0, s1))
    p0, p1 = vals[0] * vals[1], vals[1] * vals[2]
    out.extend(("prodchain_" + tag, num, let) for tag, num, let in furthermore_pair(p0, p1))
    # slide the same 3-letter window across the word
    for i in range(1, n - 2):
        s0, s1 = vals[i] + vals[i + 1], vals[i + 1] + vals[i + 2]
        out.extend((f"sumchain{i}_" + tag, num, let) for tag, num, let in furthermore_pair(s0, s1))
    return out


def score_string(s: str) -> tuple[float, list[str]]:
    raw = re.sub(r"[^A-Z]", "", s.upper())
    hits = []
    score = 0.0
    if raw in LEX:
        score += 6.0
        hits.append(raw)
    n = len(raw)
    for i in range(n):
        for j in range(i + 2, min(n, i + 8) + 1):
            sub = raw[i:j]
            if sub in LEX:
                score += max(0.3, len(sub) * 0.3)
                if sub not in hits:
                    hits.append(sub)
    if raw and any(c in raw for c in "AEIOU"):
        score += 0.2
    return score, hits[:12]


@dataclass
class Candidate:
    source: str
    method: str
    integer: int
    base22: str
    letters: str
    score: float
    hits: list[str]
    clue: str


def emit(source: str, method: str, n: int, letters: str) -> Candidate:
    b22 = to_base22(n) if n >= 0 else "-"
    sc, hits = score_string(letters)
    # pair variants
    extra = []
    for tag, alt in apply_pairs(letters):
        if tag != "id":
            extra.append(f"{tag}:{alt}")
            s2, h2 = score_string(alt)
            if s2 > sc:
                sc = s2
            for h in h2:
                if h not in hits:
                    hits.append(h)
    clue = "; ".join(hits[:8] + extra[:4])
    return Candidate(source, method, n, b22, letters, sc, hits[:12], clue)


def encode_word(word: str) -> list[Candidate]:
    w = clean(word)
    if not w:
        return []
    vals = [ORD[ch] for ch in w]
    cands: list[Candidate] = []
    s_ord = sum(vals)
    cands.append(emit(w, "a1z26_sum", s_ord, "".join(int_to_letters_mixed(s_ord)[:1])))
    for lab in int_to_letters_mixed(s_ord):
        cands.append(emit(w, "a1z26_sum_bundle", s_ord, lab))
    cands.append(emit(w, "a1z26_sum_b22_A0", s_ord, b22_as_letters(to_base22(s_ord), "A0")))
    cands.append(emit(w, "a1z26_sum_b22_A1", s_ord, b22_as_letters(to_base22(s_ord), "A1")))
    # concatenated digit string
    cat = "".join(str(v) for v in vals)
    try:
        cat_n = int(cat)
        cands.append(emit(w, "a1z26_concat", cat_n, cat))
        for lab in int_to_letters_mixed(cat_n if cat_n < 10**6 else cat_n % 10**6):
            cands.append(emit(w, "a1z26_concat_bundle", cat_n, lab))
    except ValueError:
        cat_n = 0
    for tag, n in window_ops(vals):
        if n > 10**12:
            continue
        bundles = int_to_letters_mixed(n) if n < 10**5 else [str(n)]
        for lab in bundles[:4]:
            cands.append(emit(w, "op_" + tag, n, lab))
    for tag, n, lab in encode_furthermore(w, vals):
        if n > 10**12:
            continue
        cands.append(emit(w, "op_" + tag, n, lab))
    # pair expand/collapse on the source itself
    for tag, alt in apply_pairs(w):
        if tag != "id":
            cands.append(emit(w, tag, s_ord, alt))
    return cands


def b22_as_letters(b22: str, mode: str) -> str:
    letters = []
    for ch in b22.upper():
        v = DIGITS22.index(ch)
        if mode == "A0":
            letters.append(chr(ord("A") + v))
        else:
            letters.append("O" if v == 0 else chr(ord("A") + v - 1))
    return "".join(letters)


def encode_integer(label: str, n: int) -> list[Candidate]:
    cands = []
    b22 = to_base22(n)
    tree = decode_tree(label, str(n))
    for node, freq in list(tree["leaf_freq"].items())[:24]:
        cands.append(emit(label, f"tree_leaf_x{freq}", n, node))
    for node, freq in list(tree["full_string_freq"].items())[:12]:
        cands.append(emit(label, f"tree_full_x{freq}", n, node))
    cands.append(emit(label, "int_b22", n, b22))
    cands.append(emit(label, "int_b22_A0", n, b22_as_letters(b22, "A0")))
    cands.append(emit(label, "int_b22_A1", n, b22_as_letters(b22, "A1")))
    for lab in int_to_letters_mixed(n if n < 10**5 else int(str(n)[-4:])):
        cands.append(emit(label, "int_a1z26_tail", n, lab))
    # decimal digit letters 0=O 1=A
    dec = "".join("O" if d == "0" else chr(ord("A") + int(d) - 1) for d in str(n))
    cands.append(emit(label, "int_dec_letters", n, dec))
    for tag, alt in apply_pairs(dec):
        if tag != "id":
            cands.append(emit(label, "int_dec_" + tag, n, alt))
    for tag, alt in apply_pairs(b22_as_letters(b22, "A1")):
        if tag != "id":
            cands.append(emit(label, "int_b22A1_" + tag, n, alt))
    return cands


def rank_all(names: Iterable[str], integers: list[tuple[str, int]]) -> list[Candidate]:
    bag: list[Candidate] = []
    for n in names:
        bag.extend(encode_word(n))
    for lab, val in integers:
        bag.extend(encode_integer(lab, val))
    bag.sort(key=lambda c: (-c.score, c.source, c.method))
    return bag


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("names", nargs="*")
    p.add_argument("--presidents", action="store_true")
    p.add_argument("--jfk", action="store_true")
    p.add_argument("--integers", default="")
    p.add_argument("--out", default="")
    p.add_argument("--top", type=int, default=60)
    args = p.parse_args()
    names = list(args.names)
    if args.presidents:
        names.extend(PRESIDENTS)
    if args.jfk:
        names.extend(JFK_TERMS)
    # unique preserve
    seen = set()
    uniq = []
    for n in names:
        k = clean(n)
        if k and k not in seen:
            seen.add(k)
            uniq.append(k)
    ints = []
    if args.integers:
        for part in args.integers.split(","):
            part = part.strip()
            if not part:
                continue
            if "=" in part:
                lab, val = part.split("=", 1)
                ints.append((lab.strip(), int(val)))
            else:
                ints.append((part, int(part)))
    ranked = rank_all(uniq, ints)
    trees = [decode_tree(lab, str(val)) for lab, val in ints]
    for name in uniq[:80]:
        w = clean(name)
        if w:
            concat = "".join(str(ORD[ch]) for ch in w)
            trees.append(decode_tree(w, concat))
    payload = {
        "base": 22,
        "digits": DIGITS22,
        "operators": ["+", "*"],
        "pairs": {"K": "AA", "V": "BB", "FC": "SFC", "AA": "K", "BB": "V", "SFC": "FC"},
        "count": len(ranked),
        "sources": uniq,
        "integers": [{"label": a, "n": b, "base22": to_base22(b)} for a, b in ints],
        "trees": trees,
        "ranked": [asdict(c) for c in ranked[: args.top]],
        "presidents_sum": [
            {"name": clean(n), "a1z26_sum": sum(ORD[ch] for ch in clean(n)), "base22": to_base22(sum(ORD[ch] for ch in clean(n)))}
            for n in PRESIDENTS
        ],
    }
    text = json.dumps(payload, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
