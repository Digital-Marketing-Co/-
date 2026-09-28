# Inventory schema

One JSON object per distinguishable item. Save the full list as `inventory.json` in the work directory when a machine-readable copy is useful.

```json
{
  "id": "C3-god-did-it-card",
  "pane": "C3",
  "placement": "right front",
  "name": "printed card",
  "category": "text-plaque",
  "colors": ["white", "black", "blue photograph"],
  "material_guess": "paper or card in a plastic sleeve",
  "size_rel": "small",
  "readable_text": "GOD DID IT!",
  "confidence": "high",
  "notes": "headline in bold caps; small photo of a person under the line"
}
```

Pane labels default to spreadsheet order on the display grid

- columns A B C from left to right
- rows 1 2 3 from top to bottom
- so top-left is A1 and bottom-right is C3

If the container is not a window, say `shelf-2-left` or `table-front-center` instead.

Confidence

- high — shape and class are clear at source resolution
- medium — class is clear, exact identity (which saint, which animal breed) is not
- low — blob, glare, or occlusion; describe geometry rather than forcing a proper name
