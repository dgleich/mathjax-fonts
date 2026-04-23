"""Horizontal delimiter entries from MathJax newCM font.

These encode MathJax-specific stretchy logic (stretchv, schar, etc.)
that does not map directly from the OpenType MATH table.
Used as a reliable source for horizontal stretchy constructions.
"""

# 99 horizontal delimiter entries from newCM
NEWCM_HORIZ_DELIMITERS_JS = """
        0x2D: {
        c: 0x2212,
        dir: Direction_js_1.H,
        stretch: [0, 0x2212],
        HDW: [0.583, 0.083, .778],
        hd: [.583, .083]
    },
        0x3D: {
        dir: Direction_js_1.H,
        stretch: [0, 0x3D],
        HDW: [0.367, -0.133, .778],
        hd: [.367, -.133]
    },
        0x5E: {
        c: 0x302,
        dir: Direction_js_1.H,
        sizes: [.5, .644, .768, .919, 1.1, 1.32, 1.581, 1.896]
    },
        0x5F: {
        c: 0x2013,
        dir: Direction_js_1.H,
        stretch: [0, 0x2013],
        HDW: [0.277, -0.255, .5],
        hd: [.277, -.255]
    },
        0x7E: {
        c: 0x303,
        dir: Direction_js_1.H,
        sizes: [.5, .652, .778, .931, 1.115, 1.335, 1.599, 1.915]
    },
        0xAF: {
        c: 0x305,
        dir: Direction_js_1.H,
        sizes: [.392, .568],
        stretch: [0, 0x305],
        stretchv: [0, 1],
        HDW: [0.67, -0.63, 0],
        hd: [.67, -.63]
    },
        0x2C6: {
        c: 0x302,
        dir: Direction_js_1.H,
        sizes: [.5, .644, .768, .919, 1.1, 1.32, 1.581, 1.896]
    },
        0x2C7: {
        c: 0x30C,
        dir: Direction_js_1.H,
        sizes: [.366, .644, .768, .919, 1.1, 1.32, 1.581, 1.896]
    },
        0x2C9: {
        c: 0x305,
        dir: Direction_js_1.H,
        sizes: [.392, .568],
        stretch: [0, 0x305],
        stretchv: [0, 1],
        HDW: [0.67, -0.63, 0],
        hd: [.67, -.63]
    },
        0x2D8: {
        c: 0x306,
        dir: Direction_js_1.H,
        sizes: [.376, .658, .784, .937, 1.12, 1.341, 1.604, 1.92]
    },
        0x2DC: {
        c: 0x303,
        dir: Direction_js_1.H,
        sizes: [.5, .652, .778, .931, 1.115, 1.335, 1.599, 1.915]
    },
        0x302: {
        dir: Direction_js_1.H,
        sizes: [.5, .644, .768, .919, 1.1, 1.32, 1.581, 1.896]
    },
        0x303: {
        dir: Direction_js_1.H,
        sizes: [.5, .652, .778, .931, 1.115, 1.335, 1.599, 1.915]
    },
        0x305: {
        dir: Direction_js_1.H,
        sizes: [.392, .568],
        stretch: [0, 0x305],
        stretchv: [0, 1],
        HDW: [0.67, -0.63, 0],
        hd: [.67, -.63]
    },
        0x306: {
        dir: Direction_js_1.H,
        sizes: [.376, .658, .784, .937, 1.12, 1.341, 1.604, 1.92]
    },
        0x30C: {
        dir: Direction_js_1.H,
        sizes: [.366, .644, .768, .919, 1.1, 1.32, 1.581, 1.896]
    },
        0x2013: {
        dir: Direction_js_1.H,
        stretch: [0, 0x2013],
        HDW: [0.277, -0.255, .5],
        hd: [.277, -.255]
    },
        0x2014: {
        dir: Direction_js_1.H,
        stretch: [0, 0x2014],
        HDW: [0.277, -0.255, 1],
        hd: [.277, -.255]
    },
        0x2015: {
        dir: Direction_js_1.H,
        stretch: [0, 0x2015],
        HDW: [0.27, -0.23, 1.152],
        hd: [.27, -.23]
    },
        0x203E: {
        c: 0xAF,
        dir: Direction_js_1.H,
        sizes: [.392, .568],
        stretch: [0, 0x305],
        stretchv: [0, 1],
        HDW: [0.67, -0.63, 0],
        hd: [.67, -.63]
    },
        0x20D0: {
        dir: Direction_js_1.H,
        sizes: [.422, .667],
        stretch: [0x20D0, 0x20D0],
        stretchv: [3, 1],
        HDW: [0.711, -0.601, 0],
        hd: [.631, -.601]
    },
        0x20D1: {
        dir: Direction_js_1.H,
        sizes: [.422, .667],
        stretch: [0, 0x20D0, 0x20D1],
        stretchv: [0, 1, 4],
        HDW: [0.711, -0.601, 0],
        hd: [.631, -.601]
    },
        0x20D6: {
        dir: Direction_js_1.H,
        sizes: [.416, .659],
        stretch: [0x20D6, 0x20D0],
        stretchv: [3, 1],
        HDW: [0.711, -0.521, 0],
        hd: [.631, -.601]
    },
        0x20D7: {
        dir: Direction_js_1.H,
        sizes: [.416, .659],
        stretch: [0, 0x20D0, 0x20D7],
        stretchv: [0, 1, 4],
        HDW: [0.711, -0.521, 0],
        hd: [.631, -.601]
    },
        0x20E1: {
        dir: Direction_js_1.H,
        sizes: [.47, .715],
        stretch: [0x20D6, 0x20D0, 0x20D7],
        stretchv: [3, 1, 4],
        HDW: [0.711, -0.521, 0],
        hd: [.631, -.601]
    },
        0x20EC: {
        dir: Direction_js_1.H,
        sizes: [.422, .667],
        stretch: [0, 0x34D, 0x20EC],
        stretchv: [0, 1, 4],
        HDW: [-0.171, 0.281, 0],
        hd: [-.171, .201]
    },
        0x20ED: {
        dir: Direction_js_1.H,
        sizes: [.422, .667],
        stretch: [0x20ED, 0x34D],
        stretchv: [3, 1],
        HDW: [-0.171, 0.281, 0],
        hd: [-.171, .201]
    },
        0x20EE: {
        dir: Direction_js_1.H,
        sizes: [.416, .659],
        stretch: [0x20EE, 0x34D],
        stretchv: [3, 1],
        HDW: [-0.091, 0.281, 0],
        hd: [-.171, .201]
    },
        0x20EF: {
        dir: Direction_js_1.H,
        sizes: [.416, .659],
        stretch: [0, 0x34D, 0x20EF],
        stretchv: [0, 1, 4],
        HDW: [-0.091, 0.281, 0],
        hd: [-.171, .201]
    },
        0x2190: {
        dir: Direction_js_1.H,
        sizes: [1, 1.463],
        variants: [0, 0],
        schar: [0x2190, 0x27F5],
        stretch: [0x2190, 0x2190],
        stretchv: [3, 1],
        HDW: [0.51, 0.01, 1],
        hd: [.274, -.226]
    },
        0x2192: {
        dir: Direction_js_1.H,
        sizes: [1, 1.463],
        variants: [0, 0],
        schar: [0x2192, 0x27F6],
        stretch: [0, 0x2190, 0x2192],
        stretchv: [0, 1, 4],
        HDW: [0.51, 0.01, 1],
        hd: [.274, -.226]
    },
        0x2194: {
        dir: Direction_js_1.H,
        sizes: [1, 1.442],
        variants: [0, 0],
        schar: [0x2194, 0x27F7],
        stretch: [0x2190, 0x2190, 0x2192],
        stretchv: [3, 1, 4],
        HDW: [0.51, 0.01, 1],
        hd: [.274, -.226]
    },
        0x219A: {
        dir: Direction_js_1.H,
        sizes: [.997, 1.463],
        variants: [0, 2],
        stretch: [0x219A, 0x2190, 0, 0x219A],
        stretchv: [3, 1, 0, 1],
        HDW: [0.51, 0.01, .997],
        hd: [.274, -.226]
    },
        0x219B: {
        dir: Direction_js_1.H,
        sizes: [.997, 1.463],
        variants: [0, 2],
        stretch: [0, 0x2190, 0x219B, 0x219A],
        stretchv: [0, 1, 4, 1],
        HDW: [0.51, 0.01, .997],
        hd: [.274, -.226]
    },
        0x219E: {
        dir: Direction_js_1.H,
        sizes: [1.017, 1.463],
        variants: [0, 2],
        stretch: [0x219E, 0x2190],
        stretchv: [3, 1],
        HDW: [0.51, 0.01, 1.017],
        hd: [.274, -.226]
    },
        0x21A0: {
        dir: Direction_js_1.H,
        sizes: [1.017, 1.463],
        variants: [0, 2],
        stretch: [0, 0x2190, 0x21A0],
        stretchv: [0, 1, 4],
        HDW: [0.51, 0.01, 1.017],
        hd: [.274, -.226]
    },
        0x21A2: {
        dir: Direction_js_1.H,
        sizes: [1.192, 1.658],
        variants: [0, 2],
        stretch: [0x2190, 0x2190, 0x21A2],
        stretchv: [3, 1, 4],
        HDW: [0.51, 0.01, 1.192],
        hd: [.274, -.226]
    },
        0x21A3: {
        dir: Direction_js_1.H,
        sizes: [1.192, 1.658],
        variants: [0, 2],
        stretch: [0x21A3, 0x2190, 0x2192],
        stretchv: [3, 1, 4],
        HDW: [0.51, 0.01, 1.192],
        hd: [.274, -.226]
    },
        0x21A4: {
        dir: Direction_js_1.H,
        sizes: [.977, 1.443],
        variants: [0, 0],
        schar: [0x21A4, 0x27FB],
        stretch: [0x2190, 0x2190, 0x21A4],
        stretchv: [3, 1, 4],
        HDW: [0.51, 0.011, .977],
        hd: [.274, -.226]
    },
        0x21A6: {
        dir: Direction_js_1.H,
        sizes: [.977, 1.443],
        variants: [0, 0],
        schar: [0x21A6, 0x27FC],
        stretch: [0x21A6, 0x2190, 0x2192],
        stretchv: [3, 1, 4],
        HDW: [0.51, 0.011, .977],
        hd: [.274, -.226]
    },
        0x21A9: {
        dir: Direction_js_1.H,
        sizes: [.997, 1.463],
        variants: [0, 2],
        stretch: [0x2190, 0x21A9, 0x21A9],
        stretchv: [3, 1, 4],
        HDW: [0.546, 0.01, .997],
        hd: [.274, -.226]
    },
        0x21AA: {
        dir: Direction_js_1.H,
        sizes: [.997, 1.463],
        variants: [0, 2],
        stretch: [0x21AA, 0x21A9, 0x2192],
        stretchv: [3, 1, 4],
        HDW: [0.546, 0.01, .997],
        hd: [.274, -.226]
    },
        0x21AB: {
        dir: Direction_js_1.H,
        sizes: [.997, 1.463],
        variants: [0, 2],
        stretch: [0x2190, 0x21A9, 0x21AB],
        stretchv: [3, 1, 4],
        HDW: [0.55, 0.05, .997],
        hd: [.274, -.226]
    },
        0x21AC: {
        dir: Direction_js_1.H,
        sizes: [.997, 1.463],
        variants: [0, 2],
        stretch: [0x21AC, 0x21A9, 0x2192],
        stretchv: [3, 1, 4],
        HDW: [0.55, 0.05, .997],
        hd: [.274, -.226]
    },
        0x21B6: {
        dir: Direction_js_1.H,
        sizes: [.98, 1.33],
        variants: [0, 2]
    },
        0x21B7: {
        dir: Direction_js_1.H,
        sizes: [.98, 1.33],
        variants: [0, 2]
    },
        0x21BC: {
        dir: Direction_js_1.H,
        sizes: [1, 1.478],
        variants: [0, 2],
        stretch: [0x21BC, 0x21BC],
        stretchv: [3, 1],
        HDW: [0.499, -0.226, 1],
        hd: [.273, -.226]
    },
        0x21BD: {
        dir: Direction_js_1.H,
        sizes: [1.012, 1.478],
        variants: [0, 2],
        stretch: [0x21BD, 0x21BC],
        stretchv: [3, 1],
        HDW: [0.273, 0, 1.012],
        hd: [.273, -.226]
    },
        0x21C0: {
        dir: Direction_js_1.H,
        sizes: [1, 1.478],
        variants: [0, 2],
        stretch: [0, 0x21BC, 0x21C0],
        stretchv: [0, 1, 4],
        HDW: [0.499, -0.226, 1],
        hd: [.273, -.226]
    },
        0x21C1: {
        dir: Direction_js_1.H,
        sizes: [1.012, 1.478],
        variants: [0, 2],
        stretch: [0, 0x21BC, 0x21C1],
        stretchv: [0, 1, 4],
        HDW: [0.273, 0, 1.012],
        hd: [.273, -.226]
    },
        0x21C4: {
        dir: Direction_js_1.H,
        sizes: [1.018, 1.484],
        variants: [0, 2],
        stretch: [0x21C4, 0x21C4, 0x21C4],
        stretchv: [3, 1, 4],
        HDW: [0.669, 0.172, 1.018],
        hd: [.432, -.065]
    },
        0x21C6: {
        dir: Direction_js_1.H,
        sizes: [1.018, 1.484],
        variants: [0, 2],
        stretch: [0x21C6, 0x21C4, 0x21C6],
        stretchv: [3, 1, 4],
        HDW: [0.669, 0.172, 1.018],
        hd: [.432, -.065]
    },
        0x21C7: {
        dir: Direction_js_1.H,
        sizes: [.997, 1.463],
        variants: [0, 2],
        stretch: [0x21C7, 0x21C7],
        stretchv: [3, 1],
        HDW: [0.75, 0.25, .997],
        hd: [.512, .012]
    },
        0x21C9: {
        dir: Direction_js_1.H,
        sizes: [.997, 1.463],
        variants: [0, 2],
        stretch: [0, 0x21C7, 0x21C9],
        stretchv: [0, 1, 4],
        HDW: [0.75, 0.25, .997],
        hd: [.512, .012]
    },
        0x21CB: {
        dir: Direction_js_1.H,
        sizes: [1.018, 1.484],
        variants: [0, 2],
        stretch: [0x21CB, 0x21CB, 0x21CB],
        stretchv: [3, 1, 4],
        HDW: [0.598, 0.098, 1.018],
        hd: [.369, -.131]
    },
        0x21CC: {
        dir: Direction_js_1.H,
        sizes: [1.018, 1.484],
        variants: [0, 2],
        stretch: [0x21CC, 0x21CB, 0x21CC],
        stretchv: [3, 1, 4],
        HDW: [0.598, 0.098, 1.018],
        hd: [.369, -.131]
    },
        0x21CD: {
        dir: Direction_js_1.H,
        sizes: [.991, 1.457],
        variants: [0, 2],
        stretch: [0x21CD, 0x21CE, 0, 0x21CD],
        stretchv: [3, 1, 0, 1],
        HDW: [0.52, 0.02, .991],
        hd: [.369, -.131]
    },
        0x21CE: {
        dir: Direction_js_1.H,
        sizes: [1.068, 1.534],
        variants: [0, 2],
        stretch: [0x21D0, 0x21CE, 0x21D2, 0x21CD],
        stretchv: [3, 1, 4, 1],
        HDW: [0.52, 0.02, 1.068],
        hd: [.369, -.131]
    },
        0x21CF: {
        dir: Direction_js_1.H,
        sizes: [.991, 1.457],
        variants: [0, 2],
        stretch: [0, 0x21CE, 0x21D2, 0x21CD],
        stretchv: [0, 1, 4, 1],
        HDW: [0.52, 0.02, .991],
        hd: [.369, -.131]
    },
        0x21D0: {
        dir: Direction_js_1.H,
        sizes: [1, 1.457],
        variants: [0, 0],
        schar: [0x21D0, 0x27F8],
        stretch: [0x21D0, 0x21D0],
        stretchv: [3, 1],
        HDW: [0.52, 0.02, 1],
        hd: [.369, -.131]
    },
        0x21D2: {
        dir: Direction_js_1.H,
        sizes: [1, 1.457],
        variants: [0, 0],
        schar: [0x21D2, 0x27F9],
        stretch: [0, 0x21D0, 0x21D2],
        stretchv: [0, 1, 4],
        HDW: [0.52, 0.02, 1],
        hd: [.369, -.131]
    },
        0x21D4: {
        dir: Direction_js_1.H,
        sizes: [1, 1.534],
        variants: [0, 0],
        schar: [0x21D4, 0x27FA],
        stretch: [0x21D0, 0x21D0, 0x21D2],
        stretchv: [3, 1, 4],
        HDW: [0.52, 0.02, 1],
        hd: [.369, -.131]
    },
        0x21DA: {
        dir: Direction_js_1.H,
        sizes: [1.015, 1.461],
        variants: [0, 2],
        stretch: [0x21DA, 0x21DA],
        stretchv: [3, 1],
        HDW: [0.617, 0.117, 1.015],
        hd: [.466, -.034]
    },
        0x21DB: {
        dir: Direction_js_1.H,
        sizes: [1.015, 1.461],
        variants: [0, 2],
        stretch: [0, 0x21DA, 0x21DB],
        stretchv: [0, 1, 4],
        HDW: [0.617, 0.117, 1.015],
        hd: [.466, -.034]
    },
        0x21F6: {
        dir: Direction_js_1.H,
        sizes: [.997, 1.463],
        variants: [0, 2],
        stretch: [0, 0x21F6, 0x21F6],
        stretchv: [0, 1, 4],
        HDW: [0.99, 0.49, .997],
        hd: [.751, .251]
    },
        0x2212: {
        dir: Direction_js_1.H,
        stretch: [0, 0x2212],
        HDW: [0.583, 0.083, .778],
        hd: [.583, .083]
    },
        0x2261: {
        dir: Direction_js_1.H,
        stretch: [0, 0x2261],
        HDW: [0.464, -0.036, .778],
        hd: [.464, -.036]
    },
        0x2263: {
        dir: Direction_js_1.H,
        stretch: [0, 0x2263],
        HDW: [0.561, 0.061, .778],
        hd: [.561, .061]
    },
        0x2312: {
        c: 0x23DC,
        dir: Direction_js_1.H,
        sizes: [.504, 1.006, 1.508, 2.012, 2.516, 3.02, 3.524, 4.032],
        stretch: [0x23DC, 0x23DC, 0x23DC],
        stretchv: [3, 1, 4],
        HDW: [0.796, -0.502, .504],
        hd: [.796, -.689]
    },
        0x2322: {
        c: 0x23DC,
        dir: Direction_js_1.H,
        sizes: [.504, 1.006, 1.508, 2.012, 2.516, 3.02, 3.524, 4.032],
        stretch: [0x23DC, 0x23DC, 0x23DC],
        stretchv: [3, 1, 4],
        HDW: [0.796, -0.502, .504],
        hd: [.796, -.689]
    },
        0x2323: {
        c: 0x23DD,
        dir: Direction_js_1.H,
        sizes: [.504, 1.006, 1.508, 2.012, 2.516, 3.02, 3.524, 4.032],
        stretch: [0x23DD, 0x23DD, 0x23DD],
        stretchv: [3, 1, 4],
        HDW: [-0.072, 0.366, .504],
        hd: [-.259, .366]
    },
        0x23AF: {
        c: 0x2013,
        dir: Direction_js_1.H,
        stretch: [0, 0x2013],
        HDW: [0.277, -0.255, .5],
        hd: [.277, -.255]
    },
        0x23B4: {
        dir: Direction_js_1.H,
        sizes: [.36, .735, 1.11, 1.485, 1.86, 2.235, 2.61, 2.985],
        stretch: [0x23B4, 0x23B4, 0x23B4],
        stretchv: [3, 1, 4],
        HDW: [0.772, -0.504, .36],
        hd: [.772, -.706]
    },
        0x23B5: {
        dir: Direction_js_1.H,
        sizes: [.36, .735, 1.11, 1.485, 1.86, 2.235, 2.61, 2.985],
        stretch: [0x23B5, 0x23B5, 0x23B5],
        stretchv: [3, 1, 4],
        HDW: [-0.074, 0.342, .36],
        hd: [-.276, .342]
    },
        0x23DC: {
        dir: Direction_js_1.H,
        sizes: [.504, 1.006, 1.508, 2.012, 2.516, 3.02, 3.524, 4.032],
        stretch: [0x23DC, 0x23DC, 0x23DC],
        stretchv: [3, 1, 4],
        HDW: [0.796, -0.502, .504],
        hd: [.796, -.689]
    },
        0x23DD: {
        dir: Direction_js_1.H,
        sizes: [.504, 1.006, 1.508, 2.012, 2.516, 3.02, 3.524, 4.032],
        stretch: [0x23DD, 0x23DD, 0x23DD],
        stretchv: [3, 1, 4],
        HDW: [-0.072, 0.366, .504],
        hd: [-.259, .366]
    },
        0x23DE: {
        dir: Direction_js_1.H,
        sizes: [.492, .993, 1.494, 1.996, 2.498, 3, 3.502, 4.006],
        stretch: [0x23DE, 0xAF, 0x23DE, 0x23DE],
        stretchv: [3, 1, 4, 1],
        HDW: [0.85, -0.493, .492],
        hd: [.724, -.618]
    },
        0x23DF: {
        dir: Direction_js_1.H,
        sizes: [.492, .993, 1.494, 1.996, 2.498, 3, 3.502, 4.006],
        stretch: [0x23DF, 0x5F, 0x23DF, 0x23DF],
        stretchv: [3, 1, 4, 1],
        HDW: [-0.062, 0.419, .492],
        hd: [-.188, .294]
    },
        0x23E0: {
        dir: Direction_js_1.H,
        sizes: [.546, 1.048, 1.55, 2.056, 2.564, 3.068, 3.574, 4.082],
        stretch: [0x23E0, 0x23E0, 0x23E0],
        stretchv: [3, 1, 4],
        HDW: [0.873, -0.605, .546],
        hd: [.873, -.766]
    },
        0x23E1: {
        dir: Direction_js_1.H,
        sizes: [.546, 1.048, 1.55, 2.056, 2.564, 3.068, 3.574, 4.082],
        stretch: [0x23E1, 0x23E1, 0x23E1],
        stretchv: [3, 1, 4],
        HDW: [-0.175, 0.443, .546],
        hd: [-.336, .443]
    },
        0x2500: {
        c: 0x2013,
        dir: Direction_js_1.H,
        stretch: [0, 0x2013],
        HDW: [0.277, -0.255, .5],
        hd: [.277, -.255]
    },
        0x27F5: {
        c: 0x2190,
        dir: Direction_js_1.H,
        sizes: [1, 1.463],
        variants: [0, 0],
        schar: [0x2190, 0x27F5],
        stretch: [0x2190, 0x2190],
        stretchv: [3, 1],
        HDW: [0.51, 0.01, 1],
        hd: [.274, -.226]
    },
        0x27F6: {
        c: 0x2192,
        dir: Direction_js_1.H,
        sizes: [1, 1.463],
        variants: [0, 0],
        schar: [0x2192, 0x27F6],
        stretch: [0, 0x2190, 0x2192],
        stretchv: [0, 1, 4],
        HDW: [0.51, 0.01, 1],
        hd: [.274, -.226]
    },
        0x27F7: {
        c: 0x2194,
        dir: Direction_js_1.H,
        sizes: [1, 1.442],
        variants: [0, 0],
        schar: [0x2194, 0x27F7],
        stretch: [0x2190, 0x2190, 0x2192],
        stretchv: [3, 1, 4],
        HDW: [0.51, 0.01, 1],
        hd: [.274, -.226]
    },
        0x27F8: {
        c: 0x21D0,
        dir: Direction_js_1.H,
        sizes: [1, 1.457],
        variants: [0, 0],
        schar: [0x21D0, 0x27F8],
        stretch: [0x21D0, 0x21D0],
        stretchv: [3, 1],
        HDW: [0.52, 0.02, 1],
        hd: [.369, -.131]
    },
        0x27F9: {
        c: 0x21D2,
        dir: Direction_js_1.H,
        sizes: [1, 1.457],
        variants: [0, 0],
        schar: [0x21D2, 0x27F9],
        stretch: [0, 0x21D0, 0x21D2],
        stretchv: [0, 1, 4],
        HDW: [0.52, 0.02, 1],
        hd: [.369, -.131]
    },
        0x27FA: {
        c: 0x21D4,
        dir: Direction_js_1.H,
        sizes: [1, 1.534],
        variants: [0, 0],
        schar: [0x21D4, 0x27FA],
        stretch: [0x21D0, 0x21D0, 0x21D2],
        stretchv: [3, 1, 4],
        HDW: [0.52, 0.02, 1],
        hd: [.369, -.131]
    },
        0x27FB: {
        c: 0x21A4,
        dir: Direction_js_1.H,
        sizes: [.977, 1.443],
        variants: [0, 0],
        schar: [0x21A4, 0x27FB],
        stretch: [0x2190, 0x2190, 0x21A4],
        stretchv: [3, 1, 4],
        HDW: [0.51, 0.011, .977],
        hd: [.274, -.226]
    },
        0x27FC: {
        c: 0x21A6,
        dir: Direction_js_1.H,
        sizes: [.977, 1.443],
        variants: [0, 0],
        schar: [0x21A6, 0x27FC],
        stretch: [0x21A6, 0x2190, 0x2192],
        stretchv: [3, 1, 4],
        HDW: [0.51, 0.011, .977],
        hd: [.274, -.226]
    },
        0x294A: {
        dir: Direction_js_1.H,
        sizes: [1.012],
        stretch: [0x21BC, 0x21BC, 0x21C1],
        stretchv: [3, 1, 4],
        HDW: [0.499, 0, 1.012],
        hd: [.273, -.226]
    },
        0x294B: {
        dir: Direction_js_1.H,
        sizes: [1.012],
        stretch: [0x21BD, 0x21BC, 0x21C0],
        stretchv: [3, 1, 4],
        HDW: [0.499, 0, 1.012],
        hd: [.273, -.226]
    },
        0x294E: {
        dir: Direction_js_1.H,
        sizes: [1],
        stretch: [0x21BC, 0x21BC, 0x21C0],
        stretchv: [3, 1, 4],
        HDW: [0.499, -0.226, 1],
        hd: [.273, -.226]
    },
        0x2950: {
        dir: Direction_js_1.H,
        sizes: [1],
        stretch: [0x21BD, 0x21BC, 0x21C1],
        stretchv: [3, 1, 4],
        HDW: [0.273, 0, 1],
        hd: [.273, -.226]
    },
        0x295A: {
        dir: Direction_js_1.H,
        sizes: [1],
        stretch: [0x21BC, 0x21BC, 0x21A4],
        stretchv: [3, 1, 4],
        HDW: [0.51, 0.011, 1],
        hd: [.273, -.226]
    },
        0x295B: {
        dir: Direction_js_1.H,
        sizes: [1],
        stretch: [0x21A6, 0x21BC, 0x21C0],
        stretchv: [3, 1, 4],
        HDW: [0.51, 0.011, 1],
        hd: [.273, -.226]
    },
        0x295E: {
        dir: Direction_js_1.H,
        sizes: [1],
        stretch: [0x21BD, 0x21BC, 0x21A4],
        stretchv: [3, 1, 4],
        HDW: [0.51, 0.011, 1],
        hd: [.273, -.226]
    },
        0x295F: {
        dir: Direction_js_1.H,
        sizes: [1],
        stretch: [0x21A6, 0x21BC, 0x21C1],
        stretchv: [3, 1, 4],
        HDW: [0.51, 0.011, 1],
        hd: [.273, -.226]
    },
        0xFE37: {
        c: 0x23DE,
        dir: Direction_js_1.H,
        sizes: [.492, .993, 1.494, 1.996, 2.498, 3, 3.502, 4.006],
        stretch: [0x23DE, 0xAF, 0x23DE, 0x23DE],
        stretchv: [3, 1, 4, 1],
        HDW: [0.85, -0.493, .492],
        hd: [.724, -.618]
    },
        0xFE38: {
        c: 0x23DF,
        dir: Direction_js_1.H,
        sizes: [.492, .993, 1.494, 1.996, 2.498, 3, 3.502, 4.006],
        stretch: [0x23DF, 0x5F, 0x23DF, 0x23DF],
        stretchv: [3, 1, 4, 1],
        HDW: [-0.062, 0.419, .492],
        hd: [-.188, .294]
    },
"""
