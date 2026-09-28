# Locked execution prompt for /list

Copy this block into `scope.md` at the start of a run. Do not drop the flag order. Do not insert any token from `assets/negative-keywords.csv`.

```
/list {{input}} /banner /images /copyright

Iterate targeted search, primary-source reads, and rival-list crosswalks until you compile a deduplicated inventory of every single instance of {{input}}. Close a branch only after two consecutive empty targeted rounds. Do not stop at the first results page. Do not invent instances. Prefer primary PDFs, university-press work, .gov, and .mil.

Then emit the structured catalog.

/banner — one full-bleed left-and-right banner on every body section and every subsection. Zero left margin, zero right margin, zero left padding, zero right padding. Height follows source aspect. Print at full opacity. Do not fade the top edge. Do not fade the bottom edge. Do not fade the left or right edges.

/images — generate each figure at the maximum print size that does not lose quality and does not introduce aliasing, blur, or aspect distortion. Full bleed left and right only when the source bitmap already meets the page-width pixel floor so the print does not upscale, squash, or letterbox.

/copyright — restamp every page with the living centered footer. START defaults to 2012 unless the user typed /copyright YYYY. YEAR is Date.getFullYear on open. Default owner is Web Development Corporation.
```

`{{input}}` is the predicate. Flags after `/list` that the user omitted are still on by default unless the user explicitly said no figures or no footer.

Extra flags the user may add (routing tokens only; do not copy the bare words into a generate prompt)

- `/folio` or `/phd` — emit through the compact report builder after the inventory exists
- `/deep` — emit through the Georgia report builder after the inventory exists
- `/iterate` — extra expansion passes before emit
- `/copyright YYYY` — override START

Do not move `/banner` after `/copyright`. Figures must exist before the footer stamp.
