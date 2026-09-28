# Extraction for /print

`scripts/extract_print.py` fetches the URL, writes `source.html`, then walks the article into `print.json` blocks.

## Keep

- Headline, byline, published date, source name
- Headings h2–h4 in source order
- Body paragraphs and lists in source order
- Block quotes that belong to the article
- Hero / overlay / cover / masthead / banner images
- In-body photographs and figures with their captions
- YouTube (or similar) embeds as a thumbnail plus the iframe title

## Drop

- Site header, nav, footer, menus
- Sidebars, trending, related, recirc, keep-reading cards
- Share, comment, newsletter, subscribe, cookie, paywall, modal
- Ads, sponsor units, adsense, promo, tracking pixels
- Avatars, logos used as chrome, 1x1 pixels, sprites, icons
- Captions that are ads, related, trending, or subscribe

## Banner vs figure

Mark `role: banner` when any of these are true

- First large image on the page, or `og:image` used as the hero
- Parent or class/id matches hero, banner, overlay, cover, masthead, featured, splash
- Image is wider than tall and sits before the first body paragraph

Everything else downloadable is `role: figure`.

## Caption rule

Keep a caption only when it is attached (figcaption, iframe title, or a short alt that names the subject). Empty caption is correct when the source had none. Never invent a credit.

## If extraction is messy

1. Open saved `source.html`
2. Find the real body class or id
3. Edit `print.json` by hand — delete junk blocks, retag leftover card images
4. Then run `build_print_pdf.py`
