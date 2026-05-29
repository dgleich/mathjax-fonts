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
# Exclude parens/brackets/operators from text font — monospace too wide/short for math.
# MUST include modifier accents (0x2C6+) — MathJax uses these for \hat, \tilde, etc.
TEXT_RANGES = [
    (0x20, 0x27),     # space through apostrophe
    # skip 0x28-0x29 ( )
    (0x2A, 0x2A),     # *
    # skip 0x2B + 0x2D -
    (0x2C, 0x2C),     # comma
    (0x2E, 0x2F),     # . /
    (0x30, 0x39),     # digits 0-9
    (0x3A, 0x3B),     # : ;
    # skip 0x3C < 0x3D = 0x3E >
    (0x3F, 0x5A),     # ? @ A-Z
    # skip 0x5B [
    (0x5C, 0x5C),     # backslash
    # skip 0x5D ]
    (0x5E, 0x7A),     # ^ through z
    # skip 0x7B { 0x7C | 0x7D }
    (0x7E, 0x7E),     # tilde
    (0xA0, 0xFF),     # Latin-1 Supplement
    # Modifier accents — CRITICAL for \hat, \tilde, \breve etc.
    (0x2C6, 0x2C6),   # circumflex (hat)
    (0x2C7, 0x2C7),   # caron
    (0x2C9, 0x2C9),   # macron
    (0x2D8, 0x2DC),   # breve through tilde
    # Greek
    (0x391, 0x3A9),   # Greek capitals
    (0x3B1, 0x3C9),   # Greek lowercase
    (0x3D1, 0x3D6),   # Greek symbols
    (0x3F0, 0x3F6),   # Greek symbols
]
MATH_RANGES = DEFAULT_MATH_RANGES
EXTRA_MATH = (DEFAULT_EXTRA_MATH or []) + [
    0x28, 0x29,   # ( ) — use math font
    0x2B, 0x2D,   # + - — use math font
    0x3C, 0x3D, 0x3E, # < = > — use math font
    0x5B, 0x5D,   # [ ] — use math font
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

    # 3. Greek sk (angle-based, 1.3x) + slant Greek for italic/bold-italic
    import math as _math
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.transformPen import TransformPen
    _angle = 12.0; _tan = _math.tan(_math.radians(_angle))
    _xh = 486; _cap = 660
    _sk_lc = round(_xh * _tan / 2 / 1000 * 1.3, 4)
    _sk_uc = round(_cap * _tan / 2 / 1000 * 1.3, 4)
    _GREEK_SLANT = [
        (0x1D6FC, 0x3B1, 25, text_fonts['regular'], _sk_lc),
        (0x1D6E2, 0x391, 25, text_fonts['regular'], _sk_uc),
        (0x1D736, 0x3B1, 25, text_fonts['bold'], _sk_lc),
        (0x1D71C, 0x391, 25, text_fonts['bold'], _sk_uc),
        (0x1D7AA, 0x3B1, 25, text_fonts['bold'], _sk_lc),
        (0x1D790, 0x391, 25, text_fonts['bold'], _sk_uc),
    ]
    for js_subdir in ['cjs/svg', 'cjs/chtml']:
        np = os.path.join(OUTPUT_DIR, js_subdir, 'normal.js')
        if not os.path.exists(np): continue
        with open(np) as f: content = f.read()
        ct = 0
        for ms, bs, n, font, sk in _GREEK_SLANT:
            gs = font.getGlyphSet(); cmap_f = font.getBestCmap(); upm_f = font['head'].unitsPerEm
            for i in range(n):
                mcp = ms + i; bcp = bs + i
                if bcp == 0x3A2 or bcp not in cmap_f: continue
                gn = cmap_f[bcp]
                sp = SVGPathPen(gs); tp = TransformPen(sp, (1, 0, _tan, 1, 0, 0))
                gs[gn].draw(tp)
                path = sp.getCommands()
                if path.startswith('M'): path = path[1:]
                bp = BoundsPen(gs); tp2 = TransformPen(bp, (1, 0, _tan, 1, 0, 0))
                gs[gn].draw(tp2); b = bp.bounds
                if not b: continue
                h = round(b[3]/upm_f, 3); d = round(-b[1]/upm_f, 3) if b[1]<0 else 0
                w = round(gs[gn].width/upm_f, 3)
                om = re.search(rf'0x{mcp:X}: \[([^\]]+)\]', content)
                iv = 0
                if om:
                    im = re.search(r'ic: ([\d.]+)', om.group(0))
                    if im: iv = float(im.group(1))
                props = []
                if iv: props.append(f'ic: {iv}')
                props.append(f'sk: {sk}'); props.append(f"p: '{path}'")
                ne = f"0x{mcp:X}: [{h}, {d}, {w}, {{ {', '.join(props)} }}]"
                m = re.search(rf'0x{mcp:X}: \[[^\]]+\]', content)
                if m: content = content.replace(m.group(0), ne); ct += 1
        with open(np, 'w') as f: f.write(content)
        if ct: print(f"  Slanted {ct} Greek in {js_subdir}/normal.js")

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

    # 5. Script dupe removal + bracket shift
    import glob
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

    _BRACKET_CPS = [0x28, 0x29, 0x5B, 0x5D, 0x7B, 0x7C, 0x7D]
    _SHIFT = 50
    for js_file in (glob.glob(os.path.join(OUTPUT_DIR, 'cjs/svg/*.js')) +
                    glob.glob(os.path.join(OUTPUT_DIR, 'cjs/chtml/*.js'))):
        with open(js_file) as f: content = f.read()
        changed = False
        for cp in _BRACKET_CPS:
            for m in re.finditer(rf'0x{cp:X}: \[([\d.]+), ([\d.]+),', content):
                h = float(m.group(1)); d = float(m.group(2))
                new_h = round(h - _SHIFT/1000, 3); new_d = round(d + _SHIFT/1000, 3)
                content = content.replace(m.group(0), f'0x{cp:X}: [{new_h}, {new_d},')
                changed = True
        if changed:
            with open(js_file, 'w') as f: f.write(content)

    print("  All post-build fixes applied")

    write_boilerplate(OUTPUT_DIR, FONT_ID, FONT_NAME)
    print(f"Done! Output in {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
