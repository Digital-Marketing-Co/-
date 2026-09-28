# Locked execution prompt for /global

Copy this block into `scope.md` at the start of a run. Do not drop the flag order. Do not insert any token from `assets/negative-keywords.csv`.

```
/global {{input}} /banner /images /copyright

Compile a country-by-country intelligence report on {{input}}. Discover the natural categories, units, and time grain of the topic. Do not import leftover example taxonomies. Convert every monetary figure to United States dollars and state the FX date. Rank sovereign countries by the single most relevant aggregate variable for {{input}}, descending, unless the user named a different sort key.

For each ranked country write one section that contains a waving national flag, a full-bleed scenic banner of that country, the ranking value with year and source, every relevant subcategory, and a last-12-period series with an electric-blue semi-transparent chart when numbers exist.

Prefer primary statistical agencies, central banks, UN and specialized-agency yearbooks, OECD, IMF, World Bank, Eurostat, .gov, .mil, and university-press work. Do not invent a national total.

/banner — one full-bleed left-and-right banner on every body section and every subsection. Zero left margin, zero right margin, zero left padding, zero right padding. Height follows source aspect. Print at full opacity. Do not fade any edge.

/images — maximum print size without quality loss, aliasing, blur, or aspect distortion.

/copyright — living centered footer. START defaults to 2012 unless the user typed /copyright YYYY. YEAR is Date.getFullYear on open. Default owner is Web Development Corporation.
```

`{{input}}` is the topic. Flags after `/global` that the user omitted are still on by default unless the user explicitly said no figures or no footer.

Extra flags the user may add (routing tokens only; do not copy the bare words into a generate prompt)

- `/folio` or `/phd` — emit through the compact report builder after the dossier exists
- `/deep` — emit through the Georgia report builder after the dossier exists
- `/iterate` — extra expansion passes before emit
- `/copyright YYYY` — override START
- `/itqe` `/latex` — render gate and equation tables

Do not move `/banner` after `/copyright`. Figures must exist before the footer stamp.
