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

# Shantell Sans has NO Greek — use Source Code Pro as middle layer.
# But Shantell DOES have handwriting-style math symbols — pull those from text font.
TEXT_RANGES = DEFAULT_TEXT_RANGES + [
    (0x00B1, 0x00B1),   # ±
    (0x00D7, 0x00D7),   # ×
    (0x00F7, 0x00F7),   # ÷
    (0x03A9, 0x03A9),   # Ω
    (0x03C0, 0x03C0),   # π
    (0x2190, 0x2199),   # arrows ← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙
    (0x2202, 0x2202),   # ∂
    (0x2205, 0x2206),   # ∅ ∆
    (0x220F, 0x2212),   # ∏ ∑ − ∕
    (0x2219, 0x2219),   # ∙
    (0x221A, 0x221A),   # √
    (0x221E, 0x221E),   # ∞
    (0x222B, 0x222B),   # ∫
    (0x2248, 0x2248),   # ≈
    (0x2260, 0x2260),   # ≠
    (0x2264, 0x2265),   # ≤ ≥
    (0x25A0, 0x25C6),   # geometric shapes
    (0x25CB, 0x25CF),   # ○ ● etc.
]
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

    # Override uppercase Greek with Shantell Latin/Cyrillic glyphs where possible
    from mathjax_font_lib import get_glyph_metrics_and_path
    shantell_greek_map = {
        # Greek CP -> Shantell source CP
        0x0391: 0x0041,  # Alpha <- A
        0x0392: 0x0042,  # Beta <- B
        0x0393: 0x0413,  # Gamma <- Cyrillic Г
        0x0394: 0x2206,  # Delta <- Shantell ∆
        0x0395: 0x0045,  # Epsilon <- E
        0x0396: 0x005A,  # Zeta <- Z
        0x0397: 0x0048,  # Eta <- H
        0x0398: 0x04E8,  # Theta <- Cyrillic Ө
        0x0399: 0x0049,  # Iota <- I
        0x039A: 0x004B,  # Kappa <- K
        0x039B: 0x041B,  # Lambda <- Cyrillic Л
        0x039C: 0x004D,  # Mu <- M
        0x039D: 0x004E,  # Nu <- N
        # 0x039E: Xi — no match, keep SCP
        0x039F: 0x004F,  # Omicron <- O
        0x03A0: 0x041F,  # Pi <- Cyrillic П
        0x03A1: 0x0050,  # Rho <- P
        0x03A3: 0x2211,  # Sigma <- Shantell ∑
        0x03A4: 0x0054,  # Tau <- T
        0x03A5: 0x0423,  # Upsilon <- Cyrillic У
        0x03A6: 0x0424,  # Phi <- Cyrillic Ф
        0x03A7: 0x0058,  # Chi <- X
        # 0x03A8: Psi — no match, keep SCP
        # 0x03A9: Omega — already in font via text_ranges
        # Lowercase
        0x03BC: 0x00B5,  # mu <- Shantell µ
    }
    shantell_reg = text_fonts['regular']
    shantell_cmap = shantell_reg.getBestCmap()
    override_count = 0
    for greek_cp, source_cp in shantell_greek_map.items():
        if source_cp in shantell_cmap:
            info = get_glyph_metrics_and_path(shantell_reg, source_cp)
            if info:
                info['source'] = 'shantell-mapped'
                middle_layer[greek_cp] = info
                override_count += 1
    print(f"    Overrode {override_count} Greek with Shantell Latin/Cyrillic glyphs")

    # Fix Sigma (∑): scale down and shift up to remove descent
    # Target: match Gamma cap height (~0.707), minimal descent (~0.01)
    if 0x03A3 in middle_layer:
        sigma = middle_layer[0x03A3]
        # Current: H=0.718, D=0.27, total span = 0.988
        # Target: H=0.707, D=0.01, total span = 0.717
        target_h = 0.707
        target_d = 0.01
        old_h, old_d = sigma['height'], sigma['depth']
        old_span = old_h - old_d  # old_d is positive for descent below baseline
        target_span = target_h + target_d
        scale = target_span / (old_h + old_d)
        # Shift: move everything up so descent becomes ~0.01
        # In font coords (1000 UPM): old bottom = -old_d*1000, new bottom = -target_d*1000
        y_shift = int((-target_d - (-old_d)) * 1000 * scale)  # shift after scaling
        import re as _re
        path = sigma.get('path', '')
        if path:
            tokens = _re.findall(r'[A-Za-z]|-?\d+(?:\.\d+)?', path)
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
                            result.append(str(round(float(tokens[i]) * scale)))
                            result.append(str(round(float(tokens[i+1]) * scale + y_shift)))
                            i += 2
                elif t == 'H':
                    result.append('H')
                    i += 1
                    if i < len(tokens):
                        result.append(str(round(float(tokens[i]) * scale)))
                        i += 1
                elif t == 'V':
                    result.append('V')
                    i += 1
                    if i < len(tokens):
                        result.append(str(round(float(tokens[i]) * scale + y_shift)))
                        i += 1
                elif t == 'Z':
                    result.append('Z')
                    i += 1
                else:
                    if i + 1 < len(tokens) and not tokens[i+1].isalpha():
                        result.append(str(round(float(tokens[i]) * scale)))
                        result.append(str(round(float(tokens[i+1]) * scale + y_shift)))
                        i += 2
                    else:
                        result.append(tokens[i])
                        i += 1
            sigma['path'] = ' '.join(result)
        sigma['height'] = round(target_h, 3)
        sigma['depth'] = round(target_d, 3)
        sigma['width'] = round(sigma['width'] * scale, 3)
        print(f"    Fixed Sigma: H={target_h} D={target_d} (scaled {scale:.3f}x, shifted)")

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

    # Scale uppercase Greek — only SCP glyphs (not Shantell-mapped ones)
    scp_uc = [cp for cp in range(0x0391, 0x03AA)
              if cp != 0x03A2 and cp in middle_layer
              and middle_layer[cp].get('source') != 'shantell-mapped']
    _scale_glyphs(middle_layer, scp_uc, uc_scale)
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

    # Post-build: override math alphanumeric uppercase Greek in normal variant
    # with Shantell Latin/Cyrillic glyphs from bold/italic/bold-italic styles
    _math_alpha_uc_greek = [
        # (math_alpha_base, greek_base, count, text_font_key)
        (0x1D6E2, 0x0391, 25, 'italic'),       # Math italic Greek caps
        (0x1D6A8, 0x0391, 25, 'bold'),          # Math bold Greek caps
        (0x1D71C, 0x0391, 25, 'bold_italic'),   # Math bold italic Greek caps
        (0x1D756, 0x0391, 25, 'bold'),          # Math sans bold Greek caps
        (0x1D790, 0x0391, 25, 'bold_italic'),   # Math sans bold italic Greek caps
    ]
    normal_path = os.path.join(OUTPUT_DIR, "cjs/svg/normal.js")
    with open(normal_path) as f:
        nc = f.read()
    patch_count = 0
    for math_base, greek_base, n, style_key in _math_alpha_uc_greek:
        font = text_fonts[style_key]
        font_cmap = font.getBestCmap()
        for i in range(n):
            math_cp = math_base + i
            greek_cp = greek_base + i
            if greek_cp == 0x03A2:  # reserved
                continue
            # Find the source glyph in Shantell via our mapping
            source_cp = shantell_greek_map.get(greek_cp)
            if source_cp is None or source_cp not in font_cmap:
                continue
            info = get_glyph_metrics_and_path(font, source_cp)
            if info is None:
                continue
            h, d, w = info['height'], info['depth'], info['width']
            path = info.get('path', '')
            # Apply Sigma descent fix if needed (same as upright fix)
            if greek_cp == 0x03A3 and d > 0.1:
                sig_target_h, sig_target_d = 0.707, 0.01
                sig_scale = (sig_target_h + sig_target_d) / (h + d)
                sig_y_shift = int((-sig_target_d - (-d)) * 1000 * sig_scale)
                tokens = re.findall(r'[A-Za-z]|-?\d+(?:\.\d+)?', path)
                result = []
                ti = 0
                while ti < len(tokens):
                    tok = tokens[ti]
                    if tok in 'MLCSQT':
                        result.append(tok); ti += 1
                        pairs = {'M':1,'L':1,'S':2,'Q':2,'C':3,'T':1}
                        for _ in range(pairs.get(tok, 1)):
                            if ti + 1 < len(tokens):
                                result.append(str(round(float(tokens[ti]) * sig_scale)))
                                result.append(str(round(float(tokens[ti+1]) * sig_scale + sig_y_shift)))
                                ti += 2
                    elif tok == 'H':
                        result.append('H'); ti += 1
                        if ti < len(tokens):
                            result.append(str(round(float(tokens[ti]) * sig_scale))); ti += 1
                    elif tok == 'V':
                        result.append('V'); ti += 1
                        if ti < len(tokens):
                            result.append(str(round(float(tokens[ti]) * sig_scale + sig_y_shift))); ti += 1
                    elif tok == 'Z':
                        result.append('Z'); ti += 1
                    else:
                        if ti + 1 < len(tokens) and not tokens[ti+1].isalpha():
                            result.append(str(round(float(tokens[ti]) * sig_scale)))
                            result.append(str(round(float(tokens[ti+1]) * sig_scale + sig_y_shift)))
                            ti += 2
                        else:
                            result.append(tokens[ti]); ti += 1
                path = ' '.join(result)
                h, d, w = sig_target_h, sig_target_d, round(w * sig_scale, 3)
            # Build the replacement entry
            old_pattern = rf'0x{math_cp:X}:\s*\[[^\]]+\]'
            new_entry = f"0x{math_cp:X}: [{h}, {d}, {w}, {{ p: '{path}' }}]"
            nc_new = re.sub(old_pattern, new_entry, nc)
            if nc_new != nc:
                nc = nc_new
                patch_count += 1
    with open(normal_path, 'w') as f:
        f.write(nc)
    print(f"  Patched {patch_count} math alphanumeric uppercase Greek with Shantell glyphs")

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
        y_shift = 0  # no vertical shift
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
