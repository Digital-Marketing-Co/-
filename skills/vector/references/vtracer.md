# VTracer settings for posters with small type

Python package `vtracer` (visioncortex). Install from PyPI if missing

```bash
pip install vtracer cairosvg -i https://pypi.org/simple
```

Text-preserving defaults used by `scripts/vectorize.py`

- colormode color
- hierarchical stacked
- mode spline
- filter_speckle 1
- color_precision 8
- layer_difference 8
- corner_threshold 30
- length_threshold 3.0
- max_iterations 10
- splice_threshold 30
- path_precision 3

`filter_speckle 0` plus `mode polygon` keeps more of each serif and also explodes file size. Use that only on a cropped title or on a tile the user named.

Working-raster cap is 5400 px on the long edge so a 3600x5400 poster stays 1-to-1. A 7200x10800 /upscale baseline is downsampled with BOX before tracing unless `--fullres` is set.
