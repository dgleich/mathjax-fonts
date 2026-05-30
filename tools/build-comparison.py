#!/usr/bin/env python3
"""Build an HTML comparison page from test-renders/ SVG files."""
import os

FONTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

fonts = ['mathjax-libertinus', 'mathjax-libertinus-sans', 'mathjax-lm-sans',
         'mathjax-noto-sans', 'mathjax-source-sans', 'mathjax-source-code',
         'mathjax-concrete-euler', 'mathjax-shantell', 'mathjax-lato', 'mathjax-ptsans']

short_names = {
    'mathjax-libertinus': 'Libertinus',
    'mathjax-libertinus-sans': 'Lib Sans',
    'mathjax-lm-sans': 'LM Sans',
    'mathjax-noto-sans': 'Noto Sans',
    'mathjax-source-sans': 'Source Sans',
    'mathjax-source-code': 'Source Code',
    'mathjax-concrete-euler': 'Concrete',
    'mathjax-shantell': 'Shantell',
    'mathjax-lato': 'Lato',
    'mathjax-ptsans': 'PT Sans',
}

# Read expressions
labels = []
current_section = ''
with open(os.path.join(FONTS_DIR, 'tools/test-expressions.txt')) as f:
    for line in f:
        line = line.strip()
        if line.startswith('#') and '===' in line:
            current_section = line.replace('#', '').replace('===', '').strip()
            continue
        if not line or line.startswith('#'):
            continue
        labels.append((current_section, line))

n = len(labels)
print(f'{n} expressions, {len(fonts)} fonts')

parts = []
parts.append('''<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>MathJax Font Comparison</title>
<style>
body { font-family: -apple-system, sans-serif; max-width: 100%%; margin: 0; padding: 1em; background: #fafafa; }
h1 { text-align: center; margin-bottom: 0.3em; }
.section-header { background: #e8e8e8; padding: 8px 12px; margin-top: 2em; font-size: 16px; font-weight: bold; border-left: 4px solid #333; }
.expr-group { margin: 1em 0; background: white; padding: 8px 12px; border: 1px solid #ddd; border-radius: 4px; }
.expr-label { font-family: monospace; font-size: 11px; color: #888; margin-bottom: 4px; }
.font-row { display: flex; align-items: center; margin: 1px 0; }
.font-name { width: 100px; min-width: 100px; font-size: 12px; font-weight: 600; color: #555; }
.font-render { flex: 1; overflow: hidden; }
.font-render img { height: 28px; }
.font-render.display img { height: 50px; }
.controls { position: sticky; top: 0; background: white; z-index: 10; padding: 8px; border-bottom: 2px solid #ddd; display: flex; flex-wrap: wrap; gap: 4px 12px; align-items: center; }
.controls label { font-size: 12px; cursor: pointer; }
.controls button { font-size: 12px; padding: 2px 8px; cursor: pointer; }
</style>
<script>
function toggleFont(cls, checked) {
    document.querySelectorAll('.font-' + cls).forEach(function(el) {
        el.style.display = checked ? '' : 'none';
    });
}
function setSize(px) {
    document.querySelectorAll('.font-render:not(.display) img').forEach(function(i) { i.style.height = px + 'px'; });
    document.querySelectorAll('.font-render.display img').forEach(function(i) { i.style.height = (px * 1.6) + 'px'; });
}
</script>
</head><body>
<h1>MathJax Font Comparison</h1>
<div class="controls">
<strong>Fonts:&nbsp;</strong>
''')

for f in fonts:
    sn = short_names[f]
    cls = f.replace('-', '')
    parts.append(f'<label><input type="checkbox" checked onchange="toggleFont(\'{cls}\', this.checked)">{sn}</label>\n')

parts.append('''<strong>&nbsp;Size:&nbsp;</strong>
<button onclick="setSize(20)">S</button>
<button onclick="setSize(28)">M</button>
<button onclick="setSize(42)">L</button>
<button onclick="setSize(60)">XL</button>
</div>
''')

prev_section = ''
for i, (section, expr) in enumerate(labels, 1):
    if section != prev_section:
        parts.append(f'<div class="section-header">{section}</div>\n')
        prev_section = section

    padded = f'{i:03d}'
    is_display = 'display' in section.lower()
    display_class = ' display' if is_display else ''
    safe_expr = expr.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    parts.append(f'<div class="expr-group">\n')
    parts.append(f'  <div class="expr-label">{padded}: <code>{safe_expr}</code></div>\n')
    for f in fonts:
        sn = short_names[f]
        cls = f.replace('-', '')
        svg_path = os.path.join(FONTS_DIR, f'test-renders/{f}/{padded}.svg')
        if os.path.exists(svg_path):
            rel_path = f'test-renders/{f}/{padded}.svg'
            parts.append(f'  <div class="font-row font-{cls}"><span class="font-name">{sn}</span><span class="font-render{display_class}"><img src="{rel_path}" alt="{sn}"></span></div>\n')
    parts.append('</div>\n')

parts.append('</body></html>')

html = ''.join(parts)
out = os.path.join(FONTS_DIR, 'comparison.html')
with open(out, 'w') as f:
    f.write(html)
print(f'Written {out} ({len(html)} bytes)')
