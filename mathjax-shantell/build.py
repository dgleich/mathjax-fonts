#!/usr/bin/env python3
"""Build MathJax font package for Shantell Sans + Source Code Pro Greek + LM Math."""

import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from mathjax_font_lib import (
    load_font, get_x_height, extract_italic_corrections, override_integral_ics,
    build_all_variants, write_boilerplate, instantiate_variable_font,
    build_middle_layer_from_otf,
    DEFAULT_TEXT_RANGES, DEFAULT_MATH_RANGES, DEFAULT_EXTRA_MATH,
)
import re

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_NAME = "MathJaxShantell"
FONT_ID = "mathjax-shantell"
CSS_PREFIX = "SHANTELL"

FONTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'shantell-sans')
SCP_DIR = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'source-code-pro')
LM_MATH = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'lm-math', 'latinmodern-math.otf')

UPRIGHT_VAR = os.path.join(FONTS_DIR, 'ShantellSans[BNCE,INFM,SPAC,wght].ttf')
ITALIC_VAR = os.path.join(FONTS_DIR, 'ShantellSans-Italic[BNCE,INFM,SPAC,wght].ttf')

SCP_UPRIGHT_VAR = os.path.join(SCP_DIR, 'SourceCodePro[wght].ttf')

# Greek ranges for middle layer
GREEK_RANGES = [
    (0x391, 0x3A9),   # Greek capitals
    (0x3B1, 0x3C9),   # Greek lowercase
    (0x3D1, 0x3D6),   # Greek symbols (thetasym, phi, etc.)
    (0x3F0, 0x3F6),   # Greek symbols (kappa, rho, etc.)
]

# Shantell Sans has NO Greek — use Source Code Pro as middle layer
TEXT_RANGES = DEFAULT_TEXT_RANGES
MATH_RANGES = DEFAULT_MATH_RANGES
EXTRA_MATH = DEFAULT_EXTRA_MATH


def main():
    print(f"Building {FONT_ID}...")
    print(f"  Text: Shantell Sans (variable, pinned wght+BNCE+INFM+SPAC)")
    print(f"  Greek: Source Code Pro (middle layer)")
    print(f"  Math: Latin Modern Math")

    # Instantiate Shantell Sans: pin all custom axes to defaults, vary weight
    print("  Instantiating variable fonts...")
    text_fonts = {
        'regular':     instantiate_variable_font(UPRIGHT_VAR, weight=400, BNCE=0, INFM=0, SPAC=0),
        'bold':        instantiate_variable_font(UPRIGHT_VAR, weight=700, BNCE=0, INFM=0, SPAC=0),
        'italic':      instantiate_variable_font(ITALIC_VAR, weight=400, BNCE=0, INFM=0, SPAC=0),
        'bold_italic': instantiate_variable_font(ITALIC_VAR, weight=700, BNCE=0, INFM=0, SPAC=0),
    }
    math_font = load_font(LM_MATH)

    # Save static instances to temp files for WOFF2 generation
    tmpdir = tempfile.mkdtemp(prefix='shantell-static-')
    text_font_paths = {}
    for style, font in text_fonts.items():
        path = os.path.join(tmpdir, f'ShantellSans-{style}.ttf')
        font.save(path)
        text_font_paths[style] = path

    # Build Source Code Pro Greek middle layer
    # Instantiate SCP at regular weight, save to temp, then build middle layer
    print("  Building Source Code Pro Greek middle layer...")
    scp_regular = instantiate_variable_font(SCP_UPRIGHT_VAR, weight=400)
    scp_path = os.path.join(tmpdir, 'SourceCodePro-regular.ttf')
    scp_regular.save(scp_path)
    middle_layer = build_middle_layer_from_otf(scp_path, GREEK_RANGES)
    print(f"    {len(middle_layer)} Greek glyphs from Source Code Pro")

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
        middle_layer_data=middle_layer,
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

    shutil.rmtree(tmpdir, ignore_errors=True)

    write_boilerplate(OUTPUT_DIR, FONT_ID, FONT_NAME)
    print(f"Done! Output in {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
