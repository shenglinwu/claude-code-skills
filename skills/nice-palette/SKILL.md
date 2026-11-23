---
name: "nice-palette"
description: "Default colour theme for any HTML Claude builds (pages, presentations, dashboards, reports, charts, SVG): blue-green base #0D98BA plus mint, orange, cinnabar, gold, grape, amber-brown and gray side colours. Named palettes to pick from: blue-green (default), steel-blue, galaxy, natural. Use unless the user names other colours."
---

# Nice Palette

The user's default colour theme. Apply it to **every HTML file or HTML-based output you hand-build**: web pages, HTML presentations (the nice-presentation skill already uses it), dashboards, reports, charts (Chart.js, D3, Plotly, SVG), emails written in HTML, and inline HTML/SVG visuals.

Don't apply it when:
- the user names other colours, a brand, or another theme for this output (theirs wins), or
- the output is an existing file or template that already has its own colours (keep them unless asked to restyle), or
- a dedicated artifact type or skill with its own fixed design system is producing the output.

## Choosing a palette

Four named palettes. Use **blue-green** unless the user names another one ("use the galaxy palette", "natural colours", `/nice-palette galaxy`).

| Palette | Base | Side colours | Where the details are |
|---|---|---|---|
| `blue-green` (default) | `#0D98BA` | mint, dark orange, cinnabar, gold, grape, amber brown, gray | The palette (below) |
| `steel-blue` | `#4682B4` | same as blue-green | Run the script with `steel-blue`; side colours stay the same |
| `galaxy` | `#324856` | sage `#4A746A`, ochre `#D18237`, terracotta `#D66C44` | Galaxy and Natural |
| `natural` | `#6C838B` | copper `#BB7748`, mauve `#9E6D70`, taupe `#7F726A` | Galaxy and Natural |

Galaxy and natural bring their **own** side colours: they replace the blue-green side colours, they do not add to them. Say which palette you used when you hand over the output.

## The palette

**Base colour: Blue Green `#0D98BA`.** It carries the structure: headings' accent words, links, buttons, navigation, active states, focus rings, the primary chart series.

| Token | Hex | RGB | Use |
|---|---|---|---|
| `--accent` | `#0A748D` | 10,116,141 | Accent **text**, buttons, links (4.5:1 on the background) |
| `--accent-mid` | `#0D98BA` | 13,152,186 | The base colour itself: fills, bars, icons, borders |
| `--accent-light` | `#62BCD2` | 98,188,210 | Glows, accents on dark surfaces |
| `--bg` | `#E2F3F7` | | Page background |
| `--bg-alt` | `#D3ECF3` | | Table headers, alternate sections |
| `--surface` | `#F0F9FB` | | Light panels |
| `--surface-2` | `#FFFFFF` | | Cards |
| `--ink` / `--text-1` | `#0E2025` | 14,32,37 | Headings, body text, dark sections |
| `--text-2` | `#3A5C64` | | Secondary text |
| `--text-3` | `#6C8B93` | | Captions, meta |

**Side colours** decorate repeated or categorical items: cards, stats, chart series, tags, timeline steps, avatars, status. Each has an **-ink** shade. Use the exact colour for fills, bars and borders, and the -ink shade for any **text or thin glyph** in that colour, so light colours like gold and orange stay readable.

| Name | Fill | RGB | -ink (text) |
|---|---|---|---|
| Mint | `#00AB78` | 0,171,120 | `#007653` |
| Dark Orange | `#FF8C00` | 255,140,0 | `#9B5500` |
| Cinnabar | `#E34234` | 227,66,52 | `#BD372B` |
| Gold | `#FFD700` | 255,215,0 | `#796600` |
| Grape | `#6F2DA8` | 111,45,168 | `#6F2DA8` |
| Amber Brown | `#A6674C` | 166,103,76 | `#935B43` |
| Metallic Gray | `#999B9B` | 153,155,155 | `#6A6B6B` |

## Rules

1. **Base colour first.** Most of the page is neutral (backgrounds, ink, greys) plus blue-green. Side colours are decoration, not structure: never use them for headlines, body text, links or primary buttons.
2. **Cycle order** for repeated items and chart series: blue-green → dark orange → grape → mint → cinnabar → gold → amber brown. Metallic gray is for "other", neutral, disabled or baseline items.
3. **At most about four side colours in one view.** With more categories, group the tail into gray "Other".
4. **Status meanings are fixed:** mint = success/done/positive, dark orange = warning/in progress, cinnabar = error/failed/negative, gray = inactive/queued, blue-green = info/active. Don't reuse cinnabar or mint for unrelated decoration on the same view where they carry status.
5. **Text contrast:** text in any side colour uses its -ink shade. On dark (`--ink`) backgrounds use the fill colours or `--accent-light`, never the -ink shades.
6. **Tints:** for soft backgrounds of chips, icons and badges use the colour at 10–14% alpha with a 25–35% alpha border, as in `rgba(0,171,120,0.10)`.
7. **Fonts are not part of this skill.** Keep whatever typography the output calls for. If nothing else decides it, DM Sans for text with Playfair Display italic for accent words pairs well with this palette.

## Drop-in CSS

Paste into the `<style>` of any HTML file, then use the variables. The `.tone-*` classes set `--tone`, `--tone-rgb` and `--tone-ink` on an element so components can read one colour. `.tone-cycle` applies the cycle order to its children automatically.

```css
:root {
  /* Base: Blue Green #0D98BA */
  --bg: #E2F3F7; --bg-alt: #D3ECF3; --surface: #F0F9FB; --surface-2: #FFFFFF;
  --accent: #0A748D; --accent-mid: #0D98BA; --accent-light: #62BCD2;
  --accent-rgb: 10,116,141; --mid-rgb: 13,152,186; --light-rgb: 98,188,210;
  --ink: #0E2025; --ink-rgb: 14,32,37; --text-1: #0E2025; --text-2: #3A5C64; --text-3: #6C8B93;
  --border: rgba(14,32,37,0.08);
  /* Side colours: fill / rgb / -ink (text) */
  --c-mint: #00AB78;        --c-mint-rgb: 0,171,120;         --c-mint-ink: #007653;
  --c-orange: #FF8C00;      --c-orange-rgb: 255,140,0;       --c-orange-ink: #9B5500;
  --c-cinnabar: #E34234;    --c-cinnabar-rgb: 227,66,52;     --c-cinnabar-ink: #BD372B;
  --c-gold: #FFD700;        --c-gold-rgb: 255,215,0;         --c-gold-ink: #796600;
  --c-grape: #6F2DA8;       --c-grape-rgb: 111,45,168;       --c-grape-ink: #6F2DA8;
  --c-amber-brown: #A6674C; --c-amber-brown-rgb: 166,103,76; --c-amber-brown-ink: #935B43;
  --c-gray: #999B9B;        --c-gray-rgb: 153,155,155;       --c-gray-ink: #6A6B6B;
}
.tone-base        { --tone: var(--accent-mid);     --tone-rgb: var(--mid-rgb);             --tone-ink: var(--accent); }
.tone-mint        { --tone: var(--c-mint);         --tone-rgb: var(--c-mint-rgb);         --tone-ink: var(--c-mint-ink); }
.tone-orange      { --tone: var(--c-orange);       --tone-rgb: var(--c-orange-rgb);       --tone-ink: var(--c-orange-ink); }
.tone-cinnabar    { --tone: var(--c-cinnabar);     --tone-rgb: var(--c-cinnabar-rgb);     --tone-ink: var(--c-cinnabar-ink); }
.tone-gold        { --tone: var(--c-gold);         --tone-rgb: var(--c-gold-rgb);         --tone-ink: var(--c-gold-ink); }
.tone-grape       { --tone: var(--c-grape);        --tone-rgb: var(--c-grape-rgb);        --tone-ink: var(--c-grape-ink); }
.tone-amber-brown { --tone: var(--c-amber-brown);  --tone-rgb: var(--c-amber-brown-rgb);  --tone-ink: var(--c-amber-brown-ink); }
.tone-gray        { --tone: var(--c-gray);         --tone-rgb: var(--c-gray-rgb);         --tone-ink: var(--c-gray-ink); }
.tone-cycle > :nth-child(7n+1) { --tone: var(--accent-mid);    --tone-rgb: var(--mid-rgb);            --tone-ink: var(--accent); }
.tone-cycle > :nth-child(7n+2) { --tone: var(--c-orange);      --tone-rgb: var(--c-orange-rgb);      --tone-ink: var(--c-orange-ink); }
.tone-cycle > :nth-child(7n+3) { --tone: var(--c-grape);       --tone-rgb: var(--c-grape-rgb);       --tone-ink: var(--c-grape-ink); }
.tone-cycle > :nth-child(7n+4) { --tone: var(--c-mint);        --tone-rgb: var(--c-mint-rgb);        --tone-ink: var(--c-mint-ink); }
.tone-cycle > :nth-child(7n+5) { --tone: var(--c-cinnabar);    --tone-rgb: var(--c-cinnabar-rgb);    --tone-ink: var(--c-cinnabar-ink); }
.tone-cycle > :nth-child(7n+6) { --tone: var(--c-gold);        --tone-rgb: var(--c-gold-rgb);        --tone-ink: var(--c-gold-ink); }
.tone-cycle > :nth-child(7n+7) { --tone: var(--c-amber-brown); --tone-rgb: var(--c-amber-brown-rgb); --tone-ink: var(--c-amber-brown-ink); }
/* example component use: */
/* .badge { background: rgba(var(--tone-rgb),0.10); border: 1.5px solid rgba(var(--tone-rgb),0.30); color: var(--tone-ink); } */
```

## Charts

Series colours in cycle order, for any charting library:

```js
const NICE_SERIES = ['#0D98BA', '#FF8C00', '#6F2DA8', '#00AB78', '#E34234', '#FFD700', '#A6674C'];
const NICE_OTHER  = '#999B9B';   // "Other", baseline, comparison series
const NICE_STATUS = { success: '#00AB78', warning: '#FF8C00', error: '#E34234', info: '#0D98BA', neutral: '#999B9B' };
const NICE_TEXT   = { title: '#0E2025', label: '#3A5C64', axis: '#6C8B93', grid: 'rgba(14,32,37,0.08)' };
```

- For a single series, use blue-green alone. Don't rainbow one series's bars.
- Sequential scales (heatmaps, choropleths) run from `--bg` `#E2F3F7` to blue-green `#0D98BA` to `#0A748D`. Diverging scales run cinnabar → `#F0F9FB` → blue-green.
- Gold as a thin line is hard to see; use it for bars, areas or large markers, or move it later in the order.
- If a dataviz skill is also in use, follow its method (form, marks, interaction) but use these colours instead of its placeholder palette.

## Dark surfaces

For dark sections, dark slides or a dark mode: background `--ink` `#0E2025`; text `#FFFFFF` at 100% / 70% / 50% opacity for primary / secondary / meta; base accent `--accent-light` `#62BCD2`; side colours as fills; borders `rgba(255,255,255,0.10)`.

## Galaxy and Natural

These two palettes are each a base colour plus three side colours of their own. Everything in The palette, Rules, Charts and Dark surfaces still applies, with these changes.

**Galaxy**, a dark slate-blue base with warm accents.

| Token | Hex | | Token | Hex |
|---|---|---|---|---|
| `--accent` | `#283A45` | | `--bg` | `#E6E9EB` |
| `--accent-mid` (base) | `#324856` | | `--bg-alt` | `#DADEE1` |
| `--accent-light` | `#7A8891` | | `--surface` | `#F3F4F5` |
| `--ink` / `--text-1` | `#131B20` | | `--text-2` / `--text-3` | `#3A5464` / `#6C8493` |

| Name | Fill | RGB | -ink (text) |
|---|---|---|---|
| Sage | `#4A746A` | 74,116,106 | `#466E65` |
| Ochre | `#D18237` | 209,130,55 | `#925B26` |
| Terracotta | `#D66C44` | 214,108,68 | `#9D4F32` |

**Natural**, a soft gray-blue base with earthy accents.

| Token | Hex | | Token | Hex |
|---|---|---|---|---|
| `--accent` | `#56696F` | | `--bg` | `#EDF0F1` |
| `--accent-mid` (base) | `#6C838B` | | `--bg-alt` | `#E5E9EA` |
| `--accent-light` | `#9FAEB4` | | `--surface` | `#F6F8F8` |
| `--ink` / `--text-1` | `#161B1D` | | `--text-2` / `--text-3` | `#455459` / `#6F8790` |

| Name | Fill | RGB | -ink (text) |
|---|---|---|---|
| Copper | `#BB7748` | 187,119,72 | `#915C38` |
| Mauve | `#9E6D70` | 158,109,112 | `#875D60` |
| Taupe | `#7F726A` | 127,114,106 | `#736760` |

Changes from blue-green:

- **Cycle order** is the base, then the three side colours in the order listed: galaxy is slate → sage → ochre → terracotta; natural is gray-blue → copper → mauve → taupe. Metallic gray `#999B9B` is still "other".
- **Status meanings:**

  | Status | Galaxy | Natural |
  |---|---|---|
  | success / done | sage `#4A746A` | mint `#00AB78` (status only) |
  | warning / in progress | ochre `#D18237` | copper `#BB7748` |
  | error / failed | cinnabar `#E34234` (status only) | cinnabar `#E34234` (status only) |
  | info / active | base | base |
  | inactive / neutral | metallic gray | metallic gray |

  "Status only" colours come from the blue-green set and appear only on status marks, never as decoration. In galaxy, don't put terracotta next to error marks, because the two reds look alike. In natural, taupe is close to metallic gray, so give "other" items a lighter gray tint or leave taupe out of that view.
- **Charts:** galaxy `['#324856', '#4A746A', '#D18237', '#D66C44']`, natural `['#6C838B', '#BB7748', '#9E6D70', '#7F726A']`. Sequential scales run from the palette's `--bg` to its base to its `--accent`.
- **Dark surfaces:** background is the palette's `--ink`, base accent is its `--accent-light`. The galaxy base is itself dark, so dark sections can also use `--accent-mid` `#324856` as their background.
- **Drop-in CSS:** run the script below with `galaxy` or `natural`. It prints the `:root` tokens, the `.tone-*` classes and a four-step `.tone-cycle` to paste in place of the blue-green block.

## Other base colours and the palette script

The script prints the tokens for any palette name or hex. For a name in `PALETTES` (galaxy, natural) it also prints that palette's side colours, `.tone-*` classes, `.tone-cycle` and chart series. For any other base colour (a hex or a preset name: `blue-green` #0D98BA, `steel-blue` #4682B4, `teal` #2A9D8F, `plum` #9A4A9A, `amber` #C27530), keep the blue-green side colours and replace only the base tokens. If the new base is close to a side colour, drop that side colour from the cycle.

```python
import colorsys, sys
PRESETS = {'steel-blue': '#4682B4', 'blue-green': '#0D98BA', 'teal': '#2A9D8F', 'plum': '#9A4A9A', 'amber': '#C27530'}
# Full palettes: a base colour plus their own side colours, in cycle order.
PALETTES = {
    'galaxy':  ('#324856', [('sage', '#4A746A'), ('ochre', '#D18237'), ('terracotta', '#D66C44')]),
    'natural': ('#6C838B', [('copper', '#BB7748'), ('mauve', '#9E6D70'), ('taupe', '#7F726A')]),
}
def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def hx(c): return '#%02X%02X%02X' % tuple(round(max(0, min(255, v))) for v in c)
def mix(a, b, t): return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))
def hsl(h, s, l): return tuple(v * 255 for v in colorsys.hls_to_rgb(h, l, s))
def lum(c):
    f = lambda v: (v / 255) / 12.92 if v / 255 <= 0.03928 else ((v / 255 + 0.055) / 1.055) ** 2.4
    r, g, b = map(f, c); return 0.2126 * r + 0.7152 * g + 0.0722 * b
def contrast(a, b): la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)
def base_hex(name): n = name.lower(); return PALETTES[n][0] if n in PALETTES else PRESETS.get(n, name)
def sides(name, bg):
    out = []
    for n, h in PALETTES.get(name.lower(), (None, []))[1]:
        ink = rgb(h)
        while contrast(ink, bg) < 4.5: ink = tuple(v * 0.95 for v in ink)  # readable text on bg
        out.append((n, h, ','.join(map(str, rgb(h))), hx(ink)))
    return out
def palette(base):
    base = rgb(base_hex(base))
    H, L, S = colorsys.rgb_to_hls(*(v / 255 for v in base))
    W = (255, 255, 255)
    bg = mix(W, base, 0.12)
    accent = tuple(v * 0.8 for v in base)
    while contrast(accent, bg) < 4.5: accent = tuple(v * 0.95 for v in accent)  # readable text on bg
    ink = hsl(H, min(S, 0.45), 0.10)
    t = {
        '--bg': hx(bg), '--bg-alt': hx(mix(W, base, 0.18)), '--surface': hx(mix(W, base, 0.06)),
        '--accent': hx(accent), '--accent-mid': hx(base), '--accent-light': hx(mix(base, W, 0.35)),
        '--ink': hx(ink), '--text-1': hx(ink),
        '--text-2': hx(hsl(H, min(S, 0.26), 0.31)), '--text-3': hx(hsl(H, min(S, 0.15), 0.50)),
        '--letterbox': hx(mix(W, base, 0.25)),
    }
    for k, src in (('--accent-rgb', '--accent'), ('--mid-rgb', '--accent-mid'), ('--light-rgb', '--accent-light'), ('--ink-rgb', '--ink')):
        t[k] = ','.join(map(str, rgb(t[src])))
    shell = hx(mix(W, hsl(H, min(S, 0.2), 0.6), 0.55))
    return t, shell
if __name__ == '__main__':
    name = sys.argv[1] if len(sys.argv) > 1 else 'blue-green'
    t, shell = palette(name)
    for k, v in t.items(): print(f'  {k}: {v};')
    print(f'  --shell: {shell};')
    sd = sides(name, rgb(t['--bg']))
    if sd:
        for n, h, r, ink in sd: print(f'  --c-{n}: {h}; --c-{n}-rgb: {r}; --c-{n}-ink: {ink};')
        tones = [('base', 'var(--accent-mid)', 'var(--mid-rgb)', 'var(--accent)')]
        tones += [(n, f'var(--c-{n})', f'var(--c-{n}-rgb)', f'var(--c-{n}-ink)') for n, *_ in sd]
        print()
        for n, a, b, c in tones: print(f'.tone-{n} {{ --tone: {a}; --tone-rgb: {b}; --tone-ink: {c}; }}')
        for i, (n, a, b, c) in enumerate(tones, 1):
            print(f'.tone-cycle > :nth-child({len(tones)}n+{i}) {{ --tone: {a}; --tone-rgb: {b}; --tone-ink: {c}; }}')
        print()
        print('const NICE_SERIES = ' + repr([t['--accent-mid']] + [h for _, h, *_ in sd]) + ';')
```

Run it as `python3 palette.py galaxy`, `python3 palette.py natural`, `python3 palette.py steel-blue` or `python3 palette.py "#4682B4"`, after saving the block above as `palette.py`. Paste the `--` lines over the matching lines in `:root` (ignore `--letterbox` and `--shell` outside slide decks). `.tone-gray` and the `--c-gray` tokens stay as they are in every palette.

Side-colour -ink shades were computed for at least 4.5:1 contrast on each palette's own `--bg`. With a much darker or warmer background, check them again.