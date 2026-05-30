#!/usr/bin/env node
/**
 * Render TeX to SVG/PNG using MathJax server-side with custom fonts.
 * Usage: node render-tex.js <font-package> '<tex>' [output.svg] [--inline]
 *
 * IMPORTANT: Use single quotes for the TeX string to preserve backslashes!
 * Example: node render-tex.js mathjax-libertinus '\hat{f}\;\hat{x}\;U\Sigma V^T' test.svg
 *          node render-tex.js mathjax-libertinus '\int_a^b' test.svg --inline
 */
const path = require('path');
const fs = require('fs');

const fontPkg = process.argv[2] || 'mathjax-libertinus';
const tex = process.argv[3] || '\\hat{f} \\quad \\hat{x} \\quad U\\Sigma V^T';
const outFile = process.argv[4] || 'output.svg';
const displayMode = !process.argv.includes('--inline');

// Redirect font module resolution to our custom font package
const fontCjsDir = path.resolve(__dirname, '..', fontPkg, 'cjs');
const Module = require('module');
const origResolve = Module._resolveFilename;
Module._resolveFilename = function(request, parent, isMain, options) {
    if (request.includes('@mathjax/mathjax-newcm-font/cjs')) {
        const r = request.replace(/@mathjax\/mathjax-newcm-font\/cjs/, fontCjsDir);
        try { return origResolve.call(this, r, parent, isMain, options); } catch(e) {}
    }
    if (request.includes('#default-font')) {
        const r = request.replace(/#default-font/, fontCjsDir);
        try { return origResolve.call(this, r, parent, isMain, options); } catch(e) {}
    }
    return origResolve.call(this, request, parent, isMain, options);
};

const {mathjax} = require('@mathjax/src/cjs/mathjax.js');
const {TeX} = require('@mathjax/src/cjs/input/tex.js');
const {SVG} = require('@mathjax/src/cjs/output/svg.js');
const {liteAdaptor} = require('@mathjax/src/cjs/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require('@mathjax/src/cjs/handlers/html.js');

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);

require('@mathjax/src/cjs/input/tex/ams/AmsConfiguration.js');
require('@mathjax/src/cjs/input/tex/boldsymbol/BoldsymbolConfiguration.js');
const texInput = new TeX({packages: ['base', 'ams', 'boldsymbol']});
const svgOutput = new SVG({fontCache: 'local'});
const html = mathjax.document('', {InputJax: texInput, OutputJax: svgOutput});

const node = html.convert(tex, {display: displayMode});
const svgString = adaptor.outerHTML(node);

// Extract just the SVG element
const svgMatch = svgString.match(/<svg[^>]*>[\s\S]*<\/svg>/);
const svg = svgMatch ? svgMatch[0] : svgString;

fs.writeFileSync(outFile, svg);
console.log(`SVG: ${outFile} (${svg.length} chars)${displayMode ? '' : ' [inline]'}`);

// Also generate PNG via sharp
const pngFile = outFile.replace(/\.svg$/, '.png');
try {
    const sharp = require('sharp');
    sharp(Buffer.from(svg))
        .flatten({background: {r: 255, g: 255, b: 255}})
        .resize({width: 1200})
        .png()
        .toFile(pngFile)
        .then(() => console.log(`PNG: ${pngFile}`))
        .catch(e => console.log(`PNG failed: ${e.message}`));
} catch(e) {
    console.log('sharp not available for PNG conversion');
}
