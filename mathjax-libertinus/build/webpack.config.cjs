const path = require('path');

module.exports = {
  mode: 'production',
  entry: path.resolve(__dirname, 'tex-mml-svg-mathjax-libertinus.js'),
  output: {
    filename: 'tex-mml-svg-mathjax-libertinus.js',
    path: path.resolve(__dirname, '..', 'dist'),
    library: 'MathJax',
    libraryTarget: 'umd',
    globalObject: 'this'
  },
  resolve: {
    alias: {
      '@mathjax/mathjax-libertinus-font': path.resolve(__dirname, '..')
    }
  },
  performance: {
    maxAssetSize: 5000000,
    maxEntrypointSize: 5000000
  }
};
