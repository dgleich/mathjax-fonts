"use strict";
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
})();
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
};
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
};
var __spreadArray = (this && this.__spreadArray) || function (to, from, pack) {
    if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
        if (ar || !(i in from)) {
            if (!ar) ar = Array.prototype.slice.call(from, 0, i);
            ar[i] = from[i];
        }
    }
    return to.concat(ar || Array.prototype.slice.call(from));
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.MathJaxShantell = void 0;
var FontData_js_1 = require("@mathjax/src/cjs/output/chtml/FontData.js");
var common_js_1 = require("./common.js");
var normal_js_1 = require("./chtml/normal.js");
var bold_js_1 = require("./chtml/bold.js");
var italic_js_1 = require("./chtml/italic.js");
var bold_italic_js_1 = require("./chtml/bold-italic.js");
var monospace_js_1 = require("./chtml/monospace.js");
var smallop_js_1 = require("./chtml/smallop.js");
var largeop_js_1 = require("./chtml/largeop.js");
var size3_js_1 = require("./chtml/size3.js");
var size4_js_1 = require("./chtml/size4.js");
var size5_js_1 = require("./chtml/size5.js");
var size6_js_1 = require("./chtml/size6.js");
var size7_js_1 = require("./chtml/size7.js");
var size8_js_1 = require("./chtml/size8.js");
var size9_js_1 = require("./chtml/size9.js");
var size10_js_1 = require("./chtml/size10.js");
var size11_js_1 = require("./chtml/size11.js");
var size12_js_1 = require("./chtml/size12.js");
var size13_js_1 = require("./chtml/size13.js");
var size14_js_1 = require("./chtml/size14.js");
var size15_js_1 = require("./chtml/size15.js");
var lf_tp_js_1 = require("./chtml/lf-tp.js");
var rt_bt_js_1 = require("./chtml/rt-bt.js");
var ext_js_1 = require("./chtml/ext.js");
var mid_js_1 = require("./chtml/mid.js");
var up_js_1 = require("./chtml/up.js");
var dup_js_1 = require("./chtml/dup.js");
var delimiters_js_1 = require("./chtml/delimiters.js");
var Base = (0, common_js_1.CommonMathJaxShantellMixin)(FontData_js_1.ChtmlFontData);
var MathJaxShantell = (function (_super) {
    __extends(MathJaxShantell, _super);
    function MathJaxShantell() {
        var _this = _super.apply(this, __spreadArray([], __read(arguments), false)) || this;
        _this.cssFontPrefix = 'SHANTELL';
        return _this;
    }
    MathJaxShantell.NAME = 'MathJaxShantell';
    MathJaxShantell.OPTIONS = __assign(__assign({}, Base.OPTIONS), { fontURL: '@mathjax/mathjax-shantell-font/js/chtml/woff2', dynamicPrefix: '@mathjax/mathjax-shantell-font/js/chtml/dynamic' });
    MathJaxShantell.defaultCssFamilyPrefix = 'MJX-SHANTELL-ZERO';
    MathJaxShantell.defaultVariantLetters = {
        'normal': '',
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
        '-mid': 'M-a',
        '-up': 'U',
        '-dup': 'D'
    };
    MathJaxShantell.defaultDelimiters = delimiters_js_1.delimiters;
    MathJaxShantell.defaultChars = {
        'normal': normal_js_1.normal,
        'bold': bold_js_1.bold,
        'italic': italic_js_1.italic,
        'bold-italic': bold_italic_js_1.boldItalic,
        'monospace': monospace_js_1.monospace,
        '-smallop': smallop_js_1.smallop,
        '-largeop': largeop_js_1.largeop,
        '-size3': size3_js_1.size3,
        '-size4': size4_js_1.size4,
        '-size5': size5_js_1.size5,
        '-size6': size6_js_1.size6,
        '-size7': size7_js_1.size7,
        '-size8': size8_js_1.size8,
        '-size9': size9_js_1.size9,
        '-size10': size10_js_1.size10,
        '-size11': size11_js_1.size11,
        '-size12': size12_js_1.size12,
        '-size13': size13_js_1.size13,
        '-size14': size14_js_1.size14,
        '-size15': size15_js_1.size15,
        '-lf-tp': lf_tp_js_1.lfTp,
        '-rt-bt': rt_bt_js_1.rtBt,
        '-ext': ext_js_1.ext,
        '-mid': mid_js_1.mid,
        '-up': up_js_1.up,
        '-dup': dup_js_1.dup
    };
    MathJaxShantell.defaultStyles = __assign(__assign({}, FontData_js_1.ChtmlFontData.defaultStyles), {
        'mjx-container[jax="CHTML"] > mjx-math.SHANTELL-N[breakable] > *': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-N' },
        '.SHANTELL-N': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-N' },
        '.SHANTELL-N': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-N' },
        '.SHANTELL-B': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-B' },
        '.SHANTELL-I': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-I' },
        '.SHANTELL-BI': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-BI' },
        '.SHANTELL-M': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-M' },
        '.SHANTELL-SO': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-SO' },
        '.SHANTELL-LO': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-LO' },
        '.SHANTELL-S3': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-S3' },
        '.SHANTELL-S4': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-S4' },
        '.SHANTELL-S5': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-S5' },
        '.SHANTELL-S6': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-S6' },
        '.SHANTELL-S7': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-S7' },
        '.SHANTELL-S8': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-S8' },
        '.SHANTELL-S9': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-S9' },
        '.SHANTELL-S10': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-S10' },
        '.SHANTELL-S11': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-S11' },
        '.SHANTELL-S12': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-S12' },
        '.SHANTELL-S13': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-S13' },
        '.SHANTELL-S14': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-S14' },
        '.SHANTELL-S15': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-S15' },
        '.SHANTELL-LT': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-LT' },
        '.SHANTELL-RB': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-RB' },
        '.SHANTELL-E': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-E' },
        '.SHANTELL-M-a': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-M-a' },
        '.SHANTELL-U': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-U' },
        '.SHANTELL-D': { 'font-family': 'MJX-SHANTELL-ZERO, MJX-SHANTELL-D' }
    });
    MathJaxShantell.defaultFonts = __assign(__assign({}, FontData_js_1.ChtmlFontData.defaultFonts), {
        '@font-face /* MJX-SHANTELL-ZERO */': {
            'font-family': 'MJX-SHANTELL-ZERO',
            src: 'url("%%URL%%/mjx-shantell-zero.woff2") format("woff2")'
        },
        '@font-face /* MJX-SHANTELL-N */': {
            'font-family': 'MJX-SHANTELL-N',
            src: 'url("%%URL%%/mjx-shantell-n.woff2") format("woff2")'
        },
        '@font-face /* MJX-SHANTELL-B */': {
            'font-family': 'MJX-SHANTELL-B',
            src: 'url("%%URL%%/mjx-shantell-b.woff2") format("woff2")'
        },
        '@font-face /* MJX-SHANTELL-I */': {
            'font-family': 'MJX-SHANTELL-I',
            src: 'url("%%URL%%/mjx-shantell-i.woff2") format("woff2")'
        },
        '@font-face /* MJX-SHANTELL-BI */': {
            'font-family': 'MJX-SHANTELL-BI',
            src: 'url("%%URL%%/mjx-shantell-bi.woff2") format("woff2")'
        }
    });
    return MathJaxShantell;
}(Base));
exports.MathJaxShantell = MathJaxShantell;
