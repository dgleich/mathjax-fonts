# MathJax Custom Font Packages

**[Browse all font specimens](https://dgleich.github.io/mathjax-fonts/)**

`<human>`

I've long wanted more fonts in MathJax. Computer/Latin Modern are beautiful when
printed on a high dpi laser printer, but really leave something to be desired on
screen -- even a retina screen.

MathJax 4 added the ability to work with custom fonts. But they have no tooling to do this.
There are only a few fonts. I know why after this project. It's a pain.

I worked with Claude for a few weeks in my spare time to prep this bundle.

I find font selection a deeply personal thing and picked a few that
carry a range of expression.

There's Libertinus and Libertinus Sans for a classic look.

Concrete and Euler because of Knuth and it hasn't been done. I love the Denealian look of
Concrete Italics.

I have a dear colleague who gave talks in
Comic Sans, which is surprisingly lovely for math, and hence, I've used
the free (and superior!) alternative Shantell Sans for that purpose.

I _love_ PT Sans. The soft curves just look stately on a screen, and the italic adds a
nice pop.

Lato is another favorite of mine and Noto looks amazing. Just two classic sans serif pairings.

Surprisingly, no one has done the standard Latin Modern that we are all used to with Beamer.
So now we can do that too!

We have a range here. They aren't perfect. Typographers are probably
aghast -- this needs more refinement -- kerning problems, slight mismatches abound.
But if they saw the horror that is regularly done with mixtures
of math and other fonts, I hope they will forgive me. I think these combos often look nice.

The rest of this was written by Claude to document ... probably to other LLMs at this point ...
what is in this repo and how to use it.

`</human>`

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

## Using these fonts on your site

Each font package is a **single JavaScript file** (~5 MB) that includes MathJax 4,
the TeX input processor, the SVG renderer, and all the font data. No MathJax CDN needed.

### 1. Download the bundle

Grab the `.js` file for your chosen font from this repo:

```
mathjax-source-sans/tex-mml-svg-mathjax-source-sans.js
```

### 2. Replace the MathJax script tag

```html
<!-- Instead of the CDN: -->
<!-- <script src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-mml-svg.js"></script> -->

<!-- Use your bundle: -->
<script id="MathJax-script" async src="tex-mml-svg-mathjax-source-sans.js"></script>
```

That's it. All LaTeX math on the page renders in the chosen font.

### 3. Or load directly from GitHub Pages (for testing)

```html
<script id="MathJax-script" async
  src="https://dgleich.github.io/mathjax-fonts/mathjax-source-sans/tex-mml-svg-mathjax-source-sans.js"></script>
```

### Available bundles

| Font | Bundle |
|------|--------|
| Libertinus Serif | `tex-mml-svg-mathjax-libertinus.js` |
| Libertinus Sans | `tex-mml-svg-mathjax-libertinus-sans.js` |
| CMU Sans Serif | `tex-mml-svg-mathjax-lm-sans.js` |
| Noto Sans | `tex-mml-svg-mathjax-noto-sans.js` |
| Source Sans 3 | `tex-mml-svg-mathjax-source-sans.js` |
| Source Code Pro | `tex-mml-svg-mathjax-source-code.js` |
| CMU Concrete + Euler | `tex-mml-svg-mathjax-concrete-euler.js` |
| Shantell Sans | `tex-mml-svg-mathjax-shantell.js` |

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
