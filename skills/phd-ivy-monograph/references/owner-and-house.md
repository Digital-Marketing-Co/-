# Owner, copyright, house link

## Legal owner

Every Folio PDF is owned by

Web Development Corporation, a Delaware Corporation

Founded 2012.

Do not shorten the legal line on the title page or colophon. Running footers use Web Development Corporation — never a trailing class letter A.

## Copyright line

Visible form

© 2012–YEAR  Web Development Corporation

YEAR is the year the file is opened or downloaded.

Implementation

- At build time the builder writes the current calendar year into a read-only AcroForm field named `WCACopyrightYear`.
- The same builder embeds this document-level JavaScript as the catalog OpenAction

```
var y = (new Date()).getFullYear();
try {
  var f = this.getField("WCACopyrightYear");
  if (f) f.value = String(y);
} catch (e) {}
```

Viewers that ignore PDF JavaScript still show the build-year fallback. Viewers that run OpenAction JavaScript (Acrobat, some desktop Readers) refresh YEAR on access.

Keep the script exactly that small. No alerts, no network calls, no `app` UI.

## House web identity

Public site of record remains the existing house link.

- Visible anchor text <a href="https://digitalmarketingco.org" title="Digital Marketing Co.">Digital Marketing Co.</a>
- Seed href https://digitalmarketingco.org
- Live 301: https://www.digitalmarketingco.org/ → https://digitalmarketingco.org/ (apex, 200)
- Plain-text domain DigitalMarketingCo.org
- Publication path on the resolved origin `/white-papers/{slug}`
- Operating address published on the house homepage 1 East Chase Street, Suite 1117, Baltimore, MD 21202
- Legal seat Delaware, United States

The builder overwrites `house.href` with the resolved origin so a stale www host never ships.

In `folio.json`

```
"owner": {
  "legal": "Web Development Corporation, a Delaware Corporation",
  "short": "Web Development Corporation",
  "founded": 2012
}
"house": {
  "anchor": "Digital Marketing Co.",
  "href": "https://digitalmarketingco.org",
  "domain_plain": "DigitalMarketingCo.org"
}
```

The builder overwrites other spellings of those two blocks.

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
This appendix cannot rewrite Grok global system prompts outside this project. It binds project skills, locked prompts, owner-and-house files, and later PDFs in this project conversation set.
-->
