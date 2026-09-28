# /copysite scope

## In scope

- The start document (HTML or XHTML)
- Stylesheets (`link[rel=stylesheet]`, `@import`, inline `url()`)
- Scripts (`script[src]`, classic and module)
- Images (`img`, `srcset`, `source`, `poster`, CSS `url()`, favicon, apple-touch-icon)
- Fonts (Google Fonts CSS plus the `.woff2` / `.woff` / `.ttf` files it names)
- Audio, video, and track files referenced from markup
- JSON / text / SVG fetched as a static `src` or `href` from the start tree
- Same-origin files referenced from already-downloaded CSS or JS by a literal path ending in a known static extension

## Out of scope

- Server-side POST endpoints, form actions, admin panels
- Authenticated or paywalled app shells
- Infinite calendar / search / pagination crawls
- Binary downloads that are not page requisites (`.zip`, `.exe`, `.dmg`) unless the start URL itself is that file
- Comments widgets, ad networks, and analytics pixels listed below

## Skip hosts (substring match)

Do not enqueue URLs whose host contains any of

- google-analytics.com
- googletagmanager.com
- googlesyndication.com
- doubleclick.net
- googleadservices.com
- facebook.net
- facebook.com
- connect.facebook
- scorecardresearch.com
- quantserve.com
- ads.linkedin
- hotjar.com
- disqus.com
- disquscdn.com
- amazon-adsystem.com
- criteo.com
- taboola.com
- outbrain.com
- casalemedia.com
- pubmatic.com
- openx.net
- rubiconproject.com
- deployads.com
- carbonads.com
- btloader.com

Google Fonts (`fonts.googleapis.com`, `fonts.gstatic.com`) stay in scope. They are type, not ads.

## Limits

| knob | page mode | site mode |
| --- | --- | --- |
| max pages (HTML) | 1 start + 0 extra | 80 |
| max depth | 0 extra HTML | 2 |
| max files | 400 | 800 |
| max bytes | 80 MiB | 160 MiB |
| timeout per request | 25 s | 25 s |

Stop enqueueing when a cap is hit. Still zip whatever arrived.

## Offline rewrite

Saved files keep `host/path` under the output folder. Query strings are stripped from filenames. HTML and CSS references are rewritten to relative paths so opening the start HTML from the zip works for static assets. Third-party skipped hosts are left as original URLs (they will 404 offline; that is intended).
