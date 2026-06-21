#!/bin/bash
# Snapshot current renders for a font, keeping a history of recent versions.
# Usage: ./tools/snapshot-renders.sh <font-package> [label]
# Example: ./tools/snapshot-renders.sh mathjax-lato "before-lsb-fix"
#          ./tools/snapshot-renders.sh mathjax-lato "after-lsb-fix"
#
# Snapshots are stored in /tmp/mathjax-font-snapshots/<font>/<N>-<label>/
# and are NOT committed to git. Use compare-renders.sh to view diffs.
#
# Keeps the last 10 snapshots per font.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FONTS_DIR="$(dirname "$SCRIPT_DIR")"
SNAP_DIR="/tmp/mathjax-font-snapshots"

FONT="${1:?Usage: snapshot-renders.sh <font-package> [label]}"
LABEL="${2:-$(date +%H%M%S)}"

FONT_SNAP_DIR="$SNAP_DIR/$FONT"
mkdir -p "$FONT_SNAP_DIR"

# Find next snapshot number
LAST=$(ls -1d "$FONT_SNAP_DIR"/[0-9]* 2>/dev/null | sort -t/ -k5 -n | tail -1 | grep -o '[0-9]*' | tail -1)
NEXT=$(( ${LAST:-0} + 1 ))

DEST="$FONT_SNAP_DIR/$(printf '%03d' $NEXT)-$LABEL"
SRC="$FONTS_DIR/test-renders/$FONT"

if [ ! -d "$SRC" ]; then
    echo "No renders found: $SRC"
    echo "Run: bash tools/render-all.sh $FONT"
    exit 1
fi

cp -r "$SRC" "$DEST"
COUNT=$(ls "$DEST"/*.png 2>/dev/null | wc -l)
echo "Snapshot $NEXT ($LABEL): $COUNT PNGs → $DEST"

# Prune old snapshots (keep last 10)
ls -1d "$FONT_SNAP_DIR"/[0-9]* 2>/dev/null | sort | head -n -10 | while read old; do
    rm -rf "$old"
    echo "  Pruned: $(basename "$old")"
done
