# Libertinus Sans Bold Italic — Synthetic Generation

Libertinus Sans has no bold italic font file. We synthesize bold italic
glyphs using two approaches:

## Approach 1: Skewed Bold (default)

For most glyphs, take the upright Bold font and apply a 12° italic skew
via `TransformPen(pen, (1, 0, tan(12°), 1, 0, 0))`. This works well when
the italic and upright letter shapes are the same (just slanted).

## Approach 2: Directional Emboldened Italic (select glyphs)

For glyphs where italic has a fundamentally different shape from upright
(e.g., single-story 'a' vs double-story, cursive 'l' vs straight), we
embolden the italic outline directly.

### Algorithm: Split X/Y offset along contour normals

For each on-curve point:
1. Compute incoming tangent (from previous control point or previous point)
2. Compute outgoing tangent (toward next control point or next point)
3. Compute outward normal for each: `N = (tangent.y, -tangent.x)`
4. Compute anisotropic offset: `O = (N.x * amount_v, N.y * amount_h)`
   - amount_v = 35 (fattens vertical strokes)
   - amount_h = 5 (barely affects horizontal strokes)

### Corner handling: Miter join

At corners where incoming and outgoing segments meet:
- Define offset lines for each segment direction
- Find their intersection (miter point)
- If intersection too far (miter_limit=4x max offset), fall back to averaged normal

This prevents "kinks" (dents at sharp corners) that occur with simple
normal averaging.

For control points on cubic beziers:
- C1 gets the previous endpoint's offset
- C2 gets the current endpoint's offset
- Valid when offset << curve radius (35 units vs ~100-400 unit radii)

### Per-glyph method choice

Some glyphs work better with miter, others with averaged normals:
- **Miter join**: f, g, l, e, κ, ϰ (sharp corners need clean intersections)
- **Averaged normals**: a (gentle curves, miter over-extends at some corners)

## Glyph assignments

| Category | Method | Glyphs |
|----------|--------|--------|
| Most Latin, digits, punctuation | Skewed bold | A-Z (except below), 0-9, symbols |
| Different italic shape | Emboldened italic | a, e, f, g, l |
| Greek lowercase (different shape) | Emboldened italic | κ, ϰ |
| Greek uppercase | Skewed bold | Σ, Ψ, all others |
| Greek lowercase (same shape) | Skewed bold | β, π, ψ, all others |
| Cyrillic | Skewed bold | all |
| Letterlike symbols | Italic font directly | ℎ, ℏ, ℓ, ℂ, ℍ, etc. (except ℚ → skewed bold) |
| Math operators | Italic for ∂, ∅, ∆, ∈; skewed bold for ∇, ∏, ∐ |
| IPA | Would need emboldened italic but rarely used in math |

## Notes

- β: would benefit from emboldened italic but the curve at the waist
  thickens too much with current technique. Using skewed bold for now.
- IoU scoring (pixel-level with best-fit translation) was used to compare
  emboldened italic vs skewed bold for all A-Z, a-z, 0-9: 11 SAME, 27 CLOSE,
  7 CHECK, 7 DIFF.
- The V35/H5 parameters were tuned visually against the actual Bold font.
