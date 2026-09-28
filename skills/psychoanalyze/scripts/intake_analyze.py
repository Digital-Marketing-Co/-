#!/usr/bin/env python3
"""Closed-artifact surface inventory for /PsychoAnalyze.

Counts only. Does not infer a diagnosis. Word lists are house-small
and must be treated as heuristics in the monograph.
"""

from __future__ import annotations

import argparse
import json
import re
import time
from collections import Counter
from pathlib import Path

TOKEN_RE = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?")

PRONOUNS = {
    "i": "first_sing",
    "me": "first_sing",
    "my": "first_sing",
    "mine": "first_sing",
    "myself": "first_sing",
    "we": "first_plur",
    "us": "first_plur",
    "our": "first_plur",
    "ours": "first_plur",
    "ourselves": "first_plur",
    "you": "second",
    "your": "second",
    "yours": "second",
    "yourself": "second",
    "yourselves": "second",
    "he": "third",
    "him": "third",
    "his": "third",
    "she": "third",
    "her": "third",
    "hers": "third",
    "they": "third",
    "them": "third",
    "their": "third",
    "theirs": "third",
    "himself": "third",
    "herself": "third",
    "themselves": "third",
    "it": "it",
    "its": "it",
    "itself": "it",
}

AFFECT_POS = {
    "love", "loved", "loving", "joy", "happy", "hope", "hoped", "hopeful",
    "good", "great", "safe", "warm", "tender", "grateful", "peace", "peaceful",
    "beautiful", "beauty", "trust", "trusted",
}
AFFECT_NEG = {
    "hate", "hated", "angry", "anger", "fear", "afraid", "sad", "sadness",
    "shame", "ashamed", "guilt", "guilty", "envy", "envious", "rage",
    "dead", "death", "kill", "hurt", "pain", "painful", "alone", "empty",
    "dark", "cold", "lost", "broken", "worthless",
}
DEFENSE_MARKERS = {
    "but": "reversal_or_undoing",
    "however": "isolation",
    "obviously": "intellectualization",
    "clearly": "intellectualization",
    "never": "negation",
    "not": "negation",
    "always": "splitting_or_totalization",
    "everyone": "splitting_or_totalization",
    "nobody": "splitting_or_totalization",
    "should": "superego_demand",
    "must": "superego_demand",
    "need": "demand",
}


def tokenize(text: str) -> list[str]:
    return [m.group(0).lower().replace("’", "'") for m in TOKEN_RE.finditer(text)]


def sentences(text: str) -> list[str]:
    parts = re.split(r"[.!?]+", text)
    return [p.strip() for p in parts if p.strip()]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    src = Path(args.input)
    raw = src.read_text(encoding="utf-8", errors="replace")
    toks = tokenize(raw)
    n = len(toks)
    types = sorted(set(toks))
    v = len(types)
    counts = Counter(toks)
    sents = sentences(raw)
    sent_lens = [len(tokenize(s)) for s in sents] or [0]

    pron = {k: 0 for k in ("first_sing", "first_plur", "second", "third", "it")}
    for t in toks:
        bucket = PRONOUNS.get(t)
        if bucket:
            pron[bucket] += 1

    pos = sum(counts[w] for w in AFFECT_POS)
    neg = sum(counts[w] for w in AFFECT_NEG)
    defenses: dict[str, int] = {}
    for w, label in DEFENSE_MARKERS.items():
        if counts[w]:
            defenses[label] = defenses.get(label, 0) + counts[w]

    hapax = sum(1 for _, c in counts.items() if c == 1)
    top = counts.most_common(25)
    ttr = (v / n) if n else 0.0
    repetition = 1.0 - ttr

    payload = {
        "generated_unix": int(time.time()),
        "source_path": str(src),
        "n_chars": len(raw),
        "n_tokens": n,
        "n_types": v,
        "n_sentences": len(sents),
        "mean_sentence_tokens": sum(sent_lens) / len(sent_lens),
        "type_token_ratio": ttr,
        "repetition_index": repetition,
        "hapax_share": (hapax / v) if v else 0.0,
        "pronouns": pron,
        "pronoun_share": {k: (v_ / n if n else 0.0) for k, v_ in pron.items()},
        "affect_positive_tokens": pos,
        "affect_negative_tokens": neg,
        "affect_ratio_neg_over_pos": (neg / pos) if pos else (None if neg == 0 else "inf"),
        "defense_markers": defenses,
        "top_tokens": [{"token": w, "count": c} for w, c in top],
        "small_n": n < 80,
        "notes": [
            "Word lists are house heuristics, not LIWC and not a clinical instrument.",
            "H0 is genre and rhetoric until two schools converge on one quoted mechanism.",
        ],
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
