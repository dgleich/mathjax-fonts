#!/usr/bin/env node
/**
 * Render TeX to PNG using MathJax + sharp.
 * Usage: node render-tex.js <font-package> <tex-string> [output.png]
 * Example: node render-tex.js mathjax-libertinus '\hat{f}\;\hat{x}\;\hat{A}' accents.png
 */

const path = require('path');
const fs = require('fs');

const fontPkg = process.argv[2] || 'mathjax-libertinus';
const tex = process.argv[3] || '\\hat{f}\\;\\hat{x}\\;U\\Sigma V^T';
const outFile = process.argv[4] || 'output.png';

// Load the font bundle
const bundlePath = path.resolve(__dirname, '..', fontPkg, `tex-mml-svg-${fontPkg}.js`);
if (!fs.existsSync(bundlePath)) {
    console.error(`Bundle not found: ${bundlePath}`);
    process.exit(1);
}

// MathJax server-side rendering
require(bundlePath);

const {mathjax} = require('@mathjax/src/cjs/mathjax.js');
const {TeX} = require('@mathjax/src/cjs/input/tex.js');
const {SVG} = require('@mathjax/src/cjs/output/svg.js');
const {liteAdaptor} = require('@mathjax/src/cjs/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require('@mathjax/src/cjs/handlers/html.js');

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);

const texInput = new TeX({});
const svgOutput = new SVG({fontCache: 'local'});
const html = mathjax.document('', {InputJax: texInput, OutputJax: svgOutput});

const node = html.convert(tex, {display: true});
const svgString = adaptor.outerHTML(node);

// Save SVG
const svgFile = outFile.replace('.png', '.svg');
fs.writeFileSync(svgFile, svgString);
console.log(`SVG saved: ${svgFile}`);

// Convert to PNG
try {
    const sharp = require('sharp');
    sharp(Buffer.from(svgString))
        .resize({width: 800})
        .png()
        .toFile(outFile)
        .then(() => console.log(`PNG saved: ${outFile}`))
        .catch(err => console.error('PNG conversion failed:', err.message));
} catch(e) {
    console.log('sharp not available, SVG only');
}
