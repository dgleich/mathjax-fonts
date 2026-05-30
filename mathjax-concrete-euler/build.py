#!/usr/bin/env python3
"""Build MathJax font package for CMU Concrete + Euler Math."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from mathjax_font_lib import (
    load_font, get_x_height, extract_italic_corrections, override_integral_ics,
    build_all_variants, write_boilerplate, adjust_integral_widths,
    TEXT_RANGES_WITH_GREEK, DEFAULT_MATH_RANGES, DEFAULT_EXTRA_MATH,
)
import re

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_NAME = "MathJaxConcreteEuler"
FONT_ID = "mathjax-concrete-euler"
CSS_PREFIX = "CONCRETE"

FONTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'concrete')
EULER_MATH = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'euler-math', 'Euler-Math.otf')

TEXT_FONTS = {
    'regular':     os.path.join(FONTS_DIR, 'CMUConcrete-Roman.otf'),
    'bold':        os.path.join(FONTS_DIR, 'CMUConcrete-Bold.otf'),
    'italic':      os.path.join(FONTS_DIR, 'CMUConcrete-Italic.otf'),
    'bold_italic': os.path.join(FONTS_DIR, 'CMUConcrete-BoldItalic.otf'),
}

# CMU Concrete has Greek built in — no middle layer needed
TEXT_RANGES = TEXT_RANGES_WITH_GREEK
MATH_RANGES = DEFAULT_MATH_RANGES
EXTRA_MATH = DEFAULT_EXTRA_MATH


def main():
    print(f"Building {FONT_ID}...")
    print(f"  Text: CMU Concrete (R+B+I+BI)")
    print(f"  Math: Euler Math")

    text_fonts = {k: load_font(v) for k, v in TEXT_FONTS.items()}
    math_font = load_font(EULER_MATH)

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
        greek_from_text=True,
        italic_lsb=0,
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
    adjust_integral_widths(OUTPUT_DIR, smallop_w_ratio=0.80, smallop_ic=0.05, largeop_w_ratio=0.75, largeop_ic=0.13)

    # --- Post-build fixes (must run after build_all_variants) ---

    # 1. Compute and apply ic from CMU Concrete italic glyph overhang.
    #    Euler MATH table has few ic entries (upright font). We compute from
    #    the actual text font's italic glyph bounds instead.
    from fontTools.pens.boundsPen import BoundsPen
    ci = load_font(TEXT_FONTS['italic'])
    ci_gs = ci.getGlyphSet(); ci_cmap = ci.getBestCmap(); ci_upm = ci['head'].unitsPerEm
    concrete_ic = {}
    for cp in list(range(0x41, 0x5B)) + list(range(0x61, 0x7B)):
        gn = ci_cmap.get(cp)
        if not gn: continue
        bp = BoundsPen(ci_gs); ci_gs[gn].draw(bp); b = bp.bounds
        if not b: continue
        overhang = max(0, b[2] - ci_gs[gn].width)
        if overhang > 5:
            concrete_ic[cp] = round(overhang / ci_upm, 3)
    math_ic = {}
    for cp, ic_v in concrete_ic.items():
        if 0x41 <= cp <= 0x5A:
            for base in [0x1D434, 0x1D468, 0x1D608, 0x1D63C]:
                math_ic[base + (cp - 0x41)] = ic_v
        elif 0x61 <= cp <= 0x7A:
            for base in [0x1D44E, 0x1D482, 0x1D622, 0x1D656]:
                math_ic[base + (cp - 0x61)] = ic_v
    for js_subdir in ['cjs/svg', 'cjs/chtml']:
        np = os.path.join(OUTPUT_DIR, js_subdir, 'normal.js')
        if not os.path.exists(np): continue
        with open(np) as f: c = f.read()
        ct = 0
        for mcp, ic_v in math_ic.items():
            m = re.search(rf'0x{mcp:X}: \[([^\]]+)\]', c)
            if not m: continue
            e = m.group(0)
            if 'ic:' in e: ne = re.sub(r'ic: [\d.]+', f'ic: {ic_v}', e)
            elif '{ sk:' in e: ne = e.replace('{ sk:', f'{{ ic: {ic_v}, sk:')
            elif '{ p:' in e: ne = e.replace('{ p:', f'{{ ic: {ic_v}, p:')
            else: continue
            c = c.replace(e, ne); ct += 1
        # Also apply Euler ic for non-Latin (integrals etc), skip upright Greek
        for cp_e, iv in ic_map.items():
            if iv == 0 or cp_e in math_ic: continue
            if 0x391 <= cp_e <= 0x3C9: continue
            m = re.search(rf'0x{cp_e:X}: \[([^\]]+)\]', c)
            if not m: continue
            e = m.group(0)
            if 'ic:' in e: continue
            if '{ sk:' in e: c = c.replace(e, e.replace('{ sk:', f'{{ ic: {iv}, sk:'))
            elif '{ p:' in e: c = c.replace(e, e.replace('{ p:', f'{{ ic: {iv}, p:'))
        # Remove wrongly-applied Euler ic from upright Greek
        for cp_g in list(range(0x391, 0x3AA)) + list(range(0x3B1, 0x3CA)):
            m = re.search(rf'0x{cp_g:X}: \[([^\]]+)\]', c)
            if not m: continue
            e = m.group(0)
            if 'ic:' not in e: continue
            ne = re.sub(r',\s*ic:\s*[\d.]+', '', e)
            ne = re.sub(r'ic:\s*[\d.]+,\s*', '', ne)
            if ne != e: c = c.replace(e, ne)
        with open(np, 'w') as f: f.write(c)
        if ct: print(f"  Applied {ct} concrete-derived ic in {js_subdir}/normal.js")

    # 2. Remove basic Latin+Greek from italic.js (smp redirect fix)
    for variant_file in ['cjs/svg/italic.js', 'cjs/chtml/italic.js']:
        fpath = os.path.join(OUTPUT_DIR, variant_file)
        if not os.path.exists(fpath): continue
        with open(fpath) as f: vc = f.read()
        for cp in (list(range(0x41, 0x5B)) + list(range(0x61, 0x7B)) +
                   list(range(0x391, 0x3AA)) + list(range(0x3B1, 0x3CA))):
            vc = re.sub(rf'    0x{cp:X}: \[[^\]]+\],?\n', '', vc)
        with open(fpath, 'w') as f: f.write(vc)

    # 3. Apply angle-based sk to math italic/bold-italic Greek
    import math as _math
    _angle = 14.04  # CMU Concrete italic angle
    _tan = _math.tan(_math.radians(_angle))
    _xh = 445; _cap = 689
    _sk_lc = round(_xh * _tan / 2 / 1000 * 1.3, 4)
    _sk_uc = round(_cap * _tan / 2 / 1000 * 1.3, 4)
    for js_subdir in ['cjs/svg', 'cjs/chtml']:
        np = os.path.join(OUTPUT_DIR, js_subdir, 'normal.js')
        if not os.path.exists(np): continue
        with open(np) as f: c = f.read()
        for s, n, sk in [(0x1D6FC,25,_sk_lc),(0x1D6E2,25,_sk_uc),(0x1D736,25,_sk_lc),
                          (0x1D71C,25,_sk_uc),(0x1D7AA,25,_sk_lc),(0x1D790,25,_sk_uc)]:
            for j in range(n):
                cp = s + j
                m = re.search(rf'0x{cp:X}: \[([^\]]+)\]', c)
                if not m: continue
                e = m.group(0)
                if 'sk:' in e: c = c.replace(e, re.sub(r'sk: [-\d.]+', f'sk: {sk}', e))
                elif '{ p:' in e: c = c.replace(e, e.replace('{ p:', f'{{ sk: {sk}, p:'))
                elif '{ ic:' in e: c = c.replace(e, e.replace('{ ic:', f'{{ sk: {sk}, ic:'))
        with open(np, 'w') as f: f.write(c)

    # 4. Wire up calligraphic/script variant files in svg.js
    svg_js = os.path.join(OUTPUT_DIR, 'cjs/svg.js')
    with open(svg_js) as f: sjs = f.read()
    if 'tex_calligraphic' not in sjs:
        sjs = sjs.replace(
            'var delimiters_js_1 = require("./svg/delimiters.js");',
            'var tex_calligraphic_js_1 = require("./svg/tex-calligraphic.js");\n'
            'var tex_calligraphic_bold_js_1 = require("./svg/tex-calligraphic-bold.js");\n'
            'var script_js_1 = require("./svg/script.js");\n'
            'var script_bold_js_1 = require("./svg/script-bold.js");\n'
            'var delimiters_js_1 = require("./svg/delimiters.js");')
        sjs = sjs.replace(
            "'-dup': dup_js_1.dup\n    };",
            "'-dup': dup_js_1.dup,\n"
            "        '-tex-calligraphic': tex_calligraphic_js_1.texCalligraphic,\n"
            "        '-tex-bold-calligraphic': tex_calligraphic_bold_js_1.texCalligraphicBold,\n"
            "        'script': script_js_1.script,\n"
            "        'bold-script': script_bold_js_1.scriptBold\n"
            "    };")
        sjs = sjs.replace(
            "'-dup': 'D'\n    };",
            "'-dup': 'D',\n"
            "        '-tex-calligraphic': 'TC',\n"
            "        '-tex-bold-calligraphic': 'TBC',\n"
            "        'script': 'SC',\n"
            "        'bold-script': 'BSC'\n"
            "    };")
        with open(svg_js, 'w') as f: f.write(sjs)
        print("  Wired calligraphic/script variants in svg.js")

    # 5. Remove script dupes from bold/italic/bold-italic
    _SCRIPT_CPS = list(range(0x1D49C, 0x1D504))
    _LETTERLIKE = [0x212C, 0x2130, 0x2131, 0x210B, 0x2110, 0x2112, 0x2133, 0x211B, 0x212F, 0x210A, 0x2134]
    _ALL_SCRIPT = _SCRIPT_CPS + _LETTERLIKE
    for variant in ['bold.js', 'italic.js', 'bold-italic.js']:
        for js_subdir in ['cjs/svg', 'cjs/chtml']:
            fpath = os.path.join(OUTPUT_DIR, js_subdir, variant)
            if not os.path.exists(fpath): continue
            with open(fpath) as f: content = f.read()
            for cp in _ALL_SCRIPT:
                content = re.sub(rf'    0x{cp:X}: \[[^\]]+\],?\n', '', content)
            with open(fpath, 'w') as f: f.write(content)

    print("  All post-build fixes applied")

    write_boilerplate(OUTPUT_DIR, FONT_ID, FONT_NAME)
    print(f"Done! Output in {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
