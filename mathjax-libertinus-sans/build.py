#!/usr/bin/env python3
"""Build MathJax font package for Libertinus Sans + Libertinus Math."""

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
from xml.etree import ElementTree as ET
FONT_NAME = "MathJaxLibertinusSans"
FONT_ID = "mathjax-libertinus-sans"
CSS_PREFIX = "LIBSANS"

FONTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'libertinus')

TEXT_FONTS = {
    'regular':     os.path.join(FONTS_DIR, 'LibertinusSans-Regular.otf'),
    'bold':        os.path.join(FONTS_DIR, 'LibertinusSans-Bold.otf'),
    'italic':      os.path.join(FONTS_DIR, 'LibertinusSans-Italic.otf'),
    # Synthetic Bold Italic: skewed bold + hand-edited italic-shape glyphs
    'bold_italic': os.path.join(FONTS_DIR, 'LibertinusSans-BoldItalic-Synth.otf'),
}
MATH_FONT = os.path.join(FONTS_DIR, 'LibertinusMath-Regular.otf')

TEXT_RANGES = TEXT_RANGES_WITH_GREEK
MATH_RANGES = DEFAULT_MATH_RANGES
EXTRA_MATH = DEFAULT_EXTRA_MATH


def _parse_svg_path_to_mathjax(d_str):
    """Parse SVG path d string, return (height, depth, width, path_str) in em/font units."""
    tokens = re.findall(r'[MmLlHhVvCcSsQqTtAaZz]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?', d_str.strip())
    all_points, current, start, parts = [], [0.0, 0.0], [0.0, 0.0], []
    i = 0
    while i < len(tokens):
        cmd = tokens[i]; i += 1
        if cmd in ('M', 'm'):
            rel = (cmd == 'm')
            x = (current[0] if rel else 0)+float(tokens[i]); y = (current[1] if rel else 0)+float(tokens[i+1]); i+=2
            current = [x, y]; start = [x, y]; all_points.append((x, y))
            parts.append(f'{int(round(x))} {int(round(y))}')
            while i < len(tokens) and tokens[i] not in 'MmLlHhVvCcSsQqTtAaZz':
                nx = (current[0] if rel else 0)+float(tokens[i]); ny = (current[1] if rel else 0)+float(tokens[i+1]); i+=2
                current = [nx, ny]; all_points.append((nx, ny))
                parts.append(f'L{int(round(nx))} {int(round(ny))}')
        elif cmd in ('L', 'l'):
            rel = (cmd == 'l')
            while i < len(tokens) and tokens[i] not in 'MmLlHhVvCcSsQqTtAaZz':
                x = (current[0] if rel else 0)+float(tokens[i]); y = (current[1] if rel else 0)+float(tokens[i+1]); i+=2
                current = [x, y]; all_points.append((x, y))
                parts.append(f'L{int(round(x))} {int(round(y))}')
        elif cmd in ('H', 'h'):
            rel = (cmd == 'h')
            while i < len(tokens) and tokens[i] not in 'MmLlHhVvCcSsQqTtAaZz':
                x = (current[0] if rel else 0)+float(tokens[i]); i+=1; current[0] = x
                all_points.append((x, current[1]))
                parts.append(f'L{int(round(x))} {int(round(current[1]))}')
        elif cmd in ('V', 'v'):
            rel = (cmd == 'v')
            while i < len(tokens) and tokens[i] not in 'MmLlHhVvCcSsQqTtAaZz':
                y = (current[1] if rel else 0)+float(tokens[i]); i+=1; current[1] = y
                all_points.append((current[0], y))
                parts.append(f'L{int(round(current[0]))} {int(round(y))}')
        elif cmd in ('C', 'c'):
            rel = (cmd == 'c')
            while i < len(tokens) and tokens[i] not in 'MmLlHhVvCcSsQqTtAaZz':
                ox, oy = (current[0], current[1]) if rel else (0, 0)
                x1=ox+float(tokens[i]);y1=oy+float(tokens[i+1]);i+=2
                x2=ox+float(tokens[i]);y2=oy+float(tokens[i+1]);i+=2
                x=ox+float(tokens[i]);y=oy+float(tokens[i+1]);i+=2
                all_points.extend([(x1,y1),(x2,y2),(x,y)]); current=[x,y]
                parts.append(f'C{int(round(x1))} {int(round(y1))} {int(round(x2))} {int(round(y2))} {int(round(x))} {int(round(y))}')
        elif cmd in ('Z', 'z'):
            current = start[:]; parts.append('Z')
    path_str = ''.join(parts)
    if not all_points: return None
    xs = [p[0] for p in all_points]; ys = [p[1] for p in all_points]
    return round(max(ys)/1000, 3), round(-min(ys)/1000, 3) if min(ys)<0 else 0, round(max(xs)/1000, 3), path_str


def _patch_bold_italic_glyphs(output_dir):
    """Replace bold italic glyphs with hand-edited versions from SVG file."""
    svg_file = os.path.join(output_dir, 'bold-italic-glyphs.svg')
    if not os.path.exists(svg_file):
        print("  No bold-italic-glyphs.svg found, skipping synthetic BI patch")
        return

    # Codepoint targets
    targets = {
        'a': [0x1D482, 0x1D656], 'e': [0x1D486, 0x1D65A],
        'f': [0x1D487, 0x1D65B], 'g': [0x1D488, 0x1D65C],
        'l': [0x1D48D, 0x1D661], 'kappa': [0x1D73F],
    }

    tree = ET.parse(svg_file)
    root = tree.getroot()
    paths = {}
    for path_el in root.iter('{http://www.w3.org/2000/svg}path'):
        pid = path_el.get('id', '')
        if '_italic' in pid: continue
        d = path_el.get('d', '')
        if d and pid in targets:
            paths[pid] = d

    entries = {}
    for name, d_str in paths.items():
        result = _parse_svg_path_to_mathjax(d_str)
        if result:
            entries[name] = result

    for js_subdir in ['cjs/svg', 'cjs/chtml']:
        normal_path = os.path.join(output_dir, js_subdir, 'normal.js')
        if not os.path.exists(normal_path): continue
        with open(normal_path) as f:
            content = f.read()
        count = 0
        for name, cps in targets.items():
            if name not in entries: continue
            h, d, w, p = entries[name]
            for cp in cps:
                pattern = rf'(0x{cp:X}: \[)[^\]]+(\])'
                m = re.search(pattern, content)
                if not m: continue
                old_entry = m.group(0)
                sk_match = re.search(r'sk: ([\d.]+)', old_entry)
                sk = sk_match.group(1) if sk_match else '0'
                new_entry = f"0x{cp:X}: [{h}, {d}, {w}, {{ sk: {sk}, p: '{p}' }}]"
                content = content.replace(old_entry, new_entry)
                count += 1
        with open(normal_path, 'w') as f:
            f.write(content)
        print(f"  Patched {count} synthetic bold italic glyphs in {js_subdir}/normal.js")


def _reapply_italic_corrections(output_dir, ic_map):
    """Re-inject italic corrections from MATH table into normal.js entries.
    greek_from_text replaces entries and drops their ic values."""
    for js_subdir in ['cjs/svg', 'cjs/chtml']:
        normal_path = os.path.join(output_dir, js_subdir, 'normal.js')
        if not os.path.exists(normal_path):
            continue
        with open(normal_path) as f:
            content = f.read()

        count = 0
        for cp, ic_val in ic_map.items():
            if ic_val == 0:
                continue
            pattern = rf'0x{cp:X}: \[([^\]]+)\]'
            m = re.search(pattern, content)
            if not m:
                continue
            entry = m.group(0)
            if 'ic:' in entry:
                continue  # already has ic
            # Add ic to the entry: insert before 'p:' or 'sk:'
            if "{ p:" in entry:
                new_entry = entry.replace("{ p:", f"{{ ic: {ic_val}, p:")
            elif "{ sk:" in entry:
                new_entry = entry.replace("{ sk:", f"{{ ic: {ic_val}, sk:")
            else:
                continue
            content = content.replace(entry, new_entry)
            count += 1

        with open(normal_path, 'w') as f:
            f.write(content)
        if count:
            print(f"  Re-applied {count} italic corrections in {js_subdir}/normal.js")


def _fix_math_alpha_overhang(output_dir):
    """Extend advance widths for math alphanumeric italic/BI entries in normal.js
    so they cover xMax (no overhang). Same as ensure_width_covers_overhang but
    for the math alphanumeric codepoints placed by greek_from_text."""
    # Math italic A-Z: U+1D434-1D44D, a-z: U+1D44E-1D467
    # Math bold italic A-Z: U+1D468-1D481, a-z: U+1D482-1D49B
    # Math sans italic A-Z: U+1D608-1D621, a-z: U+1D622-1D63B
    # Math sans BI A-Z: U+1D63C-1D655, a-z: U+1D656-1D66F
    ranges = [
        (0x1D434, 0x1D467),  # math italic A-z
        (0x1D468, 0x1D49B),  # math bold italic A-z
        (0x1D608, 0x1D63B),  # math sans italic A-z
        (0x1D63C, 0x1D66F),  # math sans bold italic A-z
    ]

    for js_subdir in ['cjs/svg', 'cjs/chtml']:
        normal_path = os.path.join(output_dir, js_subdir, 'normal.js')
        if not os.path.exists(normal_path):
            continue
        with open(normal_path) as f:
            content = f.read()

        count = 0
        for start, end in ranges:
            for cp in range(start, end + 1):
                pattern = rf"0x{cp:X}: \[([^\]]+)\]"
                m = re.search(pattern, content)
                if not m:
                    continue

                entry = m.group(0)
                # Extract width and path
                parts = m.group(1)
                w_match = re.match(r'([\d.]+), ([\d.]+), ([\d.]+)', parts)
                if not w_match:
                    continue
                h, d, w = float(w_match.group(1)), float(w_match.group(2)), float(w_match.group(3))

                # Find xMax from path coordinates
                p_match = re.search(r"p: '([^']+)'", entry)
                if not p_match:
                    continue
                path = p_match.group(1)
                nums = re.findall(r'[-+]?\d+', path)
                if not nums:
                    continue
                # xMax is approximately the largest x coordinate
                # (not perfect but good enough for overhang detection)
                max_x = max(int(n) for n in nums) / 1000.0

                if max_x > w + 0.005:  # has overhang
                    new_w = round(max_x + 0.005, 3)  # tiny margin
                    new_entry = entry.replace(f', {w},', f', {new_w},')
                    content = content.replace(entry, new_entry)
                    count += 1

        with open(normal_path, 'w') as f:
            f.write(content)
        if count:
            print(f"  Fixed {count} math-alpha overhang widths in {js_subdir}/normal.js")


def _replace_basic_greek_with_sans(output_dir, regular_font_path):
    """Replace basic Greek (U+0391-03C9) in normal variant with sans text font glyphs."""
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.boundsPen import BoundsPen

    font = TTFont(regular_font_path)
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upm = font['head'].unitsPerEm

    # Greek uppercase U+0391-03A9, lowercase U+03B1-03C9
    greek_ranges = list(range(0x0391, 0x03AA)) + list(range(0x03B1, 0x03CA))

    for js_subdir in ['cjs/svg', 'cjs/chtml']:
        normal_path = os.path.join(output_dir, js_subdir, 'normal.js')
        if not os.path.exists(normal_path):
            continue
        with open(normal_path) as f:
            content = f.read()

        count = 0
        for cp in greek_ranges:
            gn = cmap.get(cp)
            if not gn:
                continue

            # Get SVG path
            pen = SVGPathPen(gs)
            gs[gn].draw(pen)
            path_str = pen.getCommands()
            if not path_str:
                continue

            # Get bounds for metrics
            bp = BoundsPen(gs)
            gs[gn].draw(bp)
            bounds = bp.bounds
            if not bounds:
                continue

            h = round(bounds[3] / upm, 3)
            d = round(-bounds[1] / upm, 3) if bounds[1] < 0 else 0
            w = round(gs[gn].width / upm, 3)

            # Find existing entry
            pattern = rf'0x{cp:X}: \[[^\]]+\]'
            m = re.search(pattern, content)
            if not m:
                continue

            # Preserve existing sk if present
            old = m.group(0)
            sk_match = re.search(r'sk: ([-\d.]+)', old)
            sk = sk_match.group(1) if sk_match else None

            if sk:
                new_entry = f"0x{cp:X}: [{h}, {d}, {w}, {{ sk: {sk}, p: '{path_str}' }}]"
            else:
                new_entry = f"0x{cp:X}: [{h}, {d}, {w}, {{ p: '{path_str}' }}]"

            content = content.replace(old, new_entry)
            count += 1

        with open(normal_path, 'w') as f:
            f.write(content)
        print(f"  Replaced {count} basic Greek glyphs with sans in {js_subdir}/normal.js")


def main():
    print(f"Building {FONT_ID}...")
    print(f"  Text: Libertinus Sans (R+B+I, BI=I fallback)")
    print(f"  Math: Libertinus Math")

    text_fonts = {k: load_font(v) for k, v in TEXT_FONTS.items()}
    math_font = load_font(MATH_FONT)

    # Use actual 'x' glyph height, not OS/2 sxHeight (which can differ)
    from mathjax_font_lib import get_glyph_metrics_and_path
    x_info = get_glyph_metrics_and_path(text_fonts['regular'], 0x78)
    x_height = x_info['height'] if x_info else get_x_height(text_fonts['regular'])
    print(f"  x_height: {x_height} (glyph-based)")

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

    # Post-build: adjust overbrace/underbrace label spacing
    delim_path = os.path.join(OUTPUT_DIR, "cjs/svg/delimiters.js")
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
    chtml_delim_path = os.path.join(OUTPUT_DIR, "cjs/chtml/delimiters.js")
    with open(chtml_delim_path) as f:
        cc = f.read()
    cc = re.sub(
        r'(0x23DE: \{[^}]*HDW: \[)([^,]+)',
        lambda m: m.group(1) + str(round(float(m.group(2)) + 0.35, 3)),
        cc
    )
    cc = re.sub(
        r'(0x23DF: \{[^}]*HDW: \[[^,]+, )([^,]+)',
        lambda m: m.group(1) + str(round(float(m.group(2)) + 0.35, 3)),
        cc
    )
    with open(chtml_delim_path, 'w') as f:
        f.write(cc)
    print("  Adjusted overbrace/underbrace label spacing (+0.35em)")

    # Re-apply italic corrections from MATH table. greek_from_text replaces
    # glyphs in normal.js, dropping the ic that was applied earlier. Re-inject them.
    _reapply_italic_corrections(OUTPUT_DIR, ic_map)

    # Note: _fix_math_alpha_overhang removed — ic from MATH table handles spacing now.
    # Extending widths to xMax made everything too loose.

    # Remove basic Latin A-Z, a-z from italic and bold-italic variants.
    # MathJax renders $U$ by looking up 0x55 in italic.js. If found there,
    # it uses that entry (no ic). If NOT found, it follows smp redirect to
    # U+1D448 in normal.js (which has ic from the MATH table). Computer Modern
    # doesn't put basic Latin in italic.js — we shouldn't either.
    for variant_file in ['cjs/svg/italic.js', 'cjs/svg/bold-italic.js',
                         'cjs/chtml/italic.js', 'cjs/chtml/bold-italic.js']:
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
        print(f"  Removed {before - after} basic Latin from {variant_file}")

    # Adjust integral widths for better subscript tucking
    adjust_integral_widths(OUTPUT_DIR, smallop_w_ratio=0.88, smallop_ic=0.02, largeop_w_ratio=0.82, largeop_ic=0.03)

    # Wire calligraphic in svg.js
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
    # Script dupe removal
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
