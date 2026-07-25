#!/usr/bin/env python3

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "rendercv"

# Order matters
FILES = [
    "locale.yaml",
    "settings.yaml",
    "cv.yaml"
    "design.yaml",
]

merged = {}

# Merge top-level files
for filename in FILES:
    path = SRC / filename
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if data:
                merged.update(data)



output = SRC / "cv.generated.yaml"

with open(output, "w", encoding="utf-8") as f:
    yaml.dump(
        merged,
        f,
        sort_keys=False,
        allow_unicode=True,
    )

print(f"Generated {output}")