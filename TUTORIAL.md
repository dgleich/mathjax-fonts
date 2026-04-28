# Building a Custom MathJax 4 Font from a Text Font + Math Font

This tutorial walks through creating a MathJax 4 SVG font package that uses your
chosen text font (e.g., PT Sans, Lato, Source Sans) for Latin characters and a
compatible OpenType math font (e.g., Lete Sans Math, Fira Math) for Greek letters,
math symbols, operators, and stretchy delimiters.

## What You Need

### 1. A text font (TTF or OTF)
Your text font provides Latin letters (A-Z, a-z), digits (0-9), and basic
punctuation. You need at minimum:

- **Regular** (upright)
- **Bold**
- **Italic**
- **Bold Italic**

These are standard `.ttf` or `.otf` files. For example:
- `PTSans-Regular.ttf`, `PTSans-Bold.ttf`, `PTSans-Italic.ttf`, `PTSans-BoldItalic.ttf`

### 2. An OpenType math font (OTF with MATH table)
This provides everything your text font doesn't have:
- Greek letters (α, β, γ, ..., Γ, Δ, Σ, ...)
- Math operators (+, −, ×, ÷, ∑, ∫, ∏, ...)
- Arrows (→, ←, ⇒, ...)
- Relations (≤, ≥, ≈, ∈, ⊂, ...)
- Stretchy delimiters with size variants (parentheses, brackets, braces that grow)
- Size variants for large operators

**The MATH table is critical** — it contains the assembly instructions for stretchy
characters (how to build a tall parenthesis from top/middle/bottom/extension pieces).

Good math font choices for sans-serif text:
- **Lete Sans Math** — designed for sans-serif text, available on CTAN
- **Fira Math** — matches Fira Sans
- **GFS Neohellenic Math** — another sans-serif option

For serif text fonts, consider:
- **STIX Two Math**, **Latin Modern Math**, **TeX Gyre math fonts**

### 3. Tools
```bash
# Python with fonttools for font analysis and path extraction
pip install fonttools  # or: uv pip install fonttools

# Node.js with MathJax and webpack for bundling
npm install @mathjax/src mathjax webpack webpack-cli terser-webpack-plugin
```

## Overview of the Pipeline

```
Text Font (TTF/OTF)  ──┐
                        ├──▶  build_mathjax_font.py  ──▶  mathjax-FONT-font/
Math Font (OTF+MATH) ──┘         (Python)                    cjs/svg/normal.js
                                                              cjs/svg/bold.js
                                                              cjs/svg/italic.js
                                                              cjs/svg/delimiters.js
                                                              cjs/svg/size3..15.js
                                                              cjs/common.js
                                                              cjs/svg.js
                                                              ...

mathjax-FONT-font/  ──▶  webpack  ──▶  tex-mml-svg-mathjax-FONT.js
  + build entry           (Node)         (single 2-3MB browser bundle)
  + webpack config
```

## Step-by-Step

### Step 1: Measure Your Text Font

Before building, you need your text font's key metrics to configure scaling.

```python
from fontTools.ttLib import TTFont

font = TTFont('PTSans-Regular.ttf')
upm = font['head'].unitsPerEm
cap_height = font['OS/2'].sCapHeight
x_height = font['OS/2'].sxHeight

print(f"UPM: {upm}")
print(f"Cap height: {cap_height} ({cap_height/upm:.4f} em)")
print(f"x-height:   {x_height} ({x_height/upm:.4f} em)")
```

The **x-height in em units** is the critical number — you'll set this as MathJax's
`x_height` parameter so the SVG output scales correctly relative to the surrounding
CSS text.

For example:
- Lato: x-height = 0.506 em (UPM 2000, x-height 1013)
- PT Sans: x-height ≈ 0.500 em (check yours)
- Fira Sans: x-height = 0.527 em

### Step 2: Character Assignment

Decide which codepoints come from which font:

**From your text font:**
```python
TEXT_RANGES = [
    (0x20, 0x7E),     # Basic ASCII (space through tilde)
    (0xA0, 0xFF),     # Latin-1 Supplement (accented chars, symbols)
]
```

**From the math font (everything else):**
```python
MATH_RANGES = [
    (0x391, 0x3C9),   # Greek
    (0x2190, 0x21FF),  # Arrows
    (0x2200, 0x22FF),  # Mathematical operators
    (0x2300, 0x23FF),  # Miscellaneous technical
    (0x2500, 0x257F),  # Box drawing
    (0x25A0, 0x25FF),  # Geometric shapes
    (0x2600, 0x26FF),  # Miscellaneous symbols
    (0x27C0, 0x27EF),  # Miscellaneous math symbols-A
    (0x27F0, 0x27FF),  # Supplemental arrows-A
    (0x2900, 0x297F),  # Supplemental arrows-B
    (0x2980, 0x29FF),  # Miscellaneous math symbols-B
    (0x2A00, 0x2AFF),  # Supplemental math operators
    # ... add more as needed
]
```

### Step 3: Extract Glyph Data

For each character in each variant, extract:

1. **Height** (em): how far above the baseline the glyph extends
2. **Depth** (em): how far below the baseline (positive number)
3. **Width** (em): advance width
4. **SVG path**: the outline, in a 1000-unit coordinate system with y-up

```python
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

def extract_glyph(font, codepoint):
    cmap = font.getBestCmap()
    glyph_name = cmap[codepoint]
    upm = font['head'].unitsPerEm
    glyph_set = font.getGlyphSet()

    # Metrics
    advance_width = font['hmtx'].metrics[glyph_name][0]
    bp = BoundsPen(glyph_set)
    glyph_set[glyph_name].draw(bp)
    xMin, yMin, xMax, yMax = bp.bounds

    height = round(yMax / upm, 3)
    depth = round(-yMin / upm, 3)   # NOT `if yMin < 0 else 0` — see note below
    width = round(advance_width / upm, 3)

    # SVG path scaled to 1000 UPM
    scale = 1000 / upm
    pen = SVGPathPen(glyph_set)
    glyph_set[glyph_name].draw(pen)
    path = pen.getCommands()
    if scale != 1.0:
        path = scale_path(path, scale)  # scale all coordinates
    path = round_path(path)              # round to integers

    # IMPORTANT: strip leading 'M' — MathJax prepends its own
    if path.startswith('M'):
        path = path[1:]

    return height, depth, width, path
```

**Why strip the leading M?** MathJax's SVG renderer prepends `M x y` when inserting
each glyph path into the SVG. If your path already starts with `M`, you get
`M M472 266...` which is invalid. The published MathJax fonts (Fira, TeX) all store
paths without the leading M.

### Step 4: Extract Delimiter Data from the MATH Table

The OpenType MATH table contains `MathVariants` with:
- **Vertical glyph constructions** (for parentheses, brackets, etc. that grow tall)
- **Horizontal glyph constructions** (for arrows, overbars that grow wide)

Each construction has:
- **Size variants**: a list of progressively larger pre-built glyphs
- **Glyph assembly**: instructions to build arbitrarily tall/wide versions from parts
  (top piece + extension piece + bottom piece, optionally with a middle piece)

```python
math_table = font['MATH'].table
mv = math_table.MathVariants

# Vertical variants
for i, glyph_name in enumerate(mv.VertGlyphCoverage.glyphs):
    rec = mv.VertGlyphConstruction[i]

    # Size variants (pre-built larger glyphs)
    sizes = [round(v.AdvanceMeasurement / upm, 3)
             for v in rec.MathGlyphVariantRecord]

    # Assembly parts (for stretchy construction)
    if rec.GlyphAssembly:
        parts = rec.GlyphAssembly.PartRecords
        # parts[0] = top, parts[1] = extension, parts[2] = bottom
        # (or 5 parts for braces: top, ext, mid, ext, bottom)
```

The delimiter output format for MathJax is:
```javascript
0x28: {                              // left parenthesis
    dir: V,                          // V=vertical, H=horizontal
    sizes: [0.925, 1.151, 1.648, ...], // total height of each size variant
    stretch: [0x239B, 0x239C, 0x239D], // [top, extension, bottom] codepoints
    HDW: [0.742, 0.182, 0.315]        // [height, depth, width] of assembly
}
```

### Step 5: Generate MathJax Data Files

Each variant (normal, bold, italic, bold-italic) needs an SVG data file:

```javascript
// cjs/svg/normal.js
exports.normal = {
    0x20: [0, 0, 0.256],                    // space: [height, depth, width]
    0x41: [0.717, 0, 0.677, { p: '472 266 ...' }],  // A: + path
    0x61: [0.515, 0.008, 0.497, { p: '690 456...' }], // a: has depth
    // ... ~1500 entries
};
```

You also need:
- `cjs/svg/delimiters.js` — stretchy delimiter data
- `cjs/svg/smallop.js`, `largeop.js` — operator variants
- `cjs/svg/size3.js` through `size15.js` — size variants
- `cjs/svg/lf-tp.js`, `rt-bt.js`, `ext.js`, `mid.js` — stretchy assembly parts
- `cjs/chtml/` — same structure but metrics only (no paths), for CHTML output

### Step 6: Generate Framework Files

**`cjs/common.js`** — Font mixin that sets parameters:
```javascript
// The critical parameter:
defaultParams: {
    x_height: .506,        // YOUR text font's x-height in em
    rule_thickness: 0.075,
    surd_height: 0.075
}
```

The `x_height` parameter controls how MathJax converts between em units (used in
the font data) and `ex` units (used for SVG sizing in the browser). Set this to
your text font's actual x-height so the math scales correctly.

**`cjs/svg.js`** — SVG font class that registers all character data.

**`cjs/svg/default.js`** — Entry point that MathJax loads:
```javascript
exports.Font = {
    fontName: 'mathjax-yourfont',
    DefaultFont: YourFontClass
};
```

### Step 7: Bundle with Webpack

Create a webpack entry point that loads MathJax core + your font:

```javascript
// build/tex-mml-svg-mathjax-yourfont.js
var init = require("@mathjax/src/components/cjs/startup/init.js");
var loader = require("@mathjax/src/cjs/components/loader.js");
require("@mathjax/src/components/cjs/core/core.js");
require("@mathjax/src/components/cjs/input/tex/tex.js");
require("@mathjax/src/components/cjs/input/mml/mml.js");
var svg = require("@mathjax/src/components/cjs/output/svg/svg.js");
require("@mathjax/src/components/cjs/ui/menu/menu.js");
// a11y components...
loader.Loader.preLoaded('loader', 'startup', 'core', 'input/tex',
    'input/mml', 'output/svg', 'ui/menu', ...);
svg.loadFont(init.startup, true);
```

The webpack config redirects `#default-font` to your font's CJS directory:

```javascript
plugins: [
    new webpack.NormalModuleReplacementPlugin(/#default-font/, function(r) {
        r.request = r.request.replace(/#default-font/, '/path/to/your/cjs');
    })
]
```

This produces a single `tex-mml-svg-mathjax-yourfont.js` file (~2-3MB) containing
all of MathJax plus your font data.

### Step 8: Create a No-Op Speech Worker

MathJax's a11y system tries to load a speech worker. Create a stub:

```javascript
// sre/speech-worker.js
self.onmessage = function(e) { self.postMessage({id: e.data.id, result: ''}); };
self.postMessage({id: 'ready'});
```

### Step 9: Use It

```html
<script>
MathJax = {
    options: {
        enableEnrichment: false,
        enableComplexity: false,
        enableExplorer: false,
        enableSpeech: false,
        enableBraille: false,
    },
    tex: { inlineMath: [['$', '$']] },
    svg: { fontCache: 'global' },
};
</script>
<script src="mathjax-yourfont-font/tex-mml-svg-mathjax-yourfont.js"></script>
```

## Key Gotchas

### 1. Strip the leading M from SVG paths
MathJax prepends its own `M x y` to every glyph path. If your extracted path
starts with `M`, strip it — otherwise you get `M M...` which renders nothing.

### 2. Set x_height to match your text font
This is the single most important parameter. MathJax uses it to convert em-based
metrics to `ex`-based SVG dimensions. If it doesn't match the browser's rendering
of your text font, math will appear too large or too small.

Calculate it from the font: `x_height = OS/2.sxHeight / head.unitsPerEm`

### 3. The Python build script wipes the output directory
If your build script clears the output directory, you'll lose `default.js`,
`build/`, and `sre/` each time. Either preserve them in the script or recreate
them after each build.

### 4. Don't scale the glyph metrics
You might be tempted to scale metrics to match text size. Don't — just set the
correct `x_height` parameter and MathJax handles the rest through its ex-unit
conversion.

### 5. Scale everything uniformly if you do scale
If for some reason you need to apply an em_scale to glyph metrics and paths,
apply the same factor to ALL glyphs (text font and math font) and to delimiter
sizes and HDW values. Don't scale one source differently from the other.

### 6. Depth must be negative for accents (don't clamp to zero!)
Accents and combining marks (tilde, hat, overline, etc.) sit entirely above the
baseline, so their `yMin` is positive. The depth calculation **must** be
`depth = -yMin / upm` for all glyphs — do NOT use `if yMin < 0 else 0`.

When yMin is positive (glyph above baseline), depth becomes negative. This
negative depth tells MathJax where the bottom of the accent sits. For example,
a combining tilde with `yMin = 556` at UPM 1000 gets `depth = -0.556`, meaning
its bottom edge is 0.556em above the baseline.

If you clamp depth to zero, all accents (`\tilde`, `\hat`, `\widehat`,
`\overline`, `\bar`) render at the baseline instead of floating over letters.
This affects every function that computes glyph metrics: the main variant
builder, the size variant builder, the stretchy parts builder, and the CHTML
metrics-only builder. Fix them all.

### 7. Invisible operators (U+2061–2064) must be zero-width
Some math fonts (notably Latin Modern Math) include visible "debug" glyphs for
invisible operators like FUNCTION APPLICATION (U+2061). These render as dashed
boxes with `f()` inside them. MathJax inserts U+2061 between function names and
parentheses, so if your font has a visible glyph, you'll see dashed boxes before
every `(`. Force these to `[0, 0, 0]` (zero height, depth, width, no path).

### 8. Include modifier accent codepoints (U+02C6–02DC) in your text font ranges
MathJax uses the **spacing/modifier** versions of accents for `\hat`, `\tilde`,
`\dot`, `\bar` on single characters — not the combining versions. These are:

| Codepoint | Character | LaTeX command |
|-----------|-----------|---------------|
| U+02C6   | ˆ modifier circumflex | `\hat` |
| U+02C7   | ˇ caron | `\check` |
| U+02C9   | ˉ macron | `\bar` |
| U+02D8   | ˘ breve | `\breve` |
| U+02D9   | ˙ dot above | `\dot` |
| U+02DA   | ˚ ring above | |
| U+02DC   | ˜ small tilde | `\tilde` |

These live in the "Spacing Modifier Letters" block (U+02B0–02FF), which falls
between Basic ASCII (U+0020–007E) and Latin-1 Supplement (U+00A0–00FF). If your
text font ranges don't include them, and your math font doesn't have them either
(e.g., Lete Sans Math lacks all of these), then `\hat{x}`, `\tilde{x}`, and
`\dot{x}` will silently fail or render incorrectly.

The **combining** versions (U+0302, U+0303, U+0307, etc.) are used for wide
accents (`\widehat`, `\widetilde`) and come from the math font, so those may
work fine even when the modifier versions are missing — making the bug confusing
to diagnose.

**Fix:** Add these codepoints to your text font ranges:
```python
TEXT_RANGES = [
    (0x20, 0x7E),     # Basic ASCII
    (0xA0, 0xFF),     # Latin-1 Supplement
    (0x2C6, 0x2C6),   # modifier circumflex (\hat)
    (0x2C7, 0x2C7),   # caron (\check)
    (0x2C9, 0x2C9),   # macron (\bar)
    (0x2D8, 0x2DC),   # breve, dot above, ring, ogonek, small tilde
]
```

### 9. Extract and apply italic corrections (ic:) from the MATH table
The MATH table's `MathItalicsCorrectionInfo` contains per-glyph italic
corrections that control how subscripts tuck under slanted glyphs — most
importantly for integrals (`\int_0^1`). Without these, subscript limits
sit too far right.

```python
def extract_italic_corrections(font):
    math_table = font['MATH'].table
    mic = math_table.MathGlyphInfo.MathItalicsCorrectionInfo
    ic_map = {}
    for i, glyph_name in enumerate(mic.Coverage.glyphs):
        cp = rev_cmap.get(glyph_name)
        if cp is not None:
            ic_map[cp] = round(mic.ItalicsCorrection[i].Value / upm, 3)
    return ic_map
```

Apply the `ic:` field in your glyph entry format:
```javascript
0x222B: [1.361, .861, .669, { p: '...', ic: 0.33 }]
```

**Important:** Apply IC to **all** variant files — normal, bold, italic,
bold-italic, smallop, largeop, and size3–size15. Missing IC on size
variants means display-mode integrals won't tuck their limits.

### 10. Override integral italic corrections — tuning required
Math fonts often have IC values for integrals that don't work well in MathJax.
Latin Modern Math's raw values (0.332) are too large. Start with IC=0 and
tune from there.

```python
INTEGRAL_CPS = range(0x222B, 0x2234)  # ∫ through ∰
for cp in INTEGRAL_CPS:
    if cp in ic_map:
        ic_map[cp] = 0  # start here, tune per font
```

**Note:** IC affects inline subscript placement (e.g., `f_i`) but its effect
on display-mode operator limits (`\int_a^b`) is unclear — MathJax may use a
different code path for those. Negative IC values are clamped to 0. The
relationship between IC, glyph width, and limit placement needs more
investigation. For Libertinus, IC=0 matches newCM's appearance.

### 11. Compute accent skews (sk:) from the text font, not the math font
MathJax uses the `sk:` property to center accents (`\hat`, `\tilde`, `\bar`)
over letters. The MATH table's `TopAccentAttachment` provides this data, but
it's calibrated for the **math font's** glyph shapes. When your text font has
different glyph shapes (especially italic), accents will be off-center.

The formula is: `sk = (visual_center - advance_center) / upm`

where `visual_center = (xMin + xMax) / 2` from the glyph's bounding box.

**Best practice:** Compute sk from the actual text font glyphs for text-sourced
codepoints, and use the MATH table's TopAccentAttachment only for math-only
glyphs (Greek, operators, symbols). Apply text font skews **after** MATH table
skews so they override for glyphs that come from both sources.

```python
def compute_visual_skews(font):
    sk_map = {}
    for cp, gn in font.getBestCmap().items():
        bp = BoundsPen(gs)
        gs[gn].draw(bp)
        bounds = bp.bounds
        if bounds:
            vis_center = (bounds[0] + bounds[2]) / 2
            adv_center = gs[gn].width / 2
            sk = round((vis_center - adv_center) / upm, 3)
            if sk != 0:
                sk_map[cp] = sk
    return sk_map
```

This is especially important for italic variants, where the glyph's visual
center is shifted right by the italic slant. Without per-variant text skews,
`\hat{f}` and `\tilde{a}` will be visibly off-center in italic math.

### 12. `\overline` uses U+2015, not U+0305 — add self-stretching delimiters
MathJax renders `\overline{content}` using **U+2015 (HORIZONTAL BAR)**, not
U+0305 (combining overline) or U+00AF (macron). If U+2015 is missing from your
delimiter data, `\overline` will render as a fixed-width bar that never grows.

The fix: add self-referencing stretch entries for horizontal rules/bars. These
glyphs stretch by tiling themselves:

```python
SELF_STRETCH = [0x2015, 0x2500, 0x2013, 0x2014, 0x23AF, 0x2212, 0x3D]
for cp in SELF_STRETCH:
    if cp in cmap and cp not in delimiters:
        delimiters[cp] = {'dir': 'H', 'stretch': [0, cp], 'HDW': [...], 'hd': [...]}
```

**How to debug:** Inspect the SVG output — look for `data-c="XXXX"` on the bar's
`<path>` element to see which codepoint MathJax is actually using. Don't assume
it matches the LaTeX command name.

### 13. `stretchv` values are variant indices into `defaultStretchVariants`
The `stretchv` array in delimiter entries contains **indices** into the
`defaultStretchVariants` array, NOT abstract piece-type codes. The order must
match newCM's convention:

```
defaultStretchVariants: ['normal', '-ext', '-size3', '-lf-tp', '-rt-bt']
                          0        1       2         3         4
```

So `stretchv: [3, 1, 4]` means: left piece from `-lf-tp`, extension from `-ext`,
right piece from `-rt-bt`. Getting the order wrong (e.g., putting `-lf-tp` at
index 2 instead of 3) causes MathJax to look up pieces in the wrong variant files.

### 14. Assembly part glyphs need base-name codepoint fallback
Font-internal assembly glyphs like `uni0305.size1` or `arrowright.left` have no
Unicode codepoint. When mapping them to codepoints for the stretch/size data,
try stripping the suffix (`.size1`, `.left`, `.ex`, etc.) to find the base
glyph's codepoint. This applies to BOTH the delimiter builder AND the stretchy
part builder (lf-tp, rt-bt, ext files).

### 15. Remove regular Greek and Latin from bold/bold-italic variants
MathJax's `\boldsymbol` remaps characters to the math alphanumeric bold range
(e.g., α → U+1D6C2, x → U+1D482) and looks them up in the **normal** variant.
If your bold or bold-italic variant has those base codepoints with non-bold
glyphs, MathJax finds them first and renders non-bold.

Remove from **bold** variant:
- Greek: U+0391–03C9, U+03D1–03D6, U+03F0–03F6

Remove from **bold-italic** variant:
- Greek: same as above
- Latin: U+0041–005A (A-Z), U+0061–007A (a-z)

### 16. Adjust overbrace/underbrace label spacing via HDW
The HDW values in delimiter entries control how far the label
(`^{text}` for overbrace, `_{text}` for underbrace) sits from the brace.
Some math fonts produce HDW values that place labels too close.

- **Overbrace** (U+23DE): Increase HDW[0] (height) to push superscript up
- **Underbrace** (U+23DF): Increase HDW[1] (depth) to push subscript down

Compare with newCM's values and adjust by ~0.1–0.15em if labels are too tight.
This is a per-font tweak done in the build script after generating delimiter data.

### 17. Delimiter codepoints must exist in your font data
The stretchy delimiter `stretch` array references codepoints for assembly parts
(e.g., 0x239B for left paren top). These glyphs must appear in your `-lf-tp`,
`-rt-bt`, `-ext`, and `-mid` variant data files.

## File Inventory

A complete MathJax font package contains:

```
mathjax-yourfont-font/
├── package.json
├── tex-mml-svg-mathjax-yourfont.js    # webpack bundle (THE deliverable)
├── sre/
│   └── speech-worker.js               # no-op stub
├── build/                              # webpack build files
│   ├── tex-mml-svg-mathjax-yourfont.js # entry point
│   └── webpack.config.cjs
├── cjs/
│   ├── common.js                       # font mixin (x_height lives here)
│   ├── svg.js                          # SVG font class
│   ├── svg/
│   │   ├── default.js                  # font registration
│   │   ├── normal.js                   # normal variant (metrics + paths)
│   │   ├── bold.js
│   │   ├── italic.js
│   │   ├── bold-italic.js
│   │   ├── monospace.js
│   │   ├── delimiters.js               # stretchy delimiter data
│   │   ├── smallop.js                  # small operator variants
│   │   ├── largeop.js                  # large operator variants
│   │   ├── size3.js .. size15.js       # size variants
│   │   ├── lf-tp.js                    # stretchy left/top parts
│   │   ├── rt-bt.js                    # stretchy right/bottom parts
│   │   ├── ext.js                      # stretchy extension parts
│   │   ├── mid.js                      # stretchy middle parts
│   │   ├── up.js                       # upright variants (can be empty)
│   │   └── dup.js                      # display upright (can be empty)
│   └── chtml/
│       └── (same structure, metrics only, no paths)
└── chtml/
    └── woff2/                          # subsetted WOFF2 fonts for CHTML mode
```

## Adapting the Build Script

The build script at `/work/build_mathjax_lato.py` can be adapted for any font by
changing these variables at the top:

```python
# Paths to your fonts
TEXT_FONTS = {
    'regular': 'PTSans-Regular.ttf',
    'bold': 'PTSans-Bold.ttf',
    'italic': 'PTSans-Italic.ttf',
    'bold_italic': 'PTSans-BoldItalic.ttf',
}
MATH_FONT = 'LeteSansMath.otf'

# Output
OUTPUT_DIR = 'mathjax-ptsans-font'
FONT_NAME = 'MathJaxPTSans'
FONT_ID = 'mathjax-ptsans'
CSS_PREFIX = 'PTSANS'

# Character ranges (usually don't need to change)
TEXT_RANGES = [(0x20, 0x7E), (0xA0, 0xFF)]
MATH_RANGES = [(0x391, 0x3C9), (0x2190, 0x21FF), ...]

# Scaling (set to 1.0 — use x_height param instead)
EM_SCALE = 1.0
```

Then run:
```bash
python3 build_mathjax_font.py
# recreate default.js, build/, sre/ (see above)
cd mathjax-yourfont-font/build && npx webpack --config webpack.config.cjs
```

## Choosing a Math Font

The math font must have an OpenType MATH table. Without it, you won't get:
- Stretchy delimiters (parentheses that grow to fit content)
- Size variants for operators (∑, ∫ in display mode)
- Proper accent positioning
- Sub/superscript shift parameters

**For sans-serif text fonts**, good matches:
| Math Font | Style | Notes |
|-----------|-------|-------|
| Lete Sans Math | Sans-serif | Clean, modern. On CTAN. |
| Fira Math | Sans-serif | Matches Fira Sans. |
| GFS Neohellenic Math | Sans-serif | Greek heritage. |

**For serif text fonts**, good matches:
| Math Font | Style | Notes |
|-----------|-------|-------|
| STIX Two Math | Serif | Very complete coverage. |
| Latin Modern Math | Serif | Classic TeX look. |
| TeX Gyre Termes Math | Serif | Times-like. |
| TeX Gyre Pagella Math | Serif | Palatino-like. |
| Asana Math | Serif | Palatino-inspired. |

Pick a math font whose weight and style feel compatible with your text font.
The Greek letters and symbols will come from the math font, so they should
harmonize with the text font's Latin characters.
