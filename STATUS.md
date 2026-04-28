# MathJax Custom Font Packages — Project Status

## Current State (as of latest commit)

### Completed Packages
1. **mathjax-libertinus** — Libertinus Serif + Libertinus Math (R+B+I+BI)
2. **mathjax-libertinus-sans** — Libertinus Sans + Libertinus Math (R+B+I, BI=I fallback)
3. **mathjax-lm-sans** — CMU Sans Serif + NewCM Sans Math (R+B+I+BI)
4. **mathjax-noto-sans** — Noto Sans (variable, pinned wght+wdth) + Noto Sans Math (R+B+I+BI)

### Remaining Packages (planned)
5. **mathjax-source-sans** — Source Sans 3 (variable) + Latin Modern Math
6. **mathjax-source-code** — Source Code Pro (variable) + Latin Modern Math
7. **mathjax-concrete-euler** — CMU Concrete (+ generated slanted) + Euler Math
8. **mathjax-shantell** — Shantell Sans (variable) + Source Code Pro Greek + LM Math
9. **mathjax-lato** — Lato (serifed I) + Lete Sans Math (rebuild through new library)
10. **mathjax-ptsans** — PT Sans (serifed I) + newtxsf Greek + LM Math (rebuild)

### Git Structure
- **main branch**: Clean working state with completed packages
- **experimental-horizontal-stretch branch**: Previous experimental work on horizontal stretchy (PUA, stretchv, variant reordering) — preserved for reference, DO NOT merge

## Shared Library: `lib/mathjax_font_lib.py`

Extracted from battle-tested `build_mathjax_ptsans.py`. Key features:
- Glyph extraction with depth bug fixed (`-yMin/upm` always, never clamped)
- Italic correction (ic:) extraction and application from MATH table
- Top accent skew (sk:) computation from text font visual centers
- Invisible operator fix (U+2061-2064 forced zero-width)
- Self-stretching delimiters for U+2015 etc. (\overline fix)
- PUA codepoint assignment for unmapped horizontal assembly parts
- Bold Greek removal from bold/bold-italic variants (\boldsymbol fix)
- Modifier accent ranges (U+02C6-02DC) in DEFAULT_TEXT_RANGES
- Math alphanumeric (U+1D400-1D7FF) and letterlike (U+2100-214F) ranges
- Parameterized template writers (common.js, svg.js, chtml.js, webpack configs)
- `build_all_variants()` high-level helper

## Per-Font Build Pattern

Each package has a `build.py` that:
1. Imports from `lib/mathjax_font_lib`
2. Defines font paths, name, ID, CSS prefix
3. Calls `build_all_variants()` with font-specific config
4. Applies post-build tweaks (overbrace spacing, etc.)
5. Calls `write_boilerplate()` for webpack configs

## Known Issues / Gotchas (17 total in TUTORIAL.md)

Critical ones to remember:
- **\overline uses U+2015**, not U+0305 — needs self-stretching delimiter entry
- **Bold Greek**: remove regular Greek from bold/bold-italic variants
- **Accent depth**: must be `-yMin/upm` always (never clamp to 0)
- **Accent skew (sk:)**: compute from text font visual centers, not MATH table
- **Invisible operators**: U+2061-2064 must be zero-width
- **Modifier accents**: U+02C6-02DC must be in text font ranges
- **Bold-italic Latin**: also remove A-Z/a-z from bold-italic variant (same issue as Greek)
- **Overbrace/underbrace**: HDW values may need +0.35em adjustment
- **Integral IC**: Set to 0 for Libertinus (LM Math raw values too large). Largeop IC override in library.

## Open Items / Future Improvements

- **Libertinus Sans Bold Italic**: Currently uses Italic as fallback. LaTeX package
  uses `embolden=3` (synthetic stroke thickening). Could implement via fontTools
  outline offset for slightly bolder SVG paths, but effect is very subtle (0.3%).
- **Angle bracket scaling (langle/rangle)**: NewCM Sans Math only has 8 size
  variants (~3em max) and no stretchy assembly for U+27E8/27E9. They don't grow
  large enough for tall fractions. Fix: synthesize a stretchy assembly by splitting
  the largest glyph into top/bottom caps + angled line extender. Libertinus Math
  has 13 sizes (enough in practice) but also lacks assembly. Check each math font.
- **Integral limit positioning**: Revisit — IC=0 works but needs more investigation.
  The current approach may not be optimal for all math fonts.
- **Horizontal stretchy arrows**: Arrows render as fixed-size glyphs (no stretchy
  arrowheads). The experimental-horizontal-stretch branch has PUA-based attempts
  but they broke overbraces. Needs a different approach — possibly copying newCM's
  horizontal delimiter entries directly for arrow codepoints.

## Font Files Location

Source fonts in `/work/mathjax-fonts/fonts/` (not in git):
- `fonts/libertinus/` — LibertinusSerif-*.otf, LibertinusSans-*.otf, LibertinusMath-Regular.otf
- `fonts/cmu-sans/` — cmunss.otf, cmunsx.otf, cmunsi.otf, cmunso.otf, NewCMSansMath-Regular.otf
- `fonts/noto-sans/` — NotoSans[wdth,wght].ttf, NotoSans-Italic[wdth,wght].ttf, NotoSansMath-Regular.ttf
- `fonts/source-sans/` — SourceSans3[wght].ttf, SourceSans3-Italic[wght].ttf
- `fonts/lm-math/` — latinmodern-math.otf
- See `fonts/README.md` for download instructions for all fonts

Other fonts already downloaded in workspace:
- `/work/font-demos/noto-sans/`, `/work/font-demos/source-sans/`, etc.
- `/work/font-demos/concrete/`, `/work/font-demos/euler-math/`
- `/work/cmu-sans/` — CMU Sans Serif fonts
- `/tmp/ncm/newcomputermodern/otf/NewCMSansMath-Regular.otf`
- `/work/font-demos/shantell-sans/`, `/work/font-demos/source-code-pro/`
- `/tmp/newtxsf/newtxsf/type1/` — newtxsf Type 1 fonts (for PT Sans)
- `/work/lato-patched/`, `/work/ptsans-mathjax/` — patched text fonts
- `/work/lete-sans-math/`, `/work/lm-math/` — math fonts

## Special Handling Notes

### Variable Fonts (Noto Sans, Source Sans, Source Code Pro, Shantell Sans)
Need `fontTools.instancer.instantiateVariableFont()` to pin wght axis at 400/700.
Pin wdth=100 if present (Noto Sans). Library needs `instantiate_variable_font()` function — not yet implemented.

### CMU Concrete Slanted
Already generated at `/work/font-demos/concrete/CMUConcrete-Slanted.otf` via CFF FontMatrix shear at slant=1/6 (9.46°). Use as italic variant.

### Shantell Sans Greek (3-layer)
Source Code Pro provides Greek (25/25). Use `build_middle_layer_from_otf()` from library. x-heights match well (485 vs 478).

### PT Sans (3-layer with Type 1)
newtxsf Type 1 fonts provide sans-serif Greek. Library has `load_ntxsf_font()`, `build_ntxsf_layer()`, and the glyph maps.

### Libertinus Sans Bold Italic
No BI font exists. LaTeX uses Italic+embolden=3 (very subtle). Current build uses Italic as BI fallback.

## Build Commands

```bash
cd /work/mathjax-fonts

# Build a package
python mathjax-{name}/build.py

# Build webpack bundle (optional, for testing)
cd mathjax-{name}/build
npx webpack --config webpack.config.cjs        # full
npx webpack --config webpack-nosre.config.cjs   # no accessibility
```

## Specimen Test Pages

Each package should have a `test.html` generated from `lib/specimen-template.html`.
To generate, build the webpack bundle first, then:

```python
with open('lib/specimen-template.html') as f:
    template = f.read()
result = template.replace('FONT_TITLE', 'Font Name + Math Font')
result = result.replace('FONT_BUNDLE', 'tex-mml-svg-mathjax-name.js')
result = result.replace('FONT_CSS', '@font-face { ... }')
result = result.replace('FONT_FAMILY', '"Font Name", serif')
with open('mathjax-name/test.html', 'w') as f:
    f.write(result)
```

The template includes: full math specimens (linear algebra, analysis, topology,
combinatorics, probability, abstract algebra, physics), display specimens, and
complete glyph inventory (accents, alphabets in all 4 styles, Greek, script/
decorative, operators, delimiters at multiple sizes).

**Remember:** test.html needs a webpack bundle to work. Build it first:
```bash
cd mathjax-name/build && npx webpack --config webpack.config.cjs
```

## Workspace Files (outside git repo)

Key files in `/work/` (the original workspace):
- `build_mathjax_ptsans.py` — Original PT Sans builder (1910 lines)
- `build_mathjax_lato.py` — Original Lato builder
- `TUTORIAL-custom-mathjax-font.md` — Full tutorial (also copied into repo)
- `mathjax-ptsans-font/` — Working PT Sans MathJax package
- `mathjax-lato-font/` — Working Lato MathJax package
- `mathjax-ptsans-bundle/` — Distribution bundle for PT Sans
- `font-demo.html` — Font comparison demo page
- `specimen-lato.html`, `specimen-ptsans.html` — Specimen pages
- `patch_lato_serif_i.py`, `patch_ptsans_replace_i.py` — Serifed I patchers
