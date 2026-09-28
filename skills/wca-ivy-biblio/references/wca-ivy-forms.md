# WCA Ivy note and bibliography forms

Sentence form is CMOS 17/18 notes-bibliography with the house superscript-run revision already locked in `/folio/references/chicago-folio.md`.

## Superscript runs

Markers `{{12}}` or `{{12, 15, 18}}`. Adjacent marks collapse. The builder prints `12, 15, 18` in one superscript run — comma then space, no trailing comma. Each number links to `note-N`. Page-local footnotes reprint those notes on the cited page.

Do not write (Author Year). Do not use a hyphen between note numbers.

## Note form (`notes[].text`)

Book, first citation

`Author First Last, <i>Title</i> (Place: Publisher, year), pages.`

Article

`Author First Last, “Article Title,” <i>Journal</i> volume, no. issue (Year): pages, https://doi.org/...`

Official report

`U.S. Agency, <i>Title</i> (Place: Agency, year), pages, URL.`

Short form after the first full note for that work

`Last, <i>Short Title</i>, pages.`

Page locators list every page actually used. Do not collapse 14, 17, and 21 to 14–21.

Ibid. is allowed only for the immediately previous note. Prefer the short form.

Optional fields on the note object

- `n` — integer, rewritten by the remapper
- `work_id` — stable slug (`freud-se-14`)
- `biblio` — index into `bibliography[]` before or after remap (the remapper rewrites it)
- `locator` — pages actually used

## Bibliography form (`bibliography[]`)

`Last, First. <i>Title</i>. Place: Publisher, year.`

`Last, First. “Article Title.” <i>Journal</i> volume, no. issue (Year): pages. https://doi.org/...`

Hanging indent is applied by the Folio builder. Do not number these lines. Sort is first appearance of the work, not the alphabet.

An entry may be a string or an object

```json
{"work_id": "freud-se-14", "text": "Freud, Sigmund. <i>The Standard Edition</i>…"}
```

The remapper accepts both.

## Markup the builders accept

`i`, `em`, `b`, `sup`, `a href="..."`.
