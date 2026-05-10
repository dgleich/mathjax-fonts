#!/usr/bin/env python3
"""Build MathJax font package for Noto Sans + Noto Sans Math."""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from mathjax_font_lib import (
    load_font, get_x_height, extract_italic_corrections, override_integral_ics,
    build_all_variants, write_boilerplate, adjust_integral_widths, instantiate_variable_font,
    DEFAULT_TEXT_RANGES, DEFAULT_MATH_RANGES, DEFAULT_EXTRA_MATH,
)
import re

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_NAME = "MathJaxNotoSans"
FONT_ID = "mathjax-noto-sans"
CSS_PREFIX = "NOTO"

FONTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'noto-sans')

UPRIGHT_VAR = os.path.join(FONTS_DIR, 'NotoSans[wdth,wght].ttf')
ITALIC_VAR = os.path.join(FONTS_DIR, 'NotoSans-Italic[wdth,wght].ttf')
MATH_FONT_PATH = os.path.join(FONTS_DIR, 'NotoSansMath-Regular.ttf')

# Noto Sans has Greek built in — no middle layer needed
TEXT_RANGES = DEFAULT_TEXT_RANGES
MATH_RANGES = DEFAULT_MATH_RANGES
EXTRA_MATH = DEFAULT_EXTRA_MATH


def main():
    print(f"Building {FONT_ID}...")
    print(f"  Text: Noto Sans (variable, pinned wght+wdth)")
    print(f"  Math: Noto Sans Math")

    # Instantiate variable fonts at specific weights, pin wdth=100
    print("  Instantiating variable fonts...")
    text_fonts = {
        'regular':     instantiate_variable_font(UPRIGHT_VAR, weight=400, width=100),
        'bold':        instantiate_variable_font(UPRIGHT_VAR, weight=700, width=100),
        'italic':      instantiate_variable_font(ITALIC_VAR, weight=400, width=100),
        'bold_italic': instantiate_variable_font(ITALIC_VAR, weight=700, width=100),
    }
    math_font = load_font(MATH_FONT_PATH)

    # Save static instances to temp files for WOFF2 generation
    tmpdir = tempfile.mkdtemp(prefix='noto-static-')
    text_font_paths = {}
    for style, font in text_fonts.items():
        path = os.path.join(tmpdir, f'NotoSans-{style}.ttf')
        font.save(path)
        text_font_paths[style] = path

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
        text_font_paths=text_font_paths,
    )

    # Post-build: adjust overbrace/underbrace label spacing
    for delim_path in [
        os.path.join(OUTPUT_DIR, "cjs/svg/delimiters.js"),
        os.path.join(OUTPUT_DIR, "cjs/chtml/delimiters.js"),
    ]:
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
    print("  Adjusted overbrace/underbrace label spacing (+0.35em)")
    
    # Adjust integral widths for better subscript tucking
    adjust_integral_widths(OUTPUT_DIR)

    # Clean up temp files
    import shutil
    shutil.rmtree(tmpdir, ignore_errors=True)

    write_boilerplate(OUTPUT_DIR, FONT_ID, FONT_NAME)
    print(f"Done! Output in {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
