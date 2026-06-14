#!/usr/bin/env python3
"""Regenerate all test.html specimen pages from the template."""
import os

FONTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(FONTS_DIR, 'lib', 'specimen-template.html')

SPECIMENS = [
    {
        'dir': 'mathjax-libertinus',
        'title': 'Libertinus Serif + Libertinus Math',
        'bundle': 'tex-mml-svg-mathjax-libertinus.js',
        'css': """@font-face { font-family: 'Libertinus'; src: url('../fonts/libertinus/LibertinusSerif-Regular.otf'); }
@font-face { font-family: 'Libertinus'; src: url('../fonts/libertinus/LibertinusSerif-Italic.otf'); font-style: italic; }
@font-face { font-family: 'Libertinus'; src: url('../fonts/libertinus/LibertinusSerif-Bold.otf'); font-weight: bold; }
@font-face { font-family: 'Libertinus'; src: url('../fonts/libertinus/LibertinusSerif-BoldItalic.otf'); font-weight: bold; font-style: italic; }""",
        'family': '"Libertinus", serif',
    },
    {
        'dir': 'mathjax-libertinus-sans',
        'title': 'Libertinus Sans + Libertinus Math',
        'bundle': 'tex-mml-svg-mathjax-libertinus-sans.js',
        'css': """@font-face { font-family: 'Libertinus Sans'; src: url('../fonts/libertinus/LibertinusSans-Regular.otf'); }
@font-face { font-family: 'Libertinus Sans'; src: url('../fonts/libertinus/LibertinusSans-Italic.otf'); font-style: italic; }
@font-face { font-family: 'Libertinus Sans'; src: url('../fonts/libertinus/LibertinusSans-Bold.otf'); font-weight: bold; }""",
        'family': '"Libertinus Sans", sans-serif',
    },
    {
        'dir': 'mathjax-lm-sans',
        'title': 'CMU Sans Serif + NewCM Sans Math',
        'bundle': 'tex-mml-svg-mathjax-lm-sans.js',
        'css': """@font-face { font-family: 'CMU Sans'; src: url('../fonts/cmu-sans/cmunss.otf'); }
@font-face { font-family: 'CMU Sans'; src: url('../fonts/cmu-sans/cmunsi.otf'); font-style: italic; }
@font-face { font-family: 'CMU Sans'; src: url('../fonts/cmu-sans/cmunsx.otf'); font-weight: bold; }
@font-face { font-family: 'CMU Sans'; src: url('../fonts/cmu-sans/cmunso.otf'); font-weight: bold; font-style: italic; }""",
        'family': '"CMU Sans", sans-serif',
    },
    {
        'dir': 'mathjax-noto-sans',
        'title': 'Noto Sans + Noto Sans Math',
        'bundle': 'tex-mml-svg-mathjax-noto-sans.js',
        'css': """@font-face { font-family: 'Noto Sans'; src: url('../fonts/noto-sans/NotoSans[wdth,wght].ttf'); }
@font-face { font-family: 'Noto Sans'; src: url('../fonts/noto-sans/NotoSans-Italic[wdth,wght].ttf'); font-style: italic; }""",
        'family': '"Noto Sans", sans-serif',
    },
    {
        'dir': 'mathjax-source-sans',
        'title': 'Source Sans 3 + Latin Modern Math',
        'bundle': 'tex-mml-svg-mathjax-source-sans.js',
        'css': """@font-face { font-family: 'Source Sans'; src: url('../fonts/source-sans/SourceSans3[wght].ttf'); }
@font-face { font-family: 'Source Sans'; src: url('../fonts/source-sans/SourceSans3-Italic[wght].ttf'); font-style: italic; }""",
        'family': '"Source Sans", sans-serif',
    },
    {
        'dir': 'mathjax-source-code',
        'title': 'Source Code Pro + Latin Modern Math',
        'bundle': 'tex-mml-svg-mathjax-source-code.js',
        'css': """@font-face { font-family: 'Source Code Pro'; src: url('../fonts/source-code/SourceCodePro[wght].ttf'); }
@font-face { font-family: 'Source Code Pro'; src: url('../fonts/source-code/SourceCodePro-Italic[wght].ttf'); font-style: italic; }""",
        'family': '"Source Code Pro", monospace',
    },
    {
        'dir': 'mathjax-concrete-euler',
        'title': 'CMU Concrete + Euler Math',
        'bundle': 'tex-mml-svg-mathjax-concrete-euler.js',
        'css': """@font-face { font-family: 'Concrete'; src: url('../fonts/concrete/CMUConcrete-Roman.otf'); }
@font-face { font-family: 'Concrete'; src: url('../fonts/concrete/CMUConcrete-Italic.otf'); font-style: italic; }
@font-face { font-family: 'Concrete'; src: url('../fonts/concrete/CMUConcrete-Bold.otf'); font-weight: bold; }""",
        'family': '"Concrete", serif',
    },
    {
        'dir': 'mathjax-shantell',
        'title': 'Shantell Sans + Latin Modern Math',
        'bundle': 'tex-mml-svg-mathjax-shantell.js',
        'css': """@font-face { font-family: 'Shantell Sans'; src: url('../fonts/shantell/ShantellSans[BNCE,INFM,SPAC,wght].ttf'); }
@font-face { font-family: 'Shantell Sans'; src: url('../fonts/shantell/ShantellSans-Italic[BNCE,INFM,SPAC,wght].ttf'); font-style: italic; }""",
        'family': '"Shantell Sans", cursive',
    },
    {
        'dir': 'mathjax-lato',
        'title': 'Lato + Lete Sans Math',
        'bundle': 'tex-mml-svg-mathjax-lato.js',
        'css': """@font-face { font-family: 'Lato'; src: url('../fonts/lato/Lato-Regular-Patched.otf'); }
@font-face { font-family: 'Lato'; src: url('../fonts/lato/Lato-Italic.ttf'); font-style: italic; }
@font-face { font-family: 'Lato'; src: url('../fonts/lato/Lato-Bold.ttf'); font-weight: bold; }
@font-face { font-family: 'Lato'; src: url('../fonts/lato/Lato-BoldItalic.ttf'); font-weight: bold; font-style: italic; }""",
        'family': '"Lato", sans-serif',
    },
    {
        'dir': 'mathjax-ptsans',
        'title': 'PT Sans + Latin Modern Math',
        'bundle': 'tex-mml-svg-mathjax-ptsans.js',
        'css': """@font-face { font-family: 'PT Sans'; src: url('../fonts/ptsans/PTSans-Regular-Patched.otf'); }
@font-face { font-family: 'PT Sans'; src: url('../fonts/ptsans/PT_Sans-Web-Italic.ttf'); font-style: italic; }
@font-face { font-family: 'PT Sans'; src: url('../fonts/ptsans/PT_Sans-Web-Bold.ttf'); font-weight: bold; }
@font-face { font-family: 'PT Sans'; src: url('../fonts/ptsans/PT_Sans-Web-BoldItalic.ttf'); font-weight: bold; font-style: italic; }""",
        'family': '"PT Sans", sans-serif',
    },
    # Default MathJax reference
    {
        'dir': None,  # goes to repo root
        'outfile': 'specimen-default-mathjax.html',
        'title': 'Default MathJax (newCM)',
        'bundle': 'https://cdn.jsdelivr.net/npm/mathjax@4.1.2/tex-mml-svg.js',
        'css': '/* default MathJax — no custom CSS */',
        'family': 'serif',
    },
]


def main():
    with open(TEMPLATE) as f:
        template = f.read()

    for spec in SPECIMENS:
        result = template.replace('FONT_TITLE', spec['title'])
        result = result.replace('FONT_BUNDLE', spec['bundle'])
        result = result.replace('FONT_CSS', spec['css'])
        result = result.replace('FONT_FAMILY', spec['family'])

        if spec.get('outfile'):
            outpath = os.path.join(FONTS_DIR, spec['outfile'])
        else:
            outpath = os.path.join(FONTS_DIR, spec['dir'], 'test.html')

        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        with open(outpath, 'w') as f:
            f.write(result)
        print(f'  {os.path.relpath(outpath, FONTS_DIR)}')

    print(f'Done: {len(SPECIMENS)} specimens generated')


if __name__ == '__main__':
    main()
