# /stack quality profile

## Acceptance

- Distinguish declared, locked, supported stable and canary versions.
- Choose compatible updates using official sources and verify a frozen install, build and smoke test before release.
- Keep the last verified value and date and mark it stale.
- Disclose unknowns and withhold upgrades lacking compatibility evidence.

Run the matching scenarios in `evals/quality-cases.json`. Report what the evidence verifies and label unexecuted checks.
