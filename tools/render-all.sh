#!/bin/bash
# Render all test expressions for all fonts (or specified font)
# Usage: ./render-all.sh [font-package]
# Example: ./render-all.sh mathjax-libertinus
#          ./render-all.sh   (renders all fonts)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FONTS_DIR="$(dirname "$SCRIPT_DIR")"
EXPR_FILE="$SCRIPT_DIR/test-expressions.txt"
OUT_DIR="$FONTS_DIR/test-renders"

if [ -n "$1" ]; then
    FONTS="$1"
else
    FONTS="mathjax-libertinus mathjax-libertinus-sans mathjax-lm-sans mathjax-noto-sans mathjax-source-sans mathjax-source-code mathjax-concrete-euler mathjax-lato mathjax-ptsans mathjax-shantell"
fi

mkdir -p "$OUT_DIR"

for font in $FONTS; do
    echo "=== $font ==="
    font_dir="$OUT_DIR/$font"
    mkdir -p "$font_dir"

    i=0
    while IFS= read -r line; do
        # Skip comments and empty lines
        [[ "$line" =~ ^# ]] && continue
        [[ -z "$line" ]] && continue

        i=$((i + 1))
        padded=$(printf "%03d" $i)
        outfile="$font_dir/${padded}.svg"

        # Run render (suppress output for speed)
        node "$SCRIPT_DIR/render-tex.js" "$font" "$line" "$outfile" 2>/dev/null

        if [ -f "$outfile" ]; then
            echo "  $padded: $line"
        else
            echo "  $padded: FAILED: $line"
        fi
    done < "$EXPR_FILE"

    echo "  Rendered $i expressions to $font_dir/"
    echo ""
done
