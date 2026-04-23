require('@mathjax/src/cjs/startup/startup.js');
require('@mathjax/src/cjs/input/tex.js');
require('@mathjax/src/cjs/input/mml.js');
require('@mathjax/src/cjs/output/svg.js');
var font = require('@mathjax/mathjax-libertinus-font/js/svg.js');
MathJax.config.output = MathJax.config.output || {};
MathJax.config.output.font = new font.MathJaxLibertinus();
require('@mathjax/src/cjs/startup/ready.js');
