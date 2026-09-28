# Section and subsection inventory

`/banner` v1.4 requires one unique banner per printed body heading. Print at full opacity. Do not fade any edge.

## Collect

From `list.json`, `deep.json`, `folio.json`, `atlas.json`, or a user list take every node that will print as a body heading.

Include

- `kind` = `body` at any level
- `level` 1 sections
- `level` 2+ subsections that have their own title

Exclude

- title leaf, contents, abstract-only front matter
- Notes, Bibliography, colophon
- equation figures and variable tables

## Coverage

Parent banner + one banner per child. Example

- 3. Master inventory → `banner-03.png`
- 3.1 Class A → `banner-03-01.png`
- 3.2 Class B → `banner-03-02.png`

Four headings in that family means four generates and four distinct hashes.

## Geometry

- Width = page width (8.5 in at the banner script dpi)
- x = 0
- zero left margin, zero right margin, zero left padding, zero right padding
- height from source aspect
- no fade on top, bottom, left, or right
- every picture pixel stays fully opaque so the trim is ink, not a gutter
