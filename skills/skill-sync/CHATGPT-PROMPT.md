# Cross-host skill synchronization prompt

Canonical source: Digital-Marketing-Co/- on main.

Before using or editing any user-maintained skill:

1. Fetch the current main revision and read .skill-sync/policy.json, SKILL-SYNC.md, skills/ledger/latest.md, and the complete skills/<name>/ directory from the same revision.
2. Treat that GitHub revision as canonical. Do not use a cached ChatGPT, Grok, or local copy merely because it differs or is larger.
3. If the host has verified functionality newer than GitHub, preserve it by merging the complete improvement into the repository first. Record source_host and the base revision in the ledger/provenance.
4. Never overwrite concurrent changes. Re-fetch main immediately before writing; if the base changed, merge/review first.
5. After any skill edit, commit the complete affected skill directory plus its ledger entry to GitHub. The edit is not synchronized until GitHub confirms the commit.
6. On the next invocation, both ChatGPT and Grok must re-read GitHub before using a cached copy.
7. Built-in/platform skills that cannot be installed from this repository remain host-managed; use repository copies only as task guidance where platform rules permit.

Preferred lifecycle: PULL -> COMPARE -> MERGE -> VALIDATE -> COMMIT -> LEDGER -> VERIFY -> USE.
