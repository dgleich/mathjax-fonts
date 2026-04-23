const path = require('path');

module.exports = {
  mode: 'production',
  entry: path.resolve(__dirname, 'tex-mml-svg-mathjax-libertinus-nosre.js'),
  output: {
    filename: 'tex-mml-svg-mathjax-libertinus-nosre.js',
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
  externals: {
    'speech-rule-engine': 'SRE'
  },
  performance: {
    maxAssetSize: 5000000,
    maxEntrypointSize: 5000000
  }
};
