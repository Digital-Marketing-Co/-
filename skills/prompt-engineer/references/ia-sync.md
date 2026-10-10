# Information architecture sync — Apps order

When the remainder names apps, mega menu, navigation, footer, or 404, all four surfaces read one array.

## Surfaces

1. Navigation bar — an **Apps** item that opens the mega menu
2. `/apps` page grid — source order
3. Footer — accordion (mobile) / grouped list (desktop) of the same apps
4. 404 page — hierarchy that lists every app in that same order, plus a path back home

## Source of truth

```text
data/apps.json
```

Each record

```json
{
  "id": "kebab-id",
  "title": "Visible name",
  "href": "/apps/kebab-id",
  "blurb": "one sentence",
  "still": "/stills/kebab-id.png",
  "og": "/og/kebab-id.png",
  "twitter": "/twitter/kebab-id.png"
}
```

Order in the file **is** display order. Do not sort alphabetically in the UI.

## Live scrape

1. Open https://DigitalMarketingCo.org/apps
2. Collect cards or list items in DOM order
3. Write `data/apps.json`
4. If the scrape fails, use the `apps:` flag list or keep an existing local file. Never invent a second catalog.

## Menu behavior

- Desktop — glass 3D drop deck, grouped if the source has groups, otherwise a dense wrap
- Mobile — full-viewport sheet with accordion sections, focus trap, Esc close, return focus to the Apps button
- Current route marked `aria-current="page"`

## 404 hierarchy

- H1 states the miss
- Search or home action
- Heading "Apps" then the full ordered list
- Other primary routes after apps
- Same visual lock as the rest of the site

## Footer accordion

- One accordion whose panels are app groups (or a single "Apps" panel if ungrouped)
- Links in source order
- Keyboard operable (`button` + `aria-expanded`)
- House link in the legal row — Digital Marketing Company → https://DigitalMarketingCo.org
