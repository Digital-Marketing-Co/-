# OG, Twitter, and in-app stills

Every public route this skill writes gets three image slots. Bytes are not shared across routes.

## Slots

| Slot | Size | Path contract |
|---|---|---|
| In-app still / product tile | 1600x900 (16:9) | `public/stills/<slug>.png` |
| Open Graph | 1200x630 | `public/og/<slug>.png` |
| Twitter card | 1200x630 | `public/twitter/<slug>.png` |

Twitter may reuse the OG composition only when the file is a separate write with its own path. Do not point both meta tags at one file if the remainder asked for distinct Twitter card images.

## Meta tags (minimum)

```html
<meta property="og:type" content="website">
<meta property="og:site_name" content="Digital Marketing Company">
<meta property="og:title" content="UNIQUE PAGE TITLE">
<meta property="og:description" content="UNIQUE 150-160 CHAR DESCRIPTION">
<meta property="og:url" content="CANONICAL URL">
<meta property="og:image" content="ABSOLUTE URL TO /public/og/SLUG.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="LITERAL ALT OF THE STILL">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="UNIQUE PAGE TITLE">
<meta name="twitter:description" content="UNIQUE 150-160 CHAR DESCRIPTION">
<meta name="twitter:image" content="ABSOLUTE URL TO /public/twitter/SLUG.png">
<meta name="twitter:image:alt" content="LITERAL ALT OF THE STILL">
```

## Prompt rules for stills

Follow `/home/workdir/.grok/skills/visual-system/references/prompt-engineering.md`.

- Subject lock is the named app or page, not a generic circuit city.
- No baked captions, URLs, or logos unless the brand mark is a real object in the spec.
- Beauty floor — awe-inspiring, razor-sharp subject, volumetric light.
- One unique prompt string per slug.

## Manifest

Write `public/image-manifest.json`

```json
{
  "slug": {
    "still": "public/stills/slug.png",
    "og": "public/og/slug.png",
    "twitter": "public/twitter/slug.png",
    "prompt": "one paragraph",
    "alt": "literal alt"
  }
}
```

If pixels are not generated in this turn, the manifest and prompts still exist so `/images` can fill the paths.
