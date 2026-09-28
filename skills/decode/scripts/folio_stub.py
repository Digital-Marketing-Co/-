#!/usr/bin/env python3
"""Emit a WCA Folio JSON stub whose measured numbers match analysis.json.

The agent must still write historiography, notes, and bibliography.
Numeric fields are copied from the battery so they are not re-rounded by hand.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


OWNER = {
    "legal": "Web Development Corporation, a Delaware Corporation",
    "short": "Web Development Corporation",
    "founded": 2012,
}
HOUSE = {
    "anchor": "Digital Marketing Company",
    "href": "https://digitalmarketingco.org",
    "domain_plain": "DigitalMarketingCo.org",
}


def _fmt(x, digits=6):
    if x is None:
        return "not identified"
    if isinstance(x, float):
        if x != x:
            return "not identified"
        return f"{x:.{digits}g}"
    return str(x)


def build_stub(analysis: dict, sample_label: str, today: str) -> dict:
    n = analysis.get("n_tokens")
    v = analysis.get("v_types")
    title = f'Statistical Decode of "{sample_label}"'
    running = "Statistical Decode"
    if len(running) > 40:
        running = running[:37] + "..."
    hyp = analysis.get("hypothesis") or "undecided — inspect tests"
    first_bar = analysis.get("recommended_first_bar") or "(none)"
    return {
        "title": title,
        "subtitle": (
            "Closed-corpus information theory, Zipf diagnostics, "
            "and a classical-cipher battery"
        ),
        "author": "Web Development Corporation Research Desk",
        "date": today,
        "running_title": running,
        "abstract": (
            f"This Folio reports a closed-corpus decode of a sample of "
            f"N = {_fmt(n, 8)} tokens and V = {_fmt(v, 8)} types. "
            f"Unigram entropy H₁ = {_fmt(analysis.get('h1_bits'))} bits, "
            f"redundancy R = {_fmt(analysis.get('redundancy'))}, "
            f"letter entropy = {_fmt(analysis.get('h_letter_bits'))} bits, "
            f"index of coincidence = {_fmt(analysis.get('index_of_coincidence'))}, "
            f"and χ² versus published English letter frequencies = "
            f"{_fmt(analysis.get('chi_square_vs_english'))}. "
            f"The battery hypothesis string is “{hyp}”. "
            f"The interpolated first-bar recommendation on this sample is "
            f"“{first_bar}”. Accept a cipher hypothesis only when two "
            f"independent tests reject chance and a concrete encoding "
            f"reconstructs a second text. Small-n estimators are reported "
            f"with their caveats. Replace this abstract with 150–250 words "
            f"of finished prose before building the PDF."
        ),
        "keywords": [
            "closed corpus",
            "unigram entropy",
            "index of coincidence",
            "Zipf",
            "Good-Turing",
            "next-token interpolation",
            "classical cipher battery",
            "Chicago notes",
        ],
        "owner": OWNER,
        "house": HOUSE,
        "measured": {
            "n_tokens": analysis.get("n_tokens"),
            "v_types": analysis.get("v_types"),
            "ttr": analysis.get("ttr"),
            "h1_bits": analysis.get("h1_bits"),
            "hmax_bits": analysis.get("hmax_bits"),
            "redundancy": analysis.get("redundancy"),
            "perplexity": analysis.get("perplexity"),
            "h2_conditional_bits": analysis.get("h2_conditional_bits"),
            "mutual_information_adjacent": analysis.get(
                "mutual_information_adjacent"
            ),
            "h_letter_bits": analysis.get("h_letter_bits"),
            "letters_n": analysis.get("letters_n"),
            "index_of_coincidence": analysis.get("index_of_coincidence"),
            "chi_square_vs_english": analysis.get("chi_square_vs_english"),
            "zipf_alpha_ols_f_ge_2": analysis.get("zipf_alpha_ols_f_ge_2"),
            "zlib_ratio": analysis.get("zlib_ratio"),
            "recommended_first_bar": analysis.get("recommended_first_bar"),
            "hypothesis": analysis.get("hypothesis"),
            "first_letters": analysis.get("first_letters"),
            "missing_letters": analysis.get("missing_letters"),
        },
        "sections": [
            {
                "id": "intro",
                "title": "I. Introduction and Research Questions",
                "kind": "body",
                "paragraphs": [
                    "Replace this stub. State the closed-corpus rule, the two hypotheses H0 and H1, and four to eight research questions. Cite method notes with {{n}} markers."
                ],
            },
            {
                "id": "historiography",
                "title": "II. Historiography",
                "kind": "body",
                "paragraphs": [
                    "Replace this stub. Situate Shannon 1951, Zipf 1949, Good 1953, and the Friedman index of coincidence. Do not invent page numbers."
                ],
            },
            {
                "id": "method",
                "title": "III. Sources and Method",
                "kind": "body",
                "paragraphs": [
                    "Tokenizer is the battery regex [A-Za-z]+(?:'[A-Za-z]+)?. Logs are base 2. Interpolation lambdas are (0.5, 0.3, 0.15, 0.05) unless analysis.json supplies another set. Accept H1 only when two independent tests reject chance and a concrete encoding reconstructs a second text."
                ],
            },
            {
                "id": "inventory",
                "title": "IV. Inventory and Information Theory",
                "kind": "body",
                "paragraphs": [
                    f"N = {_fmt(n, 8)} tokens. V = {_fmt(v, 8)} types. TTR = {_fmt(analysis.get('ttr'))}. H₁ = {_fmt(analysis.get('h1_bits'))} bits. Hₘₐₓ = {_fmt(analysis.get('hmax_bits'))} bits. R = {_fmt(analysis.get('redundancy'))}. Perplexity = {_fmt(analysis.get('perplexity'))}. H₂ = {_fmt(analysis.get('h2_conditional_bits'))} bits. Adjacent mutual information = {_fmt(analysis.get('mutual_information_adjacent'))} bits. Letter inventory n = {_fmt(analysis.get('letters_n'), 8)} with H_let = {_fmt(analysis.get('h_letter_bits'))} bits. Expand in finished prose. Do not round away JSON digits."
                ],
            },
            {
                "id": "zipf",
                "title": "V. Zipf, Change-Point, and Compression",
                "kind": "body",
                "paragraphs": [
                    f"OLS Zipf alpha on ranks with f ≥ 2 is {_fmt(analysis.get('zipf_alpha_ols_f_ge_2'))}. zlib ratio = {_fmt(analysis.get('zlib_ratio'))}. Change-point index = {_fmt(analysis.get('change_point_index'), 8)}. Report small-n non-identification when the design matrix is empty."
                ],
            },
            {
                "id": "cipher",
                "title": "VI. Cipher Battery and Hypothesis Test",
                "kind": "body",
                "paragraphs": [
                    f"Index of coincidence = {_fmt(analysis.get('index_of_coincidence'))}. Chi-square versus English letter percentages = {_fmt(analysis.get('chi_square_vs_english'))}. First-letter acrostic = {analysis.get('first_letters')!r}. Battery hypothesis string = {hyp!r}. State whether two independent tests rejected chance."
                ],
            },
            {
                "id": "next",
                "title": "VII. Next-Token Recommendation and Device Caveat",
                "kind": "body",
                "paragraphs": [
                    f"Closed-corpus first-bar recommendation is {first_bar!r}. This is not a dump of Apple on-device ranks. An iPhone first bar remains a function of the personal language model, locale, and contacts."
                ],
            },
            {
                "id": "synthesis",
                "title": "VIII. Synthesis",
                "kind": "body",
                "paragraphs": [
                    "Replace this stub. Separate surface-language explanation from any cultural allusion. Do not treat a mashup, film sample, or meme as a cipher unless the letter tests also reject chance."
                ],
            },
            {
                "id": "conclusion",
                "title": "IX. Conclusion and Open Problems",
                "kind": "body",
                "paragraphs": [
                    "Replace this stub. Restate the accepted hypothesis and the estimators that remain unidentified at this N."
                ],
            },
            {
                "id": "notes",
                "title": "Notes",
                "kind": "notes",
                "paragraphs": [],
            },
            {
                "id": "bibliography",
                "title": "Bibliography",
                "kind": "bibliography",
                "paragraphs": [],
            },
        ],
        "notes": [
            {
                "n": 1,
                "text": "Replace with a finished Chicago note. Do not invent a page number.",
            }
        ],
        "bibliography": [
            "Replace with alphabetized Chicago bibliographic entries after the notes are written."
        ],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--label", default="")
    args = ap.parse_args()
    analysis = json.loads(Path(args.analysis).read_text(encoding="utf-8"))
    label = args.label.strip() or "Closed Sample"
    stub = build_stub(analysis, label, date.today().isoformat())
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(stub, indent=2), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
