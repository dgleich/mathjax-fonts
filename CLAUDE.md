# MathJax Fonts — Development Rules

## GOLDEN RULE

**No hand tweaks to output files.** Everything must be reproducible from
`build.py` scripts and automated tools. If a fix is needed, put it in
`build.py` FIRST, then rebuild. Any manually patched CJS/JS file WILL
be overwritten on the next rebuild.

## Working Notes

All working notes, plans, and scratch files go in `~/.claude/projects/-work/notes/`,
NOT in the repo. Do not add files to .gitignore for scratch work.

See also:
- `/work/.claude/CRITICAL-BUILD-FIXES.md` — post-build fixes checklist
- `STATUS.md` — project status and open items
- `TUTORIAL.md` — full technical reference

## Python Environment

Use the project venv: `source /work/mathjax-fonts/venv/bin/activate`
Do NOT use system python (no pip, no fontTools).

## Build Process — MANDATORY STEPS

Every font change requires ALL of these steps in order. Do not skip any.

### 1. Edit build.py (not CJS files directly)

ALL fixes must be in the font's `build.py`. Never manually edit CJS files —
they get overwritten on rebuild.

### 2. Build CJS data

```bash
source venv/bin/activate
python3 mathjax-{name}/build.py
```

### 3. Rebuild webpack bundles (BOTH full and nosre)

```bash
cd mathjax-{name}/build
npx webpack --config webpack.config.cjs        # full bundle for test.html
npx webpack --config webpack-nosre.config.cjs   # nosre bundle for eigendeck
cd ../..
```

**CRITICAL**: The test.html specimen page loads the webpack bundle, not CJS
directly. If you skip this step, the browser shows stale fonts. This has
caused repeated confusion.

### 4. Verify in browser

The specimen page is at: `http://localhost:8080/mathjax-fonts/mathjax-{name}/test.html`

### 5. Render test expressions

```bash
bash tools/render-all.sh mathjax-{name}
```

### 6. Rebuild comparison page

```bash
python3 tools/build-comparison.py
```

### 7. Commit

Commit the build.py, CJS files, webpack bundles, and test renders together.

### 8. Push

```bash
git push origin main
```

### Shortcut: rebuild everything

```bash
bash tools/build-all.sh mathjax-{name}          # CJS + full + nosre bundles
bash tools/build-all.sh mathjax-{name} --nosre-only  # just nosre bundle
bash tools/build-all.sh                          # all 10 fonts
```

## Specimen Pages

All specimen pages are generated from `lib/specimen-template.html`.

**NEVER edit individual test.html files.** Edit the template, then regenerate:

```bash
python3 tools/build-specimens.py
```

## Test Render Pipeline

```bash
# Render all expressions for all fonts:
bash tools/render-all.sh

# Render one font:
bash tools/render-all.sh mathjax-{name}

# Build comparison page (uses PNGs from test-renders/):
python3 tools/build-comparison.py

# Diff against a baseline:
cp -r test-renders test-renders-baseline
# ... make changes, rebuild, re-render ...
bash tools/diff-renders.sh
```

## When Rebuilding Fonts You Didn't Change

If you rebuild a font you didn't intentionally modify, **diff the CJS output
before committing**:

```bash
git diff --stat -- mathjax-{name}/cjs/
```

The library evolves over time. Rebuilding with a newer library can produce
different (but equivalent) CJS. Don't commit these unintended changes —
restore with `git checkout HEAD -- mathjax-{name}/cjs/`.

## Key Technical Patterns

### italic_lsb=0
Fonts with `greek_from_text=True` that have italic text fonts with large
left side bearings need `italic_lsb=0` in `build_all_variants()` to shift
paths left. Without this, italic letters have visible gaps.

Applied to: concrete-euler, source-code, ptsans.
Still needed: libertinus-sans, source-sans, shantell, lato.

### Calligraphic / Script separation
- `tex-calligraphic.js` = `\mathcal` (Lete Sans Math calligraphic or NewCM default)
- `script.js` = `\mathscr` (NewCM ss01 alternates)
- Both files needed — if tex-calligraphic.js is empty, `\mathcal` falls through to script.js
- svg.js must wire both variants
- Script codepoint dupes must be removed from bold/italic/bold-italic.js

### Integral subscript tuning
`adjust_integral_widths(OUTPUT_DIR, smallop_w_ratio=X, smallop_ic=0.03, largeop_w_ratio=Y, largeop_ic=0.25)`
- smallop_w_ratio controls inline integral subscript position
- Too small = subscripts overlap integral curves
- Too large = subscripts sit too far right
- Current values: LM Sans 0.70, PT Sans/Lato 0.78, others 0.89 (default)

### x_height
`get_x_height()` uses actual 'x' glyph height, not OS/2 table. This is
critical for text-math size matching. Don't override unless you've measured.

### matchFontHeight
All specimen templates use `matchFontHeight: false` in the MathJax SVG config.
This prevents zoom scaling drift. The CDN default MathJax specimen also uses this.
