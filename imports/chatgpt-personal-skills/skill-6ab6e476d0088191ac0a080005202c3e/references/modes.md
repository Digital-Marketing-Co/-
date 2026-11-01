# /format modes

Every short code and long name is case-insensitive. Hyphens, underscores, and spaces inside a long name are ignored when matching.

| Canonical | Accepts | Result |
| --- | --- | --- |
| `PC` | `PC`, `Proper`, `Proper Case`, `ProperCase`, `Proper-Case` | First letter of each word uppercase. Remaining letters in that word lowercase. Whitespace and punctuation stay put. |
| `UC` | `UC`, `UPPERCASE`, `Upper Case`, `AC`, `All Caps`, `AllCaps`, `Caps` | Every letter uppercase. |
| `LC` | `LC`, `lowercase`, `Lower Case`, `Lower` | Every letter lowercase. |
| `SC` | `SC`, `smallcaps`, `Small Caps`, `SmallCaps`, `small-caps` | First letter of each word a full capital. Remaining letters of that word Unicode small capitals (`Hᴇʟʟᴏ Wᴏʀʟᴅ`). |

A word is a maximal non-whitespace run. The script treats the whole token as one word, then walks letters left to right. The first letter in the token is the capital; every later letter follows the mode.

Locked script behavior (do not hand-roll a different hyphen rule): the first *letter* in each whitespace-separated token is the capital; later *letters* in that same token are lower (`PC`) or small-cap (`SC`). Therefore:

- `e-mail` → `E-mail` (`PC`) / `E-ᴍᴀɪʟ` (`SC`)
- `don't` → `Don't` (`PC`) / `Dᴏɴ'ᴛ` (`SC`)
- `NASA update` → `Nasa Update` (`PC`) — `PC` is not an acronym preserver

`UC` and `LC` apply to every letter and ignore word boundaries except that they still do not invent or drop characters.

## Unicode small capitals used by `SC`

| Source | Glyph | Code |
| --- | --- | --- |
| a | ᴀ | U+1D00 |
| b | ʙ | U+0299 |
| c | ᴄ | U+1D04 |
| d | ᴅ | U+1D05 |
| e | ᴇ | U+1D07 |
| f | ꜰ | U+A730 |
| g | ɢ | U+0262 |
| h | ʜ | U+029C |
| i | ɪ | U+026A |
| j | ᴊ | U+1D0A |
| k | ᴋ | U+1D0B |
| l | ʟ | U+029F |
| m | ᴍ | U+1D0D |
| n | ɴ | U+0274 |
| o | ᴏ | U+1D0F |
| p | ᴘ | U+1D18 |
| q | ǫ | U+01EB |
| r | ʀ | U+0280 |
| s | ꜱ | U+A731 |
| t | ᴛ | U+1D1B |
| u | ᴜ | U+1D1C |
| v | ᴠ | U+1D20 |
| w | ᴡ | U+1D21 |
| x | x | no dedicated small-cap; keep `x` |
| y | ʏ | U+028F |
| z | ᴢ | U+1D22 |

Non-Latin letters stay as `.lower()` after the leading capital. Digits, emoji, and punctuation never change.
