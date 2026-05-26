# Libertinus Sans Bold Italic — Synthetic Generation

Libertinus Sans has no bold italic font file. We synthesize a complete
`LibertinusSans-BoldItalic-Synth.otf` using the pipeline below.

## Pipeline Overview

1. **Skew the bold font** 12° (all 2650 glyphs)
2. **Replace 6 glyphs** (a, e, f, g, l, kappa) with hand-edited paths
3. **Copy GPOS** (kerning) from the italic font, subset to common glyphs
4. **Set advance widths** per-glyph: `italic_width * (bold_width / regular_width) + 10`
5. **Tune sidebearings** for the 6 hand-edited glyphs via L/R visual adjustment

## Step 1: Skew Bold

For most glyphs, the italic and upright letter shapes are the same (just slanted).
We apply a 12° italic skew to every glyph in LibertinusSans-Bold.otf:

```python
TransformPen(t2pen, (1, 0, tan(12°), 1, 0, 0))
```

Important: must desubroutinize the CFF font first (via fontTools Subsetter with
`options.desubroutinize = True`) because subroutined charstrings can't be
individually transformed.

Skewing does NOT change advance widths (the shear is horizontal, measured at
baseline y=0 where the transform has no effect).

## Step 2: Replace Hand-Edited Glyphs

For glyphs where italic has a fundamentally different shape from upright
(e.g., single-story 'a' vs double-story, cursive 'f'/'l' vs straight),
the skewed bold looks wrong. These get hand-edited paths instead.

### How the hand-edited paths were created

1. Start with italic glyph outlines
2. Apply directional emboldening: V=35 (vertical strokes), H=5 (horizontal)
   using adaptive miter-averaged blend algorithm
3. Run `pathops.simplify()` to clean up self-intersections
4. Export to SVG (`bold-italic-glyphs.svg`)
5. Edit in **Inkscape**: delete problem nodes, smooth curves, adjust handles
   - Blue stroke overlay: original italic (reference)
   - Red stroke overlay: skewed bold (width/weight reference)
   - Green stroke overlay: skewed bold 'q' (bowl shape reference for 'a')
6. Read edited paths back into font via T2CharStringPen

### Glyph list

| Glyph | Why not skewed bold |
|-------|-------------------|
| a | Single-story italic vs double-story upright |
| e | Different tail shape |
| f | Descender in italic, no descender in upright |
| g | Different ear/loop structure |
| l | Curved italic vs straight upright |
| κ (kappa) | Different stroke structure |

### Coordinate system warning

When Inkscape ungroups paths, it bakes the SVG group transform into the path
coordinates. Track which glyphs are ungrouped and apply the inverse transform
when reading back:
- Grouped paths: font coordinates (y-up), no conversion needed
- Ungrouped paths: screen coordinates, need `(x-tx)*2, (y-ty)*-2`
- Each group had its own translate: 'a' was translate(50,500), 'l' was translate(50,1050)

## Step 3: GPOS (Kerning)

Copy the italic font's GPOS table, subset to glyphs present in both fonts.
We use italic GPOS (not bold) because advance widths are derived from italic
widths (see Step 4).

```python
italic_sub = TTFont(ITALIC_PATH)
opts = Options(); opts.layout_features = ['kern']
sub = Subsetter(opts)
common = set(synth.getGlyphOrder()) & set(italic_sub.getGlyphOrder())
sub.populate(glyphs=list(common))
sub.subset(italic_sub)
font['GPOS'] = italic_sub['GPOS']
```

## Step 4: Advance Widths

All glyphs (not just the 6 hand-edited ones) get widths derived from italic:

```
width = round(italic_width * bold_width / regular_width) + 10
```

This ensures consistent rhythm: the italic font's spacing proportions are
preserved, scaled up for bold weight. The +10 is a global loosening.

## Step 5: Sidebearing Tuning

The 6 hand-edited glyphs need manual L (left shift) and R (right width)
adjustments to match the rhythm of surrounding skewed-bold glyphs.

Tuning was done visually using `width-tuner.html`:
- L shifts the glyph ink right by L font units (increases LSB, decreases RSB)
- R adds R font units to the advance width (increases RSB)
- Test strings: `nnnanonn`, `nonanom`, `fundamental`, `algebra`, `eagle`, etc.
- Compare against regular, italic, and bold at multiple sizes (12-72px)

### Final tuned values (cumulative from all rounds)

| Glyph | W | LSB | RSB |
|-------|-----|------|------|
| a | 574 | 76 | -19 |
| e | 478 | 73 | -32 |
| f | 400 | -69 | -217 |
| g | 524 | 10 | -50 |
| l | 331 | 107 | -55 |
| kappa | 565 | 76 | -45 |

Negative RSB (ink overhang) is normal for italic fonts.

## Build Script Integration

The synth font is built separately and saved as
`fonts/libertinus/LibertinusSans-BoldItalic-Synth.otf`.

`build.py` references it as the `bold_italic` text font, and also runs a
post-build step `_patch_bold_italic_glyphs()` that replaces math alphanumeric
codepoints (U+1D482+ and U+1D656+) in the MathJax output with the hand-edited
SVG paths.

## Tools Used

- **fontTools**: TTFont, T2CharStringPen, TransformPen, Subsetter (desubroutinize)
- **pathops**: simplify() for cleaning emboldened outlines
- **Inkscape**: node editing of glyph outlines (excellent path editor)
- **width-tuner.html**: CSS-based visual sidebearing tuner with rhythm test strings

## Lessons Learned

- Skewing does not change advance widths (measured at baseline y=0)
- Professional typographers space by eye, not by formula
- Visual gap = RSB(prev) + LSB(next); no formula works for all contexts
- Italic fonts naturally have asymmetric/negative sidebearings
- Browser "bold synthesis" (WebKit: double-draw shift, Chromium: stroke-and-fill)
  works at the rasterizer level, not the outline level — can't replicate in fonts
- GPOS kern pairs must match the advance width system (italic GPOS for italic-derived widths)
- When multiple hand-edited glyphs are adjacent, individual adjustments compound
