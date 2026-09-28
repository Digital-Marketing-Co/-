#!/usr/bin/env python3
"""Closed-corpus statistical and classical-cipher battery for /decode."""
from __future__ import annotations

import argparse
import collections
import json
import math
import re
import zlib
from typing import Any

TOKEN_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")

# Approximate English letter probabilities (case-insensitive, a-z only).
EN_LETTER = {
    "a": 0.08167, "b": 0.01492, "c": 0.02782, "d": 0.04253, "e": 0.12702,
    "f": 0.02228, "g": 0.02015, "h": 0.06094, "i": 0.06966, "j": 0.00153,
    "k": 0.00772, "l": 0.04025, "m": 0.02406, "n": 0.06749, "o": 0.07507,
    "p": 0.01929, "q": 0.00095, "r": 0.05987, "s": 0.06327, "t": 0.09056,
    "u": 0.02758, "v": 0.00978, "w": 0.02360, "x": 0.00150, "y": 0.01974,
    "z": 0.00074,
}


def tokenize(text: str) -> list[str]:
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    return TOKEN_RE.findall(text)


def entropy_from_counts(counts: collections.Counter, n: int) -> float:
    if n <= 0:
        return 0.0
    h = 0.0
    for c in counts.values():
        if c:
            p = c / n
            h -= p * math.log2(p)
    return h


def ols_slope(xs: list[float], ys: list[float]) -> tuple[float, float]:
    n = len(xs)
    if n < 2:
        return float("nan"), float("nan")
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0:
        return float("nan"), float("nan")
    slope = num / den
    intercept = my - slope * mx
    return slope, intercept


def analyze(text: str) -> dict[str, Any]:
    orig = tokenize(text)
    toks = [t.lower() for t in orig]
    n = len(toks)
    freq = collections.Counter(toks)
    v = len(freq)
    spectrum = collections.Counter(freq.values())
    hapax = sorted(w for w, c in freq.items() if c == 1)
    ranked = freq.most_common()

    h1 = entropy_from_counts(freq, n)
    hmax = math.log2(v) if v else 0.0
    redundancy = 1.0 - (h1 / hmax) if hmax else 0.0

    bigrams = list(zip(toks, toks[1:]))
    bc = collections.Counter(bigrams)
    cond_h = 0.0
    if bigrams:
        for (u, w), c in bc.items():
            p_uw = c / len(bigrams)
            p_w_u = c / freq[u]
            if p_w_u > 0:
                cond_h -= p_uw * math.log2(p_w_u)
    mi = h1 - cond_h if bigrams else 0.0

    letters = [ch for t in toks for ch in t if ch.isalpha()]
    lc = collections.Counter(letters)
    ln = len(letters)
    h_let = entropy_from_counts(lc, ln)
    missing_letters = [c for c in "abcdefghijklmnopqrstuvwxyz" if lc[c] == 0]

    # Chi-square vs English on letters that appear plus expected rare letters.
    chi = 0.0
    if ln:
        for ch, p in EN_LETTER.items():
            obs = lc[ch]
            exp = p * ln
            if exp > 0:
                chi += (obs - exp) ** 2 / exp

    # Index of coincidence
    ic = 0.0
    if ln >= 2:
        ic = sum(c * (c - 1) for c in lc.values()) / (ln * (ln - 1))

    # Zipf OLS on ranks with f >= 2
    xs, ys = [], []
    for r, (w, c) in enumerate(ranked, 1):
        if c >= 2:
            xs.append(math.log(r))
            ys.append(math.log(c))
    slope, intercept = ols_slope(xs, ys)
    alpha_hat = -slope if slope == slope else float("nan")

    zipf_outliers = []
    if intercept == intercept and alpha_hat == alpha_hat:
        for r, (w, c) in enumerate(ranked, 1):
            pred = math.exp(intercept) * (r ** (-alpha_hat))
            if pred > 0 and c / pred >= 3.0:
                zipf_outliers.append({"word": w, "rank": r, "count": c, "pred": pred, "ratio": c / pred})

    lengths = [len(w) for w in hapax] if hapax else [0]
    mean_len = sum(len(w) for w in toks) / n if n else 0
    hapax_mean = sum(lengths) / len(lengths) if lengths else 0
    hapax_var = sum((x - hapax_mean) ** 2 for x in lengths) / len(lengths) if lengths else 0
    hapax_sd = math.sqrt(hapax_var)
    long_hapax = [w for w in hapax if len(w) > hapax_mean + 2 * hapax_sd]

    # Change-point: max two-piece unigram loglik
    best_t, best_ll = 1, float("-inf")
    if n >= 20:
        for t in range(10, n - 10):
            left = collections.Counter(toks[:t])
            right = collections.Counter(toks[t:])
            ll = 0.0
            for w, c in left.items():
                ll += c * math.log(c / t)
            for w, c in right.items():
                ll += c * math.log(c / (n - t))
            if ll > best_ll:
                best_ll, best_t = ll, t

    # Compression proxy
    raw = " ".join(toks).encode("utf-8")
    compressed = zlib.compress(raw, 9)
    ratio = len(compressed) / len(raw) if raw else 1.0

    last = toks[-1] if toks else ""
    prev = toks[-2] if n >= 2 else ""
    followers_last = collections.Counter(w for u, w in bigrams if u == last)
    followers_bi = collections.Counter(
        w for (a, b), w in zip(zip(toks, toks[1:]), toks[2:]) if a == prev and b == last
    )

    # Interpolation next-token
    lambdas = (0.5, 0.3, 0.15, 0.05)
    candidates = set(freq) | set(followers_last) | set(followers_bi)
    if not candidates:
        candidates = {"the"}
    scores = {}
    for w in candidates:
        p3 = (followers_bi[w] / sum(followers_bi.values())) if followers_bi else 0.0
        p2 = (followers_last[w] / sum(followers_last.values())) if followers_last else 0.0
        p1 = freq[w] / n if n else 0.0
        p0 = 1.0 / v if v else 0.0
        scores[w] = lambdas[0] * p3 + lambdas[1] * p2 + lambdas[2] * p1 + lambdas[3] * p0
    top = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))[:8]

    first_letters = "".join(t[0] for t in toks)
    capitals = [t for t in orig if t[:1].isupper()]

    # Register split: blessing/health lock
    lock_words = {"stay", "healthy", "safe", "blessed", "keep"}
    lock_idx = next((i for i, w in enumerate(toks) if w == "blessed"), None)

    def pack_counter(c: collections.Counter, k=40):
        return [{"word": w, "count": n_, "p": (n_ / n if n else 0)} for w, n_ in c.most_common(k)]

    return {
        "n_tokens": n,
        "v_types": v,
        "ttr": v / n if n else 0,
        "mean_token_length": mean_len,
        "hapax_count": len(hapax),
        "hapax_rate_of_types": len(hapax) / v if v else 0,
        "hapax": hapax,
        "long_hapax": long_hapax,
        "spectrum": {str(k): spectrum[k] for k in sorted(spectrum)},
        "top_unigrams": pack_counter(freq),
        "h1_bits": h1,
        "hmax_bits": hmax,
        "redundancy": redundancy,
        "perplexity": 2 ** h1 if h1 == h1 else None,
        "h2_conditional_bits": cond_h,
        "mutual_information_adjacent": mi,
        "unique_bigrams": len(bc),
        "top_bigrams": [{"ngram": " ".join(g), "count": c} for g, c in bc.most_common(25)],
        "top_trigrams": [
            {"ngram": " ".join(g), "count": c}
            for g, c in collections.Counter(zip(toks, toks[1:], toks[2:])).most_common(15)
        ],
        "letters_n": ln,
        "h_letter_bits": h_let,
        "letter_ranks": lc.most_common(),
        "missing_letters": missing_letters,
        "chi_square_vs_english": chi,
        "index_of_coincidence": ic,
        "zipf_alpha_ols_f_ge_2": alpha_hat,
        "zipf_log_intercept": intercept,
        "zipf_outliers": zipf_outliers,
        "change_point_index": best_t,
        "change_point_token": toks[best_t] if n > best_t else None,
        "change_point_left_context": toks[max(0, best_t - 4) : best_t + 4] if n else [],
        "blessed_index": lock_idx,
        "lock_mass_after_blessed": (
            sum(1 for w in toks[lock_idx:] if w in lock_words) / (n - lock_idx)
            if lock_idx is not None and n > lock_idx
            else None
        ),
        "zlib_ratio": ratio,
        "ending": toks[-12:],
        "last_token": last,
        "followers_of_last": followers_last.most_common(),
        "trigram_continuations": followers_bi.most_common(),
        "next_token_ranking": [{"word": w, "score": s} for w, s in top],
        "recommended_first_bar": top[0][0] if top else None,
        "first_letters": first_letters,
        "capitalized_originals": capitals,
        "pronouns": {p: freq[p] for p in ["i", "she", "her", "you", "your", "he", "they", "we"]},
        "interpolation_lambdas": list(lambdas),
        "hypothesis": (
            "H0 collapsed predictive-text attractor"
            if (freq.most_common(1) and freq.most_common(1)[0][1] / n > 0.12 and ratio < 0.35)
            else "undecided — inspect tests"
        ),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    with open(args.input, encoding="utf-8") as f:
        text = f.read()
    result = analyze(text)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(json.dumps({k: result[k] for k in [
        "n_tokens", "v_types", "ttr", "h1_bits", "redundancy",
        "recommended_first_bar", "hypothesis", "change_point_index",
        "zipf_alpha_ols_f_ge_2", "chi_square_vs_english", "index_of_coincidence",
        "zlib_ratio", "lock_mass_after_blessed",
    ]}, indent=2))


if __name__ == "__main__":
    main()
