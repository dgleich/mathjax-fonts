# MathJax Custom Font Packages

Custom MathJax 4 SVG font packages for various text fonts paired with
OpenType math fonts. Each package provides CJS font data + webpack configs
that can be re-bundled into applications.

## Packages

| Package | Text Font | Math Font | Status |
|---------|-----------|-----------|--------|
| mathjax-lato | Lato (serifed I) | Lete Sans Math | Done |
| mathjax-ptsans | PT Sans (serifed I) + newtxsf Greek | Latin Modern Math | Done |
| mathjax-libertinus | Libertinus Serif | Libertinus Math | Planned |
| mathjax-libertinus-sans | Libertinus Sans | Libertinus Math | Planned |
| mathjax-lm-sans | CMU Sans Serif | NewCM Sans Math | Planned |
| mathjax-noto-sans | Noto Sans | Noto Sans Math | Planned |
| mathjax-source-sans | Source Sans 3 | Latin Modern Math | Planned |
| mathjax-source-code | Source Code Pro | Latin Modern Math | Planned |
| mathjax-concrete-euler | CMU Concrete | Euler Math | Planned |
| mathjax-shantell | Shantell Sans + Source Code Pro Greek | Latin Modern Math | Planned |

## Structure

```
mathjax-fonts/
  lib/mathjax_font_lib.py      # Shared build library
  fonts/                        # Source font files (not checked in, see fonts/README.md)
  mathjax-{name}/
    build.py                    # Per-font build script
    cjs/                        # Generated MathJax font data
    build/                      # Webpack entry points and configs
    sre/                        # Speech worker stub
    package.json
```

## Building a package

```bash
cd mathjax-{name}
python build.py

# Optional: build webpack bundles
cd build
npx webpack --config webpack.config.cjs        # Full bundle
npx webpack --config webpack-nosre.config.cjs   # No accessibility (for Tauri etc.)
```

## Key lessons learned

See `TUTORIAL-custom-mathjax-font.md` in the parent directory for the full
guide, including critical gotchas:

1. Accent depth must be negative (not clamped to 0)
2. Invisible operators U+2061-2064 must be zero-width
3. Modifier accent codepoints U+02C6-02DC must be in text font ranges
4. Set x_height to the text font's actual x-height — no other scaling needed
5. Integral italic corrections from Latin Modern Math are too large for MathJax

## License

All font packages use fonts licensed under the SIL Open Font License (OFL 1.1).
The build tooling is available for reuse.
