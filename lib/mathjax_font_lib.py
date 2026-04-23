"""
MathJax 4 Font Library — shared functions for building custom MathJax font packages.

Extracts glyphs from OTF/TTF/Type1 fonts, builds SVG + CHTML variant data,
generates delimiter tables, size variants, stretchy parts, WOFF2 subsets,
and writes the JS boilerplate (common.js, svg.js, chtml.js, entry points, webpack).

Usage:
    from mathjax_font_lib import (
        load_font, build_variant_data_svg, build_variant_data_chtml,
        build_delimiters, write_svg_variant_file, write_chtml_variant_file,
        write_common_js, write_svg_js, write_chtml_js, build_all_variants,
    )
"""

import json
import math
import os
import re
import shutil
import struct
from io import BytesIO

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.subset import Subsetter


# ========================================================================
# Default range constants
# ========================================================================

DEFAULT_TEXT_RANGES = [
    (0x20, 0x7E),     # Basic ASCII
    (0xA0, 0xFF),     # Latin-1 Supplement
    (0x2C6, 0x2C6),   # modifier circumflex (\hat)
    (0x2C7, 0x2C7),   # caron
    (0x2C9, 0x2C9),   # macron (\bar)
    (0x2D8, 0x2DC),   # breve, dot above, ring, ogonek, small tilde
]

DEFAULT_MATH_RANGES = [
    (0x391, 0x3A9), (0x3B1, 0x3C9), (0x3D1, 0x3D6), (0x3F0, 0x3F6),  # Greek
    (0x2100, 0x214F),  # Letterlike Symbols (bb C,H,N,P,Q,R,Z, hbar, ell, etc.)
    (0x2190, 0x21FF), (0x2200, 0x22FF), (0x2300, 0x23FF),  # Arrows, Math ops, Technical
    (0x2500, 0x257F), (0x25A0, 0x25FF), (0x2600, 0x26FF),  # Box, Geometric, Misc
    (0x2700, 0x27BF), (0x27C0, 0x27EF), (0x27F0, 0x27FF),  # Dingbats, Math-A, Arrows-A
    (0x2900, 0x297F), (0x2980, 0x29FF), (0x2A00, 0x2AFF), (0x2B00, 0x2BFF),  # More math
    (0x300, 0x36F), (0x2000, 0x206F), (0x20D0, 0x20FF),  # Combining, Punctuation
    (0x131, 0x131), (0x237, 0x237),  # dotless i, j
    (0x1D400, 0x1D7FF),  # Math Alphanumeric (bold/italic/script/fraktur/bb/sans alphabets)
]

DEFAULT_EXTRA_MATH = [
    0xAC, 0xB1, 0xD7, 0xF7, 0x131, 0x237,
    0x210E, 0x210F, 0x2126, 0x2127, 0x212A, 0x212B,
    0x2135, 0x2136, 0x2137, 0x2138, 0x3F4, 0x3F5, 0x3F6, 0x20AC,
]


# ========================================================================
# newtxsf glyph maps (Type1 OML encoding -> Unicode)
# ========================================================================

NTXSF_GLYPH_MAP = {
    # Lowercase Greek
    'alpha': 0x03B1, 'beta': 0x03B2, 'gamma': 0x03B3, 'delta': 0x03B4,
    'epsilon': 0x03F5, 'zeta': 0x03B6, 'eta': 0x03B7, 'theta': 0x03B8,
    'iota': 0x03B9, 'kappa': 0x03BA, 'lambda': 0x03BB, 'mu': 0x03BC,
    'nu': 0x03BD, 'xi': 0x03BE, 'pi': 0x03C0, 'rho': 0x03C1,
    'sigma': 0x03C3, 'tau': 0x03C4, 'upsilon': 0x03C5, 'phi': 0x03D5,
    'chi': 0x03C7, 'psi': 0x03C8, 'omega': 0x03C9,
    # Greek variants
    'epsilon1': 0x03B5,  # varepsilon (standard epsilon)
    'theta1': 0x03D1,    # vartheta
    'pi1': 0x03D6,       # varpi
    'rho1': 0x03F1,      # varrho
    'sigma1': 0x03C2,    # varsigma (final sigma)
    'phi1': 0x03C6,      # varphi (standard phi)
    # Uppercase Greek
    'Gamma': 0x0393, 'Delta': 0x0394, 'Theta': 0x0398, 'Lambda': 0x039B,
    'Xi': 0x039E, 'Pi': 0x03A0, 'Sigma': 0x03A3, 'Upsilon': 0x03A5,
    'Phi': 0x03A6, 'Psi': 0x03A8, 'Omega': 0x03A9,
    # Other symbols from zsfmi
    'partialdiff': 0x2202, 'weierstrass': 0x2118,
    'dotlessi': 0x0131, 'dotlessj': 0x0237,
}

NTXSF_A_GLYPH_MAP = {
    'nabla': 0x2207, 'hbar': 0x210F, 'hslash': 0x210F,
    'universalAlt': 0x2200,   # for-all
    'existentialAlt': 0x2203,  # exists
    'emptysetAlt': 0x2205,    # empty set
}


# ========================================================================
# Core utilities
# ========================================================================

def round3(v):
    """Round to 3 decimal places, strip trailing zeros."""
    r = round(v, 3)
    if r == int(r):
        return int(r)
    return r


def load_font(path):
    """Load a TTF/OTF font and return a TTFont object."""
    return TTFont(path)


def get_x_height(font):
    """Auto-calculate x_height from OS/2 table."""
    return round3(font['OS/2'].sxHeight / font['head'].unitsPerEm)


# ========================================================================
# newtxsf Type1 font functions
# ========================================================================

def load_ntxsf_font(pfb_path):
    """Load a newtxsf Type 1 font and return its glyph set."""
    from fontTools.t1Lib import T1Font
    return T1Font(pfb_path)


def get_ntxsf_glyph(t1_font, glyph_name, target_upm=1000, em_scale=1.0):
    """Extract metrics and SVG path from a newtxsf Type 1 glyph.

    Type 1 fonts from newtxsf use 1000 UPM (FontMatrix 0.001).
    Returns dict with height, depth, width, path -- same format as TTF extraction.
    """
    gs = t1_font.getGlyphSet()
    if glyph_name not in gs:
        return None

    # Bounding box
    bp = BoundsPen(gs)
    try:
        gs[glyph_name].draw(bp)
    except Exception:
        return None
    bounds = bp.bounds
    if bounds is None:
        return None

    xMin, yMin, xMax, yMax = bounds
    upm = 1000  # Type 1 newtxsf uses 1000 UPM
    scale = target_upm / upm * em_scale

    # Advance width from the font
    width_val = gs[glyph_name].width
    height = round3(yMax / upm * em_scale)
    depth = round3(-yMin / upm * em_scale)
    width = round3(width_val / upm * em_scale)

    # SVG path
    svg_pen = SVGPathPen(gs)
    gs[glyph_name].draw(svg_pen)
    path_data = svg_pen.getCommands()

    if scale != 1.0:
        path_data = scale_svg_path(path_data, scale)
    path_data = round_path_coords(path_data)

    # Strip leading M (MathJax prepends its own)
    if path_data.startswith('M'):
        path_data = path_data[1:]

    return {
        'height': height,
        'depth': depth,
        'width': width,
        'path': path_data,
        'source': 'newtxsf'
    }


def build_ntxsf_layer(t1_font, t1a_font, glyph_map, glyph_a_map, em_scale=1.0):
    """Build glyph data dict from newtxsf fonts, keyed by Unicode codepoint.

    Returns: dict of {codepoint: {height, depth, width, path, source}}
    """
    data = {}

    # Primary font (zsfmi -- Greek + math italic)
    for glyph_name, cp in glyph_map.items():
        info = get_ntxsf_glyph(t1_font, glyph_name, em_scale=em_scale)
        if info:
            data[cp] = info

    # Supplementary font (zsfmia -- nabla, hbar, blackboard bold, etc.)
    if t1a_font:
        for glyph_name, cp in glyph_a_map.items():
            if cp not in data:
                info = get_ntxsf_glyph(t1a_font, glyph_name, em_scale=em_scale)
                if info:
                    data[cp] = info

    return data


# ========================================================================
# SVG path manipulation
# ========================================================================

def scale_svg_path(path_str, scale):
    """Scale SVG path coordinates by a factor."""
    result = []
    i = 0
    while i < len(path_str):
        c = path_str[i]
        if c.isalpha():
            result.append(c)
            i += 1
        elif c in '-0123456789.':
            # Parse number
            j = i
            if c == '-':
                j += 1
            while j < len(path_str) and (path_str[j].isdigit() or path_str[j] == '.'):
                j += 1
            num_str = path_str[i:j]
            try:
                num = float(num_str) * scale
                result.append(str(round(num)))
            except ValueError:
                result.append(num_str)
            i = j
        else:
            result.append(c)
            i += 1
    return ''.join(result)


def round_path_coords(path_str):
    """Round all numeric coordinates in a path string to integers."""
    def replace_num(m):
        return str(round(float(m.group(0))))
    return re.sub(r'-?\d+\.?\d*', replace_num, path_str)


# ========================================================================
# Glyph metric and path extraction
# ========================================================================

def get_glyph_metrics_and_path(font, codepoint, target_upm=1000, em_scale=1.0):
    """Extract metrics and SVG path for a glyph.

    em_scale: additional scale factor applied to metrics and paths.
    Depth is always computed as round3(-yMin / upm * em_scale).
    """
    cmap = font.getBestCmap()
    if codepoint not in cmap:
        return None

    glyph_name = cmap[codepoint]
    upm = font['head'].unitsPerEm
    scale = target_upm / upm * em_scale

    # Get advance width
    if glyph_name in font['hmtx'].metrics:
        advance_width, lsb = font['hmtx'].metrics[glyph_name]
    else:
        return None

    glyph_set = font.getGlyphSet()
    if glyph_name not in glyph_set:
        return None

    # Get bounding box via BoundsPen
    try:
        bp = BoundsPen(glyph_set)
        glyph_set[glyph_name].draw(bp)
        bounds = bp.bounds
    except Exception:
        bounds = None

    if bounds is None or bounds == (0, 0, 0, 0):
        # Empty glyph (space, etc.)
        width = round3(advance_width / upm * em_scale)
        return {
            'height': 0,
            'depth': 0,
            'width': width,
            'path': ''
        }

    xMin, yMin, xMax, yMax = bounds

    height = round3(yMax / upm * em_scale)
    depth = round3(-yMin / upm * em_scale)
    width = round3(advance_width / upm * em_scale)

    # Get SVG path
    svg_pen = SVGPathPen(glyph_set)
    glyph_set[glyph_name].draw(svg_pen)
    path_data = svg_pen.getCommands()

    # Scale path to target coordinate system
    if scale != 1.0:
        path_data = scale_svg_path(path_data, scale)

    # Simplify path: round coordinates to integers
    path_data = round_path_coords(path_data)

    # MathJax prepends its own "M x y" to paths, so strip the leading M command.
    if path_data.startswith('M'):
        path_data = path_data[1:]

    return {
        'height': height,
        'depth': depth,
        'width': width,
        'path': path_data
    }


def get_glyph_metrics_only(font, codepoint, em_scale=1.0):
    """Extract just metrics (no SVG path) for CHTML."""
    cmap = font.getBestCmap()
    if codepoint not in cmap:
        return None

    glyph_name = cmap[codepoint]
    upm = font['head'].unitsPerEm

    if glyph_name in font['hmtx'].metrics:
        advance_width, lsb = font['hmtx'].metrics[glyph_name]
    else:
        return None

    glyph_set = font.getGlyphSet()
    if glyph_name not in glyph_set:
        return None

    try:
        bp = BoundsPen(glyph_set)
        glyph_set[glyph_name].draw(bp)
        bounds = bp.bounds
    except Exception:
        bounds = None

    if bounds is None or bounds == (0, 0, 0, 0):
        width = round3(advance_width / upm * em_scale)
        return {'height': 0, 'depth': 0, 'width': width}

    xMin, yMin, xMax, yMax = bounds
    height = round3(yMax / upm * em_scale)
    depth = round3(-yMin / upm * em_scale)
    width = round3(advance_width / upm * em_scale)
    return {'height': height, 'depth': depth, 'width': width}


def get_glyph_data_by_name_svg(font, glyph_name, target_upm=1000, em_scale=1.0):
    """Get metrics and SVG path for a glyph by name (not codepoint).

    em_scale: additional scale factor applied to metrics and paths.
    """
    upm = font['head'].unitsPerEm
    scale = target_upm / upm * em_scale
    glyph_set = font.getGlyphSet()

    if glyph_name not in glyph_set:
        return None

    if glyph_name in font['hmtx'].metrics:
        advance_width, lsb = font['hmtx'].metrics[glyph_name]
    else:
        return None

    try:
        bp = BoundsPen(glyph_set)
        glyph_set[glyph_name].draw(bp)
        bounds = bp.bounds
    except Exception:
        bounds = None

    if bounds is None or bounds == (0, 0, 0, 0):
        width = round3(advance_width / upm * em_scale)
        return {'height': 0, 'depth': 0, 'width': width, 'path': ''}

    xMin, yMin, xMax, yMax = bounds
    height = round3(yMax / upm * em_scale)
    depth = round3(-yMin / upm * em_scale)
    width = round3(advance_width / upm * em_scale)

    svg_pen = SVGPathPen(glyph_set)
    glyph_set[glyph_name].draw(svg_pen)
    path_data = svg_pen.getCommands()

    if scale != 1.0:
        path_data = scale_svg_path(path_data, scale)

    path_data = round_path_coords(path_data)

    # MathJax prepends its own "M x y" to paths, so strip the leading M command.
    if path_data.startswith('M'):
        path_data = path_data[1:]

    return {'height': height, 'depth': depth, 'width': width, 'path': path_data}


def get_glyph_data_by_name_chtml(font, glyph_name, em_scale=1.0):
    """Get metrics for a glyph by name (for CHTML)."""
    upm = font['head'].unitsPerEm
    glyph_set = font.getGlyphSet()

    if glyph_name not in glyph_set:
        return None

    if glyph_name in font['hmtx'].metrics:
        advance_width, lsb = font['hmtx'].metrics[glyph_name]
    else:
        return None

    try:
        bp = BoundsPen(glyph_set)
        glyph_set[glyph_name].draw(bp)
        bounds = bp.bounds
    except Exception:
        bounds = None

    if bounds is None or bounds == (0, 0, 0, 0):
        width = round3(advance_width / upm * em_scale)
        return {'height': 0, 'depth': 0, 'width': width}

    xMin, yMin, xMax, yMax = bounds
    height = round3(yMax / upm * em_scale)
    depth = round3(-yMin / upm * em_scale)
    width = round3(advance_width / upm * em_scale)
    return {'height': height, 'depth': depth, 'width': width}


# ========================================================================
# Italic corrections
# ========================================================================

def extract_italic_corrections(font):
    """Extract italic corrections from the MATH table, keyed by codepoint."""
    ic_map = {}
    if 'MATH' not in font:
        return ic_map
    math_table = font['MATH'].table
    if not hasattr(math_table, 'MathGlyphInfo') or not math_table.MathGlyphInfo:
        return ic_map
    mic = math_table.MathGlyphInfo.MathItalicsCorrectionInfo
    if not mic:
        return ic_map
    upm = font['head'].unitsPerEm
    cmap = font.getBestCmap()
    rev_cmap = {v: k for k, v in cmap.items()}
    for i, glyph_name in enumerate(mic.Coverage.glyphs):
        cp = rev_cmap.get(glyph_name)
        if cp is not None:
            ic_value = mic.ItalicsCorrection[i].Value
            if ic_value != 0:
                ic_map[cp] = round3(ic_value / upm)
    return ic_map


def extract_top_accent_skews(font):
    """Extract top accent attachment skew values from MATH table, keyed by codepoint.

    Returns a dict {codepoint: sk_value} where sk = (topAccent - width/2) / upm.
    This tells MathJax how to center accents over each glyph.
    """
    sk_map = {}
    if 'MATH' not in font:
        return sk_map
    math_table = font['MATH'].table
    if not hasattr(math_table, 'MathGlyphInfo') or not math_table.MathGlyphInfo:
        return sk_map
    taa = math_table.MathGlyphInfo.MathTopAccentAttachment
    if not taa:
        return sk_map
    upm = font['head'].unitsPerEm
    cmap = font.getBestCmap()
    rev_cmap = {v: k for k, v in cmap.items()}
    for i, glyph_name in enumerate(taa.TopAccentCoverage.glyphs):
        cp = rev_cmap.get(glyph_name)
        if cp is not None:
            ta_value = taa.TopAccentAttachment[i].Value
            # Get advance width for this glyph
            if glyph_name in font['hmtx'].metrics:
                adv = font['hmtx'].metrics[glyph_name][0]
            else:
                continue
            # sk = (topAccent - width/2) / upm
            sk = round3((ta_value - adv / 2) / upm)
            if sk != 0:
                sk_map[cp] = sk
    return sk_map


def compute_visual_skews(font):
    """Compute accent skews from a font's actual glyph bounding boxes.

    For each glyph, sk = (visual_center - advance_center) / upm.
    This is more accurate than MATH table TopAccentAttachment when the
    rendered glyphs come from a different font than the math font.
    Particularly important for italic text fonts.
    """
    sk_map = {}
    upm = font['head'].unitsPerEm
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()

    for cp, gn in cmap.items():
        if gn not in gs:
            continue
        try:
            bp = BoundsPen(gs)
            gs[gn].draw(bp)
            bounds = bp.bounds
        except Exception:
            continue
        if bounds is None or bounds == (0, 0, 0, 0):
            continue

        adv = gs[gn].width
        vis_center = (bounds[0] + bounds[2]) / 2
        adv_center = adv / 2
        sk = round3((vis_center - adv_center) / upm)
        if sk != 0:
            sk_map[cp] = sk
    return sk_map


def apply_skews(data, sk_map):
    """Merge top accent skew values into variant data. Returns count applied."""
    applied = 0
    for cp, sk_val in sk_map.items():
        if cp in data:
            data[cp]['sk'] = sk_val
            applied += 1
    return applied


def override_integral_ics(ic_map, normal_val=0.12):
    """Override integral italic corrections to match newCM tuning."""
    for cp in range(0x222B, 0x2234):
        if cp in ic_map:
            ic_map[cp] = normal_val


def apply_italic_corrections(data, ic_map):
    """Merge italic corrections into variant data. Returns count applied."""
    applied = 0
    for cp, ic_val in ic_map.items():
        if cp in data:
            data[cp]['ic'] = ic_val
            applied += 1
    return applied


# ========================================================================
# Codepoint collection
# ========================================================================

def collect_codepoints_from_ranges(font, ranges, extra=None):
    """Return sorted list of codepoints that exist in font and in given ranges."""
    cmap = font.getBestCmap()
    cps = set()
    for start, end in ranges:
        for cp in range(start, end + 1):
            if cp in cmap:
                cps.add(cp)
    if extra:
        for cp in extra:
            if cp in cmap:
                cps.add(cp)
    return sorted(cps)


# ========================================================================
# Invisible operator / override utilities
# ========================================================================

def fix_invisible_operators(data):
    """Zero out invisible math operators U+2061-2064."""
    for cp in [0x2061, 0x2062, 0x2063, 0x2064]:
        data[cp] = {'height': 0, 'depth': 0, 'width': 0, 'path': '', 'source': 'override'}


# ========================================================================
# Middle-layer builder (e.g. pull Greek from a separate OTF)
# ========================================================================

def build_middle_layer_from_otf(font_path, codepoint_ranges, em_scale=1.0):
    """Build a middle layer glyph data dict from an OTF/TTF font.

    Used for pulling Greek from a different font (e.g., Source Code Pro for Shantell Sans).
    Returns dict of {codepoint: {height, depth, width, path, source}}.
    """
    font = load_font(font_path)
    data = {}
    cmap = font.getBestCmap()
    for start, end in codepoint_ranges:
        for cp in range(start, end + 1):
            if cp in cmap:
                info = get_glyph_metrics_and_path(font, cp, em_scale=em_scale)
                if info:
                    info['source'] = 'middle-layer'
                    data[cp] = info
    font.close()
    return data


# ========================================================================
# Variant data builders (SVG + CHTML)
# ========================================================================

def build_variant_data_svg(text_font, math_font, text_ranges, math_ranges,
                           extra_math=None, middle_layer_data=None,
                           text_source='text', em_scale=1.0):
    """Build SVG variant data: metrics + paths.

    Font priority: text_font -> middle_layer_data -> math_font
    """
    data = {}

    # Layer 1: Text font (Latin, digits, punctuation)
    text_cmap = text_font.getBestCmap()
    for start, end in text_ranges:
        for cp in range(start, end + 1):
            if cp in text_cmap:
                info = get_glyph_metrics_and_path(text_font, cp, em_scale=em_scale)
                if info:
                    info['source'] = text_source
                    data[cp] = info

    # Layer 2: Middle layer (e.g., newtxsf Greek, or OTF Greek)
    if middle_layer_data:
        for cp, info in middle_layer_data.items():
            if cp not in data:
                data[cp] = info

    # Layer 3: Math font (operators, arrows, delimiters, everything else)
    math_cmap = math_font.getBestCmap()
    for start, end in math_ranges:
        for cp in range(start, end + 1):
            if cp in math_cmap and cp not in data:
                info = get_glyph_metrics_and_path(math_font, cp, em_scale=em_scale)
                if info:
                    info['source'] = 'math'
                    data[cp] = info

    if extra_math:
        for cp in extra_math:
            if cp in math_cmap and cp not in data:
                info = get_glyph_metrics_and_path(math_font, cp, em_scale=em_scale)
                if info:
                    info['source'] = 'math'
                    data[cp] = info

    # Fix invisible math operators
    fix_invisible_operators(data)

    return data


def build_variant_data_chtml(text_font, math_font, text_ranges, math_ranges,
                             extra_math=None, middle_layer_data=None, em_scale=1.0):
    """Build CHTML variant data: metrics only. Same multi-layer priority."""
    data = {}

    # Layer 1: Text font
    text_cmap = text_font.getBestCmap()
    for start, end in text_ranges:
        for cp in range(start, end + 1):
            if cp in text_cmap:
                info = get_glyph_metrics_only(text_font, cp, em_scale=em_scale)
                if info:
                    data[cp] = info

    # Layer 2: Middle layer (metrics only -- strip path)
    if middle_layer_data:
        for cp, info in middle_layer_data.items():
            if cp not in data:
                data[cp] = {
                    'height': info['height'],
                    'depth': info['depth'],
                    'width': info['width'],
                }

    # Layer 3: Math font
    math_cmap = math_font.getBestCmap()
    for start, end in math_ranges:
        for cp in range(start, end + 1):
            if cp in math_cmap and cp not in data:
                info = get_glyph_metrics_only(math_font, cp, em_scale=em_scale)
                if info:
                    data[cp] = info

    if extra_math:
        for cp in extra_math:
            if cp in math_cmap and cp not in data:
                info = get_glyph_metrics_only(math_font, cp, em_scale=em_scale)
                if info:
                    data[cp] = info

    return data


def build_operator_data_svg(math_font, codepoints, em_scale=1.0):
    """Build SVG data for operator/size variants (smallop, largeop, etc.)."""
    data = {}
    cmap = math_font.getBestCmap()
    for cp in codepoints:
        if cp in cmap:
            info = get_glyph_metrics_and_path(math_font, cp, em_scale=em_scale)
            if info:
                data[cp] = info
    return data


def build_operator_data_chtml(math_font, codepoints, em_scale=1.0):
    """Build CHTML data for operator variants."""
    data = {}
    cmap = math_font.getBestCmap()
    for cp in codepoints:
        if cp in cmap:
            info = get_glyph_metrics_only(math_font, cp, em_scale=em_scale)
            if info:
                data[cp] = info
    return data


# ========================================================================
# JS file formatting
# ========================================================================

def format_svg_entry(cp, info):
    """Format a single SVG entry like:  0x41: [.689, 0, .573, { sk: .01, p: 'M...' }]"""
    h = info['height']
    d = info['depth']
    w = info['width']
    p = info.get('path', '')
    ic = info.get('ic', None)
    sk = info.get('sk', None)

    # Build extras dict contents
    extra_parts = []
    if sk is not None:
        extra_parts.append(f"sk: {sk}")
    if p:
        extra_parts.append(f"p: '{p}'")
    if ic is not None:
        extra_parts.append(f"ic: {ic}")

    if extra_parts:
        extras = ", ".join(extra_parts)
        return f"    0x{cp:X}: [{h}, {d}, {w}, {{ {extras} }}]"
    else:
        return f"    0x{cp:X}: [{h}, {d}, {w}]"


def format_chtml_entry(cp, info):
    """Format a single CHTML entry like:  0x41: [.689, 0, .573]"""
    h = info['height']
    d = info['depth']
    w = info['width']
    return f"    0x{cp:X}: [{h}, {d}, {w}]"


# ========================================================================
# Variant file writers
# ========================================================================

def write_svg_variant_file(filepath, var_name, data):
    """Write an SVG variant JS file."""
    lines = [
        '"use strict";',
        'Object.defineProperty(exports, "__esModule", { value: true });',
        f'exports.{var_name} = void 0;',
        f'exports.{var_name} = {{',
    ]
    entries = []
    for cp in sorted(data.keys()):
        entries.append(format_svg_entry(cp, data[cp]))
    lines.append(',\n'.join(entries))
    lines.append('};')
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write('\n'.join(lines) + '\n')


def write_chtml_variant_file(filepath, var_name, data):
    """Write a CHTML variant JS file."""
    lines = [
        '"use strict";',
        'Object.defineProperty(exports, "__esModule", { value: true });',
        f'exports.{var_name} = void 0;',
        f'exports.{var_name} = {{',
    ]
    entries = []
    for cp in sorted(data.keys()):
        entries.append(format_chtml_entry(cp, data[cp]))
    lines.append(',\n'.join(entries))
    lines.append('};')
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write('\n'.join(lines) + '\n')


def write_empty_variant_file(filepath, var_name):
    """Write an empty variant JS file."""
    content = f'''"use strict";
Object.defineProperty(exports, "__esModule", {{ value: true }});
exports.{var_name} = void 0;
exports.{var_name} = {{}};
'''
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)


# ========================================================================
# Delimiter extraction from MATH table
# ========================================================================

def get_glyph_name_to_codepoint(font):
    """Build reverse mapping from glyph name to codepoint."""
    cmap = font.getBestCmap()
    result = {}
    for cp, gname in cmap.items():
        result[gname] = cp
    return result


def get_glyph_height_depth_width(font, glyph_name, em_scale=1.0):
    """Get metrics for a glyph by name (with em_scale applied)."""
    upm = font['head'].unitsPerEm
    glyph_set = font.getGlyphSet()
    if glyph_name not in glyph_set:
        return None

    if glyph_name in font['hmtx'].metrics:
        advance_width, lsb = font['hmtx'].metrics[glyph_name]
    else:
        return None

    try:
        bp = BoundsPen(glyph_set)
        glyph_set[glyph_name].draw(bp)
        bounds = bp.bounds
    except Exception:
        bounds = None

    if bounds is None or bounds == (0, 0, 0, 0):
        return (0, 0, round3(advance_width / upm * em_scale))

    xMin, yMin, xMax, yMax = bounds
    h = round3(yMax / upm * em_scale)
    d = round3(-yMin / upm * em_scale)
    w = round3(advance_width / upm * em_scale)
    return (h, d, w)


def get_glyph_total_height(font, glyph_name, em_scale=1.0):
    """Get total height (height + depth) of a glyph in em units."""
    metrics = get_glyph_height_depth_width(font, glyph_name, em_scale=em_scale)
    if metrics is None:
        return 0
    return metrics[0] + metrics[1]


def build_delimiters(math_font, em_scale=1.0):
    """Build delimiter data from MATH table.

    Returns (delimiters_dict, pua_map) where pua_map is {glyph_name: pua_codepoint}
    for assembly parts that have no Unicode codepoint. These need to be included
    in the stretchy part data files (ext, lf-tp, rt-bt).
    """
    math_table = math_font['MATH'].table
    mv = math_table.MathVariants
    upm = math_font['head'].unitsPerEm
    cmap = math_font.getBestCmap()
    gname_to_cp = get_glyph_name_to_codepoint(math_font)

    # Assign private-use codepoints to assembly parts that have no Unicode mapping
    pua_next = 0xE000
    pua_map = {}  # glyph_name -> PUA codepoint

    def get_cp_for_glyph(glyph_name, assign_pua=False):
        """Get codepoint for a glyph.

        If assign_pua=True and glyph has no Unicode codepoint, assign a PUA codepoint.
        If assign_pua=False (default), return 0 for unmapped glyphs.
        """
        nonlocal pua_next
        cp = gname_to_cp.get(glyph_name)
        if cp is not None:
            return cp
        if not assign_pua:
            return 0
        if glyph_name in pua_map:
            return pua_map[glyph_name]
        pua_map[glyph_name] = pua_next
        pua_next += 1
        return pua_map[glyph_name]

    def get_cp_always_pua(glyph_name):
        """Get codepoint, always assigning PUA if needed."""
        return get_cp_for_glyph(glyph_name, assign_pua=True)

    delimiters = {}

    # Process vertical variants
    if mv.VertGlyphCoverage:
        for i, glyph_name in enumerate(mv.VertGlyphCoverage.glyphs):
            cp = gname_to_cp.get(glyph_name)
            if cp is None:
                continue

            rec = mv.VertGlyphConstruction[i]
            entry = {'dir': 'V'}

            # Size variants
            if rec.VariantCount and rec.MathGlyphVariantRecord:
                sizes = []
                for v in rec.MathGlyphVariantRecord:
                    size_em = round3(v.AdvanceMeasurement / upm * em_scale)
                    sizes.append(size_em)
                entry['sizes'] = sizes

            # Stretchy assembly
            if rec.GlyphAssembly:
                parts = rec.GlyphAssembly.PartRecords
                stretch_cps = []
                for p in parts:
                    is_extender = bool(p.PartFlags & 1)
                    pcp = get_cp_for_glyph(p.glyph, assign_pua=is_extender)
                    stretch_cps.append(pcp)

                if len(parts) == 3:
                    # top, ext, bottom => [top, ext, bottom]
                    entry['stretch'] = [stretch_cps[2], stretch_cps[1], stretch_cps[0]]
                elif len(parts) == 5:
                    # top, ext, mid, ext, bottom => [top, ext, bottom, mid]
                    entry['stretch'] = [stretch_cps[4], stretch_cps[3], stretch_cps[0], stretch_cps[2]]
                elif len(parts) == 2:
                    # Just ext + one piece => [0, ext]
                    entry['stretch'] = [0, stretch_cps[0]]
                    entry['stretchv'] = [0, 1]

                # HDW
                metrics = get_glyph_height_depth_width(math_font, glyph_name, em_scale=em_scale)
                if metrics:
                    entry['HDW'] = [metrics[0], metrics[1], metrics[2]]

            delimiters[cp] = entry

    # Process horizontal variants
    if mv.HorizGlyphCoverage:
        for i, glyph_name in enumerate(mv.HorizGlyphCoverage.glyphs):
            cp = gname_to_cp.get(glyph_name)
            if cp is None:
                continue

            rec = mv.HorizGlyphConstruction[i]
            entry = {'dir': 'H'}

            if rec.VariantCount and rec.MathGlyphVariantRecord:
                sizes = []
                for v in rec.MathGlyphVariantRecord:
                    size_em = round3(v.AdvanceMeasurement / upm * em_scale)
                    sizes.append(size_em)
                entry['sizes'] = sizes

            if rec.GlyphAssembly:
                parts = rec.GlyphAssembly.PartRecords
                # For horizontal assembly, always assign PUA for unmapped parts
                stretch_cps = []
                stretch_flags = []  # True if extender
                for p in parts:
                    pcp = get_cp_always_pua(p.glyph)
                    stretch_cps.append(pcp)
                    stretch_flags.append(bool(p.PartFlags & 1))

                # Build stretch array and stretchv
                # MathJax stretchv: 0=skip, 1=extension, 2=full, 3=left end, 4=right end
                if len(parts) == 2:
                    # [end_or_ext, ext_or_end]
                    sv = []
                    for is_ext in stretch_flags:
                        sv.append(1 if is_ext else 0)
                    entry['stretch'] = stretch_cps
                    entry['stretchv'] = sv
                elif len(parts) == 3:
                    # [left, ext, right]
                    entry['stretch'] = stretch_cps
                    entry['stretchv'] = [
                        3 if not stretch_flags[0] else 1,
                        1 if stretch_flags[1] else 2,
                        4 if not stretch_flags[2] else 1,
                    ]
                elif len(parts) == 4:
                    # [start, ext, mid, ext] -> stretch [start, ext, end, mid]
                    entry['stretch'] = [stretch_cps[0], stretch_cps[1], stretch_cps[3], stretch_cps[2]]
                    entry['stretchv'] = [3, 1, 4, 2]
                elif len(parts) == 5:
                    entry['stretch'] = [stretch_cps[0], stretch_cps[1], stretch_cps[4], stretch_cps[2]]
                    entry['stretchv'] = [3, 1, 4, 2]

                metrics = get_glyph_height_depth_width(math_font, glyph_name, em_scale=em_scale)
                if metrics:
                    entry['HDW'] = [metrics[0], metrics[1], metrics[2]]
                    entry['hd'] = [metrics[0], metrics[1]]

            if cp not in delimiters:
                delimiters[cp] = entry
            else:
                # Merge -- some chars have both vert and horiz
                pass

    # Add common aliases matching Fira reference
    common_aliases = {
        0x2D: {'c': 0x2212, 'dir': 'H', 'stretch': [0, 0x2212]},
        0x5E: {'c': 0x302, 'dir': 'H'},
        0x7E: {'c': 0x303, 'dir': 'H'},
        0x2C6: {'c': 0x302, 'dir': 'H'},
        0x2C9: {'c': 0xAF, 'dir': 'H'},
        0x2DC: {'c': 0x303, 'dir': 'H'},
        0x203E: {'c': 0xAF, 'dir': 'H'},
    }

    for cp, alias in common_aliases.items():
        if cp not in delimiters:
            ref_cp = alias.get('c')
            if ref_cp and ref_cp in delimiters and 'sizes' in delimiters[ref_cp]:
                entry = dict(alias)
                entry['sizes'] = delimiters[ref_cp]['sizes']
                delimiters[cp] = entry
            else:
                delimiters[cp] = alias

    if pua_map:
        print(f"    Assigned {len(pua_map)} PUA codepoints for unmapped assembly parts")
    return delimiters, pua_map


def write_delimiters_file(filepath, delimiters):
    """Write delimiters JS file."""
    lines = [
        '"use strict";',
        'Object.defineProperty(exports, "__esModule", { value: true });',
        'exports.delimiters = void 0;',
        'var Direction_js_1 = require("@mathjax/src/cjs/output/common/Direction.js");',
        'exports.delimiters = {',
    ]

    entries = []
    for cp in sorted(delimiters.keys()):
        d = delimiters[cp]
        parts = []
        if 'c' in d:
            parts.append(f"c: 0x{d['c']:X}")
        dir_str = "Direction_js_1.V" if d.get('dir') == 'V' else "Direction_js_1.H"
        parts.append(f"dir: {dir_str}")
        if 'sizes' in d:
            sizes_str = ', '.join(str(s) for s in d['sizes'])
            parts.append(f"sizes: [{sizes_str}]")
        if 'stretch' in d:
            stretch_str = ', '.join(f"0x{s:X}" if s else '0' for s in d['stretch'])
            parts.append(f"stretch: [{stretch_str}]")
        if 'stretchv' in d:
            sv_str = ', '.join(str(s) for s in d['stretchv'])
            parts.append(f"stretchv: [{sv_str}]")
        if 'HDW' in d:
            hdw_str = ', '.join(str(s) for s in d['HDW'])
            parts.append(f"HDW: [{hdw_str}]")
        if 'hd' in d:
            hd_str = ', '.join(str(s) for s in d['hd'])
            parts.append(f"hd: [{hd_str}]")
        if 'ext' in d:
            parts.append(f"ext: {d['ext']}")

        entry = f"    0x{cp:X}: {{\n        " + ",\n        ".join(parts) + "\n    }"
        entries.append(entry)

    lines.append(',\n'.join(entries))
    lines.append('};')

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write('\n'.join(lines) + '\n')


# ========================================================================
# Size variant glyphs (smallop, largeop, size3-size15)
# ========================================================================

def collect_size_variant_glyphs(math_font):
    """Collect glyphs that appear as size variants in MATH table, organized by size."""
    math_table = math_font['MATH'].table
    mv = math_table.MathVariants
    gname_to_cp = get_glyph_name_to_codepoint(math_font)

    size_data = {}
    for idx in range(16):
        size_data[idx] = {}

    # Process vertical variants
    if mv.VertGlyphCoverage:
        for i, glyph_name in enumerate(mv.VertGlyphCoverage.glyphs):
            cp = gname_to_cp.get(glyph_name)
            if cp is None:
                continue
            rec = mv.VertGlyphConstruction[i]
            if rec.VariantCount and rec.MathGlyphVariantRecord:
                for idx, v in enumerate(rec.MathGlyphVariantRecord):
                    if idx < 16:
                        size_data[idx][cp] = v.VariantGlyph

    # Process horizontal variants
    if mv.HorizGlyphCoverage:
        for i, glyph_name in enumerate(mv.HorizGlyphCoverage.glyphs):
            cp = gname_to_cp.get(glyph_name)
            if cp is None:
                continue
            rec = mv.HorizGlyphConstruction[i]
            if rec.VariantCount and rec.MathGlyphVariantRecord:
                for idx, v in enumerate(rec.MathGlyphVariantRecord):
                    if idx < 16:
                        if cp not in size_data[idx]:
                            size_data[idx][cp] = v.VariantGlyph

    return size_data


def build_size_variant_svg(math_font, size_data, size_index, em_scale=1.0):
    """Build SVG data for a specific size index."""
    data = {}
    for cp, glyph_name in size_data.get(size_index, {}).items():
        info = get_glyph_data_by_name_svg(math_font, glyph_name, em_scale=em_scale)
        if info:
            data[cp] = info
    return data


def build_size_variant_chtml(math_font, size_data, size_index, em_scale=1.0):
    """Build CHTML data for a specific size index."""
    data = {}
    for cp, glyph_name in size_data.get(size_index, {}).items():
        info = get_glyph_data_by_name_chtml(math_font, glyph_name, em_scale=em_scale)
        if info:
            data[cp] = info
    return data


# ========================================================================
# Stretchy parts (lf-tp, rt-bt, ext, mid)
# ========================================================================

def collect_stretchy_parts(math_font):
    """Collect stretchy assembly parts from MATH table."""
    math_table = math_font['MATH'].table
    mv = math_table.MathVariants

    part_glyphs = set()

    if mv.VertGlyphCoverage:
        for i in range(mv.VertGlyphCount):
            rec = mv.VertGlyphConstruction[i]
            if rec.GlyphAssembly:
                for p in rec.GlyphAssembly.PartRecords:
                    part_glyphs.add(p.glyph)

    if mv.HorizGlyphCoverage:
        for i in range(mv.HorizGlyphCount):
            rec = mv.HorizGlyphConstruction[i]
            if rec.GlyphAssembly:
                for p in rec.GlyphAssembly.PartRecords:
                    part_glyphs.add(p.glyph)

    return part_glyphs


def build_stretchy_part_data_svg(math_font, part_glyphs, em_scale=1.0, pua_map=None):
    """Build SVG data for all stretchy part glyphs.

    pua_map: dict {glyph_name: pua_codepoint} for glyphs without Unicode codepoints.
    """
    gname_to_cp = get_glyph_name_to_codepoint(math_font)
    if pua_map is None:
        pua_map = {}
    data = {}

    for gname in part_glyphs:
        cp = gname_to_cp.get(gname) or pua_map.get(gname)
        if cp is not None:
            info = get_glyph_data_by_name_svg(math_font, gname, em_scale=em_scale)
            if info:
                data[cp] = info

    return data


def build_stretchy_part_data_chtml(math_font, part_glyphs, em_scale=1.0, pua_map=None):
    """Build CHTML data for all stretchy part glyphs."""
    gname_to_cp = get_glyph_name_to_codepoint(math_font)
    if pua_map is None:
        pua_map = {}
    data = {}

    for gname in part_glyphs:
        cp = gname_to_cp.get(gname) or pua_map.get(gname)
        if cp is not None:
            info = get_glyph_data_by_name_chtml(math_font, gname, em_scale=em_scale)
            if info:
                data[cp] = info

    return data


# ========================================================================
# WOFF2 generation
# ========================================================================

def generate_woff2(font_path, output_path, codepoints, flavor='woff2'):
    """Generate a WOFF2 subset of a font."""
    try:
        font = TTFont(font_path)
        subsetter = Subsetter()
        subsetter.populate(unicodes=codepoints)
        subsetter.subset(font)
        font.flavor = flavor
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        font.save(output_path)
        font.close()
    except Exception as e:
        print(f"  Warning: WOFF2 generation failed for {output_path}: {e}")


# ========================================================================
# JS template helpers (shared __extends / __assign / etc.)
# ========================================================================

_JS_EXTENDS = '''\
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();'''

_JS_ASSIGN = '''\
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};'''

_JS_READ = '''\
var __read = (this && this.__read) || function (o, n) {
    var m = typeof Symbol === "function" && o[Symbol.iterator];
    if (!m) return o;
    var i = m.call(o), r, ar = [], e;
    try {
        while ((n === void 0 || n-- > 0) && !(r = i.next()).done) ar.push(r.value);
    }
    catch (error) { e = { error: error }; }
    finally {
        try {
            if (r && !r.done && (m = i["return"])) m.call(i);
        }
        finally { if (e) throw e.error; }
    }
    return ar;
};'''

_JS_SPREAD_ARRAY = '''\
var __spreadArray = (this && this.__spreadArray) || function (to, from, pack) {
    if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
        if (ar || !(i in from)) {
            if (!ar) ar = Array.prototype.slice.call(from, 0, i);
            ar[i] = from[i];
        }
    }
    return to.concat(ar || Array.prototype.slice.call(from));
};'''

_JS_VALUES = '''\
var __values = (this && this.__values) || function(o) {
    var s = typeof Symbol === "function" && Symbol.iterator, m = s && o[s], i = 0;
    if (m) return m.call(o);
    if (o && typeof o.length === "number") return {
        next: function () {
            if (o && i >= o.length) o = void 0;
            return { value: o && o[i++], done: !o };
        }
    };
    throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
};'''


# ========================================================================
# JS file writers (parameterized)
# ========================================================================

def write_common_js(filepath, font_name, x_height=0.500):
    """Write common.js with the font mixin.

    font_name: JS class name, e.g. "MathJaxPTSansFont"
    x_height: x-height parameter for the font
    """
    mixin_name = f"Common{font_name}Mixin"
    content = f'''"use strict";
{_JS_EXTENDS}
{_JS_ASSIGN}
{_JS_READ}
{_JS_SPREAD_ARRAY}
Object.defineProperty(exports, "__esModule", {{ value: true }});
exports.{mixin_name} = {mixin_name};
var FontData_js_1 = require("@mathjax/src/cjs/output/common/FontData.js");
function {mixin_name}(Base) {{
    var _a;
    return _a = (function (_super) {{
            __extends(class_1, _super);
            function class_1() {{
                return _super !== null && _super.apply(this, arguments) || this;
            }}
            return class_1;
        }}(Base)),
        _a.defaultVariants = __spreadArray(__spreadArray([], __read(FontData_js_1.FontData.defaultVariants), false), [
            ['-size3', 'normal'],
            ['-size4', 'normal'],
            ['-size5', 'normal'],
            ['-size6', 'normal'],
            ['-size7', 'normal'],
            ['-size8', 'normal'],
            ['-size9', 'normal'],
            ['-size10', 'normal'],
            ['-size11', 'normal'],
            ['-size12', 'normal'],
            ['-size13', 'normal'],
            ['-size14', 'normal'],
            ['-size15', 'normal'],
            ['-tex-calligraphic', 'script'],
            ['-tex-bold-calligraphic', 'bold-script'],
            ['-lf-tp', 'normal'],
            ['-rt-bt', 'normal'],
            ['-ext', 'normal'],
            ['-mid', 'normal'],
            ['-up', 'normal'],
            ['-dup', 'normal']
        ], false),
        _a.defaultCssFonts = __assign(__assign({{}}, FontData_js_1.FontData.defaultCssFonts), {{ '-size3': ['serif', false, false], '-size4': ['serif', false, false], '-size5': ['serif', false, false], '-size6': ['serif', false, false], '-size7': ['serif', false, false], '-size8': ['serif', false, false], '-size9': ['serif', false, false], '-size10': ['serif', false, false], '-size11': ['serif', false, false], '-size12': ['serif', false, false], '-size13': ['serif', false, false], '-size14': ['serif', false, false], '-size15': ['serif', false, false], '-lf-tp': ['serif', false, false], '-rt-bt': ['serif', false, false], '-ext': ['serif', false, false], '-mid': ['serif', false, false], '-up': ['serif', false, false], '-dup': ['serif', false, false] }}),
        _a.defaultAccentMap = {{
            0x005E: '\\u02C6',
            0x007E: '\\u02DC',
            0x0300: '\\u02CB',
            0x0301: '\\u02CA',
            0x0302: '\\u02C6',
            0x0303: '\\u02DC',
            0x0304: '\\u02C9',
            0x0306: '\\u02D8',
            0x0307: '\\u02D9',
            0x0308: '\\u00A8',
            0x030A: '\\u02DA',
            0x030C: '\\u02C7',
            0x2192: '\\u20D7'
        }},
        _a.defaultParams = __assign(__assign({{}}, FontData_js_1.FontData.defaultParams), {{ surd_height: 0.075, rule_thickness: 0.075, x_height: {x_height} }}),
        _a.defaultSizeVariants = [
            'normal', '-smallop', '-largeop', '-size3', '-size4', '-size5', '-size6', '-size7', '-size8', '-size9', '-size10', '-size11', '-size12', '-size13', '-size14', '-size15'
        ],
        _a.defaultStretchVariants = [
            'normal', '-ext', '-lf-tp', '-rt-bt', '-mid'
        ],
        _a;
}}
'''
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)


# Variant cache IDs used by both SVG and CHTML
VARIANT_CACHE_IDS = {
    'normal': 'N',
    'bold': 'B',
    'italic': 'I',
    'bold-italic': 'BI',
    'monospace': 'M',
    '-smallop': 'SO',
    '-largeop': 'LO',
    '-size3': 'S3',
    '-size4': 'S4',
    '-size5': 'S5',
    '-size6': 'S6',
    '-size7': 'S7',
    '-size8': 'S8',
    '-size9': 'S9',
    '-size10': 'S10',
    '-size11': 'S11',
    '-size12': 'S12',
    '-size13': 'S13',
    '-size14': 'S14',
    '-size15': 'S15',
    '-lf-tp': 'LT',
    '-rt-bt': 'RB',
    '-ext': 'E',
    '-mid': 'MD',
    '-up': 'U',
    '-dup': 'D',
}


def _build_default_chars_block(indent="    "):
    """Build the defaultChars JS block (same for SVG and CHTML, except path prefix)."""
    lines = []
    lines.append(f"{indent}'normal': normal_js_1.normal,")
    lines.append(f"{indent}'bold': bold_js_1.bold,")
    lines.append(f"{indent}'italic': italic_js_1.italic,")
    lines.append(f"{indent}'bold-italic': bold_italic_js_1.boldItalic,")
    lines.append(f"{indent}'monospace': monospace_js_1.monospace,")
    lines.append(f"{indent}'-smallop': smallop_js_1.smallop,")
    lines.append(f"{indent}'-largeop': largeop_js_1.largeop,")
    for sz in range(3, 16):
        lines.append(f"{indent}'-size{sz}': size{sz}_js_1.size{sz},")
    lines.append(f"{indent}'-lf-tp': lf_tp_js_1.lfTp,")
    lines.append(f"{indent}'-rt-bt': rt_bt_js_1.rtBt,")
    lines.append(f"{indent}'-ext': ext_js_1.ext,")
    lines.append(f"{indent}'-mid': mid_js_1.mid,")
    lines.append(f"{indent}'-up': up_js_1.up,")
    lines.append(f"{indent}'-dup': dup_js_1.dup")
    return '\n'.join(lines)


def _build_require_block(subdir):
    """Build the require() statements for all variant files."""
    lines = []
    lines.append(f'var normal_js_1 = require("./{subdir}/normal.js");')
    lines.append(f'var bold_js_1 = require("./{subdir}/bold.js");')
    lines.append(f'var italic_js_1 = require("./{subdir}/italic.js");')
    lines.append(f'var bold_italic_js_1 = require("./{subdir}/bold-italic.js");')
    lines.append(f'var monospace_js_1 = require("./{subdir}/monospace.js");')
    lines.append(f'var smallop_js_1 = require("./{subdir}/smallop.js");')
    lines.append(f'var largeop_js_1 = require("./{subdir}/largeop.js");')
    for sz in range(3, 16):
        lines.append(f'var size{sz}_js_1 = require("./{subdir}/size{sz}.js");')
    lines.append(f'var lf_tp_js_1 = require("./{subdir}/lf-tp.js");')
    lines.append(f'var rt_bt_js_1 = require("./{subdir}/rt-bt.js");')
    lines.append(f'var ext_js_1 = require("./{subdir}/ext.js");')
    lines.append(f'var mid_js_1 = require("./{subdir}/mid.js");')
    lines.append(f'var up_js_1 = require("./{subdir}/up.js");')
    lines.append(f'var dup_js_1 = require("./{subdir}/dup.js");')
    lines.append(f'var delimiters_js_1 = require("./{subdir}/delimiters.js");')
    return '\n'.join(lines)


def _build_variant_cache_ids_block(css_prefix, indent="    "):
    """Build the variantCacheIds JS object literal."""
    lines = []
    for variant, letter in VARIANT_CACHE_IDS.items():
        lines.append(f"{indent}'{variant}': '{letter}',")
    # Remove trailing comma from last line
    lines[-1] = lines[-1].rstrip(',')
    return '\n'.join(lines)


def write_svg_js(filepath, font_name, font_id, css_prefix):
    """Write the SVG font class file.

    font_name: JS class name, e.g. "MathJaxPTSansFont"
    font_id: package name, e.g. "mathjax-ptsans"
    css_prefix: cache ID prefix, e.g. "PTSA"
    """
    mixin_name = f"Common{font_name}Mixin"
    requires = _build_require_block("svg")
    chars_block = _build_default_chars_block("        ")
    cache_ids_block = _build_variant_cache_ids_block(css_prefix, "        ")

    content = f'''"use strict";
{_JS_EXTENDS}
{_JS_ASSIGN}
{_JS_VALUES}
Object.defineProperty(exports, "__esModule", {{ value: true }});
exports.{font_name} = void 0;
var FontData_js_1 = require("@mathjax/src/cjs/output/svg/FontData.js");
var common_js_1 = require("./common.js");
{requires}
var Base = (0, common_js_1.{mixin_name})(FontData_js_1.SvgFontData);
var {font_name} = (function (_super) {{
    __extends({font_name}, _super);
    function {font_name}(options) {{
        var e_1, _a;
        if (options === void 0) {{ options = {{}}; }}
        var _this = _super.call(this, options) || this;
        var CLASS = _this.constructor;
        try {{
            for (var _b = __values(Object.keys(_this.variant)), _c = _b.next(); !_c.done; _c = _b.next()) {{
                var variant = _c.value;
                _this.variant[variant].cacheID = '{css_prefix}-' + (CLASS.variantCacheIds[variant] || 'N');
            }}
        }}
        catch (e_1_1) {{ e_1 = {{ error: e_1_1 }}; }}
        finally {{
            try {{
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }}
            finally {{ if (e_1) throw e_1.error; }}
        }}
        return _this;
    }}
    {font_name}.NAME = '{font_name.replace("Font", "")}';
    {font_name}.OPTIONS = __assign(__assign({{}}, Base.OPTIONS), {{ dynamicPrefix: '@mathjax/{font_id}-font/js/svg/dynamic' }});
    {font_name}.defaultDelimiters = delimiters_js_1.delimiters;
    {font_name}.defaultChars = {{
{chars_block}
    }};
    {font_name}.variantCacheIds = {{
{cache_ids_block}
    }};
    return {font_name};
}}(Base));
exports.{font_name} = {font_name};
'''
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)


def write_chtml_js(filepath, font_name, font_id, css_prefix):
    """Write the CHTML font class file.

    font_name: JS class name, e.g. "MathJaxPTSansFont"
    font_id: package name, e.g. "mathjax-ptsans"
    css_prefix: cache ID prefix, e.g. "PTSA"
    """
    mixin_name = f"Common{font_name}Mixin"
    requires = _build_require_block("chtml")
    chars_block = _build_default_chars_block("        ")

    # Build variant letters block (same as cache IDs but with '-mid' -> 'M-a')
    variant_letters = dict(VARIANT_CACHE_IDS)
    variant_letters['-mid'] = 'M-a'
    variant_letters['normal'] = ''
    vl_lines = []
    for variant, letter in variant_letters.items():
        vl_lines.append(f"        '{variant}': '{letter}',")
    vl_lines[-1] = vl_lines[-1].rstrip(',')
    variant_letters_block = '\n'.join(vl_lines)

    # Build styles block
    style_entries = []
    style_entries.append(f"        'mjx-container[jax=\"CHTML\"] > mjx-math.{css_prefix}-N[breakable] > *': {{ 'font-family': 'MJX-{css_prefix}-ZERO, MJX-{css_prefix}-N' }}")
    for variant, letter in variant_letters.items():
        if variant == 'normal':
            letter = 'N'
        if not letter:
            continue
        style_entries.append(f"        '.{css_prefix}-{letter}': {{ 'font-family': 'MJX-{css_prefix}-ZERO, MJX-{css_prefix}-{letter}' }}")
    # Add the normal one too
    style_entries.insert(1, f"        '.{css_prefix}-N': {{ 'font-family': 'MJX-{css_prefix}-ZERO, MJX-{css_prefix}-N' }}")
    styles_block = ',\n'.join(style_entries)

    # Build fonts block (just the 5 main variants)
    font_face_entries = []
    font_slug = font_id.replace('mathjax-', '')
    for suffix, letter in [('ZERO', 'zero'), ('N', 'n'), ('B', 'b'), ('I', 'i'), ('BI', 'bi')]:
        font_face_entries.append(f'''\
        '@font-face /* MJX-{css_prefix}-{suffix} */': {{
            'font-family': 'MJX-{css_prefix}-{suffix}',
            src: 'url("%%URL%%/mjx-{font_slug}-{letter}.woff2") format("woff2")'
        }}''')
    fonts_block = ',\n'.join(font_face_entries)

    content = f'''"use strict";
{_JS_EXTENDS}
{_JS_ASSIGN}
{_JS_READ}
{_JS_SPREAD_ARRAY}
Object.defineProperty(exports, "__esModule", {{ value: true }});
exports.{font_name} = void 0;
var FontData_js_1 = require("@mathjax/src/cjs/output/chtml/FontData.js");
var common_js_1 = require("./common.js");
{requires}
var Base = (0, common_js_1.{mixin_name})(FontData_js_1.ChtmlFontData);
var {font_name} = (function (_super) {{
    __extends({font_name}, _super);
    function {font_name}() {{
        var _this = _super.apply(this, __spreadArray([], __read(arguments), false)) || this;
        _this.cssFontPrefix = '{css_prefix}';
        return _this;
    }}
    {font_name}.NAME = '{font_name.replace("Font", "")}';
    {font_name}.OPTIONS = __assign(__assign({{}}, Base.OPTIONS), {{ fontURL: '@mathjax/{font_id}-font/js/chtml/woff2', dynamicPrefix: '@mathjax/{font_id}-font/js/chtml/dynamic' }});
    {font_name}.defaultCssFamilyPrefix = 'MJX-{css_prefix}-ZERO';
    {font_name}.defaultVariantLetters = {{
{variant_letters_block}
    }};
    {font_name}.defaultDelimiters = delimiters_js_1.delimiters;
    {font_name}.defaultChars = {{
{chars_block}
    }};
    {font_name}.defaultStyles = __assign(__assign({{}}, FontData_js_1.ChtmlFontData.defaultStyles), {{
{styles_block}
    }});
    {font_name}.defaultFonts = __assign(__assign({{}}, FontData_js_1.ChtmlFontData.defaultFonts), {{
{fonts_block}
    }});
    return {font_name};
}}(Base));
exports.{font_name} = {font_name};
'''
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)


def write_browser_entry(filepath, font_name, font_type):
    """Write browser entry point (svg.js or chtml.js at package root).

    font_name: JS class name, e.g. "MathJaxPTSansFont"
    font_type: "svg" or "chtml"
    """
    content = f'''"use strict";
Object.defineProperty(exports, "__esModule", {{ value: true }});
exports.{font_name} = void 0;
var font = require("./cjs/{font_type}.js");
exports.{font_name} = font.{font_name};
'''
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)


def write_package_json(filepath, font_id, font_name):
    """Write package.json.

    font_id: package name, e.g. "mathjax-ptsans"
    font_name: display name for description
    """
    pkg = {
        "name": f"@mathjax/{font_id}-font",
        "version": "4.1.0",
        "description": f"{font_name} font for MathJax v4",
        "license": "OFL-1.1",
        "keywords": ["MathJax", "fonts", font_name],
        "files": ["cjs", "chtml", "chtml.js", "svg.js"],
        "exports": {
            "./js/*": {"require": "./cjs/*"},
            "./*": "./*"
        }
    }
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(pkg, f, indent=2)
        f.write('\n')


# ========================================================================
# Boilerplate generation (webpack, sre, default.js)
# ========================================================================

def write_boilerplate(output_dir, font_id, font_name):
    """Generate default.js, sre/speech-worker.js, webpack configs, entry points.

    Uses the proven format from our PT Sans/Lato builds that works with
    MathJax 4's component loader system.

    font_id: package name, e.g. "mathjax-ptsans"
    font_name: JS class name, e.g. "MathJaxPTSansFont"
    """
    # cjs/svg/default.js
    default_svg_path = os.path.join(output_dir, "cjs/svg/default.js")
    os.makedirs(os.path.dirname(default_svg_path), exist_ok=True)
    with open(default_svg_path, 'w') as f:
        f.write(f'''"use strict";
Object.defineProperty(exports, "__esModule", {{ value: true }});
exports.Font = void 0;
var svg_js_1 = require("../svg.js");
exports.Font = {{ fontName: '{font_id}', DefaultFont: svg_js_1.{font_name} }};
''')

    # cjs/chtml/default.js
    default_chtml_path = os.path.join(output_dir, "cjs/chtml/default.js")
    os.makedirs(os.path.dirname(default_chtml_path), exist_ok=True)
    with open(default_chtml_path, 'w') as f:
        f.write(f'''"use strict";
Object.defineProperty(exports, "__esModule", {{ value: true }});
exports.Font = void 0;
var chtml_js_1 = require("../chtml.js");
exports.Font = {{ fontName: '{font_id}', DefaultFont: chtml_js_1.{font_name} }};
''')

    # sre/speech-worker.js
    sre_dir = os.path.join(output_dir, "sre")
    os.makedirs(sre_dir, exist_ok=True)
    with open(os.path.join(sre_dir, "speech-worker.js"), 'w') as f:
        f.write('self.onmessage = function(e) { self.postMessage({id: e.data.id, result: \'\'}); };\n')
        f.write('self.postMessage({id: \'ready\'});\n')

    # build/ directory
    build_dir = os.path.join(output_dir, "build")
    os.makedirs(build_dir, exist_ok=True)

    # build/webpack.config.cjs (full bundle with a11y)
    with open(os.path.join(build_dir, "webpack.config.cjs"), 'w') as f:
        f.write(f'''const path = require('path');
const webpack = require('webpack');
const TerserPlugin = require('terser-webpack-plugin');
module.exports = {{
  name: 'tex-mml-svg-{font_id}',
  entry: path.resolve(__dirname, 'tex-mml-svg-{font_id}.js'),
  output: {{ path: path.resolve(__dirname, '..'), filename: 'tex-mml-svg-{font_id}.js' }},
  target: ['web', 'es5'],
  plugins: [
    new webpack.NormalModuleReplacementPlugin(/#default-font/, function(r) {{ r.request = r.request.replace(/#default-font/, path.resolve(__dirname, '..', 'cjs')); }}),
    new webpack.NormalModuleReplacementPlugin(/@mathjax\\/mathjax-newcm-font\\/cjs/, function(r) {{ r.request = r.request.replace(/@mathjax\\/mathjax-newcm-font\\/cjs/, path.resolve(__dirname, '..', 'cjs')); }})
  ],
  resolve: {{ alias: {{ '#default-font': path.resolve(__dirname, '..', 'cjs') }}, fallback: {{}} }},
  performance: {{ hints: false }},
  optimization: {{ minimize: true, minimizer: [new TerserPlugin({{ extractComments: false, terserOptions: {{ output: {{ ascii_only: true }} }} }})] }},
  mode: 'production'
}};
''')

    # build/webpack-nosre.config.cjs (no accessibility/SRE)
    with open(os.path.join(build_dir, "webpack-nosre.config.cjs"), 'w') as f:
        f.write(f'''const path = require('path');
const webpack = require('webpack');
const TerserPlugin = require('terser-webpack-plugin');
module.exports = {{
  name: 'tex-mml-svg-{font_id}-nosre',
  entry: path.resolve(__dirname, 'tex-mml-svg-{font_id}-nosre.js'),
  output: {{ path: path.resolve(__dirname, '..'), filename: 'tex-mml-svg-{font_id}-nosre.js' }},
  target: ['web', 'es5'],
  plugins: [
    new webpack.NormalModuleReplacementPlugin(/#default-font/, function(r) {{ r.request = r.request.replace(/#default-font/, path.resolve(__dirname, '..', 'cjs')); }}),
    new webpack.NormalModuleReplacementPlugin(/@mathjax\\/mathjax-newcm-font\\/cjs/, function(r) {{ r.request = r.request.replace(/@mathjax\\/mathjax-newcm-font\\/cjs/, path.resolve(__dirname, '..', 'cjs')); }})
  ],
  resolve: {{ alias: {{ '#default-font': path.resolve(__dirname, '..', 'cjs') }}, fallback: {{}} }},
  performance: {{ hints: false }},
  optimization: {{ minimize: true, minimizer: [new TerserPlugin({{ extractComments: false, terserOptions: {{ output: {{ ascii_only: true }} }} }})] }},
  mode: 'production'
}};
''')

    # build/tex-mml-svg-{font_id}.js (full entry point with boldsymbol + a11y)
    with open(os.path.join(build_dir, f"tex-mml-svg-{font_id}.js"), 'w') as f:
        f.write(f'''"use strict";
var init_js_1 = require("@mathjax/src/components/cjs/startup/init.js");
var loader_js_1 = require("@mathjax/src/cjs/components/loader.js");
require("@mathjax/src/components/cjs/core/core.js");
require("@mathjax/src/components/cjs/input/tex/tex.js");
require("@mathjax/src/components/cjs/input/tex/extensions/boldsymbol/boldsymbol.js");
require("@mathjax/src/components/cjs/input/mml/mml.js");
var svg_js_1 = require("@mathjax/src/components/cjs/output/svg/svg.js");
require("@mathjax/src/components/cjs/ui/menu/menu.js");
require("@mathjax/src/components/cjs/a11y/util.js");
require("@mathjax/src/components/cjs/a11y/semantic-enrich/semantic-enrich.js");
require("@mathjax/src/components/cjs/a11y/complexity/complexity.js");
require("@mathjax/src/components/cjs/a11y/explorer/explorer.js");
require("@mathjax/src/components/cjs/a11y/assistive-mml/assistive-mml.js");
loader_js_1.Loader.preLoaded('loader','startup','core','input/tex','[tex]/boldsymbol','input/mml','output/svg','ui/menu','a11y/util','a11y/sre','a11y/semantic-enrich','a11y/complexity','a11y/explorer','a11y/assistive-mml','a11y/speech');
loader_js_1.Loader.saveVersion('tex-mml-svg-{font_id}');
(0, svg_js_1.loadFont)(init_js_1.startup, true);
''')

    # build/tex-mml-svg-{font_id}-nosre.js (no SRE, no a11y)
    with open(os.path.join(build_dir, f"tex-mml-svg-{font_id}-nosre.js"), 'w') as f:
        f.write(f'''"use strict";
var init_js_1 = require("@mathjax/src/components/cjs/startup/init.js");
var loader_js_1 = require("@mathjax/src/cjs/components/loader.js");
require("@mathjax/src/components/cjs/core/core.js");
require("@mathjax/src/components/cjs/input/tex/tex.js");
require("@mathjax/src/components/cjs/input/tex/extensions/boldsymbol/boldsymbol.js");
require("@mathjax/src/components/cjs/input/mml/mml.js");
var svg_js_1 = require("@mathjax/src/components/cjs/output/svg/svg.js");
loader_js_1.Loader.preLoaded('loader','startup','core','input/tex','[tex]/boldsymbol','input/mml','output/svg');
loader_js_1.Loader.saveVersion('tex-mml-svg-{font_id}-nosre');
(0, svg_js_1.loadFont)(init_js_1.startup, true);
''')


# ========================================================================
# High-level build_all_variants helper
# ========================================================================

def build_all_variants(output_dir, text_fonts, math_font, text_ranges, math_ranges,
                       extra_math=None, middle_layer_data=None, ic_map=None,
                       em_scale=1.0, font_name="MathJaxFont", font_id="mathjax-font",
                       css_prefix="MJX", x_height=0.500, text_source='text',
                       text_font_paths=None, woff2_slug=None):
    """Build all SVG + CHTML variant files, size variants, delimiters, stretchy parts.

    text_fonts: dict with keys 'regular', 'bold', 'italic', 'bold_italic' -> TTFont objects
    math_font: TTFont for the math font (must have a MATH table)
    text_ranges: list of (start, end) codepoint ranges for text font
    math_ranges: list of (start, end) codepoint ranges for math font
    extra_math: list of extra math codepoints to include
    middle_layer_data: dict with optional keys 'normal', 'bold', 'italic', 'bold_italic'
        each mapping to {codepoint: {height, depth, width, path, source}} dicts
        OR a single dict (used for all variants)
    ic_map: italic correction map (if None, extracted from math_font)
    em_scale: scale factor for metrics
    font_name: JS class name, e.g. "MathJaxPTSansFont"
    font_id: package name, e.g. "mathjax-ptsans"
    css_prefix: cache ID prefix, e.g. "PTSA"
    x_height: x-height parameter
    text_source: source label for text font glyphs
    text_font_paths: dict with keys 'regular', 'bold', 'italic', 'bold_italic' -> file paths
        (needed for WOFF2 generation)
    woff2_slug: short name for WOFF2 files, e.g. "lato" -> mjx-lato-n.woff2
        If None, derived from font_id by stripping "mathjax-" prefix.
    """
    if extra_math is None:
        extra_math = DEFAULT_EXTRA_MATH

    # Normalize middle_layer_data: if it's a flat dict, wrap it
    if middle_layer_data is not None and not isinstance(middle_layer_data.get('normal', None), dict):
        # Check if this looks like a per-variant dict or a flat glyph dict
        # If any key is an int (codepoint), it's a flat dict
        sample_key = next(iter(middle_layer_data), None)
        if isinstance(sample_key, int):
            # Flat dict -- use for all variants
            _ml = middle_layer_data
            middle_layer_data = {
                'normal': _ml,
                'bold': _ml,
                'italic': _ml,
                'bold_italic': _ml,
            }

    def get_middle_layer(variant_key):
        if middle_layer_data is None:
            return None
        return middle_layer_data.get(variant_key, None)

    # Extract and override italic corrections
    if ic_map is None:
        ic_map = extract_italic_corrections(math_font)
        override_integral_ics(ic_map)

    # Extract top accent skew values for accent centering
    # Use MATH table skews as base (for math-only glyphs like Greek, operators)
    sk_map_math = extract_top_accent_skews(math_font)
    print(f"  MATH table accent skews: {len(sk_map_math)} glyphs")

    # Compute visual skews from the actual text fonts (more accurate for text glyphs,
    # especially italic — the MATH font's TopAccentAttachment doesn't match the
    # text font's glyph shapes)
    sk_maps_text = {}
    for variant_key in ['regular', 'bold', 'italic', 'bold_italic']:
        sk_maps_text[variant_key] = compute_visual_skews(text_fonts[variant_key])
    print(f"  Text font visual skews: {len(sk_maps_text['regular'])} regular, {len(sk_maps_text['italic'])} italic")

    def apply_all_corrections(data, variant_key='regular'):
        """Apply IC and sk to variant data.
        Text glyphs get sk from the text font; math glyphs get sk from MATH table."""
        apply_italic_corrections(data, ic_map)
        # First apply MATH table skews (covers math-only glyphs)
        apply_skews(data, sk_map_math)
        # Then override with text font visual skews (more accurate for rendered glyphs)
        apply_skews(data, sk_maps_text.get(variant_key, {}))

    # ========== DELIMITERS (build early to get pua_map for variant injection) ==========
    print("Building delimiters...")
    delimiters, pua_map = build_delimiters(math_font, em_scale=em_scale)

    # Build PUA glyph data to inject into variant files
    # MathJax looks up stretch piece codepoints in the normal variant, not just lf-tp/ext
    pua_glyph_data = {}
    if pua_map:
        gs = math_font.getGlyphSet()
        for glyph_name, pua_cp in pua_map.items():
            info = get_glyph_data_by_name_svg(math_font, glyph_name, em_scale=em_scale)
            if info:
                info['source'] = 'pua-assembly'
                pua_glyph_data[pua_cp] = info
        print(f"    PUA assembly glyphs to inject: {len(pua_glyph_data)}")

    # ========== SVG VARIANTS ==========
    print("Building SVG normal variant...")
    svg_normal = build_variant_data_svg(
        text_fonts['regular'], math_font, text_ranges, math_ranges, extra_math,
        middle_layer_data=get_middle_layer('normal'),
        text_source=text_source, em_scale=em_scale
    )
    apply_all_corrections(svg_normal, 'regular')
    svg_normal.update(pua_glyph_data)  # inject PUA assembly glyphs
    # Report source breakdown
    sources = {}
    for cp, info in svg_normal.items():
        s = info.get('source', 'unknown')
        sources[s] = sources.get(s, 0) + 1
    print(f"  Sources: {sources}")
    write_svg_variant_file(
        os.path.join(output_dir, "cjs/svg/normal.js"), "normal", svg_normal
    )

    print("Building SVG bold variant...")
    svg_bold = build_variant_data_svg(
        text_fonts['bold'], math_font, text_ranges, math_ranges, extra_math,
        middle_layer_data=get_middle_layer('bold'),
        text_source=text_source, em_scale=em_scale
    )
    apply_all_corrections(svg_bold, 'bold')
    svg_bold.update(pua_glyph_data)
    write_svg_variant_file(
        os.path.join(output_dir, "cjs/svg/bold.js"), "bold", svg_bold
    )

    print("Building SVG italic variant...")
    svg_italic = build_variant_data_svg(
        text_fonts['italic'], math_font, text_ranges, math_ranges, extra_math,
        middle_layer_data=get_middle_layer('italic'),
        text_source=text_source, em_scale=em_scale
    )
    apply_all_corrections(svg_italic, 'italic')
    svg_italic.update(pua_glyph_data)
    write_svg_variant_file(
        os.path.join(output_dir, "cjs/svg/italic.js"), "italic", svg_italic
    )

    print("Building SVG bold-italic variant...")
    svg_bold_italic = build_variant_data_svg(
        text_fonts['bold_italic'], math_font, text_ranges, math_ranges, extra_math,
        middle_layer_data=get_middle_layer('bold_italic'),
        text_source=text_source, em_scale=em_scale
    )
    apply_all_corrections(svg_bold_italic, 'bold_italic')
    svg_bold_italic.update(pua_glyph_data)
    write_svg_variant_file(
        os.path.join(output_dir, "cjs/svg/bold-italic.js"), "boldItalic", svg_bold_italic
    )

    # Monospace (empty)
    print("Building SVG monospace variant...")
    write_empty_variant_file(
        os.path.join(output_dir, "cjs/svg/monospace.js"), "monospace"
    )

    # ========== SIZE VARIANTS ==========
    print("Collecting size variant data from MATH table...")
    size_data = collect_size_variant_glyphs(math_font)

    print("Building SVG smallop...")
    svg_smallop = build_size_variant_svg(math_font, size_data, 0, em_scale=em_scale)
    apply_all_corrections(svg_smallop)
    write_svg_variant_file(
        os.path.join(output_dir, "cjs/svg/smallop.js"), "smallop", svg_smallop
    )

    print("Building SVG largeop...")
    svg_largeop = build_size_variant_svg(math_font, size_data, 1, em_scale=em_scale)
    apply_all_corrections(svg_largeop)
    write_svg_variant_file(
        os.path.join(output_dir, "cjs/svg/largeop.js"), "largeop", svg_largeop
    )

    for sz in range(3, 16):
        actual_idx = sz - 1
        print(f"Building SVG size{sz}...")
        svg_size = build_size_variant_svg(math_font, size_data, actual_idx, em_scale=em_scale)
        apply_all_corrections(svg_size)
        write_svg_variant_file(
            os.path.join(output_dir, f"cjs/svg/size{sz}.js"), f"size{sz}", svg_size
        )

    # ========== WRITE DELIMITERS (already built above for pua_map) ==========
    write_delimiters_file(
        os.path.join(output_dir, "cjs/svg/delimiters.js"), delimiters
    )
    write_delimiters_file(
        os.path.join(output_dir, "cjs/chtml/delimiters.js"), delimiters
    )

    # ========== STRETCHY PARTS ==========
    print("Building stretchy part variants...")
    part_glyphs = collect_stretchy_parts(math_font)

    all_parts_svg = build_stretchy_part_data_svg(math_font, part_glyphs, em_scale=em_scale, pua_map=pua_map)

    write_svg_variant_file(
        os.path.join(output_dir, "cjs/svg/lf-tp.js"), "lfTp", all_parts_svg
    )
    write_svg_variant_file(
        os.path.join(output_dir, "cjs/svg/rt-bt.js"), "rtBt", all_parts_svg
    )
    write_svg_variant_file(
        os.path.join(output_dir, "cjs/svg/ext.js"), "ext", all_parts_svg
    )
    write_svg_variant_file(
        os.path.join(output_dir, "cjs/svg/mid.js"), "mid", all_parts_svg
    )
    write_empty_variant_file(os.path.join(output_dir, "cjs/svg/up.js"), "up")
    write_empty_variant_file(os.path.join(output_dir, "cjs/svg/dup.js"), "dup")

    # ========== CHTML VARIANTS ==========
    print("Building CHTML normal variant...")
    chtml_normal = build_variant_data_chtml(
        text_fonts['regular'], math_font, text_ranges, math_ranges, extra_math,
        middle_layer_data=get_middle_layer('normal'), em_scale=em_scale
    )
    write_chtml_variant_file(
        os.path.join(output_dir, "cjs/chtml/normal.js"), "normal", chtml_normal
    )

    print("Building CHTML bold variant...")
    chtml_bold = build_variant_data_chtml(
        text_fonts['bold'], math_font, text_ranges, math_ranges, extra_math,
        middle_layer_data=get_middle_layer('bold'), em_scale=em_scale
    )
    write_chtml_variant_file(
        os.path.join(output_dir, "cjs/chtml/bold.js"), "bold", chtml_bold
    )

    print("Building CHTML italic variant...")
    chtml_italic = build_variant_data_chtml(
        text_fonts['italic'], math_font, text_ranges, math_ranges, extra_math,
        middle_layer_data=get_middle_layer('italic'), em_scale=em_scale
    )
    write_chtml_variant_file(
        os.path.join(output_dir, "cjs/chtml/italic.js"), "italic", chtml_italic
    )

    print("Building CHTML bold-italic variant...")
    chtml_bold_italic = build_variant_data_chtml(
        text_fonts['bold_italic'], math_font, text_ranges, math_ranges, extra_math,
        middle_layer_data=get_middle_layer('bold_italic'), em_scale=em_scale
    )
    write_chtml_variant_file(
        os.path.join(output_dir, "cjs/chtml/bold-italic.js"), "boldItalic", chtml_bold_italic
    )

    write_empty_variant_file(
        os.path.join(output_dir, "cjs/chtml/monospace.js"), "monospace"
    )

    # CHTML size variants
    print("Building CHTML size variants...")
    chtml_smallop = build_size_variant_chtml(math_font, size_data, 0, em_scale=em_scale)
    write_chtml_variant_file(
        os.path.join(output_dir, "cjs/chtml/smallop.js"), "smallop", chtml_smallop
    )

    chtml_largeop = build_size_variant_chtml(math_font, size_data, 1, em_scale=em_scale)
    write_chtml_variant_file(
        os.path.join(output_dir, "cjs/chtml/largeop.js"), "largeop", chtml_largeop
    )

    for sz in range(3, 16):
        actual_idx = sz - 1
        chtml_size = build_size_variant_chtml(math_font, size_data, actual_idx, em_scale=em_scale)
        write_chtml_variant_file(
            os.path.join(output_dir, f"cjs/chtml/size{sz}.js"), f"size{sz}", chtml_size
        )

    # CHTML stretchy parts
    all_parts_chtml = build_stretchy_part_data_chtml(math_font, part_glyphs, em_scale=em_scale, pua_map=pua_map)

    write_chtml_variant_file(
        os.path.join(output_dir, "cjs/chtml/lf-tp.js"), "lfTp", all_parts_chtml
    )
    write_chtml_variant_file(
        os.path.join(output_dir, "cjs/chtml/rt-bt.js"), "rtBt", all_parts_chtml
    )
    write_chtml_variant_file(
        os.path.join(output_dir, "cjs/chtml/ext.js"), "ext", all_parts_chtml
    )
    write_chtml_variant_file(
        os.path.join(output_dir, "cjs/chtml/mid.js"), "mid", all_parts_chtml
    )
    write_empty_variant_file(os.path.join(output_dir, "cjs/chtml/up.js"), "up")
    write_empty_variant_file(os.path.join(output_dir, "cjs/chtml/dup.js"), "dup")

    # ========== FRAMEWORK JS FILES ==========
    print("Writing framework JS files...")
    write_common_js(os.path.join(output_dir, "cjs/common.js"), font_name, x_height=x_height)
    write_svg_js(os.path.join(output_dir, "cjs/svg.js"), font_name, font_id, css_prefix)
    write_chtml_js(os.path.join(output_dir, "cjs/chtml.js"), font_name, font_id, css_prefix)

    # Browser entry points
    write_browser_entry(os.path.join(output_dir, "svg.js"), font_name, "svg")
    write_browser_entry(os.path.join(output_dir, "chtml.js"), font_name, "chtml")

    # package.json
    write_package_json(os.path.join(output_dir, "package.json"), font_id, font_name)

    # Boilerplate (webpack, sre, default.js)
    write_boilerplate(output_dir, font_id, font_name)

    # ========== WOFF2 FONTS ==========
    if text_font_paths:
        if woff2_slug is None:
            woff2_slug = font_id.replace('mathjax-', '')

        print("Generating WOFF2 fonts...")
        woff2_dir = os.path.join(output_dir, "chtml/woff2")
        os.makedirs(woff2_dir, exist_ok=True)

        normal_cps = list(svg_normal.keys())
        bold_cps = list(svg_bold.keys())
        italic_cps = list(svg_italic.keys())
        bold_italic_cps = list(svg_bold_italic.keys())

        reg_cmap = text_fonts['regular'].getBestCmap()
        bold_cmap = text_fonts['bold'].getBestCmap()
        italic_cmap = text_fonts['italic'].getBestCmap()
        bi_cmap = text_fonts['bold_italic'].getBestCmap()

        lato_cps_normal = [cp for cp in normal_cps if cp in reg_cmap]
        print(f"  Generating mjx-{woff2_slug}-n.woff2...")
        generate_woff2(text_font_paths['regular'],
                       os.path.join(woff2_dir, f"mjx-{woff2_slug}-n.woff2"), lato_cps_normal)

        lato_cps_bold = [cp for cp in bold_cps if cp in bold_cmap]
        print(f"  Generating mjx-{woff2_slug}-b.woff2...")
        generate_woff2(text_font_paths['bold'],
                       os.path.join(woff2_dir, f"mjx-{woff2_slug}-b.woff2"), lato_cps_bold)

        lato_cps_italic = [cp for cp in italic_cps if cp in italic_cmap]
        print(f"  Generating mjx-{woff2_slug}-i.woff2...")
        generate_woff2(text_font_paths['italic'],
                       os.path.join(woff2_dir, f"mjx-{woff2_slug}-i.woff2"), lato_cps_italic)

        lato_cps_bi = [cp for cp in bold_italic_cps if cp in bi_cmap]
        print(f"  Generating mjx-{woff2_slug}-bi.woff2...")
        generate_woff2(text_font_paths['bold_italic'],
                       os.path.join(woff2_dir, f"mjx-{woff2_slug}-bi.woff2"), lato_cps_bi)

        # Zero-width font for CHTML baseline
        print(f"  Generating mjx-{woff2_slug}-zero.woff2...")
        generate_woff2(text_font_paths['regular'],
                       os.path.join(woff2_dir, f"mjx-{woff2_slug}-zero.woff2"), [0x200B])

    print(f"\nDone! Output written to: {output_dir}")

    # Summary
    file_count = 0
    for root, dirs, files in os.walk(output_dir):
        file_count += len(files)
    print(f"Total files: {file_count}")

    return {
        'svg_normal': svg_normal,
        'svg_bold': svg_bold,
        'svg_italic': svg_italic,
        'svg_bold_italic': svg_bold_italic,
        'ic_map': ic_map,
        'delimiters': delimiters,
        'size_data': size_data,
    }
