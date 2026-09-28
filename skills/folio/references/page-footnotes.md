# Page-local Chicago footnotes

Citations that appear on a page print in that page’s footnote band. They do not wait for a collected Notes chapter.

## Contract

- Body paragraphs use `{{n}}` or `{{n, m}}` markers. The builder turns those into superscripts and records which note numbers landed on the page.
- After the page is composed, every distinct note number used on that page is drawn in the footnote band, in numeric order, in Chicago note form from `notes[].text`.
- The footnote band sits above the living copyright line and below the body frame. A short rule separates body from notes.
- A note reprints on every page that cites it. Short form still follows CMOS (full form on first appearance in the document; short form thereafter in `notes[].text` as drafted).
- The bibliography remains a back-matter list in bibliographic form, ordered by first appearance of each work. It is not a substitute for the page footnotes.
- A collected Notes section is optional concordance only. Do not rely on it as the reader’s only access to citations.

## Space

- Reserve enough frame bottom so two to six short notes fit without colliding with the copyright line.
- If the page’s notes overflow the band, the builder tightens leading and point size once, then clips with a “continued on next cited page” marker rather than covering body type.
- Do not let footnote text collide with the house copyright notice or the page number.

## What not to do

- Do not use author-date parentheticals.
- Do not leave a superscript without a matching `notes[].n` entry.
- Do not dump the entire bibliography into the page footer.
- Do not invent page locators.
