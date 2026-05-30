# MathJax Custom Font Packages — Project Status

## Current State (2026-05-30)

All 10 font packages are built, tested, and have self-contained `build.py` scripts
that produce correct output without manual post-build fixes.

### Completed Packages

| # | Package | Text Font | Math Font | Weights | Notes |
|---|---------|-----------|-----------|---------|-------|
| 1 | mathjax-libertinus | Libertinus Serif | Libertinus Math | R+B+I+BI | Reference implementation |
| 2 | mathjax-libertinus-sans | Libertinus Sans | Libertinus Math | R+B+I+BI | Synthetic bold-italic (skew+hand-edit) |
| 3 | mathjax-lm-sans | CMU Sans Serif | NewCM Sans Math | R+B+I+BI | Latin-only override (Greek from NewCM) |
| 4 | mathjax-noto-sans | Noto Sans (variable) | Noto Sans Math | R+B+I+BI | Lete Sans Math calligraphic donor |
| 5 | mathjax-source-sans | Source Sans 3 (variable) | Latin Modern Math | R+B+I+BI | |
| 6 | mathjax-source-code | Source Code Pro (variable) | Latin Modern Math | R+B+I+BI | Custom TEXT_RANGES (no mono brackets) |
| 7 | mathjax-concrete-euler | CMU Concrete | Euler Math | R+B+I+BI | Synthetic slanted italic, reduced LSB |
| 8 | mathjax-shantell | Shantell Sans (variable) | Latin Modern Math | R+B+I+BI | 3-layer: SCP Greek middle layer |
| 9 | mathjax-ptsans | PT Sans | Latin Modern Math | R+B+I+BI | 3-layer: newtxsf Greek (Type 1) |
| 10 | mathjax-lato | Lato | Lete Sans Math | R+B+I+BI | Patched serifed I |

### Git Structure
- **main branch**: All 10 packages, clean working state
- **experimental-horizontal-stretch branch**: Previous experimental work — preserved, DO NOT merge

## Shared Library: `lib/mathjax_font_lib.py`

Key features:
- Glyph extraction with depth bug fixed (`-yMin/upm` always, never clamped)
- Italic correction (ic) from MATH table + computed overhang fallback
- Accent skew (sk) — angle-based formula: `sk = accent_y * tan(italic_angle) / 2 / upm * 1.3`
- `ensure_width_covers_overhang()` — extends italic advance width to cover xMax
- `reduce_italic_lsb()` — shifts italic paths left via TransformPen
- `adjust_integral_widths()` — reduces integral declared width for subscript tucking
- `override_integral_ics()` — sets IC on integral codepoints
- Invisible operator fix (U+2061-2064 forced zero-width)
- Self-stretching delimiters for U+2015 etc. (\overline fix)
- Bold Greek removal from bold/bold-italic variants (\boldsymbol fix)
- Math-alpha Latin dupe removal from bold/italic/bold-italic variants
- Calligraphic/script separation support
- Modifier accent ranges (U+02C6-02DC) in DEFAULT_TEXT_RANGES
- `build_all_variants()` high-level helper with `italic_lsb` parameter
- Parameterized template writers (common.js, svg.js, chtml.js, webpack configs)

## Per-Font Build Pattern

Each `build.py` is self-contained:
1. Imports from `lib/mathjax_font_lib`
2. Defines font paths, name, ID, CSS prefix
3. Calls `build_all_variants()` with font-specific config
4. Applies all post-build fixes inline (ic, sk, svg.js wiring, calligraphic, etc.)
5. Calls `write_boilerplate()` for webpack configs

No manual post-build steps required — everything survives a clean rebuild.

## Regression Testing Tools

In `tools/`:
- **render-tex.js** — Server-side MathJax rendering via liteAdaptor + module redirect
- **render-all.sh** — Batch renders 41 test expressions × 10 fonts to SVG
- **diff-renders.sh** — Compares SVG renders against a saved baseline
- **test-expressions.txt** — 41 standard test expressions (algebra, analysis, Greek, accents, etc.)

Workflow: `render-all.sh` → `cp -r test-renders test-renders-baseline` → make changes → `render-all.sh` → `diff-renders.sh`

## Key Patterns & Fixes (consolidated in build.py files)

### Italic Correction (ic) via smp redirects
Remove basic Latin A-Z/a-z AND basic Greek from italic.js so MathJax follows smp
redirects to normal.js (which has ic values). Applied to all fonts.

### Accent Skew (sk) — angle-based
Computed from italic font angle, not MATH table. Formula with 1.3× factor propagated
to math-alpha italic/bold-italic Greek ranges.

### Latin-only Override (LM Sans pattern)
For fonts that need text-font Latin but math-font Greek: post-build replacement of
only Latin math-alpha entries, with math-alpha Latin dupe removal from bold/italic/
bold-italic variants.

### Calligraphic/Script Separation
Two patterns:
- **Pattern A (NewCM)**: Default glyphs → tex-calligraphic.js, ss01 alternates → script.js
- **Pattern B (Lete/Euler donor)**: Donor font calligraphic → tex-calligraphic.js, math font script in normal.js

Both require svg.js wiring for `tex-calligraphic` and `script` variants, plus script
codepoint dupe removal from bold/italic/bold-italic.

### Custom TEXT_RANGES (Source Code Pro)
Excludes brackets/operators from monospace text font (too wide). Must include modifier
accents (U+02C6-02DC) or \hat breaks.

### 3-Layer Fonts (Shantell, PT Sans)
Text font (Latin) → middle layer (Greek from SCP or newtxsf) → math font (operators/delimiters).

## Known Issues / Open Items

### Active Issues
1. **NewCM Sans bold italic** — GPL3 prevents synthesis. GitHub issue #1.
2. **Noto Sans alpha glyph** — Too similar to Latin 'a', needs editing. Issue #2.
3. **Concrete/Euler italic LSB** — `reduce_italic_lsb` helps but spacing still loose. Issue #5.
4. **Libertinus calligraphic donor** — Using Euler calligraphic currently. Issue #4.
5. **Integral subscript positioning** — `adjust_integral_widths()` applied to Shantell; needs adding to other fonts.
6. **Angle bracket scaling** — NewCM Sans Math has only 8 size variants (~3em max), no stretchy assembly for U+27E8/27E9.
7. **Horizontal stretchy arrows** — Fixed-size only; experimental branch attempts broke overbraces.

### Design Decisions (accepted)
- **Lowercase Greek upright (`\mathrm{\alpha}`)**: MathJax hardcodes lowercase Greek to italic. Matches standard TeX. lcGreek patch available but not applied by default.
- **MathJax SRE issue**: `tex2svgPromise` hangs in Tauri due to SRE blob Worker. Use `-nosre` webpack bundle + lcGreek patch for integration.

## Build Commands

```bash
cd /work/mathjax-fonts

# Build a package (generates CJS font data files)
python mathjax-{name}/build.py

# Build webpack bundle (for browser testing)
cd mathjax-{name}/build
npx webpack --config webpack.config.cjs        # full
npx webpack --config webpack-nosre.config.cjs   # no accessibility (for Tauri)

# Run regression tests
cd /work/mathjax-fonts/tools
./render-all.sh                    # render all fonts
./render-all.sh mathjax-shantell   # render one font
./diff-renders.sh                  # compare against baseline
```

## Specimen Test Pages

Each package has a `test.html` generated from `lib/specimen-template.html`.
Includes: math specimens (linear algebra, analysis, topology, combinatorics,
probability, abstract algebra, physics), display specimens, and complete glyph
inventory (accents, alphabets in all 4 styles, Greek, script/decorative, operators,
delimiters at multiple sizes).

**Remember:** test.html needs a webpack bundle. Build it first.

## Font Files Location

Source fonts in `/work/mathjax-fonts/fonts/` (not in git). See `fonts/README.md`
for download instructions.
