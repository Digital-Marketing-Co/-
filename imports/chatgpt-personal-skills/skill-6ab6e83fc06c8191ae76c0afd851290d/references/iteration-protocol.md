# Iteration protocol

An iteration is one closed research pass that changes the document. A search query is not an iteration.

## Seed

Iteration 0 writes scope, empty `sources.jsonl`, empty `nodes.jsonl`, and a first outline of research questions. It does not emit a PDF unless the user asked for a stub.

## Expansion operators

Apply these in order inside each later iteration. Skip an operator only when the last two passes already returned empty for it.

1. **Core map** — name the schools, agencies, statutes, datasets, and canonical papers that define the topic set.
2. **Primary PDF harvest** — issuing-body PDFs, Ivy and university-press PDFs, `.gov` / `.mil` / NIH / FDA / CMS / WHO / CDC / VA PDFs. Record the canonical URL, not a scraper mirror.
3. **Node recursion** — every keeper that is required to explain a root becomes a node. Depth cap is 5 from that root. Decorative tangents stay out.
4. **Quantitative lift** — every rate, identity, estimator, constraint, or scored inventory the new claims support becomes a planned equation plus ITQE rows. Do not leave a quantitative sentence as prose only.
5. **Rival and revision** — search the named objection, the later statute, the erratum, the Cochrane or NAS review, the minority report.
6. **Gap register** — write what is still closed-access, unpublished at the needed grain, or internally contradictory. Do not fill a gap with a guessed number.

## Round file

Each iteration writes `rounds/round-NN.md` with

- hole under attack
- queries run (plain language plus any site: filters)
- keepers added (title, year, canonical URL, PDF yes/no)
- claims added or withdrawn
- new equation ids
- temporary note numbers used before remap
- dissent block
- open questions that survive

## Saturation gate

Stop and emit when all of the following hold, or when a cap is hit.

- Every research question in `scope.md` has a chapter or a written withdrawal.
- Two consecutive targeted passes added no keeper and no new claim.
- Every display equation has an ITQE stub with four non-empty columns.
- Every `{{n}}` in the working JSON resolves after remap.
- Open questions that remain are labeled as closed-access, unmeasured, or out of scope rather than as forgotten holes.

Caps that stop infinite recursion

- 8 iterations (12 if `/deep` is stacked)
- 120 keepers
- depth 5 from each root
- two empty consecutive passes on a branch

The user may raise a cap in the prompt. Do not raise a cap silently.

## Intelligence posture (operational, not a title)

On each pass act as if a hostile examiner will read the ledger.

- Prefer the primary instrument over a review that cites it.
- Prefer a later official revision over an early press release.
- State uncertainty in the same sentence as the point estimate.
- Do not treat model fluency as evidence.
- Do not claim hidden knowledge, classified sources, or personal genius.

## Topic sets

When the user names several topics, treat them as roots of one document if they share a research question. Otherwise emit one ledger folder per root and say so in `scope.md`. Do not fuse unrelated roots into one bibliography.
