# MathJax Custom Font Packages

<human>
</human>

## Overview

This repository contains custom MathJax 4 SVG font packages that pair
different text fonts with OpenType math fonts. Each package is a
self-contained webpack bundle that can be dropped into any web project
or Tauri app to render LaTeX math in a specific font style.

## Packages

| Package | Text Font | Math Font | Status |
|---------|-----------|-----------|--------|
| `mathjax-libertinus` | Libertinus Serif | Libertinus Math | Complete |
| `mathjax-libertinus-sans` | Libertinus Sans | Libertinus Math | Complete |
| `mathjax-lm-sans` | CMU Sans Serif | NewCM Sans Math | Complete |
| `mathjax-noto-sans` | Noto Sans | Noto Sans Math | Complete |
| `mathjax-source-sans` | Source Sans 3 | Noto Sans Math | Complete |
| `mathjax-source-code` | Source Code Pro | Noto Sans Math | Complete |
| `mathjax-concrete-euler` | CMU Concrete | Euler Math | Complete |
| `mathjax-shantell` | Shantell Sans | Noto Sans Math + SCP Greek | Complete |
| `mathjax-lato` | Lato | TBD | Planned |
| `mathjax-ptsans` | PT Sans | TBD | Planned |

## Usage

Each package produces a single webpack bundle (`tex-mml-svg-{package}.js`)
that replaces MathJax's default font. Include it in your HTML:

```html
<script id="MathJax-script" async src="tex-mml-svg-mathjax-source-sans.js"></script>
```

Or import in a bundled app:

```javascript
import './path/to/tex-mml-svg-mathjax-source-sans.js';
```

## Building

### Prerequisites

- Python 3.11+ with [fontTools](https://github.com/fonttools/fonttools) and [brotli](https://github.com/google/brotli)
- Node.js with webpack (`npm install` in the repo root)
- Source font files (see `fonts/README.md` for download instructions)

### Build a package

```bash
# Activate the Python environment
source venv/bin/activate  # or use uv

# Build the font data (CJS files + WOFF2)
python mathjax-source-sans/build.py

# Bundle with webpack
cd mathjax-source-sans/build
npx webpack --config webpack.config.cjs
```

The output bundle lands at `mathjax-source-sans/tex-mml-svg-mathjax-source-sans.js`.

## Architecture

Each package follows this structure:

```
mathjax-{name}/
  build.py                          # Per-font build script
  build/
    tex-mml-svg-mathjax-{name}.js   # Webpack entry point
    webpack.config.cjs              # Webpack config
  cjs/
    common.js                       # Font mixin (x_height, etc.)
    svg.js / chtml.js               # Font class
    svg/
      normal.js                     # Upright variant (+ math alphanumeric)
      bold.js, italic.js, ...       # Other variants
      delimiters.js                 # Stretchy delimiters
      smallop.js, largeop.js, ...   # Size variants
  tex-mml-svg-mathjax-{name}.js     # Final webpack bundle
  test.html                         # Specimen page
```

### Shared library

`lib/mathjax_font_lib.py` (~2500 lines) handles:

- Glyph extraction from OTF/TTF fonts (SVG paths + metrics)
- Variable font instantiation (`fontTools.varLib.instancer`)
- MATH table parsing (delimiters, size variants, stretchy assemblies, italic corrections)
- Accent skew computation from text font bounding boxes
- Greek/Latin override from text font (`greek_from_text`)
- Middle layer support (e.g., Source Code Pro Greek for Shantell Sans)
- WOFF2 font subsetting for CHTML output
- Webpack boilerplate generation

### Key features

- **Full typography matrix**: Upright, italic, bold, bold-italic for both Latin and Greek
- **`\mathrm{\alpha}` support**: Patched MathJax's `lcGreek` handler to respect font overrides (upright lowercase Greek)
- **Variable font support**: Pin `wght`, `wdth`, and custom axes (e.g., Shantell's `BNCE`, `INFM`, `SPAC`)
- **Per-glyph font fallback**: When a text font has some but not all Greek, falls back per-glyph rather than per-range
- **2-part stretchy assembly fix**: Correct handling of arrows and vertical bars with only 2 assembly parts

## Documentation

- `TUTORIAL.md` -- 19 gotchas for building MathJax font packages
- `STATUS.md` -- Project state, open items, font file locations
- `specimen-default-mathjax.html` -- Default MathJax/newCM reference specimen

## License

The build tooling in this repository is available under the MIT License.
Individual font files are subject to their own licenses (typically SIL OFL).
See each font's documentation for details.
