#!/usr/bin/env python3
"""Build MathJax font package for Libertinus Sans + Libertinus Math."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from mathjax_font_lib import (
    load_font, get_x_height, extract_italic_corrections, override_integral_ics,
    build_all_variants, write_boilerplate, adjust_integral_widths,
    DEFAULT_TEXT_RANGES, DEFAULT_MATH_RANGES, DEFAULT_EXTRA_MATH,
)
import re

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_NAME = "MathJaxLibertinusSans"
FONT_ID = "mathjax-libertinus-sans"
CSS_PREFIX = "LIBSANS"

FONTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'libertinus')

TEXT_FONTS = {
    'regular':     os.path.join(FONTS_DIR, 'LibertinusSans-Regular.otf'),
    'bold':        os.path.join(FONTS_DIR, 'LibertinusSans-Bold.otf'),
    'italic':      os.path.join(FONTS_DIR, 'LibertinusSans-Italic.otf'),
    # No Bold Italic exists — LaTeX package uses Italic + embolden=3
    # For MathJax SVG paths, just use Italic as bold-italic (difference is minimal)
    'bold_italic': os.path.join(FONTS_DIR, 'LibertinusSans-Italic.otf'),
}
MATH_FONT = os.path.join(FONTS_DIR, 'LibertinusMath-Regular.otf')

TEXT_RANGES = DEFAULT_TEXT_RANGES
MATH_RANGES = DEFAULT_MATH_RANGES
EXTRA_MATH = DEFAULT_EXTRA_MATH


def main():
    print(f"Building {FONT_ID}...")
    print(f"  Text: Libertinus Sans (R+B+I, BI=I fallback)")
    print(f"  Math: Libertinus Math")

    text_fonts = {k: load_font(v) for k, v in TEXT_FONTS.items()}
    math_font = load_font(MATH_FONT)

    x_height = get_x_height(text_fonts['regular'])
    print(f"  x_height: {x_height}")

    ic_map = extract_italic_corrections(math_font)
    override_integral_ics(ic_map, normal_val=0)

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

    # Post-build: adjust overbrace/underbrace label spacing
    delim_path = os.path.join(OUTPUT_DIR, "cjs/svg/delimiters.js")
    with open(delim_path) as f:
        dc = f.read()
    dc = re.sub(
        r'(0x23DE: \{[^}]*HDW: \[)([^,]+)',
        lambda m: m.group(1) + str(round(float(m.group(2)) + 0.35, 3)),
        dc
    )
    dc = re.sub(
        r'(0x23DF: \{[^}]*HDW: \[[^,]+, )([^,]+)',
        lambda m: m.group(1) + str(round(float(m.group(2)) + 0.35, 3)),
        dc
    )
    with open(delim_path, 'w') as f:
        f.write(dc)
    chtml_delim_path = os.path.join(OUTPUT_DIR, "cjs/chtml/delimiters.js")
    with open(chtml_delim_path) as f:
        cc = f.read()
    cc = re.sub(
        r'(0x23DE: \{[^}]*HDW: \[)([^,]+)',
        lambda m: m.group(1) + str(round(float(m.group(2)) + 0.35, 3)),
        cc
    )
    cc = re.sub(
        r'(0x23DF: \{[^}]*HDW: \[[^,]+, )([^,]+)',
        lambda m: m.group(1) + str(round(float(m.group(2)) + 0.35, 3)),
        cc
    )
    with open(chtml_delim_path, 'w') as f:
        f.write(cc)
    print("  Adjusted overbrace/underbrace label spacing (+0.35em)")

    # Adjust integral widths for better subscript tucking
    adjust_integral_widths(OUTPUT_DIR, smallop_w_ratio=0.94, largeop_w_ratio=0.82)

    write_boilerplate(OUTPUT_DIR, FONT_ID, FONT_NAME)
    print(f"Done! Output in {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
