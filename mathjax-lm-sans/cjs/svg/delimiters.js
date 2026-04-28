"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.delimiters = void 0;
var Direction_js_1 = require("@mathjax/src/cjs/output/common/Direction.js");
exports.delimiters = {
    0x28: {
        dir: Direction_js_1.V,
        sizes: [1.001, 1.101, 1.201, 1.461, 1.801, 2.081, 2.401, 2.981],
        stretch: [0x239B, 0x239C, 0x239D],
        HDW: [0.75, 0.25, 0.389]
    },
    0x29: {
        dir: Direction_js_1.V,
        sizes: [1.001, 1.101, 1.201, 1.461, 1.801, 2.081, 2.401, 2.981],
        stretch: [0x239E, 0x239F, 0x23A0],
        HDW: [0.75, 0.25, 0.389]
    },
    0x2D: {
        c: 0x2212,
        dir: Direction_js_1.H,
        stretch: [0, 0x2212]
    },
    0x2F: {
        dir: Direction_js_1.V,
        sizes: [1.008, 1.34, 1.739, 2.279, 2.962, 3.879, 5.084, 6.65]
    },
    0x3D: {
        dir: Direction_js_1.H,
        stretch: [0xE022, 0xE023, 0xE024],
        stretchv: [3, 1, 4],
        HDW: [0.38, -0.12, 0.778],
        hd: [0.38, -0.12]
    },
    0x5B: {
        dir: Direction_js_1.V,
        sizes: [1.001, 1.101, 1.201, 1.461, 1.801, 2.101, 2.401, 3.001],
        stretch: [0x23A1, 0x23A2, 0x23A3],
        HDW: [0.75, 0.25, 0.289]
    },
    0x5C: {
        dir: Direction_js_1.V,
        sizes: [1.008, 1.34, 1.739, 2.279, 2.962, 3.879, 5.084, 6.65]
    },
    0x5D: {
        dir: Direction_js_1.V,
        sizes: [1.001, 1.101, 1.201, 1.461, 1.801, 2.101, 2.401, 3.001],
        stretch: [0x23A4, 0x23A5, 0x23A6],
        HDW: [0.75, 0.25, 0.289]
    },
    0x5E: {
        c: 0x302,
        dir: Direction_js_1.H,
        sizes: [0.311, 0.645, 0.769, 0.92, 1.101, 1.321, 1.581, 1.897]
    },
    0x7B: {
        dir: Direction_js_1.V,
        sizes: [1.001, 1.101, 1.201, 1.461, 1.801, 2.081, 2.401, 3.001],
        stretch: [0x23A7, 0xE000, 0x23A9, 0x23A8],
        HDW: [0.75, 0.25, 0.5]
    },
    0x7C: {
        dir: Direction_js_1.V,
        sizes: [1.008, 1.208, 1.448, 1.735, 2.085, 2.505, 3.005, 3.605],
        stretch: [0, 0xE001, 0],
        HDW: [0.753, 0.254, 0.278]
    },
    0x7D: {
        dir: Direction_js_1.V,
        sizes: [1.001, 1.101, 1.201, 1.461, 1.801, 2.081, 2.401, 3.001],
        stretch: [0x23AB, 0xE002, 0x23AD, 0x23AC],
        HDW: [0.75, 0.25, 0.5]
    },
    0x7E: {
        c: 0x303,
        dir: Direction_js_1.H,
        sizes: [0.334, 0.651, 0.779, 0.931, 1.113, 1.33, 1.589, 1.915]
    },
    0x2C6: {
        c: 0x302,
        dir: Direction_js_1.H,
        sizes: [0.311, 0.645, 0.769, 0.92, 1.101, 1.321, 1.581, 1.897]
    },
    0x2C9: {
        c: 0xAF,
        dir: Direction_js_1.H
    },
    0x2DC: {
        c: 0x303,
        dir: Direction_js_1.H,
        sizes: [0.334, 0.651, 0.779, 0.931, 1.113, 1.33, 1.589, 1.915]
    },
    0x302: {
        dir: Direction_js_1.H,
        sizes: [0.311, 0.645, 0.769, 0.92, 1.101, 1.321, 1.581, 1.897]
    },
    0x303: {
        dir: Direction_js_1.H,
        sizes: [0.334, 0.651, 0.779, 0.931, 1.113, 1.33, 1.589, 1.915]
    },
    0x305: {
        dir: Direction_js_1.H,
        sizes: [0.61, 0.569],
        stretch: [0xE025, 0xE026, 0xE027],
        stretchv: [3, 1, 4],
        HDW: [0.682, -0.642, 0.778],
        hd: [0.682, -0.642]
    },
    0x306: {
        dir: Direction_js_1.H,
        sizes: [0.338, 0.661, 0.785, 0.937, 1.121, 1.341, 1.601, 1.921]
    },
    0x30C: {
        dir: Direction_js_1.H,
        sizes: [0.311, 0.645, 0.769, 0.92, 1.101, 1.321, 1.581, 1.897]
    },
    0x311: {
        dir: Direction_js_1.H,
        sizes: [0.338, 0.661, 0.785, 0.937, 1.121, 1.341, 1.601, 1.921]
    },
    0x32C: {
        dir: Direction_js_1.H,
        sizes: [0.312, 0.645, 0.769, 0.92, 1.101, 1.321, 1.581, 1.897]
    },
    0x32D: {
        dir: Direction_js_1.H,
        sizes: [0.312, 0.645, 0.769, 0.92, 1.101, 1.321, 1.581, 1.897]
    },
    0x32E: {
        dir: Direction_js_1.H,
        sizes: [0.338, 0.661, 0.785, 0.937, 1.121, 1.341, 1.601, 1.921]
    },
    0x32F: {
        dir: Direction_js_1.H,
        sizes: [0.338, 0.661, 0.785, 0.937, 1.121, 1.341, 1.601, 1.921]
    },
    0x330: {
        dir: Direction_js_1.H,
        sizes: [0.334, 0.651, 0.779, 0.931, 1.113, 1.33, 1.589, 1.915]
    },
    0x332: {
        dir: Direction_js_1.H,
        sizes: [0.362, 0.569],
        stretch: [0xE028, 0xE029, 0xE02A],
        stretchv: [3, 1, 4],
        HDW: [-0.123, 0.187, 0],
        hd: [-0.123, 0.187]
    },
    0x333: {
        dir: Direction_js_1.H,
        sizes: [0.362, 0.569],
        stretch: [0xE02B, 0xE02C, 0xE02D],
        stretchv: [3, 1, 4],
        HDW: [-0.083, 0.276, 0],
        hd: [-0.083, 0.276]
    },
    0x33F: {
        dir: Direction_js_1.H,
        sizes: [0.612, 0.569],
        stretch: [0xE02E, 0xE02F, 0xE030],
        stretchv: [3, 1, 4],
        HDW: [0.835, -0.642, 0.777],
        hd: [0.835, -0.642]
    },
    0x34D: {
        dir: Direction_js_1.H,
        sizes: [0.553, 0.624],
        stretch: [0xE031, 0xE032, 0xE033],
        stretchv: [3, 1, 4],
        HDW: [-0.025, 0.275, 0],
        hd: [-0.025, 0.275]
    },
    0x2013: {
        dir: Direction_js_1.H,
        stretch: [0, 0x2013],
        HDW: [0.305, -0.244, 0.5],
        hd: [0.305, -0.244]
    },
    0x2014: {
        dir: Direction_js_1.H,
        stretch: [0, 0x2014],
        HDW: [0.305, -0.244, 1],
        hd: [0.305, -0.244]
    },
    0x2015: {
        dir: Direction_js_1.H,
        stretch: [0, 0x2015],
        HDW: [0.305, -0.244, 1],
        hd: [0.305, -0.244]
    },
    0x2016: {
        dir: Direction_js_1.V,
        sizes: [1.008, 1.208, 1.448, 1.735, 2.085, 2.505, 3.005, 3.605],
        stretch: [0, 0xE003, 0],
        HDW: [0.753, 0.254, 0.398]
    },
    0x203E: {
        c: 0xAF,
        dir: Direction_js_1.H
    },
    0x2044: {
        dir: Direction_js_1.V,
        sizes: [0.655, 1.34, 1.739, 2.279, 2.962, 3.879, 5.084, 6.65]
    },
    0x20D0: {
        dir: Direction_js_1.H,
        sizes: [0.569, 0.569],
        stretch: [0xE034, 0xE035, 0xE036],
        stretchv: [3, 1, 4],
        HDW: [0.747, -0.597, 0],
        hd: [0.747, -0.597]
    },
    0x20D1: {
        dir: Direction_js_1.H,
        sizes: [0.569, 0.569],
        stretch: [0xE037, 0xE038, 0xE039],
        stretchv: [3, 1, 4],
        HDW: [0.747, -0.597, 0],
        hd: [0.747, -0.597]
    },
    0x20D6: {
        dir: Direction_js_1.H,
        sizes: [0.569, 0.569],
        stretch: [0xE03A, 0xE03B, 0xE03C],
        stretchv: [3, 1, 4],
        HDW: [0.747, -0.497, 0],
        hd: [0.747, -0.497]
    },
    0x20D7: {
        dir: Direction_js_1.H,
        sizes: [0.569, 0.569],
        stretch: [0xE03D, 0xE03E, 0xE03F],
        stretchv: [3, 1, 4],
        HDW: [0.747, -0.497, 0],
        hd: [0.747, -0.497]
    },
    0x20E1: {
        dir: Direction_js_1.H,
        sizes: [0.655, 0.624],
        stretch: [0xE040, 0xE041, 0xE042],
        stretchv: [3, 1, 4],
        HDW: [0.782, -0.45, 0],
        hd: [0.782, -0.45]
    },
    0x20E9: {
        dir: Direction_js_1.H,
        sizes: [0.361, 0.736, 1.111, 1.486, 1.861, 2.236, 2.611, 2.986],
        stretch: [0xE043, 0xE044, 0xE045],
        stretchv: [3, 1, 4],
        HDW: [0.726, -0.552, 0],
        hd: [0.726, -0.552]
    },
    0x20EC: {
        dir: Direction_js_1.H,
        sizes: [0.519, 0.569],
        stretch: [0xE046, 0xE047, 0xE048],
        stretchv: [3, 1, 4],
        HDW: [-0.167, 0.352, 0],
        hd: [-0.167, 0.352]
    },
    0x20ED: {
        dir: Direction_js_1.H,
        sizes: [0.519, 0.569],
        stretch: [0xE049, 0xE04A, 0xE04B],
        stretchv: [3, 1, 4],
        HDW: [-0.167, 0.352, 0],
        hd: [-0.167, 0.352]
    },
    0x20EE: {
        dir: Direction_js_1.H,
        sizes: [0.569, 0.569],
        stretch: [0xE04C, 0xE04D, 0xE04E],
        stretchv: [3, 1, 4],
        HDW: [-0.02, 0.352, 0],
        hd: [-0.02, 0.352]
    },
    0x20EF: {
        dir: Direction_js_1.H,
        sizes: [0.569, 0.569],
        stretch: [0xE04F, 0xE050, 0xE051],
        stretchv: [3, 1, 4],
        HDW: [-0.02, 0.352, 0],
        hd: [-0.02, 0.352]
    },
    0x2140: {
        dir: Direction_js_1.V,
        sizes: [1.004, 1.401]
    },
    0x2190: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.353],
        stretch: [0xE052, 0xE053, 0xE054],
        stretchv: [3, 1, 4],
        HDW: [0.511, 0.009, 1],
        hd: [0.511, 0.009]
    },
    0x2191: {
        dir: Direction_js_1.V,
        sizes: [0.889, 1.343],
        stretch: [0, 0xE004, 0],
        HDW: [0.695, 0.193, 0.558]
    },
    0x2192: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.353],
        stretch: [0xE055, 0xE056, 0xE057],
        stretchv: [3, 1, 4],
        HDW: [0.511, 0.009, 1],
        hd: [0.511, 0.009]
    },
    0x2193: {
        dir: Direction_js_1.V,
        sizes: [0.889, 1.343],
        stretch: [0, 0xE005, 0],
        HDW: [0.695, 0.193, 0.558]
    },
    0x2194: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.333],
        stretch: [0xE058, 0xE059, 0xE05A],
        stretchv: [3, 1, 4],
        HDW: [0.511, 0.009, 1],
        hd: [0.511, 0.009]
    },
    0x2195: {
        dir: Direction_js_1.V,
        sizes: [1.019, 0.999],
        stretch: [0, 0xE006, 0],
        HDW: [0.755, 0.263, 0.56]
    },
    0x2196: {
        dir: Direction_js_1.V,
        sizes: [0.939, 1.414]
    },
    0x2197: {
        dir: Direction_js_1.V,
        sizes: [0.939, 1.414]
    },
    0x2198: {
        dir: Direction_js_1.V,
        sizes: [0.939, 1.414]
    },
    0x2199: {
        dir: Direction_js_1.V,
        sizes: [0.939, 1.414]
    },
    0x219A: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.353],
        stretch: [0xE05B, 0xE05C, 0xE05E, 0xE05D],
        stretchv: [3, 1, 4, 2],
        HDW: [0.511, 0.009, 1],
        hd: [0.511, 0.009]
    },
    0x219B: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.353],
        stretch: [0xE05F, 0xE060, 0xE062, 0xE061],
        stretchv: [3, 1, 4, 2],
        HDW: [0.511, 0.009, 1],
        hd: [0.511, 0.009]
    },
    0x219E: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.354],
        stretch: [0xE063, 0xE064, 0xE065],
        stretchv: [3, 1, 4],
        HDW: [0.511, 0.009, 1],
        hd: [0.511, 0.009]
    },
    0x219F: {
        dir: Direction_js_1.V,
        sizes: [0.889, 1.339],
        stretch: [0, 0xE007, 0],
        HDW: [0.695, 0.193, 0.572]
    },
    0x21A0: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.354],
        stretch: [0xE066, 0xE067, 0xE068],
        stretchv: [3, 1, 4],
        HDW: [0.511, 0.009, 1],
        hd: [0.511, 0.009]
    },
    0x21A1: {
        dir: Direction_js_1.V,
        sizes: [0.889, 1.339],
        stretch: [0, 0xE008, 0],
        HDW: [0.695, 0.193, 0.572]
    },
    0x21A2: {
        dir: Direction_js_1.H,
        sizes: [1.016, 1.549],
        stretch: [0xE069, 0xE06A, 0xE06B],
        stretchv: [3, 1, 4],
        HDW: [0.511, 0.009, 1.127],
        hd: [0.511, 0.009]
    },
    0x21A3: {
        dir: Direction_js_1.H,
        sizes: [1.016, 1.549],
        stretch: [0xE06C, 0xE06D, 0xE06E],
        stretchv: [3, 1, 4],
        HDW: [0.511, 0.009, 1.127],
        hd: [0.511, 0.009]
    },
    0x21A4: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.333],
        stretch: [0xE06F, 0xE070, 0xE071],
        stretchv: [3, 1, 4],
        HDW: [0.511, 0.011, 1],
        hd: [0.511, 0.011]
    },
    0x21A5: {
        dir: Direction_js_1.V,
        sizes: [0.889, 1.319],
        stretch: [0, 0xE009, 0],
        HDW: [0.694, 0.194, 0.632]
    },
    0x21A6: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.333],
        stretch: [0xE072, 0xE073, 0xE074],
        stretchv: [3, 1, 4],
        HDW: [0.511, 0.011, 1],
        hd: [0.511, 0.011]
    },
    0x21A7: {
        dir: Direction_js_1.V,
        sizes: [0.889, 1.319],
        stretch: [0, 0xE00A, 0],
        HDW: [0.694, 0.194, 0.632]
    },
    0x21A9: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.354],
        stretch: [0xE075, 0xE076, 0xE077],
        stretchv: [3, 1, 4],
        HDW: [0.541, 0.009, 1],
        hd: [0.541, 0.009]
    },
    0x21AA: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.354],
        stretch: [0xE078, 0xE079, 0xE07A],
        stretchv: [3, 1, 4],
        HDW: [0.541, 0.009, 1],
        hd: [0.541, 0.009]
    },
    0x21AB: {
        dir: Direction_js_1.H,
        sizes: [0.887, 1.354],
        stretch: [0xE07B, 0xE07C, 0xE07D],
        stretchv: [3, 1, 4],
        HDW: [0.55, 0.03, 1],
        hd: [0.55, 0.03]
    },
    0x21AC: {
        dir: Direction_js_1.H,
        sizes: [0.887, 1.354],
        stretch: [0xE07E, 0xE07F, 0xE080],
        stretchv: [3, 1, 4],
        HDW: [0.55, 0.03, 1],
        hd: [0.55, 0.03]
    },
    0x21AD: {
        dir: Direction_js_1.H,
        sizes: [0.879, 1.393]
    },
    0x21AE: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.333],
        stretch: [0xE081, 0xE082, 0xE084, 0xE083],
        stretchv: [3, 1, 4, 2],
        HDW: [0.511, 0.009, 1],
        hd: [0.511, 0.009]
    },
    0x21B0: {
        dir: Direction_js_1.V,
        sizes: [0.86, 1.169]
    },
    0x21B1: {
        dir: Direction_js_1.V,
        sizes: [0.86, 1.169]
    },
    0x21B2: {
        dir: Direction_js_1.V,
        sizes: [0.86, 1.169]
    },
    0x21B3: {
        dir: Direction_js_1.V,
        sizes: [0.86, 1.169]
    },
    0x21B6: {
        dir: Direction_js_1.H,
        sizes: [0.898, 1.228]
    },
    0x21B7: {
        dir: Direction_js_1.H,
        sizes: [0.898, 1.228]
    },
    0x21BC: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.368],
        stretch: [0xE085, 0xE086, 0xE087],
        stretchv: [3, 1, 4],
        HDW: [0.481, -0.221, 1],
        hd: [0.481, -0.221]
    },
    0x21BD: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.368],
        stretch: [0xE088, 0xE089, 0xE08A],
        stretchv: [3, 1, 4],
        HDW: [0.281, -0.021, 1],
        hd: [0.281, -0.021]
    },
    0x21BE: {
        dir: Direction_js_1.V,
        sizes: [0.889, 1.367],
        stretch: [0, 0xE00B, 0],
        HDW: [0.695, 0.193, 0.441]
    },
    0x21BF: {
        dir: Direction_js_1.V,
        sizes: [0.889, 1.367],
        stretch: [0, 0xE00C, 0],
        HDW: [0.695, 0.193, 0.441]
    },
    0x21C0: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.368],
        stretch: [0xE08B, 0xE08C, 0xE08D],
        stretchv: [3, 1, 4],
        HDW: [0.481, -0.221, 1],
        hd: [0.481, -0.221]
    },
    0x21C1: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.368],
        stretch: [0xE08E, 0xE08F, 0xE090],
        stretchv: [3, 1, 4],
        HDW: [0.281, -0.021, 1],
        hd: [0.281, -0.021]
    },
    0x21C2: {
        dir: Direction_js_1.V,
        sizes: [0.889, 1.367],
        stretch: [0, 0xE00D, 0],
        HDW: [0.695, 0.193, 0.441]
    },
    0x21C3: {
        dir: Direction_js_1.V,
        sizes: [0.889, 1.367],
        stretch: [0, 0xE00E, 0],
        HDW: [0.695, 0.193, 0.441]
    },
    0x21C4: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.374],
        stretch: [0xE091, 0xE092, 0xE093],
        stretchv: [3, 1, 4],
        HDW: [0.641, 0.143, 1],
        hd: [0.641, 0.143]
    },
    0x21C5: {
        dir: Direction_js_1.V,
        sizes: [0.889, 1.374],
        stretch: [0, 0xE00F, 0],
        HDW: [0.693, 0.195, 0.896]
    },
    0x21C6: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.374],
        stretch: [0xE094, 0xE095, 0xE096],
        stretchv: [3, 1, 4],
        HDW: [0.641, 0.143, 1],
        hd: [0.641, 0.143]
    },
    0x21C7: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.353],
        stretch: [0xE097, 0xE098, 0xE099],
        stretchv: [3, 1, 4],
        HDW: [0.739, 0.239, 1],
        hd: [0.739, 0.239]
    },
    0x21C8: {
        dir: Direction_js_1.V,
        sizes: [0.889, 1.344],
        stretch: [0, 0xE010, 0],
        HDW: [0.694, 0.194, 0.992]
    },
    0x21C9: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.353],
        stretch: [0xE09A, 0xE09B, 0xE09C],
        stretchv: [3, 1, 4],
        HDW: [0.739, 0.239, 1],
        hd: [0.739, 0.239]
    },
    0x21CA: {
        dir: Direction_js_1.V,
        sizes: [0.889, 1.344],
        stretch: [0, 0xE011, 0],
        HDW: [0.694, 0.194, 0.992]
    },
    0x21CB: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.374],
        stretch: [0xE09D, 0xE09E, 0xE09F],
        stretchv: [3, 1, 4],
        HDW: [0.567, 0.067, 1],
        hd: [0.567, 0.067]
    },
    0x21CC: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.374],
        stretch: [0xE0A0, 0xE0A1, 0xE0A2],
        stretchv: [3, 1, 4],
        HDW: [0.567, 0.067, 1],
        hd: [0.567, 0.067]
    },
    0x21CD: {
        dir: Direction_js_1.H,
        sizes: [0.885, 1.344],
        stretch: [0xE0A3, 0xE0A4, 0xE0A6, 0xE0A5],
        stretchv: [3, 1, 4, 2],
        HDW: [0.511, 0.011, 1],
        hd: [0.511, 0.011]
    },
    0x21CE: {
        dir: Direction_js_1.H,
        sizes: [0.961, 1.423],
        stretch: [0xE0A7, 0xE0A8, 0xE0AA, 0xE0A9],
        stretchv: [3, 1, 4, 2],
        HDW: [0.511, 0.011, 1.04],
        hd: [0.511, 0.011]
    },
    0x21CF: {
        dir: Direction_js_1.H,
        sizes: [0.885, 1.344],
        stretch: [0xE0AB, 0xE0AC, 0xE0AE, 0xE0AD],
        stretchv: [3, 1, 4, 2],
        HDW: [0.511, 0.011, 1],
        hd: [0.511, 0.011]
    },
    0x21D0: {
        dir: Direction_js_1.H,
        sizes: [0.885, 1.343],
        stretch: [0xE0AF, 0xE0B0, 0xE0B1],
        stretchv: [3, 1, 4],
        HDW: [0.511, 0.009, 1],
        hd: [0.511, 0.009]
    },
    0x21D1: {
        dir: Direction_js_1.V,
        sizes: [0.885, 1.342],
        stretch: [0, 0xE012, 0],
        HDW: [0.693, 0.191, 0.611]
    },
    0x21D2: {
        dir: Direction_js_1.H,
        sizes: [0.885, 1.343],
        stretch: [0xE0B2, 0xE0B3, 0xE0B4],
        stretchv: [3, 1, 4],
        HDW: [0.511, 0.009, 1],
        hd: [0.511, 0.009]
    },
    0x21D3: {
        dir: Direction_js_1.V,
        sizes: [0.885, 1.342],
        stretch: [0, 0xE013, 0],
        HDW: [0.693, 0.191, 0.611]
    },
    0x21D4: {
        dir: Direction_js_1.H,
        sizes: [0.961, 1.457],
        stretch: [0xE0B5, 0xE0B6, 0xE0B7],
        stretchv: [3, 1, 4],
        HDW: [0.511, 0.009, 1.04],
        hd: [0.511, 0.009]
    },
    0x21D5: {
        dir: Direction_js_1.V,
        sizes: [0.961, 1.421],
        stretch: [0, 0xE014, 0],
        HDW: [0.731, 0.229, 0.611]
    },
    0x21D6: {
        dir: Direction_js_1.V,
        sizes: [1.004, 1.426]
    },
    0x21D7: {
        dir: Direction_js_1.V,
        sizes: [1.004, 1.426]
    },
    0x21D8: {
        dir: Direction_js_1.V,
        sizes: [1.004, 1.426]
    },
    0x21D9: {
        dir: Direction_js_1.V,
        sizes: [1.004, 1.426]
    },
    0x21DA: {
        dir: Direction_js_1.H,
        sizes: [0.901, 1.347],
        stretch: [0xE0B8, 0xE0B9, 0xE0BA],
        stretchv: [3, 1, 4],
        HDW: [0.612, 0.111, 1.015],
        hd: [0.612, 0.111]
    },
    0x21DB: {
        dir: Direction_js_1.H,
        sizes: [0.901, 1.347],
        stretch: [0xE0BB, 0xE0BC, 0xE0BD],
        stretchv: [3, 1, 4],
        HDW: [0.612, 0.111, 1.015],
        hd: [0.612, 0.111]
    },
    0x21DC: {
        dir: Direction_js_1.H,
        sizes: [0.888, 1.584]
    },
    0x21DD: {
        dir: Direction_js_1.H,
        sizes: [0.888, 1.584]
    },
    0x21E6: {
        dir: Direction_js_1.H,
        sizes: [0.939, 1.385],
        stretch: [0xE0BE, 0xE0BF, 0xE0C0],
        stretchv: [3, 1, 4],
        HDW: [0.52, 0.02, 1.05],
        hd: [0.52, 0.02]
    },
    0x21E7: {
        dir: Direction_js_1.V,
        sizes: [0.939, 1.385],
        stretch: [0, 0xE015, 0],
        HDW: [0.725, 0.213, 0.652]
    },
    0x21E8: {
        dir: Direction_js_1.H,
        sizes: [0.939, 1.385],
        stretch: [0xE0C1, 0xE0C2, 0xE0C3],
        stretchv: [3, 1, 4],
        HDW: [0.52, 0.02, 1.05],
        hd: [0.52, 0.02]
    },
    0x21E9: {
        dir: Direction_js_1.V,
        sizes: [0.939, 1.385],
        stretch: [0, 0xE016, 0],
        HDW: [0.713, 0.225, 0.652]
    },
    0x21F3: {
        dir: Direction_js_1.V,
        sizes: [0.951, 1.397],
        stretch: [0, 0xE017, 0],
        HDW: [0.725, 0.225, 0.652]
    },
    0x21F5: {
        dir: Direction_js_1.V,
        sizes: [0.889, 1.374],
        stretch: [0, 0xE018, 0],
        HDW: [0.693, 0.195, 0.896]
    },
    0x21F6: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.353],
        stretch: [0xE0C4, 0xE0C5, 0xE0C6],
        stretchv: [3, 1, 4],
        HDW: [0.987, 0.489, 1],
        hd: [0.987, 0.489]
    },
    0x220F: {
        dir: Direction_js_1.V,
        sizes: [1.001, 1.401]
    },
    0x2210: {
        dir: Direction_js_1.V,
        sizes: [1.001, 1.401]
    },
    0x2211: {
        dir: Direction_js_1.V,
        sizes: [1.007, 1.401]
    },
    0x2212: {
        dir: Direction_js_1.H,
        stretch: [0xE0C7, 0xE0C8, 0xE0C9],
        stretchv: [3, 1, 4],
        HDW: [0.28, -0.22, 0.778],
        hd: [0.28, -0.22]
    },
    0x221A: {
        dir: Direction_js_1.V,
        sizes: [0.997, 1.197, 1.797, 2.407, 2.997],
        stretch: [0, 0xE019, 0x23B7],
        HDW: [0.04, 0.956, 0.833]
    },
    0x2223: {
        dir: Direction_js_1.V,
        sizes: [1.008, 1.208, 1.448, 1.735, 2.085, 2.505, 3.005, 3.605],
        stretch: [0, 0xE001, 0],
        HDW: [0.753, 0.254, 0.278]
    },
    0x2225: {
        dir: Direction_js_1.V,
        sizes: [1.008, 1.208, 1.448, 1.735, 2.085, 2.505, 3.005, 3.605],
        stretch: [0, 0xE003, 0],
        HDW: [0.753, 0.254, 0.5]
    },
    0x222B: {
        dir: Direction_js_1.V,
        sizes: [1.114, 2.223],
        stretch: [0x2320, 0x23AE, 0x2321],
        HDW: [0.806, 0.307, 0.722]
    },
    0x222C: {
        dir: Direction_js_1.V,
        sizes: [1.114, 2.223]
    },
    0x222D: {
        dir: Direction_js_1.V,
        sizes: [1.114, 2.223]
    },
    0x222E: {
        dir: Direction_js_1.V,
        sizes: [1.114, 2.223]
    },
    0x222F: {
        dir: Direction_js_1.V,
        sizes: [1.114, 2.223]
    },
    0x2230: {
        dir: Direction_js_1.V,
        sizes: [1.114, 2.223]
    },
    0x2231: {
        dir: Direction_js_1.V,
        sizes: [1.114, 2.223]
    },
    0x2232: {
        dir: Direction_js_1.V,
        sizes: [1.114, 2.223]
    },
    0x2233: {
        dir: Direction_js_1.V,
        sizes: [1.114, 2.223]
    },
    0x2261: {
        dir: Direction_js_1.H,
        stretch: [0xE0CA, 0xE0CB, 0xE0CC],
        stretchv: [3, 1, 4],
        HDW: [0.473, -0.027, 0.778],
        hd: [0.473, -0.027]
    },
    0x2263: {
        dir: Direction_js_1.H,
        stretch: [0xE0CD, 0xE0CE, 0xE0CF],
        stretchv: [3, 1, 4],
        HDW: [0.568, 0.071, 0.778],
        hd: [0.568, 0.071]
    },
    0x22A2: {
        dir: Direction_js_1.V,
        sizes: [0.685, 0.829]
    },
    0x22A3: {
        dir: Direction_js_1.V,
        sizes: [0.685, 0.829]
    },
    0x22A4: {
        dir: Direction_js_1.V,
        sizes: [0.686, 0.869]
    },
    0x22A5: {
        dir: Direction_js_1.V,
        sizes: [0.686, 0.869]
    },
    0x22C0: {
        dir: Direction_js_1.V,
        sizes: [1.03, 1.389]
    },
    0x22C1: {
        dir: Direction_js_1.V,
        sizes: [1.03, 1.389]
    },
    0x22C2: {
        dir: Direction_js_1.V,
        sizes: [1.024, 1.355]
    },
    0x22C3: {
        dir: Direction_js_1.V,
        sizes: [1.024, 1.355]
    },
    0x2308: {
        dir: Direction_js_1.V,
        sizes: [1.001, 1.101, 1.201, 1.452, 1.801, 2.101, 2.401, 3.001],
        stretch: [0, 0x23A2],
        stretchv: [0, 1],
        HDW: [0.75, 0.25, 0.444]
    },
    0x2309: {
        dir: Direction_js_1.V,
        sizes: [1.001, 1.101, 1.201, 1.452, 1.801, 2.101, 2.401, 3.001],
        stretch: [0, 0x23A5],
        stretchv: [0, 1],
        HDW: [0.75, 0.25, 0.444]
    },
    0x230A: {
        dir: Direction_js_1.V,
        sizes: [1.001, 1.101, 1.201, 1.452, 1.801, 2.101, 2.401, 3.001],
        stretch: [0, 0x23A3],
        stretchv: [0, 1],
        HDW: [0.75, 0.25, 0.444]
    },
    0x230B: {
        dir: Direction_js_1.V,
        sizes: [1.001, 1.101, 1.201, 1.452, 1.801, 2.101, 2.401, 3.001],
        stretch: [0, 0x23A6],
        stretchv: [0, 1],
        HDW: [0.75, 0.25, 0.444]
    },
    0x2329: {
        dir: Direction_js_1.V,
        sizes: [1.029, 1.128, 1.228, 1.482, 1.834, 2.134, 2.435, 3.037]
    },
    0x232A: {
        dir: Direction_js_1.V,
        sizes: [1.029, 1.128, 1.228, 1.482, 1.834, 2.134, 2.435, 3.037]
    },
    0x23B4: {
        dir: Direction_js_1.H,
        sizes: [0.361, 0.736, 1.111, 1.486, 1.861, 2.236, 2.611, 2.986],
        stretch: [0xE043, 0xE044, 0xE045],
        stretchv: [3, 1, 4],
        HDW: [0.726, -0.576, 0.36],
        hd: [0.726, -0.576]
    },
    0x23B5: {
        dir: Direction_js_1.H,
        sizes: [0.361, 0.736, 1.111, 1.486, 1.861, 2.236, 2.611, 2.986],
        stretch: [0xE0D0, 0xE0D1, 0xE0D2],
        stretchv: [3, 1, 4],
        HDW: [-0.146, 0.296, 0.36],
        hd: [-0.146, 0.296]
    },
    0x23DC: {
        dir: Direction_js_1.H,
        sizes: [0.501, 1.001, 1.461, 1.801, 2.081, 2.401, 2.981, 3.501],
        stretch: [0xE0D3, 0xE0D4, 0xE0D5],
        stretchv: [3, 1, 4],
        HDW: [0.722, -0.53, 0.504],
        hd: [0.722, -0.53]
    },
    0x23DD: {
        dir: Direction_js_1.H,
        sizes: [0.501, 1.001, 1.461, 1.801, 2.081, 2.401, 2.981, 3.501],
        stretch: [0xE0D6, 0xE0D7, 0xE0D8],
        stretchv: [3, 1, 4],
        HDW: [-0.108, 0.3, 0.504],
        hd: [-0.108, 0.3]
    },
    0x23DE: {
        dir: Direction_js_1.H,
        sizes: [0.661, 0.995, 1.495, 2.001, 2.501, 3.001, 3.501, 4.007],
        stretch: [0xE0D9, 0xE0DA, 0xE0DC, 0xE0DB],
        stretchv: [3, 1, 4, 2],
        HDW: [1.136, -0.534, 0.66],
        hd: [0.786, -0.534]
    },
    0x23DF: {
        dir: Direction_js_1.H,
        sizes: [0.661, 0.995, 1.495, 2.001, 2.501, 3.001, 3.501, 4.007],
        stretch: [0xE0DD, 0xE0DE, 0xE0E0, 0xE0DF],
        stretchv: [3, 1, 4, 2],
        HDW: [-0.104, 0.706, 0.66],
        hd: [-0.104, 0.356]
    },
    0x23E0: {
        dir: Direction_js_1.H,
        sizes: [0.547, 1.049, 1.551, 2.057, 2.565, 3.069, 3.575, 4.083],
        stretch: [0xE0E1, 0xE0E2, 0xE0E3],
        stretchv: [3, 1, 4],
        HDW: [0.829, -0.657, 0.546],
        hd: [0.829, -0.657]
    },
    0x23E1: {
        dir: Direction_js_1.H,
        sizes: [0.547, 1.049, 1.551, 2.057, 2.565, 3.069, 3.575, 4.083],
        stretch: [0xE0E4, 0xE0E5, 0xE0E6],
        stretchv: [3, 1, 4],
        HDW: [-0.227, 0.399, 0.546],
        hd: [-0.227, 0.399]
    },
    0x2500: {
        dir: Direction_js_1.H,
        stretch: [0, 0x2500],
        HDW: [0.27, -0.23, 0.666],
        hd: [0.27, -0.23]
    },
    0x27A1: {
        dir: Direction_js_1.H,
        sizes: [0.86, 1.312],
        stretch: [0xE0E7, 0xE0E8, 0xE0E9],
        stretchv: [3, 1, 4],
        HDW: [0.463, -0.037, 0.977],
        hd: [0.463, -0.037]
    },
    0x27D5: {
        dir: Direction_js_1.V,
        sizes: [0.571, 0.663]
    },
    0x27D6: {
        dir: Direction_js_1.V,
        sizes: [0.571, 0.663]
    },
    0x27D7: {
        dir: Direction_js_1.V,
        sizes: [0.571, 0.663]
    },
    0x27E6: {
        dir: Direction_js_1.V,
        sizes: [1.001, 1.101, 1.201, 1.461, 1.801, 2.101, 2.401, 3.001],
        stretch: [0, 0xE01A, 0],
        HDW: [0.75, 0.25, 0.442]
    },
    0x27E7: {
        dir: Direction_js_1.V,
        sizes: [1.001, 1.101, 1.201, 1.461, 1.801, 2.101, 2.401, 3.001],
        stretch: [0, 0xE01B, 0],
        HDW: [0.75, 0.25, 0.442]
    },
    0x27E8: {
        dir: Direction_js_1.V,
        sizes: [1.029, 1.128, 1.228, 1.482, 1.834, 2.134, 2.435, 3.037]
    },
    0x27E9: {
        dir: Direction_js_1.V,
        sizes: [1.029, 1.128, 1.228, 1.482, 1.834, 2.134, 2.435, 3.037]
    },
    0x27EA: {
        dir: Direction_js_1.V,
        sizes: [1.029, 1.128, 1.228, 1.482, 1.834, 2.134, 2.435, 3.037]
    },
    0x27EB: {
        dir: Direction_js_1.V,
        sizes: [1.029, 1.128, 1.228, 1.482, 1.834, 2.134, 2.435, 3.037]
    },
    0x27EE: {
        dir: Direction_js_1.V,
        sizes: [1.001, 1.131, 1.301, 1.461, 1.841, 2.141, 2.441, 3.041],
        stretch: [0, 0xE01C, 0],
        HDW: [0.75, 0.25, 0.287]
    },
    0x27EF: {
        dir: Direction_js_1.V,
        sizes: [1.001, 1.131, 1.301, 1.461, 1.841, 2.141, 2.441, 3.041],
        stretch: [0, 0xE01D, 0],
        HDW: [0.75, 0.25, 0.287]
    },
    0x2906: {
        dir: Direction_js_1.H,
        sizes: [0.877, 1.323],
        stretch: [0xE0EA, 0xE0EB, 0xE0EC],
        stretchv: [3, 1, 4],
        HDW: [0.511, 0.011, 0.991],
        hd: [0.511, 0.011]
    },
    0x2907: {
        dir: Direction_js_1.H,
        sizes: [0.877, 1.323],
        stretch: [0xE0ED, 0xE0EE, 0xE0EF],
        stretchv: [3, 1, 4],
        HDW: [0.511, 0.011, 0.991],
        hd: [0.511, 0.011]
    },
    0x2980: {
        dir: Direction_js_1.V,
        sizes: [1.008, 1.108, 1.208, 1.468, 1.798, 2.108, 2.408, 3.008],
        stretch: [0, 0xE01E, 0],
        HDW: [0.753, 0.254, 0.694]
    },
    0x2983: {
        dir: Direction_js_1.V,
        sizes: [1.001, 1.101, 1.201, 1.461, 1.801, 2.081, 2.401, 3.001]
    },
    0x2984: {
        dir: Direction_js_1.V,
        sizes: [1.001, 1.101, 1.201, 1.461, 1.801, 2.081, 2.401, 3.001]
    },
    0x2985: {
        dir: Direction_js_1.V,
        sizes: [1.001, 1.101, 1.201, 1.461, 1.801, 2.081, 2.401, 2.981]
    },
    0x2986: {
        dir: Direction_js_1.V,
        sizes: [1.001, 1.101, 1.201, 1.461, 1.801, 2.081, 2.401, 2.981]
    },
    0x29F8: {
        dir: Direction_js_1.V,
        sizes: [1.095, 1.957]
    },
    0x29F9: {
        dir: Direction_js_1.V,
        sizes: [1.095, 1.957]
    },
    0x29FC: {
        dir: Direction_js_1.V,
        sizes: [0.975, 1.055, 1.155, 1.395, 1.755, 2.055, 2.345, 2.955]
    },
    0x29FD: {
        dir: Direction_js_1.V,
        sizes: [0.975, 1.055, 1.155, 1.395, 1.755, 2.055, 2.345, 2.955]
    },
    0x2A00: {
        dir: Direction_js_1.V,
        sizes: [0.987, 1.305]
    },
    0x2A01: {
        dir: Direction_js_1.V,
        sizes: [0.987, 1.305]
    },
    0x2A02: {
        dir: Direction_js_1.V,
        sizes: [0.986, 1.305]
    },
    0x2A03: {
        dir: Direction_js_1.V,
        sizes: [1.024, 1.355]
    },
    0x2A04: {
        dir: Direction_js_1.V,
        sizes: [1.024, 1.355]
    },
    0x2A05: {
        dir: Direction_js_1.V,
        sizes: [1.03, 1.373]
    },
    0x2A06: {
        dir: Direction_js_1.V,
        sizes: [1.03, 1.373]
    },
    0x2A07: {
        dir: Direction_js_1.V,
        sizes: [1.03, 1.9]
    },
    0x2A08: {
        dir: Direction_js_1.V,
        sizes: [1.03, 1.9]
    },
    0x2A09: {
        dir: Direction_js_1.V,
        sizes: [1.014, 1.296]
    },
    0x2A0A: {
        dir: Direction_js_1.V,
        sizes: [1.007, 1.401]
    },
    0x2A0B: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0x2A0C: {
        dir: Direction_js_1.V,
        sizes: [1.114, 2.223]
    },
    0x2A0D: {
        dir: Direction_js_1.V,
        sizes: [1.114, 2.223]
    },
    0x2A0E: {
        dir: Direction_js_1.V,
        sizes: [1.114, 2.223]
    },
    0x2A0F: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0x2A10: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0x2A11: {
        dir: Direction_js_1.V,
        sizes: [1.098, 2.223]
    },
    0x2A12: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0x2A13: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0x2A14: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0x2A15: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0x2A16: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0x2A17: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0x2A18: {
        dir: Direction_js_1.V,
        sizes: [1.114, 2.223]
    },
    0x2A19: {
        dir: Direction_js_1.V,
        sizes: [1.114, 2.223]
    },
    0x2A1A: {
        dir: Direction_js_1.V,
        sizes: [1.114, 2.223]
    },
    0x2A1B: {
        dir: Direction_js_1.V,
        sizes: [1.284, 2.465]
    },
    0x2A1C: {
        dir: Direction_js_1.V,
        sizes: [1.284, 2.485]
    },
    0x2A1D: {
        dir: Direction_js_1.V,
        sizes: [0.822, 1.15]
    },
    0x2A1E: {
        dir: Direction_js_1.V,
        sizes: [0.78, 1.156]
    },
    0x2A20: {
        dir: Direction_js_1.V,
        sizes: [0.609, 0.827]
    },
    0x2A21: {
        dir: Direction_js_1.V,
        sizes: [0.889, 1.26]
    },
    0x2AFC: {
        dir: Direction_js_1.V,
        sizes: [1.008, 1.915]
    },
    0x2AFF: {
        dir: Direction_js_1.V,
        sizes: [1.241, 1.921]
    },
    0x2B04: {
        dir: Direction_js_1.H,
        sizes: [0.951, 1.397],
        stretch: [0xE0F0, 0xE0F1, 0xE0F2],
        stretchv: [3, 1, 4],
        HDW: [0.52, 0.02, 1.062],
        hd: [0.52, 0.02]
    },
    0x2B05: {
        dir: Direction_js_1.H,
        sizes: [0.866, 1.312],
        stretch: [0xE0F3, 0xE0F4, 0xE0F5],
        stretchv: [3, 1, 4],
        HDW: [0.468, -0.032, 0.977],
        hd: [0.468, -0.032]
    },
    0x2B06: {
        dir: Direction_js_1.V,
        sizes: [0.866, 1.312],
        stretch: [0, 0xE01F, 0],
        HDW: [0.672, 0.193, 0.612]
    },
    0x2B07: {
        dir: Direction_js_1.V,
        sizes: [0.866, 1.312],
        stretch: [0, 0xE020, 0],
        HDW: [0.693, 0.172, 0.612]
    },
    0x2B0C: {
        dir: Direction_js_1.H,
        sizes: [0.845, 1.291],
        stretch: [0xE0F6, 0xE0F7, 0xE0F8],
        stretchv: [3, 1, 4],
        HDW: [0.468, -0.032, 1.022],
        hd: [0.468, -0.032]
    },
    0x2B0D: {
        dir: Direction_js_1.V,
        sizes: [0.845, 1.291],
        stretch: [0, 0xE021, 0],
        HDW: [0.672, 0.172, 0.549]
    },
    0x2B31: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.353],
        stretch: [0xE0F9, 0xE0FA, 0xE0FB],
        stretchv: [3, 1, 4],
        HDW: [0.987, 0.489, 1],
        hd: [0.987, 0.489]
    },
    0xE036: {
        dir: Direction_js_1.V,
        sizes: [1.01, 1.404]
    },
    0xE376: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0xE377: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0xE395: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0xE397: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0xE398: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0xE399: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0xE39A: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0xE39B: {
        dir: Direction_js_1.V,
        sizes: [1.098, 2.223]
    },
    0xE3D3: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0xEA57: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0x1EEF0: {
        dir: Direction_js_1.V,
        sizes: [0.553, 0.738]
    },
    0x1EEF1: {
        dir: Direction_js_1.V,
        sizes: [0.546, 0.743]
    }
};
