# Figures

Each body section (not Notes and not Bibliography) gets exactly one generated figure placed after the first two paragraphs of that section. If the section has one paragraph, place the figure after it.

When `/banner` or `/images` is also stacked, those skills own banners and the 500-word extra slots. This file still governs the one in-column monograph figure.

## Prompting

Write the image prompt from that section’s argument and one keeper source.

- Name the real objects the section discusses. Render those objects.
- Photoreal or textbook-accurate. High resolution (at least 2100 px on the long edge).
- No allegory. A nucleus is not a rotunda. A genome is not a library. A nuclease is not an ornamental clamp.
- Add `literal scientific diagram or photoreal model, no captions burned into the image, no watermark, no speech balloons, no private portrait`.
- Orientation `landscape` unless the object is a tall artifact.
- Do not label the image as a scan of a copyrighted plate or as a photograph of a dead person or a classified site.
- Inspect the PNG. Reject mirrored letters, tofu, invented numbers, and metaphors. Regenerate up to three times.

Follow `/home/workdir/.grok/skills/banner/references/literal-plates.md` when that file is present.

## Files

Copy or save the generated PNG to the work folder as `figures/fig-01.png`, `fig-02.png`, and so on. Paths in JSON are relative to the JSON file’s directory or absolute.

Caption form

`Figure 3. Literal reconstruction of [named object] after [Chicago short title]. Generated model, not a scan of the source.`

Attach a `{{n}}` marker when the source is in the note list.

## Checks

After `pdftoppm`, confirm the figure sits with the section whose caption it carries. If a figure drifted to the next chapter, shorten the preceding paragraphs or move the figure field to a later paragraph index (`figure.after_paragraphs`, default 2). Rebuild if the plate is still a metaphor for the heading.
