#!/bin/bash
# Build all font packages: CJS data + webpack bundles (full + nosre)
# Usage: ./tools/build-all.sh [font-package]
# Example: ./tools/build-all.sh mathjax-libertinus
#          ./tools/build-all.sh              (builds all 10)
#          ./tools/build-all.sh --nosre-only (skip CJS + full bundle, just nosre)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FONTS_DIR="$(dirname "$SCRIPT_DIR")"

if [ "$1" = "--nosre-only" ]; then
    NOSRE_ONLY=1
    shift
fi

if [ -n "$1" ]; then
    FONTS="$1"
else
    FONTS="mathjax-libertinus mathjax-libertinus-sans mathjax-lm-sans mathjax-noto-sans mathjax-source-sans mathjax-source-code mathjax-concrete-euler mathjax-shantell mathjax-lato mathjax-ptsans"
fi

# Activate venv if available
for v in "$FONTS_DIR/venv/bin/activate" /work/venv/bin/activate; do
    if [ -f "$v" ]; then source "$v"; break; fi
done

ERRORS=0
for font in $FONTS; do
    echo "=== $font ==="
    font_dir="$FONTS_DIR/$font"

    if [ ! -d "$font_dir" ]; then
        echo "  ERROR: directory not found"
        ERRORS=$((ERRORS + 1))
        continue
    fi

    # Step 1: Build CJS data via build.py
    if [ -z "$NOSRE_ONLY" ]; then
        if [ -f "$font_dir/build.py" ]; then
            echo "  Building CJS (build.py)..."
            python3 "$font_dir/build.py" 2>&1 | tail -1
        fi

        # Step 2: Build full webpack bundle
        if [ -f "$font_dir/build/webpack.config.cjs" ]; then
            echo "  Building webpack bundle..."
            (cd "$font_dir/build" && npx webpack --config webpack.config.cjs 2>&1 | tail -1)
        fi
    fi

    # Step 3: Build nosre webpack bundle
    if [ -f "$font_dir/build/webpack-nosre.config.cjs" ]; then
        echo "  Building nosre bundle..."
        (cd "$font_dir/build" && npx webpack --config webpack-nosre.config.cjs 2>&1 | tail -1)
        nosre=$(ls "$FONTS_DIR"/tex-mml-svg-*${font#mathjax-}*-nosre.js 2>/dev/null | head -1)
        if [ -n "$nosre" ]; then
            sz=$(stat -c%s "$nosre" | numfmt --to=iec 2>/dev/null || stat -c%s "$nosre")
            echo "  OK: $(basename "$nosre") ($sz)"
        else
            echo "  ERROR: nosre bundle not produced"
            ERRORS=$((ERRORS + 1))
        fi
    else
        echo "  SKIP: no webpack-nosre.config.cjs"
    fi
    echo ""
done

echo "Done. Errors: $ERRORS"
exit $ERRORS
