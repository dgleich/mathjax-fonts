#!/usr/bin/env python3
"""Build MathJax font package for Shantell Sans + SCP Greek + Noto Sans Math."""

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
NOTO_MATH = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'noto-sans', 'NotoSansMath-Regular.ttf')

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
    print(f"  Math: Noto Sans Math")

    # Instantiate Shantell Sans: pin all custom axes to defaults, vary weight
    print("  Instantiating variable fonts...")
    text_fonts = {
        'regular':     instantiate_variable_font(UPRIGHT_VAR, weight=400, BNCE=0, INFM=0, SPAC=0),
        'bold':        instantiate_variable_font(UPRIGHT_VAR, weight=700, BNCE=0, INFM=0, SPAC=0),
        'italic':      instantiate_variable_font(ITALIC_VAR, weight=300, BNCE=0, INFM=0, SPAC=0),
        'bold_italic': instantiate_variable_font(ITALIC_VAR, weight=500, BNCE=0, INFM=0, SPAC=0),
    }
    math_font = load_font(NOTO_MATH)

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

    # Scale uppercase Greek to match Shantell's cap height
    # SCP cap height ~0.656, Shantell cap height ~0.710
    x_height = get_x_height(text_fonts['regular'])
    shantell_cap = 0.680
    scp_cap = 0.656
    uc_scale = shantell_cap / scp_cap
    lc_scale = 0.97  # slight reduction for lowercase Greek
    print(f"  Scaling uppercase Greek by {uc_scale:.3f}x, lowercase by {lc_scale:.3f}x")

    import re as _re
    def _scale_glyphs(data, codepoints, scale):
        for cp in codepoints:
            if cp in data:
                info = data[cp]
                info['height'] = round(info['height'] * scale, 3)
                info['depth'] = round(info['depth'] * scale, 3)
                info['width'] = round(info['width'] * scale, 3)
                path = info.get('path', '')
                if path:
                    info['path'] = _re.sub(
                        r'-?\d+(?:\.\d+)?',
                        lambda m: str(round(float(m.group()) * scale)),
                        path
                    )

    # Scale uppercase Greek
    _scale_glyphs(middle_layer,
                  [cp for cp in range(0x0391, 0x03AA) if cp != 0x03A2],
                  uc_scale)
    # Scale lowercase Greek
    _scale_glyphs(middle_layer,
                  list(range(0x03B1, 0x03CA)) + list(range(0x03D1, 0x03D7)) + list(range(0x03F0, 0x03F7)),
                  lc_scale)
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
        greek_from_text=True,
    )

    # Post-build: flip pm (U+00B1) to make mp (U+2213)
    normal_path = os.path.join(OUTPUT_DIR, "cjs/svg/normal.js")
    with open(normal_path) as f:
        nc = f.read()
    pm_m = re.search(r"0xB1:\s*\[([^,]+),\s*([^,]+),\s*([^,]+),\s*\{[^}]*p:\s*'([^']+)'\s*\}", nc)
    if pm_m:
        h, d, w = float(pm_m.group(1)), float(pm_m.group(2)), float(pm_m.group(3))
        pm_path = pm_m.group(4)
        # 180° rotation: flip both X and Y, then shift down 10%
        # new_x = W*1000 - old_x, new_y = (H+D)*1000 - old_y
        flip_x = int(w * 1000)
        flip_y = int((h + d) * 1000)
        y_shift = -int((h - d) * 1000 * 0.10)  # shift down 10%
        import re as _re
        tokens = _re.findall(r'[A-Za-z]|-?\d+(?:\.\d+)?', pm_path)
        result = []
        i = 0
        while i < len(tokens):
            t = tokens[i]
            if t in 'MLCSQT':
                result.append(t)
                i += 1
                pairs = {'M': 1, 'L': 1, 'S': 2, 'Q': 2, 'C': 3, 'T': 1}
                for _ in range(pairs.get(t, 1)):
                    if i + 1 < len(tokens):
                        result.append(str(flip_x - int(float(tokens[i]))))     # flip x
                        result.append(str(flip_y - int(float(tokens[i+1])) + y_shift))  # flip y + shift
                        i += 2
            elif t == 'H':
                result.append('H')
                i += 1
                if i < len(tokens):
                    result.append(str(flip_x - int(float(tokens[i]))))  # flip x
                    i += 1
            elif t == 'V':
                result.append('V')
                i += 1
                if i < len(tokens):
                    result.append(str(flip_y - int(float(tokens[i])) + y_shift))  # flip y + shift
                    i += 1
            elif t == 'Z':
                result.append('Z')
                i += 1
            else:
                if i + 1 < len(tokens) and not tokens[i+1].isalpha():
                    result.append(str(flip_x - int(float(tokens[i]))))
                    result.append(str(flip_y - int(float(tokens[i+1])) + y_shift))
                    i += 2
                else:
                    result.append(tokens[i])
                    i += 1
        mp_path = ' '.join(result)
        mp_entry = f"0x2213: [{h}, {d}, {w}, {{ p: '{mp_path}' }}]"
        nc = re.sub(r'0x2213:\s*\[[^\]]+\]', mp_entry, nc)
        with open(normal_path, 'w') as f:
            f.write(nc)
        print(f"  Replaced mp with 180°-rotated pm (shift {y_shift} units)")

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
