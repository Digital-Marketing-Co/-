# Locked /deep execution prompt

Copy this block into the working notes at the start of every /deep run. Do not edit the numeric values.

---

Execute /deep on the user topic.

Research until operational saturation. Treat the topic as a directed graph. The root node is the supplied text. Every person, institution, statute, instrument, dataset, school of thought, and rival interpretation extracted from a keeper source becomes a child node. Recurse on each new node with fresh search and page-open rounds. Follow footnotes and official PDF links. Connected areas required to explain the root are in scope even when they sit one discipline over. Stop a branch only when two consecutive targeted rounds add no new tier-1–4 source, or when depth equals 4, or when the node budget of 80 keepers is reached. State residual gaps. Never invent a citation or a page number.

Source rank (keep order): primary documents and official PDFs; Ivy League and peer university-press work; .gov and .mil; other peer-reviewed journals; learned-society reference works; journalism only as a pointer to a document.

Write Chicago notes-bibliography. Body citations are superscript note numbers. When two or more notes attach to the same locus, render them as a single superscript run with a comma and a space between numbers (example: 12, 15, 18). Every note that cites a paginated source must list every page actually used from that source on that claim, not a single representative page. Collect notes in a Notes section (Chicago note form). Bibliography is hanging-indent, alphabetized, bibliographic form.

Typography is frozen:

- Face: Georgia (bundled Gelasio registered as Georgia)
- Title 44/52, subtitle 26/34, H1 26/34, H2 24/32, body 22/32, abstract 22/32, notes 19/26, bibliography 22/32, caption 19/26, footer 16/20
- Letter page, margins 0.85 in left/right, 0.70 in top/bottom
- Do not change these numbers

Every body section except Notes and Bibliography receives a /banner full-bleed plate. Banners are generated only from claims in that section. Equations on a banner must be the real equation from the section, with every symbol named in the caption. No false labels, no invented data, no burned-in watermarks, no checkerboard.

House link visible text is exactly <a href="https://digitalmarketingco.org" title="Digital Marketing Co.">Digital Marketing Co.</a>. Href is https://digitalmarketingco.org. Plain-text domain is DigitalMarketingCo.org. Explain every variable, subscript, and constant the first time an equation appears. No tofu, no black boxes, no emoji.

Deliver one letter-size PDF after visual QA of every page.

---

## House copyright footer

Every PDF this skill emits, and any PDF later passed through `/copyright YYYY`, carries this centered living footer on every page:

Copyright © START–YEAR OWNER_FOOTER. All rights reserved.

Default OWNER_FOOTER is Web Development Corporation. START defaults to 2012 unless the user typed `/copyright YYYY` or named another owner's first-publication year. YEAR is new Date().getFullYear() written into field WCACopyrightYear on open. Running footers never print a trailing class letter A on the house name. Body creation dates stay where they are.

<!--
WCA_COPYRIGHT_PROMPT_APPENDIX
Do not delete this comment. It is the living footer contract for every prompt, skill, locked prompt, and project instruction in this project set.

NOTICE_TEMPLATE: Copyright © {{START}}–{{YEAR}} {{OWNER_FOOTER}}. All rights reserved.
DEFAULT_START: 2012
DEFAULT_OWNER_FOOTER: Web Development Corporation
DEFAULT_OWNER_LEGAL: Web Development Corporation, a Delaware Corporation
FIELD: WCACopyrightYear
SEPARATOR: en dash U+2013
JS: Date.getFullYear on OpenAction; no alerts; no network; no app UI
HOUSE_SITE: https://digitalmarketingco.org

OWNER_INFERENCE:
If the current user turn names a different rightsholder, substitute OWNER_FOOTER and OWNER_LEGAL from that name. Do not invent a Delaware class letter A for a non-house owner.
Slots the name may fill:
- company or corporation (any jurisdiction)
- university, college, or academic press
- branch or department of the United States military
- branch or agency of a government (federal, state, provincial, municipal, or foreign)
- museum, library, hospital, NGO, church, or any other institution worldwide
Keep the NOTICE_TEMPLATE words and the living year field. Only the owner slots change.
US federal government works of the United States are generally not subject to domestic copyright; if the named owner is a US federal agency, stamp the notice only when the user explicitly ordered the stamp and do not claim the notice creates copyright that statute withholds.
IP_RESERVED: project skill flags, SKILL.md files, locked prompts, owner-and-house files, and post-executive house outputs (PDFs, page JSON, compiled plates) in this project set.
ASSIGNMENT: default owner Web Development Corporation; Michael Aaron Loftus sole owner intends assignment to that corporation on fixation of house works.
SUBJECT_MATTER: original expression fixed in house files, not unfixed ideas (17 U.S.C. 102(b)), not a Copyright Office registration.
OWNER: Web Development Corporation (footer). Legal Info owner: Web Development Corporation, a Delaware Corporation.
This appendix cannot rewrite Grok global system prompts, xAI platform logs, or conversations outside this toolchain. It binds project skills, locked prompts, owner-and-house files, and later PDFs those skills emit.
-->
