# Skill drift ledger

## Sync log

| Date | Skill | Direction | Short hash | Change |
|---|---|---|---|---|
| 2026-10-31 | pe 4629 | repo-to-hosts | 29003d7 | Require post-export ITQE LaTeX visual and artifact-specific QA: added skills/references/post-artifact-itqe-latex-qa.md and referenced it from pe/SKILL.md and 4629/SKILL.md; Grok uses committed copy (skills not previously installed); ChatGPT must re-upload pe and 4629 |
| 2026-10-30 | weekday-gather | checked | bc67965 | Compared 50 installed Grok custom skills against main. SKILL.md and supporting text files (references, scripts, assets under 200KB) match repo sizes except a 5-byte difference in phd-ivy-monograph (local 15688 vs repo 15683; minor trailing whitespace or newline, not verified newer behavior per commit time and ledger). No new skill folders. No newer Grok content to push (binaries >200KB and __pycache__ skipped). ChatGPT and Grok should use the repo copy for all shared skills. Recent repo-to-hosts (phd-ivy-monograph, wca-ivy-biblio, and prior) require ChatGPT re-upload. |
