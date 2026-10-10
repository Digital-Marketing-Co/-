# Gazetteer records

`atlas.json` accepts `nodes` and `gazetteer` arrays. Each record requires a stable `id`; optional fields include `name`, `title`, `description`, `variants`, `paragraphs`, `notes`, and `coordinates`. Additional source fields remain in adapted JSON and print as labelled values. Record descriptions and paragraph strings may use the same inline markup and `{{n}}` note markers as body sections.

`coordinates` uses numeric `latitude` in [-90, 90] and `longitude` in [-180, 180]. Supply either a nonempty `source` label or a positive `note` number identifying actual evidence. Coordinates require a document-level `projection` note describing the reference system, units, and applicable limits. The adapter validates ranges and finite numbers; it does not verify location, provenance, datum transformation, map accuracy, or whether note text supports a coordinate. Check those against supplied evidence.

Optional `edges` identify `source` and `target` node IDs plus a `relation`. The adapter checks endpoint membership and unique node IDs. It does not draw a graph or calculate paths. Keep disputed names, period, alternative spellings, source dates, coverage, and uncertainty as explicit supplied fields. Never infer a coordinate from a name.
