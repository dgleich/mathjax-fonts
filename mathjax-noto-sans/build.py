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
    
    # Remove basic Latin + Greek from italic.js so MathJax follows smp redirects
    # to normal.js (which has ic from MATH table and proper sk values).
    for variant_file in ['cjs/svg/italic.js', 'cjs/chtml/italic.js']:
        fpath = os.path.join(OUTPUT_DIR, variant_file)
        if not os.path.exists(fpath):
            continue
        with open(fpath) as f:
            vc = f.read()
        before = vc.count('0x')
        for cp in (list(range(0x41, 0x5B)) + list(range(0x61, 0x7B)) +
                   list(range(0x391, 0x3AA)) + list(range(0x3B1, 0x3CA))):
            vc = re.sub(rf'    0x{cp:X}: \[[^\]]+\],?\n', '', vc)
        with open(fpath, 'w') as f:
            f.write(vc)
        after = vc.count('0x')
        if before - after:
            print(f"  Removed {before - after} basic Latin+Greek from {variant_file}")

    # Apply angle-based sk to math italic/bold-italic Greek in normal.js
    import math as _math
    italic_angle = 12.024  # Noto Sans italic angle
    upm = 1000
    xh = 536
    cap = 714
    tan_a = _math.tan(_math.radians(italic_angle))
    sk_factor = 1.3
    sk_lc = round(xh * tan_a / 2 / upm * sk_factor, 4)
    sk_uc = round(cap * tan_a / 2 / upm * sk_factor, 4)
    print(f"  Greek sk: lowercase={sk_lc}, uppercase={sk_uc} (angle={italic_angle}°, {sk_factor}x)")

    _GREEK_SK_RANGES = [
        (0x1D6FC, 25, sk_lc), (0x1D6E2, 25, sk_uc),  # math italic
        (0x1D736, 25, sk_lc), (0x1D71C, 25, sk_uc),  # math bold italic
        (0x1D7AA, 25, sk_lc), (0x1D790, 25, sk_uc),  # sans bold italic
    ]
    for js_subdir in ['cjs/svg', 'cjs/chtml']:
        normal_path = os.path.join(OUTPUT_DIR, js_subdir, 'normal.js')
        if not os.path.exists(normal_path):
            continue
        with open(normal_path) as f:
            content = f.read()
        gcount = 0
        for start_cp, n, sk_val in _GREEK_SK_RANGES:
            for i in range(n):
                cp = start_cp + i
                pattern = rf'0x{cp:X}: \[([^\]]+)\]'
                m = re.search(pattern, content)
                if not m: continue
                entry = m.group(0)
                if 'sk:' in entry:
                    new_entry = re.sub(r'sk: [-\d.]+', f'sk: {sk_val}', entry)
                elif '{ p:' in entry:
                    new_entry = entry.replace('{ p:', f'{{ sk: {sk_val}, p:')
                elif '{ ic:' in entry:
                    new_entry = entry.replace('{ ic:', f'{{ sk: {sk_val}, ic:')
                else: continue
                content = content.replace(entry, new_entry)
                gcount += 1
        with open(normal_path, 'w') as f:
            f.write(content)
        if gcount:
            print(f"  Applied angle-based sk to {gcount} Greek in {js_subdir}/normal.js")

    # Adjust integral widths for better subscript tucking
    adjust_integral_widths(OUTPUT_DIR, smallop_w_ratio=0.80, smallop_ic=0.15, largeop_w_ratio=0.64, largeop_ic=0.37)

    # Clean up temp files
    import shutil
    shutil.rmtree(tmpdir, ignore_errors=True)

    write_boilerplate(OUTPUT_DIR, FONT_ID, FONT_NAME)
    print(f"Done! Output in {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
