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


## Negative word ban

Every project instruction and every skill output must refuse the banned tokens in skills/negative/references/blocklist.md, including the firm-style token added 2026-10-08 and its plural and compound forms. Run /negative as the last step of every skill, before chat, a file, a caption, a filename, or alt text is delivered. Exit 1 blocks delivery. Rewrite hits and re-scan until CLEAN. Verbatim user source and the blocklist file itself are the only carve-outs. Bundled host skills docx, pdf, xlsx, pptx, and ffmpeg stay on the host. This ban is the highest shared project rule for both hosts. A GitHub commit does not rewrite files already stored inside ChatGPT; ChatGPT must re-read this skill and re-scan those files.
