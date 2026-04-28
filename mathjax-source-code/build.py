#!/usr/bin/env python3
"""Build MathJax font package for Source Code Pro + Latin Modern Math."""

import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from mathjax_font_lib import (
    load_font, get_x_height, extract_italic_corrections, override_integral_ics,
    build_all_variants, write_boilerplate, instantiate_variable_font,
    TEXT_RANGES_WITH_GREEK, DEFAULT_MATH_RANGES, DEFAULT_EXTRA_MATH,
)
import re

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_NAME = "MathJaxSourceCode"
FONT_ID = "mathjax-source-code"
CSS_PREFIX = "SRCCODE"

FONTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'source-code-pro')
LM_MATH = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'lm-math', 'latinmodern-math.otf')

UPRIGHT_VAR = os.path.join(FONTS_DIR, 'SourceCodePro[wght].ttf')
ITALIC_VAR = os.path.join(FONTS_DIR, 'SourceCodePro-Italic[wght].ttf')

# Source Code Pro has Greek built in — no middle layer needed
TEXT_RANGES = TEXT_RANGES_WITH_GREEK
MATH_RANGES = DEFAULT_MATH_RANGES
EXTRA_MATH = DEFAULT_EXTRA_MATH


def main():
    print(f"Building {FONT_ID}...")
    print(f"  Text: Source Code Pro (variable, pinned wght)")
    print(f"  Math: Latin Modern Math")

    print("  Instantiating variable fonts...")
    text_fonts = {
        'regular':     instantiate_variable_font(UPRIGHT_VAR, weight=400),
        'bold':        instantiate_variable_font(UPRIGHT_VAR, weight=700),
        'italic':      instantiate_variable_font(ITALIC_VAR, weight=400),
        'bold_italic': instantiate_variable_font(ITALIC_VAR, weight=700),
    }
    math_font = load_font(LM_MATH)

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

    shutil.rmtree(tmpdir, ignore_errors=True)

    write_boilerplate(OUTPUT_DIR, FONT_ID, FONT_NAME)
    print(f"Done! Output in {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
