# Chicago notes and superscript marks

Use CMOS notes-bibliography with the WCA Ivy first-appearance revision. Notes that are cited on a page print in that page’s footer band in Chicago note form. A collected Notes chapter is optional concordance only. Bibliography uses bibliographic form ordered by first appearance of each work. Run `@wca-ivy-biblio/scripts/reorder_citations.py` after any insertion. Display equations carry an ITQE table.

## Body marks

Draft paragraphs may contain `{{n}}` markers.

- One mark: `{{12}}` becomes superscript 12.
- Several marks on the same locus: write `{{12, 15, 18}}` or adjacent `{{12}}{{15}}{{18}}`. The builder emits one superscript run `12, 15, 18` (comma, then space).
- Do not use author-date parentheticals.
- Do not use ibid. across a page break without repeating the short title if the reader would lose the referent; ibid. is allowed only for the immediately previous note.

## Page locators

If a claim rests on pages 14, 17, and 21 of the same work, the note lists 14, 17, and 21. Do not collapse to 14–21 unless the span is continuous and actually read.

## Note form

Book, first citation

`Author First Last, <i>Title</i> (Place: Publisher, year), pages.`

Article

`Author First Last, “Article Title,” <i>Journal</i> volume, no. issue (Year): pages, https://doi.org/...`

Official report

`U.S. Agency, <i>Title</i> (Place: Agency, year), pages, URL.`

Short form

`Last, <i>Short Title</i>, pages.`

## Bibliography form

`Last, First. <i>Title</i>. Place: Publisher, year.`

Do not number bibliographic entries. Do not alphabetize as the house sort. Markup allowed in JSON: `i`, `em`, `b`, `sup`, `a href="..."`.
