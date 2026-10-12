# /format modes

Every short code and long name is case-insensitive. Hyphens, underscores, and spaces inside a long name are ignored when matching.

By default the transformer replaces separator characters (`-`, `_`, `•`, `|`, `~`, `\`, `/`, dashes, and common punctuation) with a single space. Pass any keep flag (`-nstrips`, `-strip`, `-rmsprtrs`, `-remove`, `-rmsprtr`, `--keep`) to leave them in place.

| Canonical | Accepts | Result |
| --- | --- | --- |
| `PC` | `PC`, `Proper`, `Proper Case`, `ProperCase`, `Proper-Case` | First letter of each word uppercase. Remaining letters in that word lowercase. Whitespace and (when kept) punctuation stay put. |
| `UC` | `UC`, `UPPERCASE`, `Upper Case`, `AC`, `All Caps`, `AllCaps`, `Caps` | Every letter uppercase. |
| `LC` | `LC`, `lowercase`, `Lower Case`, `Lower` | Every letter lowercase. |
| `SC` | `SC`, `smallcaps`, `Small Caps`, `SmallCaps`, `small-caps` | First letter of each word a full capital. Remaining letters of that word Unicode small capitals. |
