#!/usr/bin/env python3
"""Build MathJax font package for Source Code Pro + Noto Sans Math."""

import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from mathjax_font_lib import (
    load_font, get_x_height, extract_italic_corrections, override_integral_ics,
    build_all_variants, write_boilerplate, adjust_integral_widths, instantiate_variable_font,
    TEXT_RANGES_WITH_GREEK, DEFAULT_MATH_RANGES, DEFAULT_EXTRA_MATH,
)
import re

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_NAME = "MathJaxSourceCode"
FONT_ID = "mathjax-source-code"
CSS_PREFIX = "SRCCODE"

FONTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'source-code-pro')
NOTO_MATH = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'noto-sans', 'NotoSansMath-Regular.ttf')

UPRIGHT_VAR = os.path.join(FONTS_DIR, 'SourceCodePro[wght].ttf')
ITALIC_VAR = os.path.join(FONTS_DIR, 'SourceCodePro-Italic[wght].ttf')

# Source Code Pro has Greek built in — no middle layer needed
# Exclude parens/brackets from text font — monospace versions are too short for math.
# Use math font (Noto Sans Math) versions instead via EXTRA_MATH.
TEXT_RANGES = [
    (0x20, 0x27),     # space through apostrophe (before parens)
    # skip 0x28-0x29 ( )
    (0x2A, 0x2A),     # *
    # skip 0x2B + 0x2C , 0x2D - (use math font for operators)
    (0x2C, 0x2C),     # comma
    (0x2E, 0x2F),     # . /
    (0x30, 0x39),     # digits 0-9
    (0x3A, 0x3B),     # : ;
    # skip 0x3C < 0x3D = 0x3E > (use math font)
    (0x3F, 0x5A),     # ? @ A-Z
    # skip 0x5B [
    (0x5C, 0x5C),     # backslash
    # skip 0x5D ]
    (0x5E, 0x7A),     # ^ through z (before {)
    # skip 0x7B { 0x7C | 0x7D }
    (0x7E, 0x7E),     # tilde
    (0xA0, 0xFF),     # Latin-1 Supplement
    (0x391, 0x3A9),   # Greek capitals
    (0x3B1, 0x3C9),   # Greek lowercase
    (0x3D1, 0x3D6),   # Greek symbols
    (0x3F0, 0x3F6),   # Greek symbols
]
MATH_RANGES = DEFAULT_MATH_RANGES
EXTRA_MATH = (DEFAULT_EXTRA_MATH or []) + [
    0x28, 0x29,   # ( ) — use math font
    0x5B, 0x5D,   # [ ] — use math font
    0x2B, 0x2D,       # + - — use math font
    0x3C, 0x3D, 0x3E, # < = > — use math font
    0x7B, 0x7C, 0x7D, # { | } — use math font
]


def main():
    print(f"Building {FONT_ID}...")
    print(f"  Text: Source Code Pro (variable, pinned wght)")
    print(f"  Math: Noto Sans Math")

    print("  Instantiating variable fonts...")
    text_fonts = {
        'regular':     instantiate_variable_font(UPRIGHT_VAR, weight=400),
        'bold':        instantiate_variable_font(UPRIGHT_VAR, weight=700),
        'italic':      instantiate_variable_font(ITALIC_VAR, weight=400),
        'bold_italic': instantiate_variable_font(ITALIC_VAR, weight=700),
    }
    math_font = load_font(NOTO_MATH)

    tmpdir = tempfile.mkdtemp(prefix='srccode-static-')
    text_font_paths = {}
    for style, font in text_fonts.items():
        path = os.path.join(tmpdir, f'SourceCodePro-{style}.ttf')
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
        greek_from_text=True,
    )

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
    adjust_integral_widths(OUTPUT_DIR, smallop_w_ratio=0.75, smallop_ic=0.15, largeop_w_ratio=0.64, largeop_ic=0.37)

    shutil.rmtree(tmpdir, ignore_errors=True)

    write_boilerplate(OUTPUT_DIR, FONT_ID, FONT_NAME)
    print(f"Done! Output in {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
