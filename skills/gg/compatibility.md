# Case-sensitive compatibility register

- `GENIUS` interactive improvement and `genius` verbatim wrapper: distinct, preserve exact-case dispatch.
- `Final` and `final`: overlapping aliases; retain both source definitions until a tested canonical dispatcher preserves all requirements. Do not silently select by filesystem order.
- `God` and `god`: overlapping orchestration; preserve both until shared-contract reconciliation and regression tests pass.

Case-insensitive filesystems require a collision-safe export mapping. No destructive renames or alias removal. Status: semantic inspection only; runtime dispatch unverified.
