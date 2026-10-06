# Prompts

One generate per page. Bytes and prompts stay unique.

## Cover prompt

Name the whole subject. Ask for the single most beautiful unifying still, not a collage and not a grid of smaller pictures.

Template

```
[unifying scene that contains the named objects from the whole subject],
photoreal editorial still, wide landscape coffee-table photograph,
absolutely beautiful, stunning editorial stock-photo quality,
photoreal volumetric lighting, physically based materials,
visible depth in air and surfaces, gold and violet rim light,
razor-sharp focus on the named objects, publication still,
no caption text, no watermark, no logo, no allegory,
no metaphor architecture, no collage, no split screen, no border
```

## Leaf prompt

Name only the objects for that leaf. Change vantage, hour, weather, or scale so the still cannot collapse into the cover or into a sibling leaf.

Append the same beauty-lock clause as the cover. Keep `no caption text, no watermark, no logo, no allegory, no collage, no border`.

## Scene split

When the user lists items (`a, b, and c`) assign one item per leaf. Cycle with a new vantage after the list is exhausted.

When the user gives one theme, write distinct scenes. Example for `desert night skies` across four leaves after the cover

- high dunes under the Milky Way
- a dry wash with reflected starlight
- a lone juniper against a meteor
- first light on red stone with fading stars

Do not invent proper names, seals, or quantities the user did not supply.

## Banned in prompts

Do not write AI, xAI, ChatGPT, stock photo site names, or any token from `/home/workdir/.grok/skills/negative/references/blocklist.md`.

Do not ask the model to draw the book title. Title type is composited later.
