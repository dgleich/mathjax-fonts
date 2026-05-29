#!/bin/bash
# Compare current renders against a baseline, report differences.
# Usage: ./diff-renders.sh [baseline-dir] [current-dir]
#
# Workflow:
#   1. Render baseline: ./render-all.sh && cp -r test-renders test-renders-baseline
#   2. Make changes, rebuild fonts
#   3. Re-render: ./render-all.sh
#   4. Diff: ./diff-renders.sh test-renders-baseline test-renders

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FONTS_DIR="$(dirname "$SCRIPT_DIR")"
BASELINE="${1:-$FONTS_DIR/test-renders-baseline}"
CURRENT="${2:-$FONTS_DIR/test-renders}"

if [ ! -d "$BASELINE" ]; then
    echo "Baseline not found: $BASELINE"
    echo "Create it first: cp -r test-renders test-renders-baseline"
    exit 1
fi

# Read expression labels
declare -a LABELS
i=0
while IFS= read -r line; do
    [[ "$line" =~ ^# ]] && continue
    [[ -z "$line" ]] && continue
    i=$((i + 1))
    LABELS[$i]="$line"
done < "$SCRIPT_DIR/test-expressions.txt"

TOTAL=0
CHANGED=0
MISSING=0

for font_dir in "$CURRENT"/mathjax-*; do
    font=$(basename "$font_dir")
    baseline_font="$BASELINE/$font"

    if [ ! -d "$baseline_font" ]; then
        echo "NEW FONT: $font (no baseline)"
        continue
    fi

    font_changes=0
    for svg_file in "$font_dir"/*.svg; do
        num=$(basename "$svg_file" .svg)
        baseline_svg="$baseline_font/$num.svg"
        TOTAL=$((TOTAL + 1))

        if [ ! -f "$baseline_svg" ]; then
            MISSING=$((MISSING + 1))
            continue
        fi

        # Compare SVG content (ignore whitespace differences)
        if ! diff -q <(tr -s '[:space:]' '\n' < "$baseline_svg") \
                      <(tr -s '[:space:]' '\n' < "$svg_file") > /dev/null 2>&1; then
            CHANGED=$((CHANGED + 1))
            font_changes=$((font_changes + 1))
            idx=$((10#$num))
            label="${LABELS[$idx]:-???}"
            echo "  CHANGED: $font/$num — $label"
        fi
    done

    if [ $font_changes -eq 0 ]; then
        echo "  OK: $font (no changes)"
    fi
done

echo ""
echo "Summary: $TOTAL compared, $CHANGED changed, $MISSING missing baseline"

if [ $CHANGED -gt 0 ]; then
    echo ""
    echo "To view changed PNGs:"
    echo "  Baseline: $BASELINE/<font>/<num>.png"
    echo "  Current:  $CURRENT/<font>/<num>.png"
    exit 1
fi
