---
name: blink
description: Propose memorable Bitly keywords and create a requested custom link when authenticated account access is available. Use for /blink, Bitly links, or custom back-half requests.
---

# Memorable Bitly links

Read [the quality profile](references/quality-profile.md), [the API workflow](references/bitly.md), and `evals/quality-cases.json`.

Run `scripts/blink.py URL` to propose short mnemonic keywords. Proposals are UNVERIFIED; do not call them available, reserved, or created. Preserve the exact destination. Do not fetch private page titles or log credentials.

To create the user-requested keyword, use `scripts/blink.py URL --keyword WORD --create` with BITLY_ACCESS_TOKEN and BITLY_GROUP_GUID supplied through the environment. The helper verifies the API response's destination and keyword. Verify the live redirect separately before saying it redirects correctly. No random hash fallback or account mutation retry after an ambiguous write.

Return the confirmed link and destination when creation succeeds; otherwise give clearly labeled proposals and the exact blocker. Use `interop/SKILL.md` for the single delivery gate. A link task does not require a PDF, equation table, artwork, or footer.
