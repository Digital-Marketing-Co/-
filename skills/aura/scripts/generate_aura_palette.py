#!/usr/bin/env python3
"""Generate a unique radiant aura palette for links and headings."""

import argparse
import json
import random
import sys
from pathlib import Path


NAVY = "#000080"
ELECTRIC_BLUE = ["#00f0ff", "#00bfff", "#1e90ff"]
EMERALD = ["#00ff9f", "#00c853", "#00e676"]
FUTURISTIC = ["#00ffff", "#7df9ff", "#39ff14", "#b026ff", "#ff6b00", "#00ffea"]


def interpolate(c1: str, c2: str, t: float) -> str:
    def hex_to_rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


def generate_palette(seed: int | None = None) -> dict:
    if seed is not None:
        random.seed(seed)
    stops = []
    stops.append(random.choice(ELECTRIC_BLUE))
    stops.append(random.choice(EMERALD))
    # 1–3 unique interpolated extras
    n_extra = random.randint(1, 3)
    for _ in range(n_extra):
        base = random.choice(ELECTRIC_BLUE + EMERALD + FUTURISTIC)
        other = random.choice(FUTURISTIC)
        t = random.uniform(0.25, 0.75)
        stops.append(interpolate(base, other, t))
    # ensure uniqueness
    stops = list(dict.fromkeys(stops))
    return {
        "link_color": NAVY,
        "link_weight": "bold",
        "heading_color": "#0a0a2a",
        "heading_weight": "bold",
        "aura_stops": stops,
        "theme": "Dark Navy / Space Force / Light Air Force",
        "css_fragment": (
            f"a {{ color: {NAVY}; font-weight: bold; "
            f"text-shadow: 0 0 8px {stops[0]}, 0 0 16px {stops[1] if len(stops)>1 else stops[0]}; }}"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()
    pal = generate_palette(args.seed)
    text = json.dumps(pal, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
