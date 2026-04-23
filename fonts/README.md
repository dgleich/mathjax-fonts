# Source Fonts

Font files are not checked into git. Download them before building.

## Math fonts (needed for all packages)

| Font | Source | Used by |
|------|--------|---------|
| Latin Modern Math | `https://mirrors.ctan.org/fonts/lm-math/opentype/latinmodern-math.otf` | ptsans, source-sans, source-code, shantell |
| Lete Sans Math | CTAN `lete-sans-math` package | lato |
| Libertinus Math | `https://mirrors.ctan.org/fonts/libertinus-fonts.zip` → otf/LibertinusMath-Regular.otf | libertinus, libertinus-sans |
| Noto Sans Math | Google Fonts `https://fonts.google.com/noto/specimen/Noto+Sans+Math` | noto-sans |
| Euler Math | `https://mirrors.ctan.org/fonts/euler-math.zip` → Euler-Math.otf | concrete-euler |
| NewCM Sans Math | `https://mirrors.ctan.org/fonts/newcomputermodern.zip` → otf/NewCMSansMath-Regular.otf | lm-sans |

## Text fonts

| Font | Source | Format |
|------|--------|--------|
| Lato (patched, serifed I) | Build with `patch_lato_serif_i.py` from workspace | Static TTF |
| PT Sans (patched, serifed I) | Build with `patch_ptsans_replace_i.py` from workspace | Static TTF |
| Libertinus Serif | `https://mirrors.ctan.org/fonts/libertinus-fonts.zip` | Static OTF |
| Libertinus Sans | Same package as above | Static OTF |
| CMU Sans Serif | `https://sourceforge.net/projects/cm-unicode/` (v0.7.0) | Static OTF |
| CMU Concrete | Same CM Unicode package | Static OTF |
| Noto Sans | Google Fonts (variable font) | Variable TTF |
| Source Sans 3 | Google Fonts (variable font) | Variable TTF |
| Source Code Pro | Google Fonts (variable font) | Variable TTF |
| Shantell Sans | Google Fonts (variable font) | Variable TTF |
| Comic Relief | Google Fonts / GitHub `loudifier/Comic-Relief` | Static TTF |

## newtxsf (for PT Sans Greek)

| Font | Source |
|------|--------|
| zsfmi-reg.pfb, zsfmi-bol.pfb | `https://mirrors.ctan.org/fonts/newtxsf.zip` → type1/ |
| zsfmia-reg.pfb, zsfmia-bol.pfb | Same package |

## Directory structure

Place fonts in subdirectories matching their package:
```
fonts/
  lm-math/latinmodern-math.otf
  lete-sans-math/LeteSansMath.otf
  libertinus/LibertinusMath-Regular.otf, LibertinusSans-*.otf, LibertinusSerif-*.otf
  noto-sans/NotoSans[wdth,wght].ttf, NotoSans-Italic[wdth,wght].ttf
  noto-sans-math/NotoSansMath-Regular.ttf
  euler-math/Euler-Math.otf
  newcomputermodern/NewCMSansMath-Regular.otf
  cmu-sans/cmunss.otf, cmunsx.otf, cmunsi.otf, cmunso.otf
  cmu-concrete/CMUConcrete-Roman.otf, CMUConcrete-Slanted.otf, CMUConcrete-Bold.otf
  source-sans/SourceSans3[wght].ttf, SourceSans3-Italic[wght].ttf
  source-code-pro/SourceCodePro[wght].ttf, SourceCodePro-Italic[wght].ttf
  shantell-sans/ShantellSans[BNCE,INFM,SPAC,wght].ttf, ShantellSans-Italic[...].ttf
  newtxsf/zsfmi-reg.pfb, zsfmi-bol.pfb, zsfmia-reg.pfb, zsfmia-bol.pfb
  lato-patched/Lato-Regular.ttf, Lato-Bold.ttf, Lato-Italic.ttf, Lato-BoldItalic.ttf
  ptsans-patched/PT_Sans-Web-Regular.ttf, PT_Sans-Web-Bold.ttf, etc.
```
