# Skill drift ledger

## Sync log

| Date | Skill | Direction | Short hash | Change |
|---|---|---|---|---|
| 2026-10-22 | weekday-gather | checked | c3c927b | All 50 installed SKILL.md contents match repo (git blob sha). Atlas negative-keywords.csv local has additional hyphenated gazetteer variants and compound rule (size 13213 vs 12827); banner/scripts/rebuild_document.py repo is newer and more robust. CHANGELOG trailing newline diffs ignored. ChatGPT and Grok should use the repo copy for banner script. No new skill folders. |
| 2026-10-21 | genius | repo-to-hosts | d2cfb76 | Add genius prompt wrapper skill; Grok installed from repo; ChatGPT must re-upload |
| 2026-10-21 | itqe | grok-to-repo | 58328b6 | Push verified newer Grok SKILL.md with v1.5 table wrapping, uniqueness, math immutability, and OWASP LLM01 |
| 2026-10-21 | images | grok-to-repo | 225067f | Restore complete verified Grok images/SKILL.md with shared mandates v3.1 (table wrapping, uniqueness, math immutability, OWASP LLM01); matches installed size 29181 bytes |
| 2026-10-21 | wca-ivy-biblio | grok-to-repo | 8c67cd2 | Replace placeholder with complete verified Grok SKILL.md including shared mandates v1.1 |
| 2026-10-21 | folio | grok-to-repo | 6e4805e | Append shared mandates v3.1 (table wrapping, uniqueness, math immutability, OWASP LLM01) |
| 2026-10-21 | alias | repo-to-hosts | 1c62b0b | Add alias skill for persistent safe skill-name mappings; Grok installed from repo; ChatGPT must re-upload |
| 2026-10-21 | deep | grok-to-repo | 4080793 | Append shared mandates v3.1 (table wrapping, uniqueness, math immutability, OWASP LLM01) |
| 2026-10-21 | images | grok-to-repo | pending | Append shared mandates v3.1 (table wrapping, uniqueness, math immutability, OWASP LLM01) |
| 2026-10-21 | interop | grok-to-repo | f42d1ed | Add shared table wrapping, uniqueness, math immutability, and OWASP LLM01 protections v1.1 |
| 2026-10-21 | itqe | grok-to-repo | pending | Append OWASP LLM01 and shared mandates; expand table and math rules |
| 2026-10-21 | negative | grok-to-repo | f8c3636 | Add OWASP LLM01 and anti-injection sweep v1.1 |
| 2026-10-21 | skill-sync | grok-to-repo | 60a9a59 | Add repository security and OWASP LLM01 protections v3.1 |
| 2026-10-21 | wca-ivy-biblio | grok-to-repo | pending | Append shared mandates v1.1 (table wrapping, uniqueness, math immutability, OWASP LLM01) |
| 2026-10-21 | weekday-gather | checked | 6e4805e | Pushed folio SKILL.md (shared mandates). Pending full push for images, itqe, wca-ivy-biblio (large content). Alias skill installed on Grok from repo. |
| 2026-10-21 | weekday-gather | checked | 4080793 | Pushed deep SKILL.md (shared mandates). Pending full push for folio, images, itqe, wca-ivy-biblio (large content). Pulled repo-newer SKILL.md for article-clip-pdf, atlas, banner, bleed, latex, textbook into Grok install. |
| 2026-10-21 | weekday-gather | checked | f42d1ed | Pushed newer Grok SKILL.md for interop, negative, skill-sync (2026-10-21 shared mandates and OWASP LLM01). Pending full push for deep, folio, images, itqe, wca-ivy-biblio. Repo newer for article-clip-pdf, atlas, banner, bleed, latex, textbook; ChatGPT and Grok should use the repo copy for those. |
| 2026-10-20 | expound | repo-to-hosts | a24d6da | Add expound skill with continuous source and bibliography synchronization; Grok installed from repo; ChatGPT must re-upload |
| 2026-10-20 | wca-ivy-biblio | repo-to-hosts | a6857fb | Enforce continuous citation renumbering and bibliography integrity; Grok installed from repo; ChatGPT must re-upload |
| 2026-10-20 | banner images atlas | grok-to-repo | d4ae576 | Restore complete verified Grok SKILL.md with MASS v4.0 layout/pagination (orphan headings, table keep-together) and multi-filetype rules; replaces placeholders |
| 2026-10-20 | MASS-v4.1 | repo-to-hosts | f44e218 | Add MASS v4.1 universal publishing and output standard (skills/MASS-v4.1-PUBLISHING-STANDARD.md); applies to all output skills |
| 2026-10-20 | banner images atlas | grok-to-repo | pending | MASS v4.0 update: append layout/pagination (orphan headings, table keep-together) and multi-filetype rules to SKILL.md. Local copies are newer and complete. Repo currently has placeholders. Full content push pending large-payload handling. |
| 2026-10-20 | weekday-gather | checked | 3dd0535 | Compared 50 shared skills; no newer Grok SKILL.md, references or scripts to push (sizes match or repo newer per prior ledger and commit time). ChatGPT and Grok should use the repo copy for banner, images, textbook and other flagged skills. |
| 2026-10-19 | negative | grok-to-repo | 287e0cf | Replace placeholder with complete verified Grok blocklist.md (full 29k 2026-10-16 hyphenated compounds and high-signal expansions) |
| 2026-10-19 | negative | grok-to-repo | a38c0be | Restore complete verified Grok blocklist.md (full 2026-10-16 expansions) and skill directory over placeholder |
| 2026-10-19 | negative | grok-to-repo | 9bb3fe3 | Restore full 2026-10-16 hyphenated compounds, high-signal indicators, and detailed humanize rules from verified Grok install; overwrites incomplete historical restore |
| 2026-10-19 | etymology | repo-to-hosts | 37df4f4 | Add etymology v2.0 research skill with evaluations; Grok installed from repo; ChatGPT must re-upload |
| 2026-10-19 | negative | grok-to-repo | 86d00d3 | Expand blocklist with hyphenated compounds and high-signal AI indicators; add humanize function to SKILL.md (v3.2) |
| 2026-10-19 | atlas | grok-to-repo | 86d00d3 | Add hyphenated gazetteer variants and compound rule to negative-keywords.csv |
| 2026-10-19 | banner | repo-to-hosts | 1203a86 | Repo SKILL.md and rebuild_document.py are newer (dense scholarship + host resolver); ChatGPT and Grok should use the repo copy |
| 2026-10-19 | images | repo-to-hosts | b8dfbe9 | Repo SKILL.md is newer (dense scholarship and full-bleed); ChatGPT and Grok should use the repo copy |
| 2026-10-19 | textbook | repo-to-hosts | e9323b9 | Repo SKILL.md is newer (forensic QA, density, ATLAS-EXPAND); ChatGPT and Grok should use the repo copy |
