#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR/rendercv"

shopt -s nullglob
GENERATED=(cv.*.generated.yaml)

if [ ${#GENERATED[@]} -eq 0 ]; then
    echo "No generated files found. Run: python scripts/generate.py" >&2
    exit 1
fi


for INPUT in "${GENERATED[@]}"; do
    VARIANT="${INPUT#cv.}"
    VARIANT="${VARIANT%.generated.yaml}"

    OUTPUT_NAME="$(sed -n 's/^output_name:[[:space:]]*\([^[:space:]#]*\).*/\1/p' "variants/${VARIANT}.yaml")"
    if [ -z "$OUTPUT_NAME" ]; then
        echo "variants/${VARIANT}.yaml has no output_name" >&2
        exit 1
    fi
    BASENAME="rendercv_output/Keeththigan-${OUTPUT_NAME}"

    echo "Rendering ${VARIANT} -> ${BASENAME}.pdf"

    rendercv render "$INPUT" \
        --quiet \
        --typst-path "${BASENAME}.typ" \
        --pdf-path "${BASENAME}.pdf" \
        --markdown-path "${BASENAME}.md" \
        --html-path "${BASENAME}.html" \
        --png-path "${BASENAME}.png"
done
