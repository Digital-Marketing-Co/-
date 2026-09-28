# Research protocol

One iteration is one closed pass, not one search query.

## Pass skeleton

1. Write three to eight targeted queries from the current gaps file.
2. Search with exact-phrase, registry, scholarly, `.gov`, `.mil`, and rival-list operators.
3. Open the primary page or PDF for every plausible candidate.
4. Accept or reject against the unit of analysis in `scope.md`.
5. Append keepers to `items.jsonl` with identity keys from `dedup.md`.
6. Append sources to `sources.jsonl`. Never invent a page number.
7. Rewrite `gaps.md` with registers still unopened and classes still thin.
8. Stamp the round with `scripts/new_round.py`.

## Source tiers (highest first)

1. Official registers, statutes, gazettes, `.gov`, `.mil`, standards bodies
2. Primary PDFs from Ivy or university presses, National Academies, major journals
3. Catalogs and finding aids that name individual instances
4. Reputable secondary lists used only as leads, never as the last word
5. News and trade pages only when they point to a primary identifier

A secondary list that cannot be confirmed in a primary source stays in `gaps.md`, not in the printed master inventory.

## Empty-round rule

A round is empty when dedup adds zero new keepers.

- Rounds 1–4 stay open even if one of them is empty.
- After round 4, two consecutive empty rounds close the gate.
- Hard cap is 12 rounds or 400 keepers unless the user raised the cap.

Do not call the list complete if a named official register in `gaps.md` was never opened. Mark that register as residual.

## What counts as deep

Deep means the next query is built from a hole in the current list (a missing class, an unopened register, a homonym, a date range). It does not mean repeating the same generic search.

## Fail closed

- No fabricated instance
- No guessed identifier
- No count that cannot be recomputed from `items.jsonl`
- No claim that a paywalled register was read
