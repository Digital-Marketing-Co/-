# Extra formats after /upscale

The PNG baseline is always written. Tokens after the flag add more files from the same upscaled raster.

| Token | File | Use |
| --- | --- | --- |
| png | lossless RGBA/RGB PNG | default vector/tensor baseline |
| tiff | LZW TIFF | print RIP, Photoshop, GIS |
| webp | lossless WebP | smaller lossless transfer |
| npy | NumPy `ndarray` | tensor / numeric graphic |
| pt | `torch.save` tensor | PyTorch tensor graphic |
| svg | SVG wrapper with embedded PNG | container only — not a traced outline |
| pdf | single-page PDF of the raster | print handoff |

Do not claim an SVG from this script is a reconstructed drawing. Dense posters (spectrum charts, infographics) need a dedicated tracer or a redraw. The PNG is the object to trace.

## ImageMagick sandbox

`convert` is capped at 8KP and 64 MP. Destinations larger than 8000 px on an edge must go through the tiled PIL script, not `convert -resize`.
