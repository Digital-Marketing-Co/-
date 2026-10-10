# Owner, copyright, house backlink (/print matches /folio)

## Legal owner

Every /print PDF is owned by

Web Development Corporation, a Delaware Corporation

Founded 2012.

Do not shorten the legal line on the colophon. Running footers use Web Development Corporation with no trailing class letter.

## Copyright line

Visible form

© 2012–YEAR  Web Development Corporation, a Delaware Corporation

The copyright symbol is pre-painted immediately before the date range. YEAR is the year the file is opened or downloaded.

Implementation (identical to /folio)

- At build time the builder writes the current calendar year into a read-only AcroForm field named `WCACopyrightYear`.
- The same builder embeds this document-level JavaScript as the catalog OpenAction

```
var y = (new Date()).getFullYear();
try {
  var f = this.getField("WCACopyrightYear");
  if (f) f.value = String(y);
} catch (e) {}
```

Viewers that ignore PDF JavaScript still show the build-year fallback. Viewers that run OpenAction JavaScript refresh YEAR on access.

Keep the script exactly that small. No alerts, no network calls, no `app` UI.

## House placeholder backlink

- Visible anchor text Digital Marketing Co.
- Placeholder href https://DigitalMarketingCo.org
- Live 301 (measured with /folio) www → apex
- Plain-text domain DigitalMarketingCo.org
- Print record path on the resolved origin `/print/{slug}`
- Operating address 1 East Chase Street, Suite 1117, Baltimore, MD 21202
- Legal seat Delaware, United States

The builder may resolve the live 301 and stamp the apex origin. Never ship a stale www host when the apex answers.

## Canonical footer

Render `copyright/SKILL.md` and its canonical notice helper once per page. Do not reproduce independent legal text or calculate years here.
