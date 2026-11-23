import colorsys, sys
PRESETS = {'steel-blue': '#4682B4', 'blue-green': '#0D98BA', 'teal': '#2A9D8F', 'plum': '#9A4A9A', 'amber': '#C27530'}
# Full nice-palette palettes: a base colour plus three side colours that fill the
# orange / grape / mint slots. Orange stays "warning" and mint stays "success".
# Any other name or hex gets the blue-green side colours (BASE_SIDES).
BASE_SIDES = {'orange': ('#FF8C00', '#9B5500'), 'grape': ('#6F2DA8', '#6F2DA8'), 'mint': ('#00AB78', '#007653')}
PALETTES = {
    'galaxy':  ('#324856', {'orange': '#D18237', 'grape': '#D66C44', 'mint': '#4A746A'}),
    'natural': ('#6C838B', {'orange': '#BB7748', 'grape': '#9E6D70', 'mint': '#7F726A'}),
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
def slots(name, bg):
    out = []
    if name.lower() not in PALETTES:
        for slot, (h, ink) in BASE_SIDES.items():
            out.append(f'  --c-{slot}: {h}; --c-{slot}-rgb: {",".join(map(str, rgb(h)))}; --c-{slot}-ink: {ink};')
        return out
    for slot, h in PALETTES[name.lower()][1].items():
        ink = rgb(h)
        while contrast(ink, bg) < 4.5: ink = tuple(v * 0.95 for v in ink)  # readable text on bg
        out.append(f'  --c-{slot}: {h}; --c-{slot}-rgb: {",".join(map(str, rgb(h)))}; --c-{slot}-ink: {hx(ink)};')
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
    # Dark blocks (bands, table headers, quotes, banners) use a soft gray, not near-black ink
    dark = hsl(H, min(S, 0.10), 0.33)
    on_dark = rgb(t['--accent-light'])
    while contrast(on_dark, dark) < 4.5: on_dark = mix(on_dark, W, 0.08)  # accent text readable on gray
    t['--dark'] = hx(dark); t['--on-dark'] = hx(on_dark)
    for k, src in (('--accent-rgb', '--accent'), ('--mid-rgb', '--accent-mid'), ('--light-rgb', '--accent-light'), ('--ink-rgb', '--ink'), ('--dark-rgb', '--dark')):
        t[k] = ','.join(map(str, rgb(t[src])))
    shell = hx(mix(W, hsl(H, min(S, 0.2), 0.6), 0.55))
    return t, shell
if __name__ == '__main__':
    name = sys.argv[1] if len(sys.argv) > 1 else 'galaxy'
    t, shell = palette(name)
    for k, v in t.items(): print(f'  {k}: {v};')
    print(f'  --shell: {shell};')
    for line in slots(name, rgb(t['--bg'])): print(line)
