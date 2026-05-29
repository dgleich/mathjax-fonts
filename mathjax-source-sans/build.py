#!/usr/bin/env python3
"""Build MathJax font package for Source Sans 3 + Noto Sans Math."""

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
FONT_NAME = "MathJaxSourceSans"
FONT_ID = "mathjax-source-sans"
CSS_PREFIX = "SRCSANS"

FONTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'source-sans')
NOTO_MATH = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'noto-sans', 'NotoSansMath-Regular.ttf')

UPRIGHT_VAR = os.path.join(FONTS_DIR, 'SourceSans3[wght].ttf')
ITALIC_VAR = os.path.join(FONTS_DIR, 'SourceSans3-Italic[wght].ttf')

# Source Sans 3 has Greek built in — no middle layer needed
TEXT_RANGES = TEXT_RANGES_WITH_GREEK
MATH_RANGES = DEFAULT_MATH_RANGES
EXTRA_MATH = DEFAULT_EXTRA_MATH


def main():
    print(f"Building {FONT_ID}...")
    print(f"  Text: Source Sans 3 (variable, pinned wght)")
    print(f"  Math: Noto Sans Math")

    print("  Instantiating variable fonts...")
    text_fonts = {
        'regular':     instantiate_variable_font(UPRIGHT_VAR, weight=400),
        'bold':        instantiate_variable_font(UPRIGHT_VAR, weight=700),
        'italic':      instantiate_variable_font(ITALIC_VAR, weight=400),
        'bold_italic': instantiate_variable_font(ITALIC_VAR, weight=700),
    }
    math_font = load_font(NOTO_MATH)

    # Save static instances to temp files for WOFF2 generation
    tmpdir = tempfile.mkdtemp(prefix='srcsans-static-')
    text_font_paths = {}
    for style, font in text_fonts.items():
        path = os.path.join(tmpdir, f'SourceSans3-{style}.ttf')
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
    adjust_integral_widths(OUTPUT_DIR, smallop_w_ratio=0.75, smallop_ic=0.15, largeop_w_ratio=0.64, largeop_ic=0.37)

    shutil.rmtree(tmpdir, ignore_errors=True)

    # --- Post-build fixes ---

    # 1. Re-apply ic from MATH table (greek_from_text drops them)
    for js_subdir in ['cjs/svg', 'cjs/chtml']:
        np = os.path.join(OUTPUT_DIR, js_subdir, 'normal.js')
        if not os.path.exists(np): continue
        with open(np) as f: content = f.read()
        ct = 0
        for cp, ic_val in ic_map.items():
            if ic_val == 0: continue
            m = re.search(rf'0x{cp:X}: \[([^\]]+)\]', content)
            if not m: continue
            entry = m.group(0)
            if 'ic:' in entry: continue
            if '{ sk:' in entry: content = content.replace(entry, entry.replace('{ sk:', f'{{ ic: {ic_val}, sk:'))
            elif '{ p:' in entry: content = content.replace(entry, entry.replace('{ p:', f'{{ ic: {ic_val}, p:'))
            else: continue
            ct += 1
        with open(np, 'w') as f: f.write(content)
        if ct: print(f"  Re-applied {ct} ic in {js_subdir}/normal.js")

    # 2. Remove basic Latin+Greek from italic.js (smp redirect fix)
    for variant_file in ['cjs/svg/italic.js', 'cjs/chtml/italic.js']:
        fpath = os.path.join(OUTPUT_DIR, variant_file)
        if not os.path.exists(fpath): continue
        with open(fpath) as f: vc = f.read()
        for cp in (list(range(0x41, 0x5B)) + list(range(0x61, 0x7B)) +
                   list(range(0x391, 0x3AA)) + list(range(0x3B1, 0x3CA))):
            vc = re.sub(rf'    0x{cp:X}: \[[^\]]+\],?\n', '', vc)
        with open(fpath, 'w') as f: f.write(vc)

    # 3. Greek sk (angle-based, 1.3x)
    import math as _math
    _angle = 12.0  # Source Sans italic angle
    _tan = _math.tan(_math.radians(_angle))
    _xh = 486; _cap = 660
    _sk_lc = round(_xh * _tan / 2 / 1000 * 1.3, 4)
    _sk_uc = round(_cap * _tan / 2 / 1000 * 1.3, 4)
    for js_subdir in ['cjs/svg', 'cjs/chtml']:
        np = os.path.join(OUTPUT_DIR, js_subdir, 'normal.js')
        if not os.path.exists(np): continue
        with open(np) as f: content = f.read()
        for s, n, sk in [(0x1D6FC,25,_sk_lc),(0x1D6E2,25,_sk_uc),(0x1D736,25,_sk_lc),
                          (0x1D71C,25,_sk_uc),(0x1D7AA,25,_sk_lc),(0x1D790,25,_sk_uc)]:
            for j in range(n):
                cp = s + j
                m = re.search(rf'0x{cp:X}: \[([^\]]+)\]', content)
                if not m: continue
                e = m.group(0)
                if 'sk:' in e: content = content.replace(e, re.sub(r'sk: [-\d.]+', f'sk: {sk}', e))
                elif '{ p:' in e: content = content.replace(e, e.replace('{ p:', f'{{ sk: {sk}, p:'))
                elif '{ ic:' in e: content = content.replace(e, e.replace('{ ic:', f'{{ sk: {sk}, ic:'))
        with open(np, 'w') as f: f.write(content)

    # 4. Wire calligraphic in svg.js
    svg_js = os.path.join(OUTPUT_DIR, 'cjs/svg.js')
    with open(svg_js) as f: sjs = f.read()
    if 'tex_calligraphic' not in sjs:
        sjs = sjs.replace(
            'var delimiters_js_1 = require("./svg/delimiters.js");',
            'var tex_calligraphic_js_1 = require("./svg/tex-calligraphic.js");\n'
            'var tex_calligraphic_bold_js_1 = require("./svg/tex-calligraphic-bold.js");\n'
            'var delimiters_js_1 = require("./svg/delimiters.js");')
        sjs = sjs.replace(
            "'-dup': dup_js_1.dup\n    };",
            "'-dup': dup_js_1.dup,\n"
            "        '-tex-calligraphic': tex_calligraphic_js_1.texCalligraphic,\n"
            "        '-tex-bold-calligraphic': tex_calligraphic_bold_js_1.texCalligraphicBold\n"
            "    };")
        sjs = sjs.replace(
            "'-dup': 'D'\n    };",
            "'-dup': 'D',\n"
            "        '-tex-calligraphic': 'TC',\n"
            "        '-tex-bold-calligraphic': 'TBC'\n"
            "    };")
        with open(svg_js, 'w') as f: f.write(sjs)
        print("  Wired calligraphic in svg.js")

    # 5. Script dupe removal
    _SCRIPT_CPS = list(range(0x1D49C, 0x1D504))
    _LETTERLIKE = [0x212C, 0x2130, 0x2131, 0x210B, 0x2110, 0x2112, 0x2133, 0x211B, 0x212F, 0x210A, 0x2134]
    for variant in ['bold.js', 'italic.js', 'bold-italic.js']:
        for js_subdir in ['cjs/svg', 'cjs/chtml']:
            fpath = os.path.join(OUTPUT_DIR, js_subdir, variant)
            if not os.path.exists(fpath): continue
            with open(fpath) as f: content = f.read()
            for cp in _SCRIPT_CPS + _LETTERLIKE:
                content = re.sub(rf'    0x{cp:X}: \[[^\]]+\],?\n', '', content)
            with open(fpath, 'w') as f: f.write(content)

    print("  All post-build fixes applied")

    write_boilerplate(OUTPUT_DIR, FONT_ID, FONT_NAME)
    print(f"Done! Output in {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
