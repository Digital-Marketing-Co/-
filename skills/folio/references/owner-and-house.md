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

- Visible anchor text Digital Marketing Company
- Seed href https://DigitalMarketingCo.org
- Live 301: https://www.DigitalMarketingCo.org/ → https://DigitalMarketingCo.org/ (apex, 200)
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
  "anchor": "Digital Marketing Company",
  "href": "https://DigitalMarketingCo.org",
  "domain_plain": "DigitalMarketingCo.org"
}
```

The builder overwrites other spellings of those two blocks.

## Canonical footer

Render `copyright/SKILL.md` and its canonical notice helper once per page. Do not reproduce independent legal text or calculate years here.
