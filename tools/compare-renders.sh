#!/bin/bash
# Compare render snapshots for a font, generating a side-by-side HTML page.
# Usage: ./tools/compare-renders.sh <font-package> [expression-numbers...]
# Example: ./tools/compare-renders.sh mathjax-lato              (all expressions)
#          ./tools/compare-renders.sh mathjax-lato 009 013 018   (specific ones)
#
# Opens: /tmp/mathjax-font-snapshots/<font>/compare.html

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FONTS_DIR="$(dirname "$SCRIPT_DIR")"
SNAP_DIR="/tmp/mathjax-font-snapshots"

FONT="${1:?Usage: compare-renders.sh <font-package> [expr-numbers...]}"
shift
EXPRS="$@"

FONT_SNAP_DIR="$SNAP_DIR/$FONT"
if [ ! -d "$FONT_SNAP_DIR" ]; then
    echo "No snapshots found for $FONT"
    echo "Run: bash tools/snapshot-renders.sh $FONT <label>"
    exit 1
fi

# Get all snapshots sorted
SNAPS=($(ls -1d "$FONT_SNAP_DIR"/[0-9]* 2>/dev/null | sort))
N=${#SNAPS[@]}
if [ $N -lt 1 ]; then
    echo "No snapshots found"
    exit 1
fi

# If no specific expressions, find all available
if [ -z "$EXPRS" ]; then
    EXPRS=$(ls "${SNAPS[-1]}"/*.png 2>/dev/null | xargs -I{} basename {} .png | sort)
fi

# Read expression labels
declare -A LABELS
i=0
while IFS= read -r line; do
    [[ "$line" =~ ^# ]] && continue
    [[ -z "$line" ]] && continue
    i=$((i + 1))
    LABELS[$(printf '%03d' $i)]="$line"
done < "$FONTS_DIR/tools/test-expressions.txt"

# Generate HTML
OUT="$FONT_SNAP_DIR/compare.html"
cat > "$OUT" << 'HEADER'
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Render Comparison</title>
<style>
body { font-family: -apple-system, sans-serif; margin: 1em; background: #fafafa; }
h1 { font-size: 1.3em; }
.expr { margin: 1.5em 0; background: white; border: 1px solid #ddd; border-radius: 6px; padding: 10px; }
.expr-label { font-family: monospace; font-size: 11px; color: #888; margin-bottom: 6px; }
.snapshots { display: flex; gap: 12px; align-items: flex-end; overflow-x: auto; }
.snap { text-align: center; }
.snap img { height: 50px; border: 1px solid #eee; }
.snap-label { font-size: 10px; color: #666; margin-top: 2px; }
.controls { margin-bottom: 1em; }
.controls button { font-size: 12px; padding: 3px 10px; cursor: pointer; }
</style>
<script>
function setSize(px) {
    document.querySelectorAll('.snap img').forEach(i => i.style.height = px + 'px');
}
</script>
</head><body>
HEADER

echo "<h1>Render Comparison — $FONT ($N snapshots)</h1>" >> "$OUT"
echo '<div class="controls"><strong>Size:</strong> <button onclick="setSize(30)">S</button> <button onclick="setSize(50)">M</button> <button onclick="setSize(80)">L</button> <button onclick="setSize(120)">XL</button></div>' >> "$OUT"

for expr in $EXPRS; do
    label="${LABELS[$expr]:-???}"
    safe_label=$(echo "$label" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')
    echo "<div class=\"expr\">" >> "$OUT"
    echo "  <div class=\"expr-label\">$expr: <code>$safe_label</code></div>" >> "$OUT"
    echo "  <div class=\"snapshots\">" >> "$OUT"
    for snap in "${SNAPS[@]}"; do
        snap_name=$(basename "$snap")
        png="$snap/$expr.png"
        if [ -f "$png" ]; then
            echo "    <div class=\"snap\"><img src=\"$snap_name/$expr.png\"><div class=\"snap-label\">$snap_name</div></div>" >> "$OUT"
        fi
    done
    # Also show current render
    current="$FONTS_DIR/test-renders/$FONT/$expr.png"
    if [ -f "$current" ]; then
        echo "    <div class=\"snap\"><img src=\"../../mathjax-fonts/test-renders/$FONT/$expr.png\" style=\"border-color:#4a9;\"><div class=\"snap-label\" style=\"color:#4a9;\">current</div></div>" >> "$OUT"
    fi
    echo "  </div>" >> "$OUT"
    echo "</div>" >> "$OUT"
done

echo "</body></html>" >> "$OUT"
echo "Compare page: $OUT ($N snapshots, $(echo $EXPRS | wc -w) expressions)"
