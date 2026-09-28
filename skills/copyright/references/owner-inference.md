# Owner inference for the living footer

The footer sentence is always

Copyright © START–YEAR OWNER_FOOTER. All rights reserved.

Only START and the two owner slots move. The words Copyright, the © mark, the en dash, All rights reserved, the field name `WCACopyrightYear`, and the OpenAction `Date.getFullYear()` contract stay fixed.

## Default (house)

| Slot | Value |
| --- | --- |
| START | 2012 |
| OWNER_FOOTER | Web Development Corporation |
| OWNER_LEGAL | Web Development Corporation, a Delaware Corporation |

Strip a trailing class letter A from OWNER_FOOTER when the house name is in use. Do not invent that letter for any other owner.

## When the user names someone else

Read the same turn as `/copyright` (or the turn that asked to restamp or to retarget the appendix). If that turn names a rightsholder, fill the slots from the name they typed. Do not guess a founding year. If they typed a year after the flag, that year is START. If they named another owner and typed no year, keep START at 2012 only when they are still talking about house files; otherwise ask once, and if they do not answer use the current calendar year as START so the range does not pretend to a founding date the user never gave.

| User names | OWNER_FOOTER | OWNER_LEGAL |
| --- | --- | --- |
| A company or corporation | the name they typed, class-letter A stripped only if it is the house name | the name they typed; add jurisdiction only if they supplied it |
| A university, college, or academic press | the name they typed | the name they typed, or the longer legal form if they supplied it (example President and Fellows of Harvard College) |
| A US military branch or department | the name they typed (example United States Navy, Department of the Army) | the same string unless they gave a longer departmental form |
| A government branch or agency anywhere | the name they typed | the same string unless they gave a longer statutory name |
| Any other institution worldwide | the name they typed | the name they typed |

Do not translate the institution into English if they gave it in another language. Do not add Inc., LLC, GmbH, Ltd., or a country suffix the user did not write.

## What inference is not

- It is not a search for the "real" legal owner behind a nickname.
- It is not a copyright registration.
- It is not a claim that a US federal work is copyrightable. 17 U.S.C. § 105 generally withholds domestic copyright from works of the United States government. If the named owner is a US federal agency or a US military department and the user still ordered the stamp, stamp the line they asked for and do not state that the notice creates a right the statute withholds.
- It cannot rewrite Grok's global system prompt or conversations outside this project.

## Script flags

```bash
python3 /home/workdir/.grok/skills/copyright/scripts/stamp_copyright.py \
  /path/to/source.pdf \
  --start START \
  --owner "OWNER_FOOTER" \
  --legal "OWNER_LEGAL" \
  --out /home/workdir/artifacts/<stem>-copyright.pdf
```
