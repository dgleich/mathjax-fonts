#!/usr/bin/env python3
"""Build MathJax font package for PT Sans (patched I) + Lete Sans Math."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from mathjax_font_lib import (
    load_font, get_x_height, extract_italic_corrections, override_integral_ics,
    build_all_variants, write_boilerplate, adjust_integral_widths,
    DEFAULT_TEXT_RANGES, DEFAULT_MATH_RANGES, DEFAULT_EXTRA_MATH,
)
import re

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_NAME = "MathJaxPTSans"
FONT_ID = "mathjax-ptsans"
CSS_PREFIX = "PTSANS"

FONTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'ptsans')
LETE_MATH = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'lete-sans-math', 'LeteSansMath.otf')

TEXT_FONTS = {
    'regular':     os.path.join(FONTS_DIR, 'PT_Sans-Web-Regular.ttf'),
    'bold':        os.path.join(FONTS_DIR, 'PT_Sans-Web-Bold.ttf'),
    'italic':      os.path.join(FONTS_DIR, 'PT_Sans-Web-Italic.ttf'),
    'bold_italic': os.path.join(FONTS_DIR, 'PT_Sans-Web-BoldItalic.ttf'),
}

# PT Sans has NO Greek — all Greek comes from Lete Sans Math
TEXT_RANGES = DEFAULT_TEXT_RANGES
MATH_RANGES = DEFAULT_MATH_RANGES
EXTRA_MATH = DEFAULT_EXTRA_MATH


def main():
    print(f"Building {FONT_ID}...")
    print(f"  Text: PT Sans (patched serifed I)")
    print(f"  Math: Lete Sans Math")

    text_fonts = {k: load_font(v) for k, v in TEXT_FONTS.items()}
    math_font = load_font(LETE_MATH)

    # Swap I (U+0049) with serifed I.ss01 alternate in all text fonts
    for style, font in text_fonts.items():
        go = font.getGlyphOrder()
        if 'I.ss01' in go:
            cmap_table = font['cmap']
            for table in cmap_table.tables:
                if 0x49 in table.cmap:
                    table.cmap[0x49] = 'I.ss01'
            print(f"  Swapped I -> I.ss01 (serifed) in {style}")

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
    )

    import re as _re
    scale = 0.700 / 0.716
    uc_greek_cps = set(range(0x0391, 0x03AA)) - {0x03A2}
    for base in [0x1D6A8, 0x1D6E2, 0x1D71C, 0x1D756, 0x1D790]:
        uc_greek_cps.update(range(base, base + 25))

    # Post-build: fix overbrace/underbrace zero-width glyphs
    # Lete Sans Math's base overbrace glyph has width=0 (but advance=601).
    # Fix HDW, normal.js, and smallop.js width fields.
    import re as _re2
    # Build a map of correct widths from MATH table advance measurements
    _lete = load_font(LETE_MATH)
    _lete_math = _lete['MATH'].table
    _lete_mv = _lete_math.MathVariants
    _lete_cmap = _lete.getBestCmap()
    _lete_gs = _lete.getGlyphSet()
    _lete_upm = _lete['head'].unitsPerEm
    _zero_width_fixes = {}  # cp -> correct_width_em
    if _lete_mv.HorizGlyphCoverage:
        for i, gn in enumerate(_lete_mv.HorizGlyphCoverage.glyphs):
            cp = {v: k for k, v in _lete_cmap.items()}.get(gn)
            if cp is None:
                continue
            if _lete_gs[gn].width == 0:
                rec = _lete_mv.HorizGlyphConstruction[i]
                if rec.MathGlyphVariantRecord:
                    adv = rec.MathGlyphVariantRecord[0].AdvanceMeasurement
                    _zero_width_fixes[cp] = round(adv / _lete_upm, 3)
    if _lete_mv.VertGlyphCoverage:
        for i, gn in enumerate(_lete_mv.VertGlyphCoverage.glyphs):
            cp = {v: k for k, v in _lete_cmap.items()}.get(gn)
            if cp is None:
                continue
            if _lete_gs[gn].width == 0:
                rec = _lete_mv.VertGlyphConstruction[i]
                if rec.MathGlyphVariantRecord:
                    adv = rec.MathGlyphVariantRecord[0].AdvanceMeasurement
                    _zero_width_fixes[cp] = round(adv / _lete_upm, 3)
    if _zero_width_fixes:
        # Fix in normal.js, smallop.js, and delimiters HDW
        for js_name in ['normal.js', 'smallop.js']:
            js_path = os.path.join(OUTPUT_DIR, f"cjs/svg/{js_name}")
            if not os.path.exists(js_path):
                continue
            with open(js_path) as f:
                c = f.read()
            for cp, correct_w in _zero_width_fixes.items():
                m = _re2.search(rf'(0x{cp:X}:\s*\[[^,]+,\s*[^,]+,\s*)0(,)', c)
                if m:
                    c = c[:m.start(2)] + f', ' + c[m.end(2):]
                    c = c[:m.start()] + m.group(1) + str(correct_w) + c[m.start(2):]
                    # Simpler: just replace the whole entry's width
                m = _re2.search(rf'(0x{cp:X}:\s*\[[^,]+,\s*[^,]+,\s*)(0)(,)', c)
                if m:
                    c = c.replace(m.group(0), m.group(1) + str(correct_w) + m.group(3))
            with open(js_path, 'w') as f:
                f.write(c)
        # Fix delimiters HDW
        for delim_path in [
            os.path.join(OUTPUT_DIR, "cjs/svg/delimiters.js"),
            os.path.join(OUTPUT_DIR, "cjs/chtml/delimiters.js"),
        ]:
            with open(delim_path) as f:
                dc = f.read()
            for cp, correct_w in _zero_width_fixes.items():
                dc = _re2.sub(
                    rf'(0x{cp:X}: \{{[^}}]*HDW: \[[^,]+, [^,]+, )0(\])',
                    lambda mx: mx.group(1) + str(correct_w) + mx.group(2),
                    dc
                )
            with open(delim_path, 'w') as f:
                f.write(dc)
        print(f"  Fixed {len(_zero_width_fixes)} zero-width glyphs from Lete (overbrace etc.)")

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

    print(f"Done! Output in {OUTPUT_DIR}")

    # Scale uppercase Greek caps (must be last — after all other post-build steps)
    # Process each file line by line to avoid cross-entry contamination
    hex_set = set(f'0x{cp:X}' for cp in uc_greek_cps)
    for js_path in [os.path.join(OUTPUT_DIR, "cjs/svg/normal.js"),
                     os.path.join(OUTPUT_DIR, "cjs/svg/italic.js")]:
        with open(js_path) as f:
            lines = f.readlines()
        changed = 0
        for i, line in enumerate(lines):
            m = _re.match(r'(\s*)(0x[0-9A-F]+)(:.*)', line)
            if not m or m.group(2) not in hex_set:
                continue
            # Scale all numbers in the line
            prefix = m.group(1) + m.group(2) + ': ['
            entry_m = _re.search(r'\[([^\]]+)\]', line)
            if not entry_m:
                continue
            entry = entry_m.group(1)
            parts = entry.split(',', 3)
            if len(parts) < 3:
                continue
            orig_h = float(parts[0])
            # Per-glyph scale to normalize to PT Sans cap height
            glyph_scale = 0.700 / orig_h if orig_h > 0.5 else scale
            h = round(orig_h * glyph_scale, 3)
            d = round(float(parts[1]) * glyph_scale, 3)
            w_str = parts[2].split('{')[0].strip()
            w = round(float(w_str) * glyph_scale, 3)
            rest = parts[3] if len(parts) > 3 else ''
            path_m = _re.search(r"p:\s*'([^']+)'", rest)
            if path_m:
                path = path_m.group(1)
                new_path = _re.sub(r'-?\d+(?:\.\d+)?',
                                    lambda m2: str(round(float(m2.group()) * glyph_scale)),
                                    path)
                rest = rest.replace(path, new_path)
            lines[i] = f'{prefix}{h}, {d}, {w},{rest}],\n'
            changed += 1
        with open(js_path, 'w') as f:
            f.writelines(lines)
        print(f"  Greek cap scaling: {changed} glyphs in {os.path.basename(js_path)}")


if __name__ == '__main__':
    main()
