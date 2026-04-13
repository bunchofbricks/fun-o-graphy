#!/usr/bin/env python3
"""Convert cities/*.md markdown tables to map/cities.geojson."""

import json
import re
from pathlib import Path

CITIES_DIR = Path("cities")
OUTPUT_FILE = Path("map/cities.geojson")

features = []

for md_file in sorted(CITIES_DIR.glob("*.md")):
    category = md_file.stem  # filename without .md → used as category

    for line in md_file.read_text(encoding="utf-8").splitlines():
        # Skip header and separator rows
        if not line.startswith("|") or re.match(r"^\|[-:| ]+\|$", line):
            continue

        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 3 or cols[0].lower() == "city":
            continue

        name, lon, lat = cols[0], cols[1], cols[2]

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(lat), float(lon)],
            },
            "properties": {
                "name": name,
                "category": category,
                "visible": True,
            },
        })

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.write_text(
    json.dumps({"type": "FeatureCollection", "features": features}, indent=2),
    encoding="utf-8",
)

print(f"Wrote {len(features)} features to {OUTPUT_FILE}")
