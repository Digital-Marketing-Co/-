# Prompts

Every still is a fresh generate. Landscape. No stock download. No reused path, byte hash, or prompt.

The still is context-locked to the subject. Futuristic light and materials may treat the subject. Do not swap the subject for a generic city, a hologram UI, or a neon grid unless the user asked for those objects.

## Beauty lock

Append to every cover and leaf prompt:

```
futuristic cinematic still of the named objects only, beautiful and inspiring,
publication-grade editorial photograph, photoreal volumetric lighting,
physically based materials, visible depth in air and surfaces,
gold and violet rim light, razor-sharp focus on the named objects,
full-bleed frame with the scene touching every edge, no caption text,
no watermark, no logo, no allegory, no collage, no split screen, no border, no margin
```

Do not write maker names, or any token from `/root/.grok/server-skills/negative/references/blocklist.md`, into a prompt.

Do not ask the model to draw the book title. Title type is composited later.

## Scene split

When the user lists items, assign one item per leaf. After the list is exhausted, cycle with a new vantage, hour, weather, or scale.

When the user gives one theme, write a distinct scene per leaf. Change vantage, hour, weather, named object, or scale. Never repeat a prompt.

Do not invent proper names, seals, or quantities the user did not supply.
