#!/usr/bin/env python3
"""Build MathJax font package for Libertinus Serif + Libertinus Math."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from mathjax_font_lib import (
    load_font, get_x_height, extract_italic_corrections, override_integral_ics,
    build_all_variants, write_boilerplate,
    DEFAULT_TEXT_RANGES, DEFAULT_MATH_RANGES, DEFAULT_EXTRA_MATH,
)

# === Font-specific configuration ===

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_NAME = "MathJaxLibertinus"
FONT_ID = "mathjax-libertinus"
CSS_PREFIX = "LIBERT"

FONTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'libertinus')

TEXT_FONTS = {
    'regular':     os.path.join(FONTS_DIR, 'LibertinusSerif-Regular.otf'),
    'bold':        os.path.join(FONTS_DIR, 'LibertinusSerif-Bold.otf'),
    'italic':      os.path.join(FONTS_DIR, 'LibertinusSerif-Italic.otf'),
    'bold_italic': os.path.join(FONTS_DIR, 'LibertinusSerif-BoldItalic.otf'),
}
MATH_FONT = os.path.join(FONTS_DIR, 'LibertinusMath-Regular.otf')

# Libertinus Serif has Greek built in — no middle layer needed
TEXT_RANGES = DEFAULT_TEXT_RANGES
MATH_RANGES = DEFAULT_MATH_RANGES
EXTRA_MATH = DEFAULT_EXTRA_MATH


def main():
    print(f"Building {FONT_ID}...")
    print(f"  Text: Libertinus Serif (R+B+I+BI)")
    print(f"  Math: Libertinus Math")

    # Load fonts
    text_fonts = {k: load_font(v) for k, v in TEXT_FONTS.items()}
    math_font = load_font(MATH_FONT)

    # Auto-calculate x_height
    x_height = get_x_height(text_fonts['regular'])
    print(f"  x_height: {x_height}")

    # Extract italic corrections
    ic_map = extract_italic_corrections(math_font)
    # Libertinus Math ICs should be reasonable, but override integrals just in case
    override_integral_ics(ic_map, normal_val=0.12)

    # Build everything
    build_all_variants(
        output_dir=OUTPUT_DIR,
        text_fonts=text_fonts,
        math_font=math_font,
        text_ranges=TEXT_RANGES,
        math_ranges=MATH_RANGES,
        extra_math=EXTRA_MATH,
        ic_map=ic_map,
        font_name=FONT_NAME,
        font_id=FONT_ID,
        css_prefix=CSS_PREFIX,
        x_height=x_height,
        text_font_paths=TEXT_FONTS,
    )

    # Generate boilerplate (webpack configs, default.js, sre/)
    write_boilerplate(OUTPUT_DIR, FONT_ID, FONT_NAME)

    print(f"Done! Output in {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
