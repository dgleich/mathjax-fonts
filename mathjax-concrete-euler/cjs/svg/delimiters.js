"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.delimiters = void 0;
var Direction_js_1 = require("@mathjax/src/cjs/output/common/Direction.js");
exports.delimiters = {
    0x28: {
        dir: Direction_js_1.V,
        sizes: [0.909, 1.201, 1.801, 2.401, 3.001],
        stretch: [0x239B, 0x239C, 0x239D],
        HDW: [0.704, 0.204, 0.328]
    },
    0x29: {
        dir: Direction_js_1.V,
        sizes: [0.909, 1.201, 1.801, 2.401, 3.001],
        stretch: [0x239E, 0x239F, 0x23A0],
        HDW: [0.704, 0.204, 0.328]
    },
    0x2D: {
        c: 0x2212,
        dir: Direction_js_1.H,
        stretch: [0, 0x2212]
    },
    0x2F: {
        dir: Direction_js_1.V,
        sizes: [0.913, 1.201, 1.8, 2.4, 3]
    },
    0x3D: {
        dir: Direction_js_1.H,
        stretch: [0xE4C0, 0xE4C2, 0xE4C1],
        stretchv: [3, 1, 4],
        HDW: [0.368, -0.132, 0.756],
        hd: [0.368, -0.132]
    },
    0x5B: {
        dir: Direction_js_1.V,
        sizes: [0.909, 1.201, 1.8, 2.4, 3.001],
        stretch: [0x23A1, 0x23A2, 0x23A3],
        HDW: [0.704, 0.204, 0.29]
    },
    0x5C: {
        dir: Direction_js_1.V,
        sizes: [0.909, 1.201, 1.8, 2.4, 3]
    },
    0x5D: {
        dir: Direction_js_1.V,
        sizes: [0.909, 1.201, 1.8, 2.4, 3.001],
        stretch: [0x23A4, 0x23A5, 0x23A6],
        HDW: [0.704, 0.204, 0.29]
    },
    0x5E: {
        c: 0x302,
        dir: Direction_js_1.H,
        sizes: [0.338, 0.537, 0.765, 0.992, 1.22, 1.782, 2.234, 2.802, 3.028]
    },
    0x7B: {
        dir: Direction_js_1.V,
        sizes: [0.909, 1.201, 1.801, 2.401, 3.001],
        stretch: [0x23A7, 0x23AA, 0x23A9, 0x23A8],
        HDW: [0.704, 0.204, 0.345]
    },
    0x7C: {
        dir: Direction_js_1.V,
        sizes: [0.909, 1.201, 1.801, 2.401, 3.001],
        stretch: [0, 0xE3D8],
        stretchv: [0, 1],
        HDW: [0.704, 0.204, 0.213]
    },
    0x7D: {
        dir: Direction_js_1.V,
        sizes: [0.909, 1.201, 1.801, 2.401, 3.001],
        stretch: [0x23AB, 0x23AA, 0x23AD, 0x23AC],
        HDW: [0.704, 0.204, 0.345]
    },
    0x7E: {
        c: 0x303,
        dir: Direction_js_1.H,
        sizes: [0.322, 0.451, 0.59, 0.772, 1.012, 1.326, 1.736, 2.274, 2.978]
    },
    0x2C6: {
        c: 0x302,
        dir: Direction_js_1.H,
        sizes: [0.338, 0.537, 0.765, 0.992, 1.22, 1.782, 2.234, 2.802, 3.028]
    },
    0x2C9: {
        c: 0xAF,
        dir: Direction_js_1.H
    },
    0x2DC: {
        c: 0x303,
        dir: Direction_js_1.H,
        sizes: [0.322, 0.451, 0.59, 0.772, 1.012, 1.326, 1.736, 2.274, 2.978]
    },
    0x302: {
        dir: Direction_js_1.H,
        sizes: [0.338, 0.537, 0.765, 0.992, 1.22, 1.782, 2.234, 2.802, 3.028]
    },
    0x303: {
        dir: Direction_js_1.H,
        sizes: [0.322, 0.451, 0.59, 0.772, 1.012, 1.326, 1.736, 2.274, 2.978]
    },
    0x305: {
        dir: Direction_js_1.H,
        stretch: [0xE50E, 0xE50F, 0],
        stretchv: [3, 1, 0],
        HDW: [0.612, -0.572, 0],
        hd: [0.612, -0.572]
    },
    0x306: {
        dir: Direction_js_1.H,
        sizes: [0.283, 0.481, 0.763, 1.003, 1.203, 1.503, 1.803, 2.203, 2.603]
    },
    0x30C: {
        dir: Direction_js_1.H,
        sizes: [0.338, 0.537, 0.765, 0.992, 1.22, 1.782, 2.234, 2.802, 3.028]
    },
    0x330: {
        dir: Direction_js_1.H,
        sizes: [0.322, 0.45, 0.59, 0.772, 1.012, 1.326, 1.736, 2.274, 2.978]
    },
    0x332: {
        dir: Direction_js_1.H,
        stretch: [0x332, 0xE5BD, 0],
        stretchv: [3, 1, 0],
        HDW: [-0.19, 0.23, 0.392],
        hd: [-0.19, 0.23]
    },
    0x34D: {
        dir: Direction_js_1.H,
        sizes: [0.451, 0.551, 0.651, 0.751],
        stretch: [0xE5C7, 0xE5C0, 0xE5C4],
        stretchv: [3, 1, 4],
        HDW: [-0.075, 0.346, 0.45],
        hd: [-0.075, 0.346]
    },
    0x2013: {
        dir: Direction_js_1.H,
        stretch: [0, 0x2013],
        HDW: [0.276, -0.236, 0.5],
        hd: [0.276, -0.236]
    },
    0x2014: {
        dir: Direction_js_1.H,
        stretch: [0, 0x2014],
        HDW: [0.276, -0.236, 1],
        hd: [0.276, -0.236]
    },
    0x2015: {
        dir: Direction_js_1.H,
        stretch: [0, 0x2015],
        HDW: [0.276, -0.236, 1.166],
        hd: [0.276, -0.236]
    },
    0x2016: {
        dir: Direction_js_1.V,
        sizes: [0.909, 1.201, 1.801, 2.401, 3.001],
        stretch: [0, 0xE3E8],
        stretchv: [0, 1],
        HDW: [0.704, 0.204, 0.392]
    },
    0x203E: {
        c: 0xAF,
        dir: Direction_js_1.H
    },
    0x20D0: {
        dir: Direction_js_1.H,
        sizes: [0.419, 0.531, 0.641, 0.751],
        stretch: [0xE5AF, 0xE5A0, 0],
        stretchv: [3, 1, 0],
        HDW: [0.75, -0.595, 0],
        hd: [0.75, -0.595]
    },
    0x20D1: {
        dir: Direction_js_1.H,
        sizes: [0.419, 0.531, 0.641, 0.751],
        stretch: [0, 0xE5A0, 0xE5AC],
        stretchv: [0, 1, 4],
        HDW: [0.75, -0.595, 0],
        hd: [0.75, -0.595]
    },
    0x20D5: {
        dir: Direction_js_1.H,
        sizes: [0.61, 1, 1.4, 1.8, 2.2]
    },
    0x20D6: {
        dir: Direction_js_1.H,
        sizes: [0.419, 0.531, 0.64, 0.75],
        stretch: [0xE5A9, 0xE5A0, 0],
        stretchv: [3, 1, 0],
        HDW: [0.75, -0.479, 0],
        hd: [0.75, -0.479]
    },
    0x20D7: {
        dir: Direction_js_1.H,
        sizes: [0.419, 0.531, 0.64, 0.75],
        stretch: [0, 0xE5A0, 0xE5A6],
        stretchv: [0, 1, 4],
        HDW: [0.75, -0.479, 0],
        hd: [0.75, -0.479]
    },
    0x20E1: {
        dir: Direction_js_1.H,
        sizes: [0.451, 0.551, 0.651, 0.751],
        stretch: [0xE5A7, 0xE5A0, 0xE5A4],
        stretchv: [3, 1, 4],
        HDW: [0.75, -0.479, 0],
        hd: [0.75, -0.479]
    },
    0x20EC: {
        dir: Direction_js_1.H,
        sizes: [0.419, 0.531, 0.641, 0.751],
        stretch: [0, 0xE5C0, 0xE5CC],
        stretchv: [0, 1, 4],
        HDW: [-0.19, 0.346, 0.418],
        hd: [-0.19, 0.346]
    },
    0x20ED: {
        dir: Direction_js_1.H,
        sizes: [0.419, 0.531, 0.641, 0.751],
        stretch: [0xE5CF, 0xE5C0, 0],
        stretchv: [3, 1, 0],
        HDW: [-0.19, 0.346, 0.418],
        hd: [-0.19, 0.346]
    },
    0x20EE: {
        dir: Direction_js_1.H,
        sizes: [0.419, 0.531, 0.64, 0.75],
        stretch: [0xE5C9, 0xE5C0, 0],
        stretchv: [3, 1, 0],
        HDW: [-0.075, 0.346, 0.418],
        hd: [-0.075, 0.346]
    },
    0x20EF: {
        dir: Direction_js_1.H,
        sizes: [0.419, 0.531, 0.64, 0.75],
        stretch: [0, 0xE5C0, 0xE5C6],
        stretchv: [0, 1, 4],
        HDW: [-0.075, 0.346, 0.418],
        hd: [-0.075, 0.346]
    },
    0x2140: {
        dir: Direction_js_1.V,
        sizes: [0.951, 1.331]
    },
    0x2190: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.499],
        stretch: [0xE4A0, 0x23AF, 0xE4AF],
        stretchv: [3, 1, 4],
        HDW: [0.5, 0, 1],
        hd: [0.5, 0]
    },
    0x2191: {
        dir: Direction_js_1.V,
        sizes: [0.888, 1.221],
        stretch: [0, 0xE3B9],
        stretchv: [0, 1],
        HDW: [0.693, 0.194, 0.5]
    },
    0x2192: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.499],
        stretch: [0xE4AE, 0x23AF, 0xE4A1],
        stretchv: [3, 1, 4],
        HDW: [0.5, 0, 1],
        hd: [0.5, 0]
    },
    0x2193: {
        dir: Direction_js_1.V,
        sizes: [0.888, 1.221],
        stretch: [0, 0xE3BC],
        stretchv: [0, 1],
        HDW: [0.693, 0.194, 0.5]
    },
    0x2194: {
        dir: Direction_js_1.H,
        sizes: [0.888, 1.588],
        stretch: [0xE4A0, 0x23AF, 0xE4A1],
        stretchv: [3, 1, 4],
        HDW: [0.5, 0, 1],
        hd: [0.5, 0]
    },
    0x219E: {
        dir: Direction_js_1.H,
        stretch: [0xE4A6, 0x23AF, 0xE4AF],
        stretchv: [3, 1, 4],
        HDW: [0.5, 0, 1],
        hd: [0.5, 0]
    },
    0x21A0: {
        dir: Direction_js_1.H,
        stretch: [0xE4AE, 0x23AF, 0xE4A7],
        stretchv: [3, 1, 4],
        HDW: [0.5, 0, 1],
        hd: [0.5, 0]
    },
    0x21A2: {
        dir: Direction_js_1.H,
        stretch: [0xE4A0, 0x23AF, 0xE4AD],
        stretchv: [3, 1, 4],
        HDW: [0.5, 0, 1],
        hd: [0.5, 0]
    },
    0x21A3: {
        dir: Direction_js_1.H,
        stretch: [0xE4AC, 0x23AF, 0xE4A1],
        stretchv: [3, 1, 4],
        HDW: [0.5, 0, 1],
        hd: [0.5, 0]
    },
    0x21A4: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.579],
        stretch: [0xE4A0, 0x23AF, 0xE4AA],
        stretchv: [3, 1, 4],
        HDW: [0.5, 0, 1],
        hd: [0.5, 0]
    },
    0x21A6: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.579],
        stretch: [0xE4AB, 0x23AF, 0xE4A1],
        stretchv: [3, 1, 4],
        HDW: [0.5, 0, 1],
        hd: [0.5, 0]
    },
    0x21A9: {
        dir: Direction_js_1.H,
        stretch: [0xE4A0, 0x23AF, 0xE4A9],
        stretchv: [3, 1, 4],
        HDW: [0.554, 0, 1],
        hd: [0.554, 0]
    },
    0x21AA: {
        dir: Direction_js_1.H,
        stretch: [0xE4A8, 0x23AF, 0xE4A1],
        stretchv: [3, 1, 4],
        HDW: [0.554, 0, 1],
        hd: [0.554, 0]
    },
    0x21BC: {
        dir: Direction_js_1.H,
        stretch: [0xE4A4, 0x23AF, 0xE4AF],
        stretchv: [3, 1, 4],
        HDW: [0.5, -0.23, 1],
        hd: [0.5, -0.23]
    },
    0x21BD: {
        dir: Direction_js_1.H,
        stretch: [0xE4A2, 0x23AF, 0xE4AF],
        stretchv: [3, 1, 4],
        HDW: [0.27, 0, 1],
        hd: [0.27, 0]
    },
    0x21C0: {
        dir: Direction_js_1.H,
        stretch: [0xE4AE, 0x23AF, 0xE4A5],
        stretchv: [3, 1, 4],
        HDW: [0.5, -0.23, 1],
        hd: [0.5, -0.23]
    },
    0x21C1: {
        dir: Direction_js_1.H,
        stretch: [0xE4AE, 0x23AF, 0xE4A3],
        stretchv: [3, 1, 4],
        HDW: [0.27, 0, 1],
        hd: [0.27, 0]
    },
    0x21C4: {
        dir: Direction_js_1.H,
        stretch: [0xE4B8, 0xE4BD, 0xE4B7],
        stretchv: [3, 1, 4],
        HDW: [0.63, 0.128, 1],
        hd: [0.63, 0.128]
    },
    0x21C6: {
        dir: Direction_js_1.H,
        stretch: [0xE4B6, 0xE4BD, 0xE4B9],
        stretchv: [3, 1, 4],
        HDW: [0.63, 0.128, 1],
        hd: [0.63, 0.128]
    },
    0x21CB: {
        dir: Direction_js_1.H,
        stretch: [0xE4B4, 0xE4C2, 0xE4B3],
        stretchv: [3, 1, 4],
        HDW: [0.599, 0.098, 0.999],
        hd: [0.599, 0.098]
    },
    0x21CC: {
        dir: Direction_js_1.H,
        stretch: [0xE4B2, 0xE4C2, 0xE4B5],
        stretchv: [3, 1, 4],
        HDW: [0.599, 0.098, 0.999],
        hd: [0.599, 0.098]
    },
    0x21D0: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.568],
        stretch: [0xE4B0, 0xE4C2, 0xE4BE],
        stretchv: [3, 1, 4],
        HDW: [0.598, 0.098, 1],
        hd: [0.598, 0.098]
    },
    0x21D1: {
        dir: Direction_js_1.V,
        sizes: [0.869, 1.201],
        stretch: [0, 0xE3C9],
        stretchv: [0, 1],
        HDW: [0.694, 0.174, 0.667]
    },
    0x21D2: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.568],
        stretch: [0xE4BF, 0xE4C2, 0xE4B1],
        stretchv: [3, 1, 4],
        HDW: [0.598, 0.098, 1],
        hd: [0.598, 0.098]
    },
    0x21D3: {
        dir: Direction_js_1.V,
        sizes: [0.869, 1.201],
        stretch: [0, 0xE3CC],
        stretchv: [0, 1],
        HDW: [0.694, 0.174, 0.667]
    },
    0x21D4: {
        dir: Direction_js_1.H,
        sizes: [0.933, 1.633],
        stretch: [0xE4B0, 0xE4C2, 0xE4B1],
        stretchv: [3, 1, 4],
        HDW: [0.598, 0.098, 1],
        hd: [0.598, 0.098]
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
        sizes: [1.001, 1.401]
    },
    0x2212: {
        dir: Direction_js_1.H,
        stretch: [0xE4C6, 0x23AF, 0xE4C7],
        stretchv: [3, 1, 4],
        HDW: [0.27, -0.23, 0.756],
        hd: [0.27, -0.23]
    },
    0x221A: {
        dir: Direction_js_1.V,
        sizes: [0.982, 1.355, 1.802, 2.404, 3.004],
        stretch: [0xE3AB, 0xE3AA, 0x23B7],
        HDW: [0.78, 0.201, 0.825]
    },
    0x221B: {
        dir: Direction_js_1.V,
        sizes: [0.982, 1.355, 1.802, 2.404, 3.004]
    },
    0x221C: {
        dir: Direction_js_1.V,
        sizes: [0.982, 1.355, 1.802, 2.404, 3.004]
    },
    0x2223: {
        dir: Direction_js_1.V,
        sizes: [0.801],
        stretch: [0, 0xE3DB],
        stretchv: [0, 1],
        HDW: [0.65, 0.15, 0.212]
    },
    0x2225: {
        dir: Direction_js_1.V,
        sizes: [0.801],
        stretch: [0, 0xE3EB],
        stretchv: [0, 1],
        HDW: [0.65, 0.15, 0.392]
    },
    0x222B: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223],
        stretch: [0x2320, 0x23AE, 0x2321],
        HDW: [0.806, 0.305, 0.556]
    },
    0x222C: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0x222D: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0x222E: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0x222F: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0x2230: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0x2231: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0x2232: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0x2233: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0x2261: {
        dir: Direction_js_1.H,
        stretch: [0xE4C3, 0xE4C5, 0xE4C4],
        stretchv: [3, 1, 4],
        HDW: [0.465, -0.036, 0.83],
        hd: [0.465, -0.036]
    },
    0x22C0: {
        dir: Direction_js_1.V,
        sizes: [0.999, 1.396]
    },
    0x22C1: {
        dir: Direction_js_1.V,
        sizes: [0.999, 1.396]
    },
    0x22C2: {
        dir: Direction_js_1.V,
        sizes: [0.965, 1.359]
    },
    0x22C3: {
        dir: Direction_js_1.V,
        sizes: [0.965, 1.359]
    },
    0x2308: {
        dir: Direction_js_1.V,
        sizes: [0.909, 1.201, 1.801, 2.401, 3.001],
        stretch: [0, 0xE38E],
        stretchv: [0, 1],
        HDW: [0.704, 0.204, 0.29]
    },
    0x2309: {
        dir: Direction_js_1.V,
        sizes: [0.909, 1.201, 1.801, 2.401, 3.001],
        stretch: [0, 0xE38F],
        stretchv: [0, 1],
        HDW: [0.704, 0.204, 0.29]
    },
    0x230A: {
        dir: Direction_js_1.V,
        sizes: [0.909, 1.201, 1.801, 2.401, 3.001],
        stretch: [0, 0xE37C],
        stretchv: [0, 1],
        HDW: [0.704, 0.204, 0.29]
    },
    0x230B: {
        dir: Direction_js_1.V,
        sizes: [0.909, 1.201, 1.801, 2.401, 3.001],
        stretch: [0, 0xE37D],
        stretchv: [0, 1],
        HDW: [0.704, 0.204, 0.29]
    },
    0x23B4: {
        dir: Direction_js_1.H,
        sizes: [0.631, 0.941, 1.411, 1.661],
        stretch: [0xE590, 0xE593, 0xE591],
        stretchv: [3, 1, 4],
        HDW: [0.74, -0.581, 0.63],
        hd: [0.74, -0.581]
    },
    0x23B5: {
        dir: Direction_js_1.H,
        sizes: [0.631, 0.941, 1.411, 1.661],
        stretch: [0xE598, 0xE59B, 0xE599],
        stretchv: [3, 1, 4],
        HDW: [-0.071, 0.23, 0.63],
        hd: [-0.071, 0.23]
    },
    0x23DC: {
        dir: Direction_js_1.H,
        sizes: [0.601, 0.901, 1.201, 1.551, 1.901, 2.301],
        stretch: [0xE5B0, 0xE5B3, 0xE5B1],
        stretchv: [3, 1, 4],
        HDW: [0.698, -0.51, 0.6],
        hd: [0.698, -0.51]
    },
    0x23DD: {
        dir: Direction_js_1.H,
        sizes: [0.601, 0.901, 1.201, 1.551, 1.901, 2.301],
        stretch: [0xE5B8, 0xE5BA, 0xE5B9],
        stretchv: [3, 1, 4],
        HDW: [-0.07, 0.258, 0.6],
        hd: [-0.07, 0.258]
    },
    0x23DE: {
        dir: Direction_js_1.H,
        sizes: [0.601, 0.901, 1.201, 1.551, 1.901, 2.301],
        stretch: [0xE570, 0xE573, 0xE571, 0xE572],
        stretchv: [3, 1, 4, 2],
        HDW: [1.076, -0.51, 0.6],
        hd: [0.726, -0.51]
    },
    0x23DF: {
        dir: Direction_js_1.H,
        sizes: [0.601, 0.901, 1.201, 1.551, 1.901, 2.301],
        stretch: [0xE578, 0xE57B, 0xE579, 0xE57A],
        stretchv: [3, 1, 4, 2],
        HDW: [-0.07, 0.636, 0.6],
        hd: [-0.07, 0.286]
    },
    0x27E6: {
        dir: Direction_js_1.V,
        sizes: [0.909, 1.201, 1.801, 2.401, 3.001],
        stretch: [0xE34C, 0xE35E, 0xE35C],
        HDW: [0.704, 0.204, 0.36]
    },
    0x27E7: {
        dir: Direction_js_1.V,
        sizes: [0.909, 1.201, 1.801, 2.401, 3.001],
        stretch: [0xE34D, 0xE35F, 0xE35D],
        HDW: [0.704, 0.204, 0.36]
    },
    0x27E8: {
        dir: Direction_js_1.V,
        sizes: [0.915, 1.201, 1.801, 2.401, 3.001]
    },
    0x27E9: {
        dir: Direction_js_1.V,
        sizes: [0.915, 1.201, 1.801, 2.401, 3.001]
    },
    0x27EA: {
        dir: Direction_js_1.V,
        sizes: [0.915, 1.201, 1.801, 2.401, 3.001]
    },
    0x27EB: {
        dir: Direction_js_1.V,
        sizes: [0.915, 1.201, 1.801, 2.401, 3.001]
    },
    0x2906: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.568],
        stretch: [0xE4B0, 0xE4C2, 0xE4BA],
        stretchv: [3, 1, 4],
        HDW: [0.598, 0.098, 1],
        hd: [0.598, 0.098]
    },
    0x2907: {
        dir: Direction_js_1.H,
        sizes: [0.889, 1.569],
        stretch: [0xE4BB, 0xE4C2, 0xE4B1],
        stretchv: [3, 1, 4],
        HDW: [0.598, 0.098, 1],
        hd: [0.598, 0.098]
    },
    0x2980: {
        dir: Direction_js_1.V,
        sizes: [0.909, 1.201, 1.801, 2.401, 3.001],
        stretch: [0, 0xE3F8],
        stretchv: [0, 1],
        HDW: [0.704, 0.204, 0.452]
    },
    0x2A00: {
        dir: Direction_js_1.V,
        sizes: [0.907, 1.135]
    },
    0x2A01: {
        dir: Direction_js_1.V,
        sizes: [0.915, 1.135]
    },
    0x2A02: {
        dir: Direction_js_1.V,
        sizes: [0.907, 1.135]
    },
    0x2A03: {
        dir: Direction_js_1.V,
        sizes: [0.965, 1.359]
    },
    0x2A04: {
        dir: Direction_js_1.V,
        sizes: [0.965, 1.359]
    },
    0x2A05: {
        dir: Direction_js_1.V,
        sizes: [0.945, 1.339]
    },
    0x2A06: {
        dir: Direction_js_1.V,
        sizes: [0.945, 1.339]
    },
    0x2A09: {
        dir: Direction_js_1.V,
        sizes: [0.695, 0.875]
    },
    0x2A0C: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0x2A11: {
        dir: Direction_js_1.V,
        sizes: [1.112, 2.223]
    },
    0xE540: {
        dir: Direction_js_1.H,
        sizes: [0.616, 0.997, 1.397, 1.797, 2.197]
    },
    0xEA81: {
        dir: Direction_js_1.V,
        sizes: [0.992, 1.355, 1.802, 2.404, 3.004],
        stretch: [0xE3AB, 0xE3AA, 0x23B7],
        HDW: [0.546, 0.046, 0.666]
    }
};
