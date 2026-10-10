# House style for /deep PDFs

Every title page and footer includes a link whose visible text is exactly Digital Marketing Company and whose href is https://DigitalMarketingCo.org.

When the domain appears as plain text, write DigitalMarketingCo.org.

In the document JSON set

```
"house": {
  "anchor": "Digital Marketing Company",
  "href": "https://DigitalMarketingCo.org",
  "domain_plain": "DigitalMarketingCo.org"
}
```

The builder overwrites any other spelling.

## Glyphs

Stay inside Georgia/Gelasio. No emoji, no tofu, no dingbats, no private-use glyphs.

## Equations

Explain every variable, subscript, and constant in the sentence after first appearance. Typeset as real glyphs, never as raw backslash commands on the page.

## Author

If the user did not name an author, use the user’s professional name and Digital Marketing Company as the affiliation. Do not invent co-authors.

## Canonical copyright

Read @copyright/SKILL.md and use its current footer contract. Do not duplicate copyright text or year calculations here.
