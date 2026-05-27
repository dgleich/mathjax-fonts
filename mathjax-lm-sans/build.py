#!/usr/bin/env python3
"""Build MathJax font package for CMU Sans Serif + NewCM Sans Math."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from mathjax_font_lib import (
    load_font, get_x_height, extract_italic_corrections, override_integral_ics,
    build_all_variants, write_boilerplate, adjust_integral_widths,
    DEFAULT_TEXT_RANGES, DEFAULT_MATH_RANGES, DEFAULT_EXTRA_MATH,
    TEXT_RANGES_WITH_GREEK,
)
import re

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_NAME = "MathJaxLMSans"
FONT_ID = "mathjax-lm-sans"
CSS_PREFIX = "LMSANS"

FONTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'cmu-sans')

TEXT_FONTS = {
    'regular':     os.path.join(FONTS_DIR, 'cmunss.otf'),
    'bold':        os.path.join(FONTS_DIR, 'cmunsx.otf'),
    'italic':      os.path.join(FONTS_DIR, 'cmunsi.otf'),
    # CMU Sans Bold Extended Oblique — not ideal (extended width, oblique not true italic)
    # but it's the only bold italic available. NewCM Sans Math's bold-italic glyphs are
    # just slanted bold (not true italic). See GitHub issue for contributing a true BI.
    'bold_italic': os.path.join(FONTS_DIR, 'cmunso.otf'),
}
MATH_FONT = os.path.join(FONTS_DIR, 'NewCMSansMath-Regular.otf')

# CMU Sans has Greek but we use the math font's Greek (proper math letterforms)
TEXT_RANGES = DEFAULT_TEXT_RANGES
MATH_RANGES = DEFAULT_MATH_RANGES
EXTRA_MATH = DEFAULT_EXTRA_MATH


def main():
    print(f"Building {FONT_ID}...")
    print(f"  Text: CMU Sans Serif (R+B+I+BI)")
    print(f"  Math: NewCM Sans Math")

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
        # NOT using greek_from_text — it overrides both Latin AND Greek from text font.
        # We want Latin from CMU Sans but Greek from NewCM Math.
        # Post-build step handles Latin-only override.
    )

    # Override math alphanumeric LATIN (not Greek) with CMU Sans text font glyphs.
    from mathjax_font_lib import get_glyph_metrics_and_path
    _LATIN_MAPPINGS = [
        (0x1D434, 0x41, 26, 'italic'),     # math italic A-Z
        (0x1D44E, 0x61, 26, 'italic'),     # math italic a-z
        (0x1D400, 0x41, 26, 'bold'),        # math bold A-Z
        (0x1D41A, 0x61, 26, 'bold'),        # math bold a-z
        (0x1D468, 0x41, 26, 'bold_italic'), # math bold italic A-Z
        (0x1D482, 0x61, 26, 'bold_italic'), # math bold italic a-z
        (0x1D5A0, 0x41, 26, 'regular'),     # math sans A-Z
        (0x1D5BA, 0x61, 26, 'regular'),     # math sans a-z
        (0x1D5D4, 0x41, 26, 'bold'),        # math sans bold A-Z
        (0x1D5EE, 0x61, 26, 'bold'),        # math sans bold a-z
        (0x1D608, 0x41, 26, 'italic'),      # math sans italic A-Z
        (0x1D622, 0x61, 26, 'italic'),      # math sans italic a-z
        (0x1D63C, 0x41, 26, 'bold_italic'), # math sans bold italic A-Z
        (0x1D656, 0x61, 26, 'bold_italic'), # math sans bold italic a-z
    ]
    for js_subdir in ['cjs/svg', 'cjs/chtml']:
        normal_path = os.path.join(OUTPUT_DIR, js_subdir, 'normal.js')
        if not os.path.exists(normal_path):
            continue
        with open(normal_path) as f:
            content = f.read()
        count = 0
        for math_start, basic_start, n, font_key in _LATIN_MAPPINGS:
            font = text_fonts.get(font_key)
            if not font:
                continue
            cmap_tf = font.getBestCmap()
            for i in range(n):
                math_cp = math_start + i
                basic_cp = basic_start + i
                if basic_cp not in cmap_tf:
                    continue
                info = get_glyph_metrics_and_path(font, basic_cp)
                if not info:
                    continue
                h, d, w = info['height'], info['depth'], info['width']
                p = info['path']
                sk = info.get('sk', 0)
                # Preserve ic from MATH table if available
                ic_val = ic_map.get(math_cp, 0)
                props = []
                if ic_val: props.append(f"ic: {ic_val}")
                if sk: props.append(f"sk: {sk}")
                props.append(f"p: '{p}'")
                new_entry = f"0x{math_cp:X}: [{h}, {d}, {w}, {{ {', '.join(props)} }}]"
                pattern = rf'0x{math_cp:X}: \[[^\]]+\]'
                m = re.search(pattern, content)
                if m:
                    content = content.replace(m.group(0), new_entry)
                    count += 1
        with open(normal_path, 'w') as f:
            f.write(content)
        print(f"  Overrode {count} math-alpha Latin with CMU Sans in {js_subdir}/normal.js")

    # Remove basic Latin from italic variant so MathJax follows smp redirects
    # to normal.js (which has ic from MATH table).
    for variant_file in ['cjs/svg/italic.js',
                         'cjs/chtml/italic.js']:
        fpath = os.path.join(OUTPUT_DIR, variant_file)
        if not os.path.exists(fpath):
            continue
        with open(fpath) as f:
            vc = f.read()
        before = vc.count('0x')
        for cp in list(range(0x41, 0x5B)) + list(range(0x61, 0x7B)):
            vc = re.sub(rf'    0x{cp:X}: \[[^\]]+\],?\n', '', vc)
        with open(fpath, 'w') as f:
            f.write(vc)
        after = vc.count('0x')
        if before - after:
            print(f"  Removed {before - after} basic Latin from {variant_file}")

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
    adjust_integral_widths(OUTPUT_DIR, smallop_w_ratio=0.75, smallop_ic=0.03, largeop_w_ratio=0.73, largeop_ic=0.25)

    # Tighten \sum, \prod limits in smallop (reduce width to tuck sub/super closer)
    for js_path in [os.path.join(OUTPUT_DIR, "cjs/svg/smallop.js")]:
        if not os.path.exists(js_path):
            continue
        with open(js_path) as f:
            sc = f.read()
        for cp in [0x2211]:  # sum only
            m = re.search(rf'0x{cp:X}:\s*\[([^\]]+)\]', sc)
            if not m:
                continue
            entry = m.group(1)
            parts = entry.split(',', 3)
            orig_w = float(parts[2].split('{')[0].strip())
            new_w = round(orig_w * 0.90, 3)
            parts[2] = f' {new_w}'
            sc = sc.replace(m.group(0), f'0x{cp:X}: [{",".join(parts)}]')
        with open(js_path, 'w') as f:
            f.write(sc)
        print("  Tightened sum/prod limits in smallop")

    write_boilerplate(OUTPUT_DIR, FONT_ID, FONT_NAME)
    print(f"Done! Output in {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
