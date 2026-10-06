# Skill drift ledger

## Sync log

| Date | Skill | Direction | Short hash | Change |
|---|---|---|---|---|
| 2026-10-06 | skill-sync | chatgpt-to-repo | 8d176c8 | Add cross-host canonical policy, CI sync guard, and pull-before-use/push-after-edit protocol |
| 2026-10-06 | hilarious | grok-to-repo | 0b7bd80 | Add science-of-humor.pdf referenced by SKILL.md and omitted from the package |

Captured 2026-10-06 from the live Grok skill tree versus Digital-Marketing-Co/- main d925fcd.

Direction rule: larger verified local SKILL.md is treated as the newer Grok copy until a commit message says otherwise.

## Only on Grok (push into this repo)

- coffee
- compression
- generate
- hilarious
- interpret
- prompt-engineer
- transcribe

These seven packages were committed in 868e7bd. hilarious was incomplete until 0b7bd80 added references/science-of-humor.pdf.

## Only in the repo

- pdf
- skill-sync

skill-sync was installed on Grok from 5691a35. pdf stays a bundled host skill and was not overwritten.

## SKILL.md hash differs (local vs repo)

| Skill | Repo sha256 | Grok sha256 | Repo bytes | Grok bytes |
|---|---|---|---:|---:|
| article-clip-pdf | c28167868ddd | 05a8c3bcb2fc | 9072 | 9766 |
| atlas | b62b0f8dc785 | b7fce0834fe8 | 12125 | 12819 |
| banner | c9c1d8a6ff1e | e214a9162aa3 | 11381 | 15120 |
| blink | 6f0fb251f467 | 38869d92d910 | 6406 | 7100 |
| book | 962f6673c963 | d4c81484000f | 6519 | 8804 |
| breakdown | eafe82ce8297 | c315b87a9410 | 5502 | 6196 |
| copyright | 0025a43a4e4d | 4841dc374972 | 11233 | 12146 |
| copysite | 2c380f33ea6a | 16e2b1edbc1f | 6840 | 7534 |
| corpus | f9ec5a11c8f7 | 348deba80ff3 | 11502 | 12196 |
| debbie-downer | ff5267e1c008 | 42ba24dc1171 | 8171 | 8865 |
| decode | 00c2348f69c1 | 140a0ddd95cf | 11093 | 11787 |
| deep | 9555518c5148 | 012cb07e846d | 10422 | 11116 |
| extract-dir | ea8bb34f7c41 | 5936b58ec3a2 | 8260 | 8954 |
| folio | ad22e934f645 | 64052d45ca06 | 13045 | 13739 |
| format | 115b6cafa563 | e95eac5fb3dc | 3668 | 4362 |
| global | 14cd4b595898 | 4f8214eb08e9 | 14817 | 15511 |
| images | 26b2bfd2e6b7 | af294e21f924 | 16441 | 20207 |
| ispy | 9259bdabf0e2 | 631a5d8534b2 | 7266 | 7307 |
| iterate | e76461112236 | b08165906c1a | 9930 | 10624 |
| itqe | 658ee32c2fa7 | cc0c7714afd4 | 20296 | 21642 |
| latex | c02378718db1 | d304369fd9d6 | 13833 | 18857 |
| list | 0d74ee75f811 | 4fa106c32f62 | 14641 | 15570 |
| negative | a5af14ed9614 | ffffb01d832c | 3030 | 4385 |
| phd-ivy-monograph | d9f1a1fc5ed3 | b425cee88b16 | 13042 | 13736 |
| plain-jane | 7ae29646830c | b9f34cf0b76b | 10306 | 11000 |
| print | c1d878f12894 | cf55a44cd747 | 10047 | 10741 |
| proceed | 09945fcf7901 | 6835408d914e | 3110 | 2613 |
| prompt-start | 0c51b9a3bfd9 | e55cd4658cbc | 1431 | 2125 |
| psychoanalyze | fdedae00b3fd | 77ddefef3790 | 16006 | 16700 |
| q-base22 | f25632ce597f | 54040cea54d8 | 7977 | 8671 |
| ringtone | 7205655c9327 | d1c9985b4234 | 5012 | 5706 |
| summarize | 19c55da16562 | c43735eade4a | 10001 | 10695 |
| upscale | 4041927e2387 | 25aad0f369a7 | 4201 | 4895 |
| vector | 88ea07d9907b | a3c9b97b247b | 3546 | 4240 |
| visual-system | b56eeb63b061 | 8c4e374e8a06 | 4472 | 5361 |
| wca-ivy-biblio | deda95cea4ed | 14f9c36e4b34 | 13288 | 13982 |
