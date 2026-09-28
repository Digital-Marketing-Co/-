# WCA Folio Chicago notes-bibliography

Base is CMOS 17/18 notes-bibliography. Three house revisions are mandatory.

## Revision 1 — superscript runs

CMOS prefers one note number per locus and puts several sources inside that note, separated by semicolons. WCA Folio also allows several independent note numbers on one locus when the argument actually rests on several numbered notes.

Write markers as `{{12}}` or `{{12, 15, 18}}` (adjacent `{{12}}{{15}}{{18}}` is accepted and collapsed).

The builder emits one superscript run

`12, 15, 18`

Rules the builder enforces

- comma after every number that is not the last number in that run (the comma sits in the same superscript as that number)
- one space after each comma, before the next number
- no trailing comma after the last number
- no space before a comma
- each number is a link to the matching destination on the Notes pages (`note-N`)

Do not write author-date parentheticals. Do not use a hyphen or en-dash between note numbers.

## Revision 2 — notes link forward

Every note number in the Notes section is a named destination `note-N`. If a note cites a work that also appears in the bibliography, keep the usual Chicago note form. Do not print a second number series on bibliography lines.

## Revision 3 — first-appearance order

Note numbers are assigned in reading order and remapped whenever a citation is inserted or deleted. After remap they are exactly `1..N` with no gaps.

A **work** (one bibliography line) is listed once, at the locus of its first note. Full form and later short form of the same book are two notes and one bibliography line. Sort key is first appearance, not the alphabet.

Give notes a stable `work_id` when the same work is cited more than once so the remapper can keep one bibliography line. Run `/home/workdir/.grok/skills/wca-ivy-biblio/scripts/reorder_citations.py` before every Folio build.

## Note form (`notes[].text`)

Book, first citation

`Author First Last, <i>Title</i> (Place: Publisher, year), pages.`

Article

`Author First Last, “Article Title,” <i>Journal</i> volume, no. issue (Year): pages, https://doi.org/...`

Official report

`U.S. Agency, <i>Title</i> (Place: Agency, year), pages, URL.`

Short form after the first full note

`Last, <i>Short Title</i>, pages.`

Page locators list every page actually used. Do not collapse 14, 17, and 21 to 14–21.

Ibid. is allowed only for the immediately previous note. CMOS 18 discourages ibid.; prefer the short form when the previous note is more than a page away.

In the Notes section the number is full size, followed by a period and a space, hanging indent.

## Bibliography form (`bibliography[]`)

`Last, First. <i>Title</i>. Place: Publisher, year.`

`Last, First. “Article Title.” <i>Journal</i> volume, no. issue (Year): pages. https://doi.org/...`

Order by first appearance of the work in the document. Do not alphabetize as the house sort key. Do not number entries. Hanging indent is applied by the builder. String entries and `{work_id, text}` objects are both accepted.

## Markup the builder accepts

`i`, `em`, `b`, `sup`, `a href="..."`.
