---
name: "nice-presentation"
description: "Create calm, editorial HTML slide decks: galaxy palette by default (slate base with ochre, terracotta and sage side colours), Playfair Display titles and big numbers, DM Sans body, soft tinted tiles, 16:9 stage. Optional argument: base colour hex or palette name (galaxy, blue-green, steel-blue, natural, ...)."
---

# Nice Presentation

Generates single-file, zero-dependency HTML presentations that all share one design system: paper tinted with the base colour (galaxy paper `#F5F7F8`, slate base `#324856` by default), **Playfair Display 700** for slide titles and big numbers, **DM Sans** for body text, DM Mono only for code, a base-colour field on the title and section slides, a faint noise texture, and slow "silk" easing (`cubic-bezier(0.16,1,0.3,1)`).

The look is a quiet **tile-and-table** build, translated from the approved document style to 16:9:

- **Blocks** (cards, panels, stat tiles, notes, callouts, quote boxes, info boxes) are plain soft tinted tiles with round corners (8px at the stage size) and no borders. There is never a thick or coloured line on the top, left or any other edge, no short coloured bar above a title and no left-border callout. A block's tone shows only as a light tint of its colour (8 to 14% over the paper, `--tint` and `--tint-strong`) and the block title in the tone's `-ink` colour. Icon circles may stay beside text, but never as decoration-only tiles above every heading.
- **Tables** have a thin 1px frame in the `--rule` colour with round corners, a light-grey header row (base colour at 7%) with secondary-ink header text (weight 600, sentence case, one step smaller than body), thin 1px row lines, no dark header, no thick rule under the header and no zebra stripes. A highlighted row (`tr.hl`) is a light tint of the orange slot.
- **Labels** (captions, table heads, tags, kickers) are sentence case, untracked and one step smaller than body; there are no spaced capitals anywhere. There is no eyebrow or kicker line above a heading: fold its words into the heading or put them in a line below it. No middle-dot-joined meta strings with two or more dots. A heading is one style: never one italic word inside a roman heading.
- **Type**: Playfair Display 700 for titles and big numbers (lining, tabular numerals), DM Sans for body, DM Mono only for code. Section and agenda numbers are large Playfair numerals in the accent-ink colour (galaxy ochre ink `#925B26`), hanging to the left of the title under a thin 1px rule.
- **Title slide**: the whole slide is the base-colour field (`slide dark title-slide`), so the deck opens and closes on the same dark colour. Left about 6/12: Playfair title, one subtitle sentence, a small muted meta line (no dots). Right: the deck's one strongest real visual as soft tiles with a soft shadow (layered tiles allowed). Never draw browser or OS window chrome (three dots, a title bar) around a visual.
- **Section dividers**: the whole slide is the base colour; the Playfair title sits on the left (about 7/12); on the right one short line in light text and a small muted range line such as "Slides 5 to 11"; title and short line share a baseline.
- **Colour**: paper is a tinted off-white (`--paper`), never pure white or black outside the `:root` token block; every colour and font family goes through a `:root` token. The accent hue (orange slot) is used sparingly. Every repeated item still takes its own side colour as a tint, so slides stay colourful without edges or bars.
- **Scale**: the whole design is drawn at 85% of the earlier size (`--zoom` 1.0625, `--zoom-tall` 0.918, padding tokens 109/128/102px). If a slide looks empty, enlarge the visual (chart, tiles, window) rather than the text.
- **Craft**: every interactive control has a `:focus-visible` style; never `transition: all`; animate only `transform` and `opacity` (colour fades are fine); every animation has a `prefers-reduced-motion` fallback.

There is **no style-discovery phase**. The look is fixed; your job is content, structure, and choosing the right layout for each slide. Never swap in other fonts, gradients-on-white, neon, or "creative" alternatives. The only allowed variations are the base colour, set by the palette argument (see Palette argument), and how the side colours are spread across items (see Colour system).

## Non-negotiables

1. **One self-contained HTML file.** Inline CSS + JS. Only external resource: the Google Fonts link. Images go in an `assets/` folder next to the file (or base64 if the user wants a single file).
2. **Fixed 1920×1080 stage**, scaled as a whole by JS. Never reflow content per device, never use media-query breakpoints for slide content. Author every size in px at 1920×1080. The Base CSS draws slide content at `--zoom` (1.0625×, which is 85% of the former 1.25×) so text, icons and tiles fill the page; the tall layouts (`.wave`, `.process`, `.tree`, `.quotes`, `.phones`) use `--zoom-tall` (0.918×) so they still fit the height. Keep both, and size deck-specific parts with them in mind (a 400px box shows as 425px).
3. **Copy the Base CSS and Controller JS below verbatim.** Only edit the `:root` tokens and add small slide-specific rules in a clearly marked `/* === DECK-SPECIFIC === */` block at the end of the `<style>`.
4. **Slide switching** uses `.active`/`.visible` (visibility + opacity). Never `display:none`.
5. **No overflow, no overlap, no scrolling.** Content must sit between y≈130 (below the deck nav) and y≈975 (above the progress dots). If it doesn't fit, split the slide.
6. **Chinese text uses a sans font only.** Set `<html lang>` to the deck language (`zh-Hant` for Traditional Chinese). The shell loads Noto Sans TC and `--font-cjk` puts it behind every font stack, so CJK glyphs are always sans. Never add a serif CJK font (Noto Serif TC, PMingLiU, Ming/Song styles). In CJK decks titles use the sans CJK font instead of Playfair, and hero titles (cover, section divider, thank-you) render at 0.74× size because full-width glyphs look bigger.
7. Never put workflow text on slides ("template", "layout", "option A" as a design label, file names).

## Workflow

### Phase 0 — Mode
- **A. New deck** → Phase 1.
- **B. Convert PPTX** → extract text, notes and images with `python-pptx` (if the pptx skill is available, use its extraction approach), show the user a slide-by-slide summary, then Phase 2 with that content.
- **C. Restyle/enhance an existing HTML deck** → read it, map each slide to the closest layout in the catalog, regenerate in this system. Keep every piece of content and speaker note.

### Phase 1 — Content discovery
Ask these together in one question round (use the structured-question UI if available):
1. **Purpose** — Pitch / Teaching / Conference talk / Internal review
2. **Length** — Short 5–10 / Medium 10–20 / Long 20+
3. **Content** — All content ready / Rough notes / Topic only
4. **Density** — *Speaker-led* (big ideas, 1–3 points per slide) / *Reading-first* (self-contained, up to 6 bullets or 4–6 cards)
5. **Brand** (optional) — deck short name for the top-left logo, base colour (skip if a palette argument was given; default galaxy, slate `#324856`), logo image if any.

Skip questions the user already answered. If the user gave content up front and is clearly in a hurry, assume Medium + Speaker-led and say so.

### Phase 2 — Outline
Map the content to layouts from the catalog. A good default arc:
Title (asymmetric split with a base-colour field) → Agenda → [Section divider (full base colour) → Feature / Points / Stats / Chart / Diagram / Cards …]×N → Statement → Table/Timeline → Q&A → Closing CTA → Thank-you (dark).
Rules: alternate `slide` and `slide alt` backgrounds so neighbours differ (light slides carry a very faint soft shape pattern, mirrored on `.alt`); use a section divider (`slide dark section`) every 4–6 slides in long decks; make the title slide a `.title-slide` (paper left, `.ts-field` right), the thank-you slide `slide dark` and add one CTA box; use the featured solid card only for the recommended item. For decks over ~12 slides, show the outline (one line per slide: layout + headline) and get a quick OK before generating.

### Phase 3 — Generate
If a palette argument (or a colour from Phase 1) was given, generate the tokens first (see Palette argument) and replace the matching lines in the Base CSS `:root`; otherwise keep the galaxy default.

Assemble: `Document shell (head)` → Base CSS → (deck-specific CSS) → `Document shell (body start)` → slides → `Document shell (end)` with the Controller JS.

Writing rules for this style:
- Headlines are one style: no `<em>` phrase, no italic word, no colour change inside a heading. Say the point in plain words (a sentence or fragment, sentence case).
- A heading may be followed by a `.label` or `.kicker` line below it (1–3 words, sentence case, untracked, for example the topic or chapter name); never put one above the heading. Fold a would-be eyebrow into the heading itself. Do not join meta strings with middle dots (write "Platform engineering, Q4 all-hands, November 2026" or use two lines). Agenda lists use `.checklist.two-col.agenda` so the numbers become large Playfair numerals; a section slide gets one `.section-num`.
- `data-section` on each `<section>` fills the pill in the top-right nav. Use short chapter names; reuse the same name for slides in one chapter.
- Add `reveal` + stagger classes `d1`…`d6` to elements in reading order. Containers like `.stats`, `.panel`, `.window` get one reveal, not every child.
- Numbers that should count up: `<span data-count="34">34</span>` (keep the real value as text so print/PDF is correct). Bars/progress fills: `style="--h:75%"` / `style="--w:72%"`.
- Speaker notes: `<div class="notes">…</div>` inside the slide (never displayed).
- Icons: inline SVG, stroke `currentColor`, `stroke-width 2–2.5` (Heroicons-outline style). The body-start shell has an icon sheet (`<svg class="sprite">` with `<symbol id="i-…">`); use one with `<svg class="ico" aria-hidden="true"><use href="#i-bolt"/></svg>` and add a `<symbol>` for any other icon you need. Put icons inside the circle holders (`.point-icon`, `.card-icon`, `.hbar-icon`, `.wstep-dot`, `.pnode-ring`, `.tnode-icon`, `.meter-knob`, `.lc-icon`), which size them. No emoji except the ✦ glyph used by the template and ✓ in checks.
- Infographic parts: give repeated items an icon that matches its meaning where it sits beside text (`.point-icon`, `.card-head`, `.tnode-icon`, chart keys); do not stack an icon tile above every heading. Keep each circle's text to a short sentence-case label (1–3 words) plus one short sentence; let the automatic colour cycle tint the items, and mark the current or recommended item (`.now`, `tr.hl`, `.card.featured`) rather than adding more colours.
- Density limits — Speaker-led: title + ≤3 checks or ≤3 cards; Reading-first: ≤6 checks (two-col), ≤6 table rows, ≤4 stats, ≤3 cards (or 4 small), ≤4 points, ≤7 bars, ≤4 donut segments, ≤4 meters, ≤4 lines of ≤8 points, 4–6 wave or process steps, 1 root + ≤4 tree nodes.
- Use `.figure` or `.window` (with `<img>`) for screenshots, `.phones` for mobile screenshots (`<img>` inside `.phone-screen`; 4–6 phones). Never reuse the same image on two slides.
- Replace the logo text (`deck-logo`) with the deck's short name; the `<span>` part takes the accent colour. For an image logo use `<img src="assets/logo.png" style="height:40px">`.

### Phase 4 — Verify (do not skip)
Render every slide in headless Chromium and look at the screenshots. Script (Python Playwright; uses system Chrome if Playwright's browser isn't installed):

```python
import asyncio, sys
from playwright.async_api import async_playwright
async def main(path, outdir):
    async with async_playwright() as p:
        try: b = await p.chromium.launch()
        except Exception: b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await b.new_page(viewport={'width':1920,'height':1080}); errs=[]
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file://' + path); await pg.wait_for_timeout(800)
        n = await pg.evaluate("document.querySelectorAll('.slide').length")
        for i in range(n):
            await pg.evaluate(f"location.hash='#{i+1}'"); await pg.wait_for_timeout(2200)
            bad = await pg.evaluate("""() => { const s=document.querySelector('.slide.active'), r0=s.getBoundingClientRect(), out=[];
              s.querySelectorAll('*').forEach(el => { if (el.closest('.orb,.ticker,.phones,.notes,.side-panel')) return; const r=el.getBoundingClientRect();
                if (r.width && (r.bottom-r0.top>1020 || r.right-r0.left>1880 || r.left-r0.left<40)) out.push(el.className); }); return out.slice(0,5); }""")
            await pg.screenshot(path=f'{outdir}/slide-{i+1:02d}.png'); print(i+1, bad or 'ok')
        print('JS errors:', errs); await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2]))
```

Fix anything flagged, then **look at the PNGs** (contact sheets of 4 help) for overlap, cramped text, orphaned single words in headlines, and empty-looking slides. Content should fill most of the area between the nav and the dots: if a slide shows a small cluster with wide empty margins, enlarge the visual (bigger chart, tiles, window or icon beside the text) rather than the text. Then grep the deck's CSS: no `border-top`/`border-left` of 2px or more, no `letter-spacing` next to `uppercase`, no `transition: all`, no `#fff`/`#000` literal outside `:root`, and no `<em>` inside a heading. Also load once at 390×844 to confirm the stage letterboxes rather than reflows.

### Phase 5 — Deliver
- Save as `<deck-name>.html` (+ `assets/`) in the user's folder if one is connected; otherwise send the file.
- Tell the user, briefly: slide count, and controls — **← → / Space / swipe / wheel** to navigate, **Home/End**, `#n` in the URL jumps to slide n, **F** fullscreen, **E** (or hover the top-left corner) to edit text in the browser, **Ctrl+S** downloads the edited copy. Colours live in `:root`.
- Offer a PDF. Export with Playwright (print CSS already lays out one slide per page):

```python
await pg.goto('file://' + path); await pg.wait_for_timeout(1500)
await pg.emulate_media(media='print')
await pg.pdf(path=out_pdf, width='1920px', height='1080px', print_background=True, prefer_css_page_size=True)
```

## Colour system
The colours come from the **nice-palette** skill, the user's default theme. The Base CSS below already contains its values. If nice-palette is available and its values differ (it was updated later), its colours win: copy its base and side-colour values over the matching `:root` tokens here.

Two layers of colour:
- **Base colour** (galaxy slate `#324856` by default) is the structure: the `--field` surfaces (title-slide field, section and dark slides, featured card, CTA box), buttons, navigation and links. Never put side colours on these.
- **Side colours** decorate repeated items. A deck uses **at most four colours in total: the base colour plus three side colours**, held in three slots named orange, grape and mint. In the default galaxy palette the slots hold Ochre `#D18237` (orange slot), Terracotta `#D66C44` (grape slot) and Sage `#4A746A` (mint slot); in blue-green they hold Dark Orange `#FF8C00`, Grape `#6F2DA8` and Mint `#00AB78`. nice-palette also defines gold and amber brown; this skill does not use them. Cinnabar `#E34234` is the one exception: it marks failed, negative or high-risk status only (`.pill.red`, `.bad`) and never decorates items. Neutrals (white, `--ink`, the text grays and Metallic Gray `#999B9B` for inactive items) do not count as colours. Each side colour has a `-ink` shade that is readable as text on the light backgrounds. Components use the exact colour for fills and the `-ink` shade for text.

How items get a colour:
- **Automatic.** Children of `.stats`, `.grid-2/3/4`, `.wave`, `.quotes`, `.checklist`, `.tags`, `.mini-stats`, `.fv-row`, `.ticker-track`, `.points`, `.hbars`, `.meters`, `.process`, `.tree-kids` and table rows (`.data > tbody`) cycle base → orange → grape → mint, then repeat. This colours stat blocks, card columns and icon circles, check circles, point and timeline circles, bars, meters, process rings, tree nodes, table row dots, quote marks and avatars, highlighted tags, mini-stat tints and progress fills. Every item shows its colour as a light tint of its tile and in its `-ink` title colour, never as an edge or bar. Donut segments and line series take an explicit `.tone-*` each, matching their callout or legend key.
- **Explicit.** Add `.tone-base`, `.tone-orange`, `.tone-grape`, `.tone-mint` or `.tone-gray` to any item to choose its colour. Use this when colour carries meaning, such as the same team always in grape across slides.
- **Single colour.** Add `.mono` to a slide to keep all its items in the base colour (for example a sober financial slide).
- **Semantic pills and table marks.** `.pill.green` (mint slot, done), `.pill.warn` (light orange slot, in progress or medium), `.pill.red` (cinnabar, failed or high risk), `.pill.grape`, `.pill.blue` (base), `.pill.dim` (gray). In tables, `.yes` is mint and `.bad` is cinnabar. Red for problems is the only colour allowed outside the four.
- **Extras.** `.card.tinted` uses the stronger tint. `.orb-d` is a soft orange glow that pairs with `.orb-a`. `.kicker` text is orange ink unless a tone is set. `.float-icon` is grape. Agenda and section numerals use the orange slot (`--c-orange-ink` on paper, `--c-orange` on the field).

Keep it calm: never more than four colours, base plus orange, grape and mint, on any slide or in the deck as a whole. The only exception is cinnabar red on failed or negative status marks. Don't add colours to body text or headlines.

## Palette argument
The skill takes one optional argument: a **base colour** or a **named palette**, either a hex code or a preset name. Examples: `/nice-presentation #0D98BA`, `/nice-presentation blue-green`, or in prose ("use blue-green #0D98BA"). With no argument, use the default galaxy palette that is already in the Base CSS.

Presets: `galaxy` #324856 (default, own side colours) · `natural` #6C838B (own side colours) · `blue-green` #0D98BA · `steel-blue` #4682B4 · `teal` #2A9D8F (original ClearWave) · `plum` #9A4A9A · `amber` #C27530. Any other hex is accepted.

The script always prints the three side-colour lines too (`--c-orange`, `--c-grape`, `--c-mint`); paste them over the same lines in `:root`. Galaxy and natural (from nice-palette) put their own colours in these slots. Every other preset or hex gets the blue-green side colours: dark orange `#FF8C00`, grape `#6F2DA8`, mint `#00AB78`. The class names stay the same, so `.tone-orange` simply shows the palette's colour in that slot:

| Slot (class) | Meaning | Galaxy | Natural |
|---|---|---|---|
| base | structure, info | slate `#324856` | gray-blue `#6C838B` |
| orange | warning, in progress | ochre `#D18237` | copper `#BB7748` |
| grape | decoration only | terracotta `#D66C44` | mauve `#9E6D70` |
| mint | success, done | sage `#4A746A` | taupe `#7F726A` |

Cinnabar red stays for failed status only. In galaxy, terracotta and red look alike, so avoid terracotta next to failed marks. In natural, taupe is close to metallic gray, so check that done and inactive marks still read as different.

The base colour becomes `--accent-mid`. Everything else is derived from it: a darker `--accent` checked for at least 4.5:1 contrast on the background (used for text and buttons), a lighter `--accent-light`, tinted backgrounds, the `--paper` off-white, the near-white tile surface `--surface-2`, the 1px `--rule` colour, the `--field` base-colour surface (the base darkened until paper text reads on it at 4.5:1), a near-black ink in the same hue, muted text colours, the letterbox colour and the phone frame (galaxy keeps the hand-set `--paper` `#F5F7F8` and `--rule` `#DCE1E4`). Never hand-pick these values. Run this script and paste its output over the same-named lines in `:root`:

```python
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
# Hand-set values for named palettes whose nice-palette design fixes them exactly
OVERRIDES = {'galaxy': {'--paper': '#F5F7F8', '--rule': '#DCE1E4'}}
def palette(name):
    base = rgb(base_hex(name))
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
        '--paper': hx(mix(W, base, 0.045)),          # slide paper: tinted off-white, never pure white
        '--surface-2': hx(mix(W, base, 0.015)),      # light tile surface
        '--rule': hx(mix(W, base, 0.165)),           # 1px frames and row lines
    }
    t.update(OVERRIDES.get(name.lower(), {}))
    field = base                                       # base-colour field: light text must read on it
    while contrast(rgb(t['--paper']), field) < 4.5: field = tuple(v * 0.95 for v in field)
    t['--field'] = hx(field)
    for k, src in (('--accent-rgb', '--accent'), ('--mid-rgb', '--accent-mid'), ('--light-rgb', '--accent-light'), ('--ink-rgb', '--ink'), ('--paper-rgb', '--paper'), ('--field-rgb', '--field')):
        t[k] = ','.join(map(str, rgb(t[src])))
    shell = hx(mix(W, hsl(H, min(S, 0.2), 0.6), 0.55))
    return t, shell
if __name__ == '__main__':
    name = sys.argv[1] if len(sys.argv) > 1 else 'galaxy'
    t, shell = palette(name)
    for k, v in t.items(): print(f'  {k}: {v};')
    print(f'  --shell: {shell};')
    for line in slots(name, rgb(t['--bg'])): print(line)
```

Run it as `python3 palette.py blue-green`, `python3 palette.py galaxy` or `python3 palette.py "#0D98BA"`. For a hex or a base-only preset, the side colours are the blue-green ones. If the base colour is close to a side colour (for example a mint or plum base), give the clashing items an explicit `.tone-*` of another side colour so the deck shows only three distinct colours plus neutrals; never bring in a palette colour outside orange, grape and mint. For a very light or very dark base (yellow, near-black), check the Phase 4 screenshots for washed-out or muddy surfaces and tell the user if the colour doesn't suit this style. Mention the base colour or palette name used when delivering.

### Hand-tuned reference palettes
Older fixed values, kept for reference only. Prefer the generator above.

| Token | Teal (original ClearWave) | Plum | Amber |
|---|---|---|---|
| `--bg` / `--bg-alt` / `--surface` | `#E8F4F2` / `#DFF0EE` / `#F4FAFA` | `#F3ECF4` / `#EBE0EE` / `#FAF6FB` | `#F6F0E6` / `#EFE6D6` / `#FBF8F2` |
| `--accent` / `--accent-rgb` | `#1A7A6E` / `26,122,110` | `#7A2F7A` / `122,47,122` | `#A0581A` / `160,88,26` |
| `--accent-mid` / `--mid-rgb` | `#2A9D8F` / `42,157,143` | `#9A4A9A` / `154,74,154` | `#C27530` / `194,117,48` |
| `--accent-light` / `--light-rgb` | `#5BBFB5` / `91,191,181` | `#C487C4` / `196,135,196` | `#E0A867` / `224,168,103` |
| `--ink` = `--text-1` / `--ink-rgb` | `#0D1E1C` / `13,30,28` | `#1E0D1E` / `30,13,30` | `#1E140A` / `30,20,10` |
| `--text-2` / `--text-3` | `#3A5C58` / `#6B8C88` | `#5A3A58` / `#8C6B8A` | `#5C4A3A` / `#8C7A68` |
| `--letterbox` | `#CFE4E0` | `#E4D6E7` | `#E9DDC8` |

A brand colour is just a palette argument: pass its hex to the generator.

## Layout catalog
Class reference (all defined in the Base CSS):
- **Structure**: `.slide` (`.alt` slightly deeper paper with the faint pattern mirrored, `.dark` base-colour field bg with no pattern, `.center` centred; on dark slides the badge, `.window`, mini-stats and `.float` turn to soft translucent tiles), `.slide.dark.title-slide` (the whole slide dark; children `.ts-field` = right-hand area holding a `.visual`, and `.ts-left` = title, `.lead`, `.ts-meta`), `.slide.dark.section` (child `.section-grid` > `.section-num`, `.title.hero`, `.section-line`, `.section-range`), `.head` (+`.center`) wrapper for title/label/lead, `.split` 2-col (`.wide-left`, `.reverse`), `.grid-2/3/4`, `.row`, decorative `.orb .orb-a|b|c|d` (first children of the slide), tones `.tone-*` and `.mono` (see Colour system).
- **Type**: `.label` and `.kicker` (a sentence-case line below the title, never above), `.title` (`.hero` bigger; Playfair 700), `.h3`, `.lead`, `.body`, `.statement`, `em` (plain emphasis in body text only, never inside a heading). `.points` > `.point` (`.point-icon`, `.point-k`, `.point-d`) for an icon list.
- **Panels**: `.side-panel` (first child of the slide: tinted block over the right 44%, holds `.panel-text`, `.panel-cta`, `.panel-sub`; the next element is the left content), `.note-band` (`.note-band-k` + `.note-band-d`), `.panel` (feature panel, see Visuals).
- **Hero bits**: `.badge` (+`.badge-dot`), `.trust` > `.trust-item` + `.trust-divider`, `.btn .btn-primary|.btn-outline|.btn-ghost-dark`.
- **Visuals**: `.window` (a plain soft tile: `.window-body`, or a direct `<img>`; no window bar or dots), `.bars` > `.bar[.on]` with `--h`, `.mini-stats`, `.visual` + `.float` / `.float.solid` floating tiles (keep them inside their own field, never across a split), `.panel` > `.fv-row` / `.fv-card[.wide]` / `.fv-track > .fv-fill` / `.fv-list > .fv-item` + `.pill .green|.blue|.dim|.warn|.red|.grape`, `.figure` + `.caption`.
- **Content**: `.checklist[.two-col][.agenda]` > `.check` (`.check-icon` ✓ or 01…; `.agenda` turns the numbers into large Playfair numerals under a 1px rule), `.stats[.three]` > `.stat`, `.card[.featured|.tinted]` (`.card-flag`, `.card-tier`, `.card-big`, `.card-title`, `.card-desc`, `.card-head` > `.card-icon` + `.card-title` (icon beside the title), `.card-divider`), `.quotes` > `.quote[.tall]`, `.tags` > `.tag-pill[.hl]`, `.ticker` (items listed twice for a seamless loop), `.faq` > `.faq-item[.open]` (`button.faq-q`), `.phones` + `.phones-ctl`, `.cta-box` + `.cta-actions`, `.contact`.
- **Tables**: `.table-wrap > table.data` (`tr.hl`, `.num`, `.yes`, `.no`, `.bad`). The first column is the row label and gets a coloured dot.
- **Charts**: `.chart-k` sentence-case caption (commas, not middle dots, between its parts), then `.hbars` > `.hbar` (`style="--v:72%"`; `.hbar-icon`, `.hbar-label`, `.hbar-track > .hbar-fill`, `.hbar-val`) · `.donut-chart` = `.donut-side` + `.donut` (SVG with `.dn-track` and one `.dn-seg.tone-*` per segment, `pathLength="100"`, `style="--p:58;--o:0"` = length and start in %, + `.donut-center` > `.dc-big` + `.dc-cap`) + `.donut-side.right`; each side holds `.dc` (`.dc-head` > `.dc-k` + `.dc-v`, `.dc-d`) · `.meters` > `.meter` (`style="--v:72%"`; `.meter-val`, `.meter-track > .meter-fill > .meter-knob`, `.meter-k`, `.meter-d`) · `.line-chart` = `.lc-plot` + `.lc-legend`. The plot holds `.lc-y` (axis numbers, top to bottom), `.lc-area` and `.lc-x` (labels with `style="--x:40%"`). `.lc-area` holds one SVG (`viewBox="0 0 100 100" preserveAspectRatio="none"`) with a `g.lc-series.tone-*` per line: `.lc-fill` (area under the line, closed to y=100), `.lc-line`, and `.lc-pts` (`M x,y h0` per point, drawn as round dots). Then one `.lc-end.tone-*` per line (`style="--x:100%;--y:16%"`) with the last value in `<b>`. Coordinates: x = 0–100 across, y = 100 − value ÷ axis max × 100. The legend holds `.lc-key.tone-*` (`.lc-icon`, `div` > `.lc-k` + `.lc-d`, `.lc-v`).
- **Diagrams**: `.process` (set `style="--n:5"`) > `.pnode` (`.pnode-text` > `.pnode-k` + `.pnode-d`, `.pnode-ring` = tinted disc with an icon) · `.tree` > `.tree-root > .tnode` + `.tree-kids` (set `style="--n:3"`) > `.tree-kid > .tnode` (`.tnode-icon` beside the text, `.tnode-k`, `.tnode-t`, `.tnode-d`).
- **Timelines**: `.wave` (set `style="--n:5"`) > `.wstep[.now|.later]` (`.wstep-text` > `.wstep-when` + `.wstep-t` + `.wstep-d`, `.wstep-dot` with an icon). Odd steps sit high with text above; even steps sit low with text below.

The full example deck below uses every layout. Copy the structure of the layout you need, **never the demo wording or numbers**.

### Example deck — every layout (slides go inside `<main class="deck-stage">`)

```html
  <!-- ================= 01 · TITLE (asymmetric split: text left, base-colour field right) ================= -->
  <section class="slide dark title-slide" data-section="Overview">
    <div class="ts-field">
      <div class="visual reveal d2">
        <div class="window">
          <div class="window-body">
            <div class="win-head"><div class="win-title">Cluster utilization</div><div class="tag">Live</div></div>
            <div class="bars">
              <div class="bar" style="--h:35%"></div><div class="bar" style="--h:55%"></div><div class="bar" style="--h:42%"></div><div class="bar on" style="--h:75%"></div>
              <div class="bar" style="--h:60%"></div><div class="bar on" style="--h:88%"></div><div class="bar" style="--h:70%"></div><div class="bar on" style="--h:92%"></div>
            </div>
            <div class="mini-stats">
              <div class="mini-stat"><div class="mini-val">94<small>%</small></div><div class="mini-label">GPU usage</div><div class="mini-chg">+12%</div></div>
              <div class="mini-stat"><div class="mini-val">2.4<small>k</small></div><div class="mini-label">Workloads</div><div class="mini-chg">+8%</div></div>
              <div class="mini-stat"><div class="mini-val">18<small>h</small></div><div class="mini-label">Saved per week</div><div class="mini-chg">+24%</div></div>
            </div>
          </div>
        </div>
        <div class="float" style="bottom:-30px;left:-34px"><div class="float-icon">✦</div><div class="float-text"><strong>Autoscaler on</strong><span>prod-east, just now</span></div></div>
        <div class="float solid" style="top:-26px;right:-8px"><div class="fv">↑ 34%</div><div class="fl">Throughput this quarter</div></div>
      </div>
    </div>
    <div class="ts-left">
      <h1 class="title hero reveal">Your platform,<br>finally clear.</h1>
      <p class="lead reveal d1">How Atlas unified twelve internal tools into one calm, observable surface, and what we ship next.</p>
      <p class="ts-meta reveal d2">Platform engineering, Q4 all-hands, November 2026</p>
    </div>
    <div class="notes">Open with the headline number; the dashboard is illustrative.</div>
  </section>

  <!-- ================= 02 · AGENDA (checklist two-col) ================= -->
  <section class="slide alt" data-section="Agenda">
    <div class="head">
      <h2 class="title reveal">What we’ll cover today</h2>
      <div class="label reveal d1">Agenda</div>
    </div>
    <div class="checklist two-col agenda">
      <div class="check reveal d2"><div class="check-icon">01</div><span><b>Where we started</b> — twelve tools, no single view</span></div>
      <div class="check reveal d3"><div class="check-icon">02</div><span><b>What we built</b> — the unified control plane</span></div>
      <div class="check reveal d3"><div class="check-icon">03</div><span><b>Results</b> — utilization, cost and uptime</span></div>
      <div class="check reveal d4"><div class="check-icon">04</div><span><b>Options</b> — three paths for 2027</span></div>
      <div class="check reveal d4"><div class="check-icon">05</div><span><b>Roadmap</b> — milestones and owners</span></div>
      <div class="check reveal d5"><div class="check-icon">06</div><span><b>Q&amp;A</b> — your questions, answered</span></div>
    </div>
  </section>

  <!-- ================= 03 · TEXT — POINTS + SIDE PANEL ================= -->
  <section class="slide" data-section="Agenda">
    <div class="side-panel reveal d2">
      <p class="panel-text">One platform team now runs what used to take <b>twelve tools</b>, four on-call rotas and a monthly finance export.</p>
      <div class="panel-cta">34% cheaper</div>
      <p class="panel-sub">than the 2025 baseline, at higher utilization</p>
    </div>
    <div>
      <h2 class="title reveal">Three things changed</h2>
      <div class="label reveal d1">Why it matters</div>
      <div class="points reveal d2" style="margin-top:52px">
        <div class="point"><div class="point-icon"><svg class="ico" aria-hidden="true"><use href="#i-eye"/></svg></div><div><div class="point-k">Visibility</div><p class="point-d">Every team sees its own cost and capacity, live.</p></div></div>
        <div class="point"><div class="point-icon"><svg class="ico" aria-hidden="true"><use href="#i-bolt"/></svg></div><div><div class="point-k">Speed</div><p class="point-d">New clusters arrive in minutes instead of days.</p></div></div>
        <div class="point"><div class="point-icon"><svg class="ico" aria-hidden="true"><use href="#i-shield"/></svg></div><div><div class="point-k">Safety</div><p class="point-d">Policy runs before anything reaches production.</p></div></div>
      </div>
    </div>
  </section>

  <!-- ================= 04 · SECTION DIVIDER (full base colour) ================= -->
  <section class="slide dark section" data-section="Chapter 1">
    <div class="section-grid">
      <div class="section-num reveal">01</div>
      <h2 class="title hero reveal d1">Built for clarity<br>at every scale</h2>
      <p class="section-line reveal d2">Every feature reduces friction and surfaces what matters.</p>
      <p class="section-range reveal d3">Slides 5 to 11</p>
    </div>
  </section>

  <!-- ================= 05 · FEATURE (content + panel) ================= -->
  <section class="slide" data-section="What we built">
    <div class="split">
      <div>
        <h2 class="title reveal">Every metric, one calm surface</h2>
        <div class="kicker reveal d1">Unified dashboard</div>
        <p class="lead reveal d2">Pull data from any source into a single composable view. Share live dashboards — no exports, no screenshots.</p>
        <div class="checklist">
          <div class="check reveal d3"><div class="check-icon">✓</div><span>Drag-and-drop widget builder</span></div>
          <div class="check reveal d4"><div class="check-icon">✓</div><span>Real-time sync across all sources</span></div>
          <div class="check reveal d5"><div class="check-icon">✓</div><span>Role-based sharing with fine permissions</span></div>
        </div>
      </div>
      <div class="panel reveal d2">
        <div class="fv-row">
          <div class="fv-card"><div class="fv-label">Monthly spend</div><div class="fv-val">$84.2k</div><div class="fv-track"><div class="fv-fill" style="--w:72%"></div></div></div>
          <div class="fv-card"><div class="fv-label">Active nodes</div><div class="fv-val">12,481</div><div class="fv-track"><div class="fv-fill" style="--w:88%"></div></div></div>
        </div>
        <div class="fv-card">
          <div class="fv-label">Recent activity</div>
          <div class="fv-list">
            <div class="fv-item"><span>Q3 capacity report synced</span><span class="pill green">Done</span></div>
            <div class="fv-item"><span>GPU pool rebalance</span><span class="pill blue">Active</span></div>
            <div class="fv-item"><span>Cost export to finance</span><span class="pill dim">Queued</span></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ================= 06 · FEATURE (reverse, with a screenshot tile) ================= -->
  <section class="slide alt" data-section="What we built">
    <div class="split reverse">
      <div>
        <h2 class="title reveal">Routines that run themselves</h2>
        <div class="kicker reveal d1">Smart automation</div>
        <p class="lead reveal d2">Describe the intent in plain language; Atlas proposes the flow and keeps an audit trail of every action.</p>
        <div class="checklist">
          <div class="check reveal d3"><div class="check-icon">✓</div><span>Natural-language flow builder</span></div>
          <div class="check reveal d4"><div class="check-icon">✓</div><span>500+ trigger templates</span></div>
        </div>
      </div>
      <div class="window reveal d2">
        <div class="window-body">
          <div class="win-head"><div class="win-title">Active automations</div><div class="tag">24 flows</div></div>
          <div class="fv-list">
            <div class="fv-item"><span>Weekly digest → Slack</span><span class="pill green">Running</span></div>
            <div class="fv-item"><span>Node drift → page on-call</span><span class="pill green">Running</span></div>
            <div class="fv-item"><span>Budget 80% → alert owner</span><span class="pill blue">Active</span></div>
            <div class="fv-item"><span>Snapshot sync → cold tier</span><span class="pill warn">Retrying</span></div>
            <div class="fv-item"><span>Report sync → Drive</span><span class="pill dim">Paused</span></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ================= 07 · STATS ================= -->
  <section class="slide" data-section="Results">
    <div class="head">
      <h2 class="title reveal">Twelve months, measured</h2>
      <div class="label reveal d1">Results</div>
    </div>
    <div class="stats reveal d2">
      <div class="stat"><div class="stat-value"><span data-count="50">50</span><span class="stat-suffix">k+</span></div><div class="stat-label">Workloads managed</div><div class="stat-sub">Across 14 clusters</div></div>
      <div class="stat"><div class="stat-value"><span data-count="34">34</span><span class="stat-suffix">%</span></div><div class="stat-label">Cost reduction</div><div class="stat-sub">Versus 2025 baseline</div></div>
      <div class="stat"><div class="stat-value"><span data-count="99.9">99.9</span><span class="stat-suffix">%</span></div><div class="stat-label">Uptime</div><div class="stat-sub">Monitored 24/7</div></div>
      <div class="stat"><div class="stat-value"><span data-count="18">18</span><span class="stat-suffix">h</span></div><div class="stat-label">Saved per team / week</div><div class="stat-sub">Self-reported survey</div></div>
    </div>
    <div class="note-band reveal d3"><div class="note-band-k">How we<br>measured</div><p class="note-band-d">Cost and uptime come from the billing export and status page for Nov 2025 – Oct 2026; time saved is the median answer from 212 engineers in the October platform survey.</p></div>
  </section>

  <!-- ================= 08 · CHART — HORIZONTAL BARS ================= -->
  <section class="slide alt" data-section="Results">
    <div class="head">
      <h2 class="title reveal">Search spends twice what anyone else does</h2>
      <div class="label reveal d1">Cost by team</div>
    </div>
    <div class="reveal d2">
      <div class="chart-k">Monthly GPU spend, US$ thousands, October 2026</div>
      <div class="hbars">
        <div class="hbar" style="--v:100%"><div class="hbar-icon"><svg class="ico" aria-hidden="true"><use href="#i-search"/></svg></div><span class="hbar-label">Search</span><div class="hbar-track"><div class="hbar-fill"></div></div><span class="hbar-val">26.1</span></div>
        <div class="hbar" style="--v:49%"><div class="hbar-icon"><svg class="ico" aria-hidden="true"><use href="#i-trend"/></svg></div><span class="hbar-label">Ads ranking</span><div class="hbar-track"><div class="hbar-fill"></div></div><span class="hbar-val">12.8</span></div>
        <div class="hbar" style="--v:41%"><div class="hbar-icon"><svg class="ico" aria-hidden="true"><use href="#i-eye"/></svg></div><span class="hbar-label">Vision</span><div class="hbar-track"><div class="hbar-fill"></div></div><span class="hbar-val">10.7</span></div>
        <div class="hbar" style="--v:34%"><div class="hbar-icon"><svg class="ico" aria-hidden="true"><use href="#i-chat"/></svg></div><span class="hbar-label">Speech</span><div class="hbar-track"><div class="hbar-fill"></div></div><span class="hbar-val">8.9</span></div>
        <div class="hbar" style="--v:22%"><div class="hbar-icon"><svg class="ico" aria-hidden="true"><use href="#i-chart"/></svg></div><span class="hbar-label">Forecasting</span><div class="hbar-track"><div class="hbar-fill"></div></div><span class="hbar-val">5.8</span></div>
      </div>
    </div>
  </section>

  <!-- ================= 09 · CHART — DONUT WITH CALLOUTS ================= -->
  <section class="slide" data-section="Results">
    <div class="head center" style="margin-bottom:40px">
      <h2 class="title reveal">Compute is most of the bill</h2>
      <div class="label reveal d1">Where the money goes</div>
    </div>
    <div class="donut-chart reveal d2">
      <div class="donut-side">
        <div class="dc tone-base"><div class="dc-head"><span class="dc-k">Compute</span><span class="dc-v">58%</span></div><p class="dc-d">GPU and CPU hours across both regions.</p></div>
        <div class="dc tone-orange"><div class="dc-head"><span class="dc-k">Storage</span><span class="dc-v">22%</span></div><p class="dc-d">Hot, warm and cold tiers.</p></div>
      </div>
      <div class="donut">
        <svg viewBox="0 0 200 200" aria-hidden="true"><circle class="dn-track" cx="100" cy="100" r="86"/><circle class="dn-seg tone-base" cx="100" cy="100" r="86" pathLength="100" style="--p:57.4;--o:0"/><circle class="dn-seg tone-orange" cx="100" cy="100" r="86" pathLength="100" style="--p:21.4;--o:58"/><circle class="dn-seg tone-grape" cx="100" cy="100" r="86" pathLength="100" style="--p:11.4;--o:80"/><circle class="dn-seg tone-mint" cx="100" cy="100" r="86" pathLength="100" style="--p:7.4;--o:92"/></svg>
        <div class="donut-center"><div class="dc-big">$84.2k</div><div class="dc-cap">per month</div></div>
      </div>
      <div class="donut-side right">
        <div class="dc tone-grape"><div class="dc-head"><span class="dc-k">Network</span><span class="dc-v">12%</span></div><p class="dc-d">Cross-region traffic and egress.</p></div>
        <div class="dc tone-mint"><div class="dc-head"><span class="dc-k">Licences</span><span class="dc-v">8%</span></div><p class="dc-d">Schedulers and monitoring.</p></div>
      </div>
    </div>
  </section>

  <!-- ================= 10 · CHART — METERS (comparison) ================= -->
  <section class="slide alt" data-section="Results">
    <div class="split" style="grid-template-columns:0.9fr 1.1fr">
      <div>
        <h2 class="title reveal">Most teams are already in</h2>
        <div class="label reveal d1">Adoption</div>
        <p class="lead reveal d2">Share of each group running production work on Atlas, October 2026.</p>
      </div>
      <div class="meters reveal d2">
        <div class="meter" style="--v:92%"><div class="meter-val">92%</div><div class="meter-track"><div class="meter-fill"><span class="meter-knob"><svg class="ico" aria-hidden="true"><use href="#i-server"/></svg></span></div></div><div class="meter-k">Platform</div><p class="meter-d">11 of 12 teams</p></div>
        <div class="meter" style="--v:72%"><div class="meter-val">72%</div><div class="meter-track"><div class="meter-fill"><span class="meter-knob"><svg class="ico" aria-hidden="true"><use href="#i-chart"/></svg></span></div></div><div class="meter-k">Research</div><p class="meter-d">18 of 25 teams</p></div>
        <div class="meter" style="--v:50%"><div class="meter-val">50%</div><div class="meter-track"><div class="meter-fill"><span class="meter-knob"><svg class="ico" aria-hidden="true"><use href="#i-users"/></svg></span></div></div><div class="meter-k">Product</div><p class="meter-d">7 of 14 teams</p></div>
      </div>
    </div>
  </section>

  <!-- ================= 11 · CHART — LINES OVER TIME ================= -->
  <section class="slide" data-section="Results">
    <div class="head">
      <h2 class="title reveal">Deploys tripled in six months</h2>
      <div class="label reveal d1">Delivery</div>
    </div>
    <div class="reveal d2">
      <div class="chart-k">Production deploys per week, May to October 2026</div>
      <div class="line-chart">
        <div class="lc-plot">
          <div class="lc-y"><span>150</span><span>100</span><span>50</span><span>0</span></div>
          <div class="lc-area">
            <svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
              <g class="lc-series tone-base"><path class="lc-fill" d="M0,73.33 L20,65.33 L40,54.67 L60,43.33 L80,30.67 L100,16 L100,100 L0,100 Z"/><path class="lc-line" d="M0,73.33 L20,65.33 L40,54.67 L60,43.33 L80,30.67 L100,16"/><path class="lc-pts" d="M0,73.33h0 M20,65.33h0 M40,54.67h0 M60,43.33h0 M80,30.67h0"/></g>
              <g class="lc-series tone-orange"><path class="lc-fill" d="M0,85.33 L20,82.67 L40,76.67 L60,68.67 L80,61.33 L100,52.67 L100,100 L0,100 Z"/><path class="lc-line" d="M0,85.33 L20,82.67 L40,76.67 L60,68.67 L80,61.33 L100,52.67"/><path class="lc-pts" d="M0,85.33h0 M20,82.67h0 M40,76.67h0 M60,68.67h0 M80,61.33h0"/></g>
              <g class="lc-series tone-grape"><path class="lc-fill" d="M0,92 L20,90 L40,88 L60,82.67 L80,78 L100,72.67 L100,100 L0,100 Z"/><path class="lc-line" d="M0,92 L20,90 L40,88 L60,82.67 L80,78 L100,72.67"/><path class="lc-pts" d="M0,92h0 M20,90h0 M40,88h0 M60,82.67h0 M80,78h0"/></g>
            </svg>
            <span class="lc-end tone-base" style="--x:100%;--y:16%"><b>126</b></span>
            <span class="lc-end tone-orange" style="--x:100%;--y:52.67%"><b>71</b></span>
            <span class="lc-end tone-grape" style="--x:100%;--y:72.67%"><b>41</b></span>
          </div>
          <div class="lc-x"><span style="--x:0%">May</span><span style="--x:20%">Jun</span><span style="--x:40%">Jul</span><span style="--x:60%">Aug</span><span style="--x:80%">Sep</span><span style="--x:100%">Oct</span></div>
        </div>
        <div class="lc-legend">
          <div class="lc-key tone-base"><div class="lc-icon"><svg class="ico" aria-hidden="true"><use href="#i-server"/></svg></div><div><div class="lc-k">Platform</div><p class="lc-d">+215% since May</p></div><span class="lc-v">126</span></div>
          <div class="lc-key tone-orange"><div class="lc-icon"><svg class="ico" aria-hidden="true"><use href="#i-chart"/></svg></div><div><div class="lc-k">Research</div><p class="lc-d">+223% since May</p></div><span class="lc-v">71</span></div>
          <div class="lc-key tone-grape"><div class="lc-icon"><svg class="ico" aria-hidden="true"><use href="#i-users"/></svg></div><div><div class="lc-k">Product</div><p class="lc-d">+242% since May</p></div><span class="lc-v">41</span></div>
        </div>
      </div>
    </div>
  </section>

  <!-- ================= 12 · CARDS (options, one featured) ================= -->
  <section class="slide alt" data-section="Options">
    <div class="head center">
      <h2 class="title reveal">Three paths, one recommendation</h2>
      <div class="label reveal d1">Options for 2027</div>
    </div>
    <div class="grid-3" style="align-items:stretch">
      <div class="card reveal d2">
        <div class="card-tier">Option A: hold</div>
        <div class="card-big">$1.2<small>M / yr</small></div>
        <p class="card-desc">Keep today’s footprint and focus on reliability work.</p>
        <div class="card-divider"></div>
        <div class="checklist"><div class="check"><div class="check-icon">✓</div><span>Lowest risk</span></div><div class="check"><div class="check-icon">✓</div><span>No new hiring</span></div><div class="check"><div class="check-icon">✓</div><span>Growth capped at 15%</span></div></div>
      </div>
      <div class="card featured reveal d3">
        <div class="card-flag">Recommended</div>
        <div class="card-tier">Option B: expand</div>
        <div class="card-big">$2.0<small>M / yr</small></div>
        <p class="card-desc">Add a second GPU region and self-service onboarding.</p>
        <div class="card-divider"></div>
        <div class="checklist"><div class="check"><div class="check-icon">✓</div><span>2× capacity by Q3</span></div><div class="check"><div class="check-icon">✓</div><span>Payback in 14 months</span></div><div class="check"><div class="check-icon">✓</div><span>Four new hires</span></div></div>
      </div>
      <div class="card reveal d4">
        <div class="card-tier">Option C: rebuild</div>
        <div class="card-big">$3.4<small>M / yr</small></div>
        <p class="card-desc">Re-platform onto a new scheduler and storage layer.</p>
        <div class="card-divider"></div>
        <div class="checklist"><div class="check"><div class="check-icon">✓</div><span>Biggest long-term upside</span></div><div class="check"><div class="check-icon">✓</div><span>18-month migration</span></div><div class="check"><div class="check-icon">✓</div><span>High delivery risk</span></div></div>
      </div>
    </div>
  </section>

  <!-- ================= 13 · ICON CARDS (pillars) ================= -->
  <section class="slide" data-section="Principles">
    <div class="head">
      <h2 class="title reveal">How we decide</h2>
      <div class="label reveal d1">Principles</div>
    </div>
    <div class="grid-3">
      <div class="card reveal d2"><div class="card-head"><div class="card-icon"><svg class="ico" aria-hidden="true"><use href="#i-shield"/></svg></div><div class="card-title">Safe by default</div></div><p class="card-desc">Every change is reversible, reviewed and observable before it reaches production.</p></div>
      <div class="card reveal d3"><div class="card-head"><div class="card-icon"><svg class="ico" aria-hidden="true"><use href="#i-bolt"/></svg></div><div class="card-title">Fast feedback</div></div><p class="card-desc">Teams see the cost and performance of a change within minutes, not at month-end.</p></div>
      <div class="card reveal d4"><div class="card-head"><div class="card-icon"><svg class="ico" aria-hidden="true"><use href="#i-layers"/></svg></div><div class="card-title">One layer</div></div><p class="card-desc">A single control plane over compute, storage and network — no parallel tooling.</p></div>
    </div>
  </section>

  <!-- ================= 14 · STATEMENT ================= -->
  <section class="slide alt center" data-section="Insight">
    <div class="orb orb-c"></div>
    <div class="center" style="display:flex;flex-direction:column">
      <p class="statement reveal d1">The bottleneck was never compute. It was knowing what we already had.</p>
      <div class="author statement-by reveal d2" style="justify-content:center"><div class="avatar">SW</div><div style="text-align:left"><div class="author-name">Platform team retro</div><div class="author-role">September 2026</div></div></div>
    </div>
  </section>

  <!-- ================= 15 · QUOTES ================= -->
  <section class="slide" data-section="Feedback">
    <div class="head">
      <h2 class="title reveal">Teams that love the change</h2>
      <div class="label reveal d1">What teams say</div>
    </div>
    <div class="quotes">
      <div class="quote tall reveal d2"><div class="quote-mark">“</div><p class="quote-text">We replaced three separate tools and actually have fewer meetings now. The automation handles the hand-offs we used to sort out every morning.</p><div class="author"><div class="avatar">SL</div><div><div class="author-name">Sarah Lin</div><div class="author-role">Head of Operations, Data</div></div></div></div>
      <div class="quote reveal d3"><div class="quote-mark">“</div><p class="quote-text">I can review capacity and approve changes between meetings.</p><div class="author"><div class="avatar">MR</div><div><div class="author-name">Marcus Reyes</div><div class="author-role">Product Director</div></div></div></div>
      <div class="quote reveal d4"><div class="quote-mark">“</div><p class="quote-text">Onboarding a 30-person team took one afternoon.</p><div class="author"><div class="avatar">PK</div><div><div class="author-name">Priya Kapoor</div><div class="author-role">Engineering Lead</div></div></div></div>
      <div class="quote reveal d4"><div class="quote-mark">“</div><p class="quote-text">We show stakeholders live data instead of preparing decks.</p><div class="author"><div class="avatar">TW</div><div><div class="author-name">Tom Wang</div><div class="author-role">Finance</div></div></div></div>
      <div class="quote reveal d5"><div class="quote-mark">“</div><p class="quote-text">Support answered an integration question in two hours.</p><div class="author"><div class="avatar">AN</div><div><div class="author-name">Aiko Nakamura</div><div class="author-role">CTO, Labs</div></div></div></div>
    </div>
  </section>

  <!-- ================= 16 · PHONE SHOWCASE ================= -->
  <section class="slide alt" data-section="Mobile">
    <div class="head center" style="margin-bottom:0">
      <h2 class="title reveal">Your cluster, in your pocket</h2>
      <div class="label reveal d1">Mobile app</div>
    </div>
    <div class="phones reveal d2">
      <div class="phone"><div class="phone-shell"><div class="phone-screen"><div class="mock"><div class="mock-h">Overview</div><div class="mock-card"><div class="mock-big">94%</div><div class="mock-line a"></div><div class="mock-line s"></div></div><div class="mock-card"><div class="mock-line s"></div><div class="mock-line"></div></div><div class="mock-nav"><i class="on"></i><i></i><i></i><i></i></div></div></div></div><div class="phone-cap">Overview</div></div>
      <div class="phone"><div class="phone-shell"><div class="phone-screen"><div class="mock"><div class="mock-h">Alerts</div><div class="mock-card"><div class="mock-line a"></div><div class="mock-line"></div></div><div class="mock-card"><div class="mock-line a"></div><div class="mock-line s"></div></div><div class="mock-card"><div class="mock-line"></div></div><div class="mock-nav"><i></i><i class="on"></i><i></i><i></i></div></div></div></div><div class="phone-cap">Alerts</div></div>
      <div class="phone"><div class="phone-shell"><div class="phone-screen"><div class="mock"><div class="mock-h">Capacity</div><div class="mock-card"><div class="mock-big">2.4k</div><div class="mock-line a"></div></div><div class="mock-card"><div class="mock-big">$84k</div><div class="mock-line s"></div></div><div class="mock-nav"><i></i><i></i><i class="on"></i><i></i></div></div></div></div><div class="phone-cap">Capacity</div></div>
      <div class="phone"><div class="phone-shell"><div class="phone-screen"><div class="mock"><div class="mock-h">Approvals</div><div class="mock-card"><div class="mock-line a"></div><div class="mock-line s"></div></div><div class="mock-card"><div class="mock-line a"></div><div class="mock-line"></div></div><div class="mock-nav"><i></i><i></i><i></i><i class="on"></i></div></div></div></div><div class="phone-cap">Approvals</div></div>
      <div class="phone"><div class="phone-shell"><div class="phone-screen"><div class="mock"><div class="mock-h">Settings</div><div class="mock-card"><div class="mock-line"></div><div class="mock-line s"></div></div><div class="mock-card"><div class="mock-line"></div></div><div class="mock-nav"><i></i><i></i><i></i><i></i></div></div></div></div><div class="phone-cap">Settings</div></div>
    </div>
    <div class="phones-ctl"><button class="round-btn" data-dir="prev" aria-label="Previous">‹</button><button class="round-btn" data-dir="next" aria-label="Next">›</button></div>
  </section>

  <!-- ================= 17 · TABLE ================= -->
  <section class="slide" data-section="Comparison">
    <div class="head">
      <h2 class="title reveal">Before and after Atlas</h2>
      <div class="label reveal d1">Comparison</div>
    </div>
    <div class="table-wrap reveal d2">
      <table class="data">
        <thead><tr><th>Capability</th><th>2025 tooling</th><th>Atlas</th><th class="num">Change</th></tr></thead>
        <tbody>
          <tr><td>Provisioning time</td><td>3 days</td><td>12 minutes</td><td class="num yes">−99%</td></tr>
          <tr class="hl"><td>GPU utilization</td><td>41%</td><td>78%</td><td class="num yes">+37 pts</td></tr>
          <tr><td>Cost visibility</td><td>Monthly, by finance</td><td>Live, per team</td><td class="num yes">✓</td></tr>
          <tr><td>Self-service onboarding</td><td class="no">—</td><td>Yes</td><td class="num yes">✓</td></tr>
          <tr><td>Tools to operate</td><td>12</td><td>1</td><td class="num yes">−11</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <!-- ================= 18 · TIMELINE ================= -->
  <section class="slide alt" data-section="Roadmap">
    <div class="head">
      <h2 class="title reveal">The next five quarters</h2>
      <div class="label reveal d1">Roadmap</div>
    </div>
    <div class="wave reveal d2" style="--n:5">
      <div class="wstep"><div class="wstep-text"><div class="wstep-when">Q4 2026</div><div class="wstep-t">Unify</div><p class="wstep-d">Retire the last three legacy dashboards.</p></div><div class="wstep-dot"><svg class="ico" aria-hidden="true"><use href="#i-layers"/></svg></div></div>
      <div class="wstep now"><div class="wstep-text"><div class="wstep-when">Q1 2027</div><div class="wstep-t">Expand</div><p class="wstep-d">Bring up the second GPU region.</p></div><div class="wstep-dot"><svg class="ico" aria-hidden="true"><use href="#i-globe"/></svg></div></div>
      <div class="wstep later"><div class="wstep-text"><div class="wstep-when">Q2 2027</div><div class="wstep-t">Self-serve</div><p class="wstep-d">Teams onboard without a ticket.</p></div><div class="wstep-dot"><svg class="ico" aria-hidden="true"><use href="#i-users"/></svg></div></div>
      <div class="wstep later"><div class="wstep-text"><div class="wstep-when">Q3 2027</div><div class="wstep-t">Optimize</div><p class="wstep-d">Predictive scaling on every cluster.</p></div><div class="wstep-dot"><svg class="ico" aria-hidden="true"><use href="#i-trend"/></svg></div></div>
      <div class="wstep later"><div class="wstep-text"><div class="wstep-when">Q4 2027</div><div class="wstep-t">Scale</div><p class="wstep-d">Open a third region for research.</p></div><div class="wstep-dot"><svg class="ico" aria-hidden="true"><use href="#i-flag"/></svg></div></div>
    </div>
  </section>

  <!-- ================= 19 · DIAGRAM — PROCESS RINGS ================= -->
  <section class="slide" data-section="How it works">
    <div class="head center" style="margin-bottom:48px">
      <h2 class="title reveal">From request to running job in five steps</h2>
      <div class="label reveal d1">Request path</div>
    </div>
    <div class="process reveal d2" style="--n:5">
      <div class="pnode"><div class="pnode-text"><div class="pnode-k">1. Request</div><p class="pnode-d">Ask for capacity in plain terms.</p></div><div class="pnode-ring"><svg class="ico" aria-hidden="true"><use href="#i-chat"/></svg></div></div>
      <div class="pnode"><div class="pnode-text"><div class="pnode-k">2. Check</div><p class="pnode-d">Quota, budget and security rules run.</p></div><div class="pnode-ring"><svg class="ico" aria-hidden="true"><use href="#i-shield"/></svg></div></div>
      <div class="pnode"><div class="pnode-text"><div class="pnode-k">3. Place</div><p class="pnode-d">Pick the cheapest region that fits.</p></div><div class="pnode-ring"><svg class="ico" aria-hidden="true"><use href="#i-globe"/></svg></div></div>
      <div class="pnode"><div class="pnode-text"><div class="pnode-k">4. Run</div><p class="pnode-d">The job starts with metrics wired in.</p></div><div class="pnode-ring"><svg class="ico" aria-hidden="true"><use href="#i-bolt"/></svg></div></div>
      <div class="pnode"><div class="pnode-text"><div class="pnode-k">5. Bill</div><p class="pnode-d">Cost lands on the team’s budget.</p></div><div class="pnode-ring"><svg class="ico" aria-hidden="true"><use href="#i-cash"/></svg></div></div>
    </div>
  </section>

  <!-- ================= 20 · DIAGRAM — TREE (org / architecture) ================= -->
  <section class="slide alt" data-section="How it works">
    <div class="head center" style="margin-bottom:76px">
      <h2 class="title reveal">One control plane over every layer</h2>
      <div class="label reveal d1">Architecture</div>
    </div>
    <div class="tree reveal d2">
      <div class="tree-root"><div class="tnode"><span class="tnode-icon"><svg class="ico" aria-hidden="true"><use href="#i-cube"/></svg></span><div class="tnode-k">Control</div><div class="tnode-t">Atlas control plane</div><p class="tnode-d">Policy, scheduling, cost tagging</p></div></div>
      <div class="tree-kids" style="--n:3">
        <div class="tree-kid"><div class="tnode"><span class="tnode-icon"><svg class="ico" aria-hidden="true"><use href="#i-server"/></svg></span><div class="tnode-k">Compute</div><div class="tnode-t">Kubernetes</div><p class="tnode-d">14 clusters in 2 regions</p></div></div>
        <div class="tree-kid"><div class="tnode"><span class="tnode-icon"><svg class="ico" aria-hidden="true"><use href="#i-database"/></svg></span><div class="tnode-k">Storage</div><div class="tnode-t">Ceph &amp; object store</div><p class="tnode-d">Hot, warm and cold tiers</p></div></div>
        <div class="tree-kid"><div class="tnode"><span class="tnode-icon"><svg class="ico" aria-hidden="true"><use href="#i-globe"/></svg></span><div class="tnode-k">Network</div><div class="tnode-t">Service mesh</div><p class="tnode-d">mTLS between every service</p></div></div>
      </div>
    </div>
  </section>

  <!-- ================= 21 · TAG CLOUD + TICKER ================= -->
  <section class="slide" data-section="Ecosystem">
    <div class="head center" style="margin-bottom:56px">
      <h2 class="title reveal">Connects with your existing stack</h2>
      <div class="label reveal d1">Integrations</div>
    </div>
    <div class="tags reveal d2">
      <span class="tag-pill hl">Kubernetes</span><span class="tag-pill">Prometheus</span><span class="tag-pill">Grafana</span><span class="tag-pill hl">NVIDIA DCGM</span>
      <span class="tag-pill">Slack</span><span class="tag-pill">GitHub</span><span class="tag-pill">Terraform</span><span class="tag-pill">ServiceNow</span>
      <span class="tag-pill">Jira</span><span class="tag-pill hl">Ceph</span><span class="tag-pill">Vault</span><span class="tag-pill">PagerDuty</span>
    </div>
    <div class="ticker reveal d3" style="margin-top:72px">
      <div class="ticker-label">Running in production at</div>
      <div class="ticker-track">
        <div class="ticker-item"><i></i>Nexaflow</div><div class="ticker-dot"></div><div class="ticker-item"><i></i>Meridian</div><div class="ticker-dot"></div><div class="ticker-item"><i></i>Vanta Labs</div><div class="ticker-dot"></div><div class="ticker-item"><i></i>Pulsar HQ</div><div class="ticker-dot"></div><div class="ticker-item"><i></i>Arclight</div><div class="ticker-dot"></div><div class="ticker-item"><i></i>Stratum IO</div><div class="ticker-dot"></div>
        <div class="ticker-item"><i></i>Nexaflow</div><div class="ticker-dot"></div><div class="ticker-item"><i></i>Meridian</div><div class="ticker-dot"></div><div class="ticker-item"><i></i>Vanta Labs</div><div class="ticker-dot"></div><div class="ticker-item"><i></i>Pulsar HQ</div><div class="ticker-dot"></div><div class="ticker-item"><i></i>Arclight</div><div class="ticker-dot"></div><div class="ticker-item"><i></i>Stratum IO</div><div class="ticker-dot"></div>
      </div>
    </div>
  </section>

  <!-- ================= 22 · FAQ ================= -->
  <section class="slide alt" data-section="Q&amp;A">
    <div class="faq">
      <div>
        <h2 class="title reveal">Questions,<br>answered</h2>
        <div class="label reveal d1">Q&amp;A</div>
        <p class="lead reveal d2">Click a question to open it. Anything else — ask now.</p>
      </div>
      <div class="reveal d2">
        <div class="faq-item open"><button class="faq-q" aria-expanded="true"><span>Does Option B need new headcount?</span><span class="faq-icon" aria-hidden="true">+</span></button><div class="faq-a"><div>Yes — four engineers, two of them in the new region. Hiring starts in January.</div></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false"><span>What happens to the legacy dashboards?</span><span class="faq-icon" aria-hidden="true">+</span></button><div class="faq-a"><div>They go read-only in December and are retired once the last owners migrate.</div></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false"><span>How is uptime measured?</span><span class="faq-icon" aria-hidden="true">+</span></button><div class="faq-a"><div>Synthetic probes every 30 seconds from three regions, published on the status page.</div></div></div>
        <div class="faq-item"><button class="faq-q" aria-expanded="false"><span>Can my team pilot self-service early?</span><span class="faq-icon" aria-hidden="true">+</span></button><div class="faq-a"><div>Yes — three pilot slots open in Q1. Ask in #atlas-pilot.</div></div></div>
      </div>
    </div>
  </section>

  <!-- ================= 23 · CLOSING (dark CTA box) ================= -->
  <section class="slide" data-section="Next steps">
    <div class="cta-box reveal">
      <div style="max-width:900px">
        <h2 class="title">Ready for a<br>clearer platform?</h2>
        <p class="lead">Decision needed: approve Option B today and we start the second region in January.</p>
      </div>
      <div class="cta-actions">
        <span class="btn btn-primary">Approve Option B <span>→</span></span>
        <span class="btn btn-ghost-dark">Schedule a deep-dive</span>
      </div>
    </div>
  </section>

  <!-- ================= 24 · THANK YOU (full dark) ================= -->
  <section class="slide dark center" data-section="">
    <div class="orb orb-a"></div><div class="orb orb-b"></div>
    <div class="center" style="display:flex;flex-direction:column">
      <h2 class="title hero reveal">Less noise,<br>more done.</h2>
      <div class="label reveal d1">Thank you</div>
      <div class="contact reveal d2" style="margin-top:56px;align-items:center"><span><b>Presenter Name</b>, Team</span><span>contact@example.com</span></div>
    </div>
  </section>
```

## Document shell (head)

Change `<title>`. Then the Base CSS goes inside `<style>`.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Atlas Platform Review</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Noto+Sans+TC:wght@400;500;700&family=DM+Mono:wght@400;500&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
<style>
```

## Base CSS (copy verbatim; edit only `:root`)

```css
/* ==========================================================
   NICE-PRESENTATION — ClearWave design system on a fixed
   1920×1080 stage. Edit :root tokens to re-theme the deck.
   ========================================================== */

/* === 1. TOKENS === */
:root {
  --bg:           #E6E9EB;
  --bg-alt:       #DADEE1;
  --surface:      #F3F4F5;
  --surface-2:    #FCFCFC;             /* light tile surface (never pure white) */
  --paper:        #F5F7F8;             /* slide paper: tinted off-white */
  --paper-rgb:    245,247,248;         /* = --paper as r,g,b */
  --on-field:     var(--paper);        /* text and marks on the base-colour field */
  --rule:         #DCE1E4;             /* 1px frames, table and row lines */
  --field:        #324856;             /* base-colour field: title-slide right side, section and dark slides */
  --field-rgb:    50,72,86;            /* = --field as r,g,b */
  --tint:         0.10;                /* tile tint over the paper (8 to 14%) */
  --tint-strong:  0.14;
  --accent:       #283A45;
  --accent-mid:   #324856;
  --accent-light: #7A8891;
  --accent-rgb:   40,58,69;          /* = --accent as r,g,b */
  --mid-rgb:      50,72,86;          /* = --accent-mid as r,g,b */
  --light-rgb:    122,136,145;          /* = --accent-light as r,g,b */
  --accent-ghost: rgba(var(--accent-rgb),0.08);
  --accent-border:rgba(var(--accent-rgb),0.15);
  --ink:          #131B20;             /* darkest text and shadow colour */
  --ink-rgb:      19,27,32;            /* = --ink as r,g,b */
  --text-1:       #131B20;
  --text-2:       #3A5464;
  --text-3:       #6C8493;
  --border:       rgba(var(--ink-rgb),0.08);
  --track:        rgba(var(--ink-rgb),0.08);   /* light gray rails, tracks and the timeline ribbon */
  --badge-shadow: 0 3px 10px rgba(var(--ink-rgb),0.10);   /* soft drop shadow under small floating marks */
  --shadow-sm:    0 2px 12px rgba(var(--ink-rgb),0.06);
  --shadow-md:    0 8px 28px rgba(var(--ink-rgb),0.09);
  --shadow-lg:    0 18px 48px rgba(var(--ink-rgb),0.14);   /* soft tile shadow */
  --silk:         cubic-bezier(0.16, 1, 0.3, 1);
  --silk-dur:     0.8s;
  --radius:       8px;
  --radius-lg:    8px;
  --font-cjk:     'Noto Sans TC', 'PingFang TC', 'Microsoft JhengHei', 'Noto Sans CJK TC', sans-serif;   /* Chinese text: always a sans font, never a serif (Ming) font */
  --font-sans:    'DM Sans', var(--font-cjk);
  --font-serif:   'Playfair Display', var(--font-cjk);   /* slide titles and big numbers (700); CJK glyphs fall through to the sans CJK font */
  --font-mono:    'DM Mono', ui-monospace, 'SFMono-Regular', Menlo, monospace;   /* code only */
  /* Type scale, authored at 1920×1080 */
  --fs-hero:      100px;
  --fs-title:     76px;
  --fs-h3:        52px;
  --fs-lead:      30px;
  --fs-body:      26px;
  --fs-small:     21px;
  --fs-label:     20px;
  --letterbox:    #CCD1D5;             /* color around the stage on non-16:9 screens */
  --shell:        #BCC9D2;             /* phone frame */
  /* Side colours: decorate repeated items. Exact colour for fills; -ink = darker shade readable as text on light bg */
  --c-mint:     #4A746A; --c-mint-rgb:     74,116,106;  --c-mint-ink:     #466E65;
  --c-orange:   #D18237; --c-orange-rgb:   209,130,55;  --c-orange-ink:   #925B26;
  /* status only: the one exception to the four-colour rule, for failed / negative marks */
  --c-cinnabar: #E34234; --c-cinnabar-rgb: 227,66,52; --c-cinnabar-ink: #BD372B;
  --c-gray:     #999B9B; --c-gray-rgb:     153,155,155; --c-gray-ink:    #656666;
  --c-grape:    #D66C44; --c-grape-rgb:    214,108,68; --c-grape-ink:    #9D4F32;
  --zoom:         1.0625;              /* content scale: 85% of the former 1.25 */
  --zoom-tall:    0.918;               /* tall layouts (wave, process, tree, quotes, phones): 85% of the former 1.08 */
  --pad-x:        109px;
  --pad-top:      128px;
  --pad-bottom:   102px;
}

/* === 1b. TONES — per-item colour. Components read --tone (fill), --tone-rgb, --tone-ink (text).
   Repeated items cycle automatically; add .tone-<name> to any element to set it explicitly. === */
.tone-base     { --tone: var(--accent-mid); --tone-rgb: var(--mid-rgb); --tone-ink: var(--accent); }
.tone-mint     { --tone: var(--c-mint);     --tone-rgb: var(--c-mint-rgb);     --tone-ink: var(--c-mint-ink); }
.tone-orange   { --tone: var(--c-orange);   --tone-rgb: var(--c-orange-rgb);   --tone-ink: var(--c-orange-ink); }
.tone-gray     { --tone: var(--c-gray);     --tone-rgb: var(--c-gray-rgb);     --tone-ink: var(--c-gray-ink); }
.tone-grape    { --tone: var(--c-grape);    --tone-rgb: var(--c-grape-rgb);    --tone-ink: var(--c-grape-ink); }
/* auto-cycle: base → orange → grape → mint, then repeat (max four colours; gray is for explicit/neutral use) */
:is(.stats,.grid-2,.grid-3,.grid-4,.wave,.quotes,.checklist,.tags,.mini-stats,.fv-row,.ticker-track,.points,.hbars,.meters,.process,.tree-kids,.data > tbody) > :nth-child(4n+1):not([class*="tone-"]) { --tone: var(--accent-mid); --tone-rgb: var(--mid-rgb); --tone-ink: var(--accent); }
:is(.stats,.grid-2,.grid-3,.grid-4,.wave,.quotes,.checklist,.tags,.mini-stats,.fv-row,.ticker-track,.points,.hbars,.meters,.process,.tree-kids,.data > tbody) > :nth-child(4n+2):not([class*="tone-"]) { --tone: var(--c-orange); --tone-rgb: var(--c-orange-rgb); --tone-ink: var(--c-orange-ink); }
:is(.stats,.grid-2,.grid-3,.grid-4,.wave,.quotes,.checklist,.tags,.mini-stats,.fv-row,.ticker-track,.points,.hbars,.meters,.process,.tree-kids,.data > tbody) > :nth-child(4n+3):not([class*="tone-"]) { --tone: var(--c-grape); --tone-rgb: var(--c-grape-rgb); --tone-ink: var(--c-grape-ink); }
:is(.stats,.grid-2,.grid-3,.grid-4,.wave,.quotes,.checklist,.tags,.mini-stats,.fv-row,.ticker-track,.points,.hbars,.meters,.process,.tree-kids,.data > tbody) > :nth-child(4n+4):not([class*="tone-"]) { --tone: var(--c-mint); --tone-rgb: var(--c-mint-rgb); --tone-ink: var(--c-mint-ink); }
.mono :is(.stats,.grid-2,.grid-3,.grid-4,.wave,.quotes,.checklist,.tags,.mini-stats,.fv-row,.ticker-track,.points,.hbars,.meters,.process,.tree-kids,.data > tbody) > * { --tone: var(--accent-mid); --tone-rgb: var(--mid-rgb); --tone-ink: var(--accent); } /* .mono on a slide = single colour */

/* === 2. RESET === */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 100%; height: 100%; overflow: hidden; background: var(--letterbox); }
html { touch-action: manipulation; }
body { font-family: var(--font-sans); color: var(--text-1); -webkit-font-smoothing: antialiased; }
a { color: inherit; text-decoration: none; }
img { display: block; max-width: 100%; }
button { cursor: pointer; border: none; background: none; font-family: inherit; color: inherit; }
:is(button, a, [tabindex]):focus-visible { outline: 2px solid var(--accent-mid); outline-offset: 3px; border-radius: 6px; }
:is(button, a, [tabindex], [role="button"]):focus-visible { outline: 2px solid var(--accent-mid); outline-offset: 3px; border-radius: 6px; }
.slide.dark :focus-visible, .deck-stage.on-dark :focus-visible { outline-color: var(--on-field); }
code, pre, .code { font-family: var(--font-mono); font-size: 0.9em; }
.sprite { position: absolute; width: 0; height: 0; overflow: hidden; }   /* icon <symbol> sheet */
.ico { width: 46%; height: 46%; flex-shrink: 0; }                         /* <svg class="ico" aria-hidden="true"><use href="#i-bolt"/></svg> */
em { font-style: italic; font-family: inherit; color: inherit; font-weight: inherit; }
:is(.title, .h3, .statement, .card-title, .stat-value, .panel-text, .panel-cta) em { font-style: normal; }   /* headings are one style: no italic word inside a roman heading */


/* CJK glyphs are full-width and look about a third bigger than Latin at the same px size: hero titles step down; titles stay sans */
:is(:lang(zh), :lang(ja), :lang(ko)) :is(.title, .h3, .statement) { font-family: var(--font-sans); }
:is(:lang(zh), :lang(ja), :lang(ko)) .title.hero { font-size: calc(var(--fs-hero) * 0.74); letter-spacing: -0.01em; line-height: 1.18; }


/* === 3. FIXED STAGE (do not change) === */
.deck-viewport { position: fixed; inset: 0; overflow: hidden; background: var(--letterbox); }
.deck-stage {
  position: absolute; left: 0; top: 0; width: 1920px; height: 1080px;
  overflow: hidden; transform-origin: 0 0; background: var(--paper);
}
/* subtle noise texture over everything */
.deck-stage::after {
  content: ''; position: absolute; inset: 0; pointer-events: none; z-index: 50; opacity: 0.025;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size: 160px 160px;
}
.slide {
  position: absolute; inset: 0; width: 1920px; height: 1080px; overflow: hidden;
  padding: var(--pad-top) var(--pad-x) var(--pad-bottom);
  display: flex; flex-direction: column; justify-content: center;
  visibility: hidden; opacity: 0; pointer-events: none;
  background: var(--paper);
  transition: opacity 0.6s var(--silk), visibility 0s linear 0.6s;
}
.slide.active { visibility: visible; opacity: 1; pointer-events: auto; z-index: 1; transition: opacity 0.6s var(--silk); }
.slide.alt     { background: var(--surface); }
.slide > *     { position: relative; z-index: 1; }
/* Content scale. zoom (not transform) so the layout reflows: grids still span the full width, text and boxes grow. */
.slide > :not(.orb, .side-panel, .ts-field, .notes), .side-panel > * { zoom: var(--zoom); }
.ts-field > * { zoom: calc(var(--zoom) * 1.14); }   /* the title-slide visual is the deck's strongest: enlarge it rather than the text */
.slide > :is(.wave, .process, .tree, .quotes, .phones, .phones-ctl) { zoom: var(--zoom-tall); }

/* Background pattern (light slides only): two soft organic shapes, top-right and bottom-left, a shade darker than the slide.
   Drawn with a mask so it follows the theme colour; .alt slides get the mirror image so neighbours differ. */
.slide:not(.dark)::before { content: ''; position: absolute; inset: 0; z-index: 0; pointer-events: none;
  background: rgba(var(--mid-rgb),0.022);
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1920 1080' preserveAspectRatio='none'%3E%3Cpath d='M1235 0C1300 95 1290 250 1385 380C1490 520 1700 545 1920 590V0Z'/%3E%3Cpath d='M0 455C150 420 290 470 330 600C375 745 250 860 285 1080H0Z'/%3E%3C/svg%3E") 0 0 / 100% 100% no-repeat;
          mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1920 1080' preserveAspectRatio='none'%3E%3Cpath d='M1235 0C1300 95 1290 250 1385 380C1490 520 1700 545 1920 590V0Z'/%3E%3Cpath d='M0 455C150 420 290 470 330 600C375 745 250 860 285 1080H0Z'/%3E%3C/svg%3E") 0 0 / 100% 100% no-repeat; }
.slide.alt:not(.dark)::before { transform: scaleX(-1); }

/* Decorative glow orbs (ClearWave hero circles). Add <div class="orb orb-a"></div> etc. */
.orb { position: absolute !important; z-index: 0 !important; border-radius: 50%; pointer-events: none; }
.orb-a { top: -180px; right: -120px; width: 1100px; height: 1100px;
  background: radial-gradient(ellipse at center, rgba(var(--light-rgb),0.20) 0%, rgba(var(--mid-rgb),0.06) 50%, transparent 72%); }
.orb-b { bottom: -320px; left: -200px; width: 820px; height: 820px;
  background: radial-gradient(ellipse at center, rgba(var(--c-mint-rgb),0.10) 0%, rgba(var(--accent-rgb),0.05) 45%, transparent 70%); }
.orb-d { bottom: -260px; right: -160px; width: 760px; height: 760px;
  background: radial-gradient(ellipse at center, rgba(var(--c-orange-rgb),0.09) 0%, transparent 68%); }
.orb-c { top: 50%; left: 50%; width: 1300px; height: 1300px; transform: translate(-50%,-50%);
  background: radial-gradient(ellipse at center, rgba(var(--light-rgb),0.16) 0%, transparent 65%); }

/* === 4. DECK CHROME (inside the stage, scales with it) === */
.deck-nav {
  position: absolute; top: 0; left: 0; right: 0; z-index: 40; height: 112px;
  display: flex; align-items: center; justify-content: space-between; padding: 0 var(--pad-x);
  pointer-events: none;
}
.deck-logo { font-size: 36px; font-weight: 700; letter-spacing: -0.04em; color: var(--text-1); }
.deck-logo span { color: var(--accent); }
.deck-meta { display: flex; align-items: center; gap: 18px; }
.deck-section {
  font-size: 22px; font-weight: 500; color: var(--text-2); padding: 12px 28px; border-radius: 100px;
  background: var(--accent-ghost); box-shadow: inset 0 0 0 1px var(--accent-border);
  transition: opacity 0.4s var(--silk);
}
.deck-count { font-size: 22px; font-weight: 600; color: var(--text-3); font-variant-numeric: tabular-nums; min-width: 72px; text-align: right; }
.deck-dots {
  position: absolute; bottom: 44px; left: 50%; transform: translateX(-50%); z-index: 40;
  display: flex; gap: 12px; align-items: center;
}
.deck-dot { width: 12px; height: 12px; border-radius: 50%; background: var(--accent-border); cursor: pointer; transition: background-color 0.4s var(--silk); }
.deck-dot.active { background: var(--accent); width: 40px; border-radius: 6px; }
.deck-stage.on-dark .deck-logo { color: var(--on-field); } .deck-stage.on-dark .deck-logo span { color: var(--accent-light); }
.deck-stage.on-dark .deck-section { color: rgba(var(--paper-rgb),0.7); background: rgba(var(--paper-rgb),0.06); box-shadow: inset 0 0 0 1px rgba(var(--paper-rgb),0.12); }
.deck-stage.on-dark .deck-dot { background: rgba(var(--paper-rgb),0.18); }
.deck-stage.on-dark .deck-dot.active { background: var(--accent-light); }
.deck-stage.on-dark .deck-count { color: rgba(var(--paper-rgb),0.72); }

/* === 5. TYPOGRAPHY PRIMITIVES === */
.label { display: block; align-self: flex-start; max-width: 1000px; font-size: var(--fs-label); font-weight: 600; line-height: 1.4; color: var(--text-2); margin: 16px 0 0; text-wrap: balance; }
.center .label { align-self: center; text-align: center; }
.title { font-family: var(--font-serif); font-size: var(--fs-title); font-weight: 700; letter-spacing: -0.015em; line-height: 1.12; color: var(--text-1); text-wrap: balance; }
.title.hero { font-size: var(--fs-hero); letter-spacing: -0.02em; line-height: 1.06; }
.h3 { font-family: var(--font-serif); font-size: var(--fs-h3); font-weight: 700; letter-spacing: -0.01em; line-height: 1.15; text-wrap: balance; }
.lead { font-size: var(--fs-lead); line-height: 1.6; color: var(--text-2); max-width: 1000px; margin-top: 22px; }
.body { font-size: var(--fs-body); line-height: 1.65; color: var(--text-2); }
.kicker { font-size: var(--fs-label); font-weight: 600; color: var(--tone-ink, var(--c-orange-ink)); margin-top: 14px; }
.center { text-align: center; align-items: center; }
.center .lead { margin-left: auto; margin-right: auto; }
.head { margin-bottom: 48px; display: flex; flex-direction: column; }
.head.center .lead { text-align: center; }

/* === 6. REVEAL ANIMATION (fires when a slide becomes active) === */
.reveal { opacity: 0; transform: translateY(36px); transition: opacity 0.8s var(--silk), transform 0.8s var(--silk); }
.slide.visible .reveal { opacity: 1; transform: none; }
.d1 { transition-delay: 0.10s; } .d2 { transition-delay: 0.20s; } .d3 { transition-delay: 0.30s; }
.d4 { transition-delay: 0.40s; } .d5 { transition-delay: 0.50s; } .d6 { transition-delay: 0.60s; }

/* === 7. COMPONENTS === */

/* 7a. Badge pill (hero) */
.badge { display: inline-flex; align-items: center; gap: 14px; align-self: flex-start;
  background: var(--accent-ghost); border-radius: 100px;
  padding: 9px 26px 9px 10px; margin-bottom: 40px;
  font-size: 21px; font-weight: 500; color: var(--text-2);
}
.badge-dot { width: 38px; height: 38px; border-radius: 50%; background: var(--accent); color: var(--on-field);
  display: flex; align-items: center; justify-content: center; font-size: 17px; font-weight: 700; }
.badge strong { color: var(--accent); }

/* 7b. Buttons / chips */
.btn { display: inline-flex; align-items: center; gap: 14px; font-size: 24px; font-weight: 600; padding: 22px 46px; border-radius: 100px; }
.btn-primary { color: var(--on-field); background: var(--accent); box-shadow: 0 6px 18px rgba(var(--accent-rgb),0.18); }
.btn-outline { color: var(--accent); background: var(--accent-ghost); }
.row { display: flex; align-items: center; gap: 20px; flex-wrap: wrap; }

/* 7c. Trust / meta row */
.trust { display: flex; align-items: center; gap: 30px; margin-top: 64px; }
.trust-item { display: flex; align-items: center; gap: 12px; font-size: 20px; font-weight: 500; color: var(--text-3); }
.trust-item svg { color: var(--accent); width: 24px; height: 24px; flex-shrink: 0; }
.trust-divider { width: 1px; height: 30px; background: var(--rule); }

/* 7d. Grids */
.split   { display: grid; grid-template-columns: 1fr 1fr; gap: 110px; align-items: center; }
.split.wide-left  { grid-template-columns: 1.15fr 1fr; }
.split.reverse > :first-child { order: 2; }
.grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 32px; }
.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 36px; }
.grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 32px; }

/* 7e. Checklist */
.checklist { display: flex; flex-direction: column; gap: 22px; margin-top: 40px; }
.check { display: flex; align-items: center; gap: 22px; font-size: var(--fs-body); line-height: 1.45; color: var(--text-2); }
.check-icon {
  width: 48px; height: 48px; border-radius: 50%; flex-shrink: 0;
  background: rgba(var(--tone-rgb, var(--accent-rgb)),var(--tint-strong)); color: var(--tone-ink, var(--accent));
  display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: 700; font-variant-numeric: tabular-nums;
}
.check b { color: var(--text-1); font-weight: 600; }
.checklist.two-col { display: grid; grid-template-columns: 1fr 1fr; column-gap: 72px; row-gap: 30px; }
/* agenda: large Playfair numerals in the accent-ink colour hang left of each line, under a thin 1px rule */
.checklist.agenda { column-gap: 72px; row-gap: 0; }
.agenda .check { display: grid; grid-template-columns: 96px 1fr; align-items: baseline; padding: 32px 0 34px; border-top: 1px solid var(--rule); }
.agenda .check-icon { width: auto; height: auto; border-radius: 0; background: none; justify-content: flex-start; font-family: var(--font-serif); font-size: 56px; font-weight: 700; line-height: 1; letter-spacing: -0.01em; color: var(--c-orange-ink); font-variant-numeric: lining-nums tabular-nums; }

/* 7e-2. Points — tinted icon circle + coloured sentence-case label + text */
.points { display: flex; flex-direction: column; gap: 44px; }
.point { display: grid; grid-template-columns: 84px 1fr; column-gap: 28px; align-items: center; }
.point-icon { width: 84px; height: 84px; border-radius: 50%; background: rgba(var(--tone-rgb, var(--accent-rgb)),var(--tint-strong)); color: var(--tone-ink, var(--accent));
  display: flex; align-items: center; justify-content: center; }
.point-k { font-size: var(--fs-label); font-weight: 600; color: var(--tone-ink, var(--accent)); margin-bottom: 6px; }
.point-d { font-size: 22px; line-height: 1.5; color: var(--text-2); text-wrap: pretty; }

/* 7e-3. Side panel — tinted block filling the right part of the slide, big text */
.slide > .side-panel { position: absolute; top: 0; right: 0; bottom: 0; width: 44%; z-index: 0;
  background: rgba(var(--mid-rgb),0.14); padding: var(--pad-top) var(--pad-x) var(--pad-bottom) 96px;
  display: flex; flex-direction: column; justify-content: center; }
.side-panel + * { max-width: 48%; }
.panel-text { font-family: var(--font-serif); font-size: 44px; line-height: 1.3; font-weight: 700; letter-spacing: -0.01em; color: var(--text-1); text-wrap: pretty; }
.panel-cta { margin-top: 40px; font-family: var(--font-serif); font-size: 60px; font-weight: 700; letter-spacing: -0.01em; color: var(--c-orange-ink); }
.panel-sub { font-size: 24px; color: var(--text-2); margin-top: 8px; }

/* 7e-4. Note band — soft tinted tile: label | 1px divider | text */
.note-band { display: grid; grid-template-columns: auto 1fr; align-items: center; column-gap: 40px; margin-top: 48px;
  background: rgba(var(--mid-rgb),0.08); border-radius: var(--radius); padding: 30px 44px; }
.note-band-k { font-family: var(--font-serif); font-size: 32px; font-weight: 700; line-height: 1.15; color: var(--text-1);
  padding-right: 40px; border-right: 1px solid var(--rule); }
.note-band-d { font-size: 21px; line-height: 1.55; color: var(--text-2); text-wrap: pretty; }

/* 7f. Window / dashboard card (hero visual, screenshots) */
.window { background: var(--surface-2); border-radius: var(--radius-lg); box-shadow: var(--shadow-lg); overflow: hidden; }

.window-body { padding: 40px; }   /* a plain soft tile: never draw browser or OS window chrome (dots, title bars) */
.window img { width: 100%; height: auto; display: block; }
.win-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; }
.win-title { font-size: 24px; font-weight: 600; }
.tag { font-size: var(--fs-label); font-weight: 600; color: var(--accent);
  background: var(--accent-ghost); padding: 5px 16px; border-radius: 100px; }
.bars { height: 150px; display: flex; align-items: flex-end; gap: 12px; margin-bottom: 32px; }
.bar { flex: 1; border-radius: 6px 6px 0 0; background: rgba(var(--accent-rgb),0.10); height: var(--h); transform: scaleY(0); transform-origin: bottom; transition: transform 1.2s var(--silk) 0.2s; }
.slide.visible .bar { transform: none; }
.bar.on { background: var(--accent); }
.mini-stats { display: grid; grid-template-columns: repeat(3,1fr); gap: 18px; }

.mini-val { font-family: var(--font-serif); font-size: 36px; font-weight: 700; letter-spacing: -0.01em; font-variant-numeric: lining-nums tabular-nums; }
.mini-val small { font-size: 22px; color: var(--tone-ink, var(--accent)); }
.mini-label { font-size: var(--fs-label); color: var(--text-2); margin-top: 4px; }
.mini-chg { font-size: var(--fs-label); font-weight: 600; color: var(--tone-ink, var(--accent)); margin-top: 6px; }
.mini-stat { background: rgba(var(--tone-rgb, var(--accent-rgb)),var(--tint)); border-radius: var(--radius); padding: 22px; }

/* Floating tiles on a visual */
.visual { position: relative; }
.float { position: absolute !important; display: flex; align-items: center; gap: 16px; background: var(--surface-2);
  border-radius: var(--radius); padding: 18px 24px; box-shadow: var(--shadow-md);
  animation: floaty 4s ease-in-out infinite; z-index: 2; }
.float-icon { width: 54px; height: 54px; border-radius: 50%; background: rgba(var(--tone-rgb, var(--accent-rgb)),var(--tint-strong)); color: var(--tone-ink, var(--c-grape-ink)); display: flex; align-items: center; justify-content: center; font-size: 24px; }
.float-text { font-size: 18px; line-height: 1.35; } .float-text strong { display: block; color: var(--text-1); } .float-text span { color: var(--text-3); }
.float.solid { background: var(--field); box-shadow: var(--shadow-lg); display: block; animation-delay: 2s; }
.float.solid .fv { font-family: var(--font-serif); font-size: 38px; font-weight: 700; color: var(--on-field); letter-spacing: -0.01em; }
.float.solid .fl { font-size: var(--fs-label); color: rgba(var(--paper-rgb),0.78); margin-top: 2px; }
@keyframes floaty { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-9px); } }

/* 7g. Feature panel (fv-cards) */
.panel { background: rgba(var(--mid-rgb),0.09); border-radius: var(--radius); padding: 44px; display: flex; flex-direction: column; gap: 22px; }
.fv-row { display: flex; gap: 22px; }
.fv-card { flex: 1; background: var(--surface-2); border-radius: var(--radius); padding: 26px 28px; box-shadow: var(--shadow-sm); }

.fv-card.wide { flex: 2; }
.fv-label { font-size: var(--fs-label); color: var(--tone-ink, var(--text-2)); font-weight: 600; margin-bottom: 10px; }
.fv-val { font-family: var(--font-serif); font-size: 44px; font-weight: 700; letter-spacing: -0.01em; font-variant-numeric: lining-nums tabular-nums; }
.fv-track { height: 10px; border-radius: 5px; margin-top: 16px; background: var(--track); overflow: hidden; }
.fv-fill { height: 100%; border-radius: 4px; background: var(--tone, var(--accent)); width: var(--w); transform: scaleX(0); transform-origin: left; transition: transform 1.4s var(--silk) 0.3s; }
.slide.visible .fv-fill { transform: none; }
.fv-list { display: flex; flex-direction: column; gap: 12px; margin-top: 8px; }
.fv-item { display: flex; align-items: center; justify-content: space-between; padding: 14px 0; border-bottom: 1px solid var(--rule); font-size: 20px; }
.fv-item:last-child { border-bottom: none; }
.fv-item span:first-child { color: var(--text-2); font-weight: 500; }
.pill { font-size: var(--fs-label); font-weight: 600; padding: 5px 16px; border-radius: 100px; }
.pill.green { background: rgba(var(--c-mint-rgb),0.14); color: var(--c-mint-ink); }
/* failed / high risk: cinnabar, the one allowed exception to the four-colour rule */
.pill.red   { background: rgba(var(--c-cinnabar-rgb),0.12); color: var(--c-cinnabar-ink); }
.pill.grape { background: rgba(var(--c-grape-rgb),0.12); color: var(--c-grape-ink); }
.pill.blue  { background: rgba(var(--mid-rgb),0.12); color: var(--accent-mid); }
.pill.dim   { background: rgba(var(--ink-rgb),0.07); color: var(--text-3); }
.pill.warn  { background: rgba(var(--c-orange-rgb),0.14); color: var(--c-orange-ink); }

/* 7h. Stats */
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 40px; }
.stats.three { grid-template-columns: repeat(3, 1fr); }
.stat { display: flex; flex-direction: column; background: rgba(var(--tone-rgb, var(--accent-rgb)),var(--tint)); border-radius: var(--radius); padding: 44px 40px 44px; }
.stat-value { align-self: flex-start; display: flex; align-items: baseline; gap: 4px; margin-bottom: 20px;
  font-family: var(--font-serif); font-size: 100px; font-weight: 700; letter-spacing: -0.02em; line-height: 1; font-variant-numeric: lining-nums tabular-nums; white-space: nowrap;
  color: var(--tone-ink, var(--accent)); }
.stat-suffix { font-size: 50%; font-weight: 700; letter-spacing: 0; }
.stat-label { font-size: var(--fs-label); font-weight: 600; color: var(--tone-ink, var(--accent)); margin-bottom: 10px; }
.stat-sub { font-size: 21px; color: var(--text-2); line-height: 1.5; }

/* 7i. Cards (pricing-card style) — options, comparisons, pillars */
/* a card is a plain soft tinted tile: no border, no coloured edge; its tone shows as the tint and the title ink */
.card { position: relative; display: flex; flex-direction: column; align-items: flex-start; text-align: left;
  padding: 44px 40px 42px; background: rgba(var(--tone-rgb, var(--accent-rgb)),var(--tint)); border-radius: var(--radius); }
.card-tier { font-size: var(--fs-label); font-weight: 600; color: var(--tone-ink, var(--accent)); margin-bottom: 16px; }
.card-big { font-family: var(--font-serif); font-size: 84px; font-weight: 700; letter-spacing: -0.02em; line-height: 1; margin-bottom: 4px; display: flex; flex-direction: column; align-items: flex-start; gap: 8px; font-variant-numeric: lining-nums tabular-nums; }
.card-big small { font-family: var(--font-sans); font-size: 24px; font-weight: 500; color: var(--text-3); letter-spacing: 0; }
.card-title { font-family: var(--font-serif); font-size: 36px; font-weight: 700; letter-spacing: -0.01em; margin-bottom: 14px; text-wrap: balance; }
.card-desc { font-size: 24px; color: var(--text-2); line-height: 1.55; margin-top: 14px; text-wrap: pretty; }
.card-divider { align-self: stretch; height: 1px; background: rgba(var(--tone-rgb, var(--accent-rgb)),0.25); margin: 28px 0 26px; }
.card .checklist { margin-top: 0; gap: 16px; align-self: stretch; text-align: left; }
.card .check { font-size: 21px; gap: 16px; }
.card .check-icon { width: 30px; height: 30px; font-size: 14px; box-shadow: none; }
.card-icon { width: 76px; height: 76px; border-radius: 50%; background: rgba(var(--tone-rgb, var(--accent-rgb)),var(--tint-strong)); color: var(--tone-ink, var(--accent)); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.card-icon svg { width: 34px; height: 34px; }
.card-head { display: flex; align-items: center; gap: 20px; margin-bottom: 18px; }
.card-head .card-title { margin-bottom: 0; }
.card.tinted { background: rgba(var(--tone-rgb, var(--accent-rgb)),var(--tint-strong)); }
/* featured = the recommended option: solid base-colour column */
.card.featured { background: var(--field); }
.card.featured :is(.card-tier, .card-big, .card-title) { color: var(--on-field); }
.card.featured :is(.card-big small, .card-desc, .check) { color: rgba(var(--paper-rgb),0.82); }
.card.featured .card-divider { background: rgba(var(--paper-rgb),0.22); }
.card.featured .check-icon { background: var(--on-field); color: var(--field); }
.card.featured .card-icon { background: var(--on-field); color: var(--field); }
.card-flag { position: absolute; top: 0; right: 24px; transform: translateY(-50%); background: var(--c-orange); color: var(--ink);
  font-size: var(--fs-label); font-weight: 600; padding: 6px 20px; border-radius: 100px; white-space: nowrap; }

/* 7j. Quotes (testimonials) */
.quotes { display: grid; grid-template-columns: 1.15fr 1fr 1fr; grid-template-rows: auto auto; gap: 24px; }
.quote { background: rgba(var(--tone-rgb, var(--accent-rgb)),var(--tint)); border-radius: var(--radius); padding: 32px 36px; display: flex; flex-direction: column; }
.quote.tall { grid-row: span 2; justify-content: space-between; }
.quote-mark { font-family: var(--font-serif); font-size: 96px; line-height: 0.6; color: var(--tone-ink, var(--accent)); height: 40px; }
.quote-text { font-size: 23px; line-height: 1.6; color: var(--text-1); margin: 14px 0 22px; flex: 1; }
.quote.tall .quote-text { font-size: 30px; }
.author { display: flex; align-items: center; gap: 16px; }
.avatar { width: 58px; height: 58px; border-radius: 50%; flex-shrink: 0; background: rgba(var(--tone-rgb, var(--accent-rgb)),var(--tint-strong));
  display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 20px; color: var(--tone-ink, var(--accent)); }
.author-name { font-size: 21px; font-weight: 600; }
.author-role { font-size: var(--fs-label); color: var(--text-3); margin-top: 2px; }

/* 7k. Statement (big quote slide) */
.statement { font-family: var(--font-serif); font-size: 92px; font-weight: 700; letter-spacing: -0.015em; line-height: 1.15; max-width: 1500px; }
.statement-by { margin-top: 56px; }

/* 7l. Tag cloud (integration pills) */
.tags { display: flex; flex-wrap: wrap; gap: 18px; justify-content: center; max-width: 1400px; margin: 0 auto; }
.tag-pill { background: rgba(var(--tone-rgb, var(--accent-rgb)),var(--tint)); border-radius: 100px; padding: 18px 36px;
  font-size: 24px; font-weight: 600; color: var(--text-2); white-space: nowrap; }
.tag-pill.hl { background: rgba(var(--tone-rgb, var(--accent-rgb)),var(--tint-strong)); color: var(--tone-ink, var(--accent)); }

/* 7m. Ticker (logo strip) */
.ticker { border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); background: var(--surface); padding: 34px 0; overflow: hidden;
  margin: 0 calc(-1 * var(--pad-x)); }
.ticker-label { text-align: center; font-size: var(--fs-label); color: var(--text-3); font-weight: 600; margin-bottom: 26px; }
.ticker-track { display: flex; align-items: center; gap: 90px; width: max-content; animation: ticker 32s linear infinite; }
.ticker:hover .ticker-track { animation-play-state: paused; }
.ticker-item { display: flex; align-items: center; gap: 14px; font-size: 27px; font-weight: 700; letter-spacing: -0.03em; color: var(--text-3); white-space: nowrap; }
.ticker-item i { width: 44px; height: 44px; border-radius: 8px; background: rgba(var(--tone-rgb, var(--accent-rgb)),var(--tint-strong)); display: block; }
.ticker-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--accent-light); opacity: 0.5; }
@keyframes ticker { from { transform: translateX(0); } to { transform: translateX(-50%); } }

/* 7n. FAQ / Q&A accordion */
.faq { display: grid; grid-template-columns: 1fr 1.6fr; gap: 110px; align-items: start; }
.faq-item { border-bottom: 1px solid var(--rule); }
.faq-item:first-child { border-top: 1px solid var(--rule); }
.faq-q { width: 100%; text-align: left; display: flex; justify-content: space-between; align-items: center; gap: 24px; padding: 30px 0; cursor: pointer; font-size: 27px; font-weight: 600; transition: color 0.3s; }
.faq-q:hover { color: var(--accent); }
.faq-icon { width: 44px; height: 44px; border-radius: 50%; background: var(--accent-ghost); flex-shrink: 0; display: flex; align-items: center; justify-content: center;
  color: var(--accent); font-size: 26px; font-weight: 300; transition: transform 0.5s var(--silk), background-color 0.4s, color 0.4s; }
.faq-item.open .faq-icon { transform: rotate(45deg); background: var(--accent); color: var(--on-field); }
.faq-a { display: none; }
.faq-item.open .faq-a { display: block; animation: faq-in 0.5s var(--silk); }
.faq-a > div { font-size: 23px; line-height: 1.65; color: var(--text-2); }
.faq-item.open .faq-a > div { padding-bottom: 30px; }
@keyframes faq-in { from { opacity: 0; transform: translateY(-8px); } to { opacity: 1; transform: none; } }

/* 7o. Wave timeline — icon circles alternate high/low along a wide gray ribbon; text sits above high
   circles and below low ones (template "timeline planning"). Set --n to the number of steps. */
.wave { --row: 150px; --band: 250px; --dot: 132px; display: grid; grid-template-columns: repeat(var(--n, 5), 1fr); position: relative; }
.wave::before { content: ''; position: absolute; left: 0; right: 0; z-index: 0;
  top: calc(var(--row) + var(--dot) / 2 - (var(--band) - var(--dot)) / 8); height: calc((var(--band) - var(--dot)) * 1.25);
  background: var(--rule);
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 100' preserveAspectRatio='none'%3E%3Cpath d='M0 50 C18 22 32 10 50 10 C68 10 82 22 100 50 C118 78 132 90 150 90 C168 90 182 78 200 50' fill='none' stroke='black' stroke-width='1.5' vector-effect='non-scaling-stroke'/%3E%3C/svg%3E") repeat-x 0 0 / calc(200% / var(--n, 5)) 100%;
          mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 100' preserveAspectRatio='none'%3E%3Cpath d='M0 50 C18 22 32 10 50 10 C68 10 82 22 100 50 C118 78 132 90 150 90 C168 90 182 78 200 50' fill='none' stroke='black' stroke-width='1.5' vector-effect='non-scaling-stroke'/%3E%3C/svg%3E") repeat-x 0 0 / calc(200% / var(--n, 5)) 100%; }
.wstep { display: grid; grid-template-rows: var(--row) var(--band) var(--row); justify-items: center; text-align: center; position: relative; z-index: 1; padding: 0 10px; }
.wstep-text { grid-row: 1; align-self: end; padding-bottom: 20px; max-width: 290px; }
.wstep:nth-child(even) .wstep-text { grid-row: 3; align-self: start; padding: 20px 0 0; }
.wstep-dot { grid-row: 2; align-self: start; width: var(--dot); height: var(--dot); border-radius: 50%;
  background: var(--tone, var(--accent)); color: var(--on-field); box-shadow: var(--badge-shadow);
  display: flex; align-items: center; justify-content: center; }
.wstep:nth-child(even) .wstep-dot { align-self: end; }
.wstep.later .wstep-dot { background: var(--surface-2); color: var(--tone-ink, var(--accent)); box-shadow: inset 0 0 0 2px var(--tone, var(--accent)); }
.wstep.now .wstep-dot { box-shadow: var(--badge-shadow), 0 0 0 12px rgba(var(--tone-rgb, var(--accent-rgb)),0.18); }
.wstep-when { font-size: var(--fs-label); font-weight: 600; color: var(--tone-ink, var(--accent)); font-variant-numeric: tabular-nums; }
.wstep.now .wstep-when::after { content: ' \2014  now'; color: var(--text-1); }
.wstep-t { font-family: var(--font-serif); font-size: 30px; font-weight: 700; letter-spacing: -0.01em; margin: 6px 0 6px; }
.wstep-d { font-size: 20px; line-height: 1.45; color: var(--text-2); text-wrap: pretty; }

/* 7o-2. Process diagram — a row of tinted discs with an icon; text alternates above/below, joined by 1px stems */
.process { display: grid; grid-template-columns: repeat(var(--n, 5), 1fr); }
.pnode { display: grid; grid-template-rows: 160px auto 160px; justify-items: center; text-align: center; }
.pnode-ring { grid-row: 2; position: relative; width: min(264px, calc(100% - 26px)); aspect-ratio: 1; border-radius: 50%;
  background: rgba(var(--tone-rgb, var(--accent-rgb)),var(--tint-strong)); color: var(--tone-ink, var(--accent)); display: flex; align-items: center; justify-content: center; margin: 15px 0; }
.pnode-ring::before { content: ''; position: absolute; inset: -58px; border-radius: 50%; border: 1px solid var(--rule); clip-path: inset(0 0 58% 0); }
.pnode:nth-child(even) .pnode-ring::before { clip-path: inset(58% 0 0 0); }
.pnode-text { grid-row: 1; align-self: end; padding-bottom: 54px; max-width: 280px; position: relative; }
.pnode-text::after { content: ''; position: absolute; left: 50%; bottom: 0; width: 1px; height: 36px; background: var(--rule); }
.pnode:nth-child(even) .pnode-text { grid-row: 3; align-self: start; padding: 54px 0 0; }
.pnode:nth-child(even) .pnode-text::after { top: 0; bottom: auto; }
.pnode-k { font-size: var(--fs-label); font-weight: 600; color: var(--tone-ink, var(--accent)); margin-bottom: 8px; }
.pnode-d { font-size: 20px; line-height: 1.45; color: var(--text-2); text-wrap: pretty; }

/* 7o-3. Tree diagram — org chart / architecture: boxed nodes with an icon circle on top, joined by lines */
.tree { display: flex; flex-direction: column; align-items: center; --gap: 48px; --stem: 50px; }
.tree-root { position: relative; padding-bottom: var(--stem); }
.tree-root::after { content: ''; position: absolute; left: 50%; bottom: 0; width: 1px; height: var(--stem); background: var(--rule); transform: translateX(-50%); }
.tree-kids { display: grid; grid-template-columns: repeat(var(--n, 3), 1fr); column-gap: var(--gap); width: 100%; }
.tree-kid { position: relative; padding-top: calc(var(--stem) + 10px); display: flex; justify-content: center; }
.tree-kid::before { content: ''; position: absolute; top: 0; left: calc(var(--gap) / -2); right: calc(var(--gap) / -2); height: 1px; background: var(--rule); }
.tree-kid:first-child::before { left: 50%; } .tree-kid:last-child::before { right: 50%; }
.tree-kid::after { content: ''; position: absolute; top: 0; left: 50%; width: 1px; height: var(--stem); background: var(--rule); transform: translateX(-50%); }
.tnode { position: relative; width: 100%; max-width: 440px; text-align: left; background: rgba(var(--tone-rgb, var(--accent-rgb)),var(--tint)); border-radius: var(--radius);
  padding: 36px 36px; display: grid; grid-template-columns: auto 1fr; column-gap: 28px; align-items: center; }
.tree-root .tnode { min-width: 520px; }
.tnode-icon { grid-row: 1 / span 3; width: 88px; height: 88px; border-radius: 50%;
  background: rgba(var(--tone-rgb, var(--accent-rgb)),var(--tint-strong)); color: var(--tone-ink, var(--accent)); display: flex; align-items: center; justify-content: center; }
.tnode-k { grid-column: 2; font-size: var(--fs-label); font-weight: 600; color: var(--tone-ink, var(--accent)); }
.tnode-t { grid-column: 2; font-family: var(--font-serif); font-size: 32px; font-weight: 700; letter-spacing: -0.01em; margin: 4px 0 4px; }
.tnode-d { grid-column: 2; font-size: 21px; line-height: 1.45; color: var(--text-2); }

/* 7p. Table */
.table-wrap { border: 1px solid var(--rule); border-radius: var(--radius); overflow: hidden; background: var(--surface-2); }
table.data { width: 100%; border-collapse: collapse; font-size: 22px; font-variant-numeric: tabular-nums; }
table.data th { text-align: left; font-size: var(--fs-label); font-weight: 600; color: var(--text-2);
  background: rgba(var(--mid-rgb),0.07); padding: 20px 28px; border-bottom: 1px solid var(--rule); }
table.data td { padding: 26px 28px; color: var(--text-2); border-bottom: 1px solid var(--rule); }
table.data :is(th, td):first-child { }
table.data td:first-child { color: var(--text-1); font-weight: 600; display: flex; align-items: center; gap: 14px; }
table.data td:first-child::before { content: ''; width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; background: var(--tone, var(--accent)); }
table.data tbody tr:last-child td { border-bottom: none; }
table.data tr.hl td { background: rgba(var(--c-orange-rgb),0.12); color: var(--text-1); font-weight: 600; }
table.data tr.hl td:not(:first-child) { }
table.data .num { text-align: right; }

/* 7p-2. Charts */
.chart-k { font-size: var(--fs-label); font-weight: 600; color: var(--text-2); margin-bottom: 26px; }
/* horizontal bars: icon circle, label, bar on a light rail, value */
.hbars { display: grid; grid-template-columns: auto max-content 1fr auto; column-gap: 24px; row-gap: 30px; align-items: center; }
.hbar { display: contents; }
.hbar-icon, .lc-icon { width: 60px; height: 60px; border-radius: 50%; background: rgba(var(--tone-rgb, var(--accent-rgb)),var(--tint-strong)); color: var(--tone-ink, var(--accent)); display: flex; align-items: center; justify-content: center; }
.hbar-label { font-size: var(--fs-small); font-weight: 600; color: var(--text-2); }
.hbar-track { height: 42px; background: rgba(var(--ink-rgb),0.06); border-radius: 8px; overflow: hidden; }
.hbar-fill { height: 100%; width: var(--v); border-radius: 8px; background: var(--tone, var(--accent)); transform: scaleX(0); transform-origin: left; transition: transform 1.2s var(--silk) 0.3s; }
.slide.visible .hbar-fill { transform: none; }
.hbar-val { font-family: var(--font-serif); font-size: 28px; font-weight: 700; color: var(--tone-ink, var(--accent)); font-variant-numeric: lining-nums tabular-nums; min-width: 84px; text-align: right; }
/* donut: ring of segments in the middle, callouts with thin leader lines on both sides */
.donut-chart { display: grid; grid-template-columns: 1fr auto 1fr; column-gap: 40px; align-items: center; }
.donut { position: relative; width: 500px; aspect-ratio: 1; }
.donut svg { width: 100%; height: 100%; transform: rotate(-90deg); overflow: visible; }
.dn-track { fill: none; stroke: var(--track); stroke-width: 26; }
.dn-seg { fill: none; stroke: var(--tone, var(--accent-mid)); stroke-width: 26; stroke-dasharray: var(--p) 100; stroke-dashoffset: calc(-1 * var(--o)); opacity: 0; transition: opacity 1s var(--silk) 0.3s; }
.slide.visible .dn-seg { opacity: 1; }
.donut-center { position: absolute; inset: 22%; border-radius: 50%; background: var(--surface-2); box-shadow: var(--shadow-md);
  display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 24px; }
.dc-big { font-family: var(--font-serif); font-size: 60px; font-weight: 700; letter-spacing: -0.01em; color: var(--text-1); font-variant-numeric: lining-nums tabular-nums; line-height: 1; }
.dc-cap { font-size: var(--fs-label); font-weight: 600; color: var(--text-3); margin-top: 10px; }
.donut-side { display: flex; flex-direction: column; gap: 52px; }
.dc { position: relative; padding-bottom: 18px; border-bottom: 1px solid rgba(var(--tone-rgb, var(--accent-rgb)),0.45); }
.dc::after { content: ''; position: absolute; bottom: -7px; right: -6px; width: 12px; height: 12px; border-radius: 50%; background: var(--tone, var(--accent)); }
.donut-side.right .dc { text-align: right; } .donut-side.right .dc::after { right: auto; left: -6px; }
.dc-head { display: flex; align-items: baseline; justify-content: space-between; gap: 20px; }
.donut-side.right .dc-head { flex-direction: row-reverse; }
.dc-k { font-size: var(--fs-label); font-weight: 600; color: var(--tone-ink, var(--accent)); }
.dc-v { font-family: var(--font-serif); font-size: 44px; font-weight: 700; letter-spacing: -0.01em; color: var(--tone-ink, var(--accent)); font-variant-numeric: lining-nums tabular-nums; }
.dc-d { font-size: 20px; line-height: 1.45; color: var(--text-2); margin-top: 6px; }
/* line chart: soft gridlines, one coloured line + tint per series, end-value bubbles, tinted icon legend on the right */
.line-chart { display: grid; grid-template-columns: 1fr 420px; column-gap: 140px; align-items: center; }
.lc-plot { display: grid; grid-template-columns: auto 1fr; grid-template-rows: 420px auto; column-gap: 26px; row-gap: 22px; padding-top: 30px; }
.lc-y { display: flex; flex-direction: column; justify-content: space-between; text-align: right; font-size: var(--fs-label); font-weight: 600; color: var(--text-3); font-variant-numeric: tabular-nums; }
.lc-y span { line-height: 0; }
.lc-area { position: relative; background: linear-gradient(rgba(var(--ink-rgb),0.09) 1px, transparent 1px) 0 0 / 100% 33.333%; border-bottom: 1px solid rgba(var(--ink-rgb),0.22); }
.lc-area svg { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; opacity: 0; transform: translateY(14px); transition: opacity 1.2s var(--silk) 0.3s, transform 1.2s var(--silk) 0.3s; }
.slide.visible .lc-area svg { opacity: 1; transform: none; }
.lc-fill { fill: var(--tone, var(--accent)); fill-opacity: 0.07; }
.lc-line { fill: none; stroke: var(--tone, var(--accent)); stroke-width: 4; stroke-linejoin: round; stroke-linecap: round; vector-effect: non-scaling-stroke; }
.lc-pts { fill: none; stroke: var(--tone, var(--accent)); stroke-width: 14; stroke-linecap: round; vector-effect: non-scaling-stroke; }
.lc-end { position: absolute; left: var(--x); top: var(--y); width: 30px; height: 30px; margin: -15px 0 0 -15px; border-radius: 50%; background: var(--tone, var(--accent));
  box-shadow: 0 0 0 5px var(--surface-2); opacity: 0; transition: opacity 0.5s ease 1.5s; }
.lc-end b { position: absolute; left: calc(100% + 14px); top: 50%; transform: translateY(-50%); padding: 6px 16px; border-radius: var(--radius); white-space: nowrap;
  background: var(--surface-2); box-shadow: var(--shadow-md);
  font-family: var(--font-serif); font-size: 24px; font-weight: 700; color: var(--tone-ink, var(--accent)); font-variant-numeric: lining-nums tabular-nums; }
.slide.visible .lc-end { opacity: 1; }
.lc-x { grid-column: 2; position: relative; height: 22px; }
.lc-x span { position: absolute; left: var(--x); transform: translateX(-50%); font-size: var(--fs-label); font-weight: 600; color: var(--text-3); }
.lc-legend { display: flex; flex-direction: column; gap: 22px; }
.lc-key { display: grid; grid-template-columns: auto 1fr auto; column-gap: 20px; align-items: center; padding: 22px 26px;
  background: rgba(var(--tone-rgb, var(--accent-rgb)),var(--tint)); border-radius: var(--radius); }
.lc-k { font-size: var(--fs-label); font-weight: 600; color: var(--tone-ink, var(--accent)); }
.lc-d { font-size: var(--fs-label); line-height: 1.4; color: var(--text-2); margin-top: 4px; }
.lc-v { font-family: var(--font-serif); font-size: 48px; font-weight: 700; letter-spacing: -0.01em; color: var(--tone-ink, var(--accent)); font-variant-numeric: lining-nums tabular-nums; }
/* vertical meters: rounded rails with a coloured fill and an icon knob on top */
.meters { display: flex; justify-content: center; align-items: flex-end; gap: 64px; }
.meter { display: flex; flex-direction: column; align-items: center; width: 170px; text-align: center; }
.meter-val { font-family: var(--font-serif); font-size: 52px; font-weight: 700; letter-spacing: -0.01em; color: var(--tone-ink, var(--accent)); font-variant-numeric: lining-nums tabular-nums; }
.meter-track { width: 48px; height: 440px; border-radius: 22px; background: rgba(var(--ink-rgb),0.06); display: flex; align-items: flex-end; margin: 52px 0 26px; }
.meter-fill { position: relative; width: 100%; height: var(--v); border-radius: 22px; background: var(--tone, var(--accent)); opacity: 0; transform: translateY(36px); transition: opacity 1s var(--silk) 0.3s, transform 1.2s var(--silk) 0.3s; }
.slide.visible .meter-fill { opacity: 1; transform: none; }
.meter-knob { position: absolute; top: 0; left: 50%; transform: translate(-50%, -50%); width: 66px; height: 66px; border-radius: 50%;
  background: var(--tone, var(--accent)); color: var(--on-field); box-shadow: 0 0 0 5px var(--paper); display: flex; align-items: center; justify-content: center; }
.meter-k { font-size: var(--fs-small); font-weight: 600; color: var(--text-2); }
.meter-d { font-size: 19px; line-height: 1.45; color: var(--text-3); margin-top: 6px; }
.yes { color: var(--c-mint-ink); font-weight: 700; } .no { color: var(--text-3); } .bad { color: var(--c-cinnabar-ink); font-weight: 700; }

/* 7q. Phone showcase (3D carousel) */
.phones { position: relative; height: 600px; perspective: 1800px; display: flex; align-items: center; justify-content: center; }
.phone { position: absolute; width: 228px; transition: transform 0.7s var(--silk), opacity 0.7s var(--silk); cursor: pointer; }
.phone-shell { background: var(--shell); border-radius: 40px; padding: 6px;
  box-shadow: 0 0 0 1px rgba(var(--ink-rgb),0.12), 0 24px 56px rgba(var(--ink-rgb),0.16); }
.phone-screen { background: var(--paper); border-radius: 34px; overflow: hidden; aspect-ratio: 9 / 19.5; }
.phone-screen img { width: 100%; height: 100%; object-fit: cover; }
.phone-cap { text-align: center; margin-top: 16px; font-size: 20px; font-weight: 600; color: var(--text-2); opacity: 0; transition: opacity 0.4s; }
.phone[data-pos="center"] .phone-cap { opacity: 1; }
.phones-ctl { display: flex; align-items: center; justify-content: center; gap: 28px; margin-top: 4px; }
.round-btn { width: 60px; height: 60px; border-radius: 50%; background: var(--accent-ghost); color: var(--accent);
  display: flex; align-items: center; justify-content: center; font-size: 24px; transition: background-color 0.4s var(--silk), color 0.4s var(--silk), border-color 0.4s var(--silk); }
.round-btn:hover { background: var(--accent); color: var(--on-field); }
/* drawn mock screen (when no screenshot available) */
.mock { height: 100%; display: flex; flex-direction: column; padding: 30px 18px 0; gap: 12px; }
.mock-h { font-size: 19px; font-weight: 700; padding: 0 4px; }
.mock-card { background: var(--surface-2); border-radius: 12px; padding: 16px; }
.mock-line { height: 9px; border-radius: 5px; background: var(--bg-alt); margin-top: 8px; }
.mock-line.a { background: var(--accent); width: 45%; } .mock-line.s { width: 70%; }
.mock-big { font-family: var(--font-serif); font-size: 30px; font-weight: 700; letter-spacing: -0.01em; }
.mock-nav { margin-top: auto; display: flex; justify-content: space-around; padding: 14px 0 20px; border-top: 1px solid var(--rule); background: var(--surface-2); margin-left: -18px; margin-right: -18px; }
.mock-nav i { width: 24px; height: 24px; border-radius: 50%; background: var(--bg-alt); display: block; } .mock-nav i.on { background: var(--accent); }

/* 7r. Dark CTA / closing banner */
.slide.dark { background: var(--field); color: var(--on-field); }
.slide.dark .title, .slide.dark .statement { color: var(--on-field); }

.slide.dark .lead, .slide.dark .body { color: rgba(var(--paper-rgb),0.75); }
.slide.dark .label { color: rgba(var(--paper-rgb),0.72); }
.slide.dark { --glass: rgba(var(--paper-rgb),0.06); --glass-line: rgba(var(--paper-rgb),0.12); }
/* on dark slides the badge, window, tiles and floating card become soft translucent tiles */
.slide.dark .badge { background: var(--glass); color: rgba(var(--paper-rgb),0.78); }
.slide.dark .badge strong { color: var(--on-field); }
.slide.dark .badge-dot { background: var(--accent-light); }
.slide.dark .window { background: rgba(var(--paper-rgb),0.06); color: var(--on-field); box-shadow: 0 18px 48px rgba(var(--ink-rgb),0.35); }
.slide.dark .tag { color: var(--on-field); background: rgba(var(--paper-rgb),0.12); }
.slide.dark .bar { background: rgba(var(--paper-rgb),0.10); }
.slide.dark .bar.on { background: var(--accent-light); }
.slide.dark .mini-stat { background: var(--glass); }
.slide.dark :is(.mini-val small, .mini-chg) { color: color-mix(in srgb, var(--tone, var(--accent-light)), var(--on-field) 40%); }
.slide.dark .mini-label { color: rgba(var(--paper-rgb),0.62); }
.slide.dark :is(.fv-item) { border-color: rgba(var(--paper-rgb),0.12); }
.slide.dark .fv-item span:first-child { color: rgba(var(--paper-rgb),0.78); }
.slide.dark .pill.blue  { background: rgba(var(--light-rgb),0.16); color: var(--accent-light); }
.slide.dark .pill.warn  { background: rgba(var(--c-orange-rgb),0.18); color: color-mix(in srgb, var(--c-orange), var(--on-field) 40%); }
.slide.dark .pill.grape { background: rgba(var(--c-grape-rgb),0.32); color: color-mix(in srgb, var(--c-grape), var(--on-field) 50%); }
.slide.dark .pill.green { background: rgba(var(--c-mint-rgb),0.18); color: color-mix(in srgb, var(--c-mint), var(--on-field) 50%); }
.slide.dark .float:not(.solid) { background: color-mix(in srgb, var(--field), var(--on-field) 12%); color: var(--on-field); box-shadow: 0 14px 36px rgba(var(--ink-rgb),0.4); }
.slide.dark .float-text strong { color: var(--on-field); } .slide.dark .float-text span { color: rgba(var(--paper-rgb),0.6); }
.slide.dark .trust-item { color: rgba(var(--paper-rgb),0.7); } .slide.dark .trust-item svg { color: var(--accent-light); }
.slide.dark .trust-divider { background: rgba(var(--paper-rgb),0.2); }
.slide.dark .orb-a { background: radial-gradient(ellipse at center, rgba(var(--light-rgb),0.16) 0%, transparent 70%); }
.slide.dark .orb-b { background: radial-gradient(ellipse at center, rgba(var(--light-rgb),0.08) 0%, transparent 70%); }
.cta-box { background: var(--field); border-radius: var(--radius-lg); padding: 96px; display: flex; align-items: center; justify-content: space-between; gap: 80px; position: relative; overflow: hidden; }
.cta-box::before { content: ''; position: absolute; top: -40%; right: -5%; width: 820px; height: 820px; border-radius: 50%;
  background: radial-gradient(ellipse at center, rgba(var(--light-rgb),0.17) 0%, transparent 70%); }
.cta-box > * { position: relative; }
.cta-box .title { color: var(--on-field); }
.cta-box .lead { color: rgba(var(--paper-rgb),0.75); }
.cta-box .label { color: rgba(var(--paper-rgb),0.72); }
.cta-actions { display: flex; flex-direction: column; gap: 18px; flex-shrink: 0; }
.btn-ghost-dark { color: var(--on-field); background: rgba(var(--paper-rgb),0.10); justify-content: center; }
.contact { display: flex; flex-direction: column; gap: 14px; font-size: 22px; color: rgba(var(--paper-rgb),0.6); }
.contact b { color: var(--on-field); font-weight: 600; }

/* 7t. Title slide (`slide dark title-slide`): the whole slide is the base-colour field, like the closing slide.
   Left about 6/12: title, one subtitle sentence, small muted meta line. Right: the deck's one strongest visual as soft tiles with a soft shadow. */
.slide > .ts-field { position: absolute; top: 0; right: 0; bottom: 0; width: 46%; z-index: 0; background: var(--field);
  display: flex; align-items: center; justify-content: center; padding: 120px 72px 90px 84px; }
.title-slide > .ts-left { max-width: 50%; display: flex; flex-direction: column; }
.title-slide .title.hero { font-size: 88px; }
.ts-meta { font-size: var(--fs-label); color: var(--text-3); margin-top: 36px; }
.ts-field .visual { width: 100%; }
.ts-field .float.solid { background: var(--paper); }
.ts-field .float.solid .fv { color: var(--c-orange-ink); }
.ts-field .float.solid .fl { color: var(--text-2); }
.slide.dark .ts-meta { color: rgba(var(--paper-rgb),0.62); }

/* 7u. Section divider: the whole slide is the base colour. Big Playfair numeral hangs left of the title under a thin 1px rule;
   on the right one short line in light text and a small muted range line; title and short line share a baseline. */
.section-grid { display: grid; grid-template-columns: 1.7fr 5.3fr 5fr; column-gap: 40px; align-items: last baseline;
  border-top: 1px solid rgba(var(--paper-rgb),0.28); padding-top: 44px; }
.section-num { font-family: var(--font-serif); font-size: 120px; font-weight: 700; line-height: 1; color: var(--c-orange); font-variant-numeric: lining-nums tabular-nums; }
.section-grid .title { font-size: 84px; line-height: 1.08; }
.section-line { font-size: var(--fs-lead); line-height: 1.4; color: rgba(var(--paper-rgb),0.92); }
.section-range { grid-column: 3; font-size: var(--fs-label); color: rgba(var(--paper-rgb),0.6); margin-top: 16px; }

/* 7s. Image figure */
.figure { border-radius: var(--radius-lg); overflow: hidden; box-shadow: var(--shadow-md); background: var(--surface-2); }
.figure img { width: 100%; height: 100%; object-fit: cover; }
.caption { font-size: var(--fs-label); color: var(--text-3); margin-top: 16px; }

/* Speaker notes are never shown */
.notes { display: none !important; }

/* === 8. INLINE EDITING === */
.edit-hotzone { position: fixed; top: 0; left: 0; width: 80px; height: 80px; z-index: 10000; cursor: pointer; }
.edit-toggle { position: fixed; top: 18px; left: 18px; z-index: 10001; width: 48px; height: 48px; border-radius: 50%;
  background: var(--surface-2); color: var(--accent); box-shadow: var(--shadow-md);
  font-size: 20px; display: flex; align-items: center; justify-content: center;
  opacity: 0; pointer-events: none; transition: opacity 0.3s, background-color 0.3s, color 0.3s; }
.edit-toggle.show, .edit-toggle.active { opacity: 1; pointer-events: auto; }
.edit-toggle.active { background: var(--accent); color: var(--on-field); }
.edit-toast { position: fixed; bottom: 24px; left: 50%; transform: translate(-50%, 20px); z-index: 10002; opacity: 0; pointer-events: none;
  background: var(--ink); color: var(--on-field); font-size: 14px; font-weight: 500; padding: 10px 20px; border-radius: 100px; transition: opacity 0.4s var(--silk), transform 0.4s var(--silk); }
.edit-toast.show { opacity: 1; transform: translate(-50%, 0); }
body.editing [contenteditable="true"] { outline: 2px dashed rgba(var(--accent-rgb),0.35); outline-offset: 6px; border-radius: 6px; cursor: text; }
body.editing [contenteditable="true"]:focus { outline-color: var(--accent); }

/* === 9. PRINT (one slide per page) & REDUCED MOTION === */
@page { size: 1920px 1080px; margin: 0; }
@media print {
  html, body { width: 1920px; height: auto; overflow: visible; background: var(--paper); }
  .deck-viewport { position: static; overflow: visible; }
  .deck-stage { position: static; width: 1920px; height: auto; transform: none !important; overflow: visible; }
  .deck-stage::after, .deck-nav, .deck-dots, .edit-hotzone, .edit-toggle, .edit-toast, .phones-ctl { display: none !important; }
  .slide { position: relative; visibility: visible !important; opacity: 1 !important; break-after: page; page-break-after: always; }
  .slide:last-child { break-after: auto; page-break-after: auto; }
  .reveal { opacity: 1 !important; transform: none !important; transition: none !important; }
  .bar, .fv-fill, .hbar-fill, .meter-fill { transform: none !important; opacity: 1 !important; } .dn-seg { opacity: 1 !important; }
  .lc-area svg { opacity: 1 !important; transform: none !important; } .lc-end { opacity: 1 !important; transition: none !important; }
  * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; transition-delay: 0s !important; }
  .float, .ticker-track { animation: none !important; }
  .reveal { opacity: 1; transform: none; }
  .bar, .fv-fill, .hbar-fill { transform: none; } .meter-fill, .dn-seg, .lc-area svg { opacity: 1; transform: none; }
  .phone { transition: none; }
}
```

## Document shell (body start)

Change the `deck-logo` text. Slides follow directly after the `deck-dots` nav.

```html
</style>
</head>
<body>
<div class="edit-hotzone"></div>
<button class="edit-toggle" id="editToggle" title="Edit text (E)" aria-label="Edit text">✎</button>
<div class="edit-toast" id="editToast" role="status" aria-live="polite"></div>
<div class="deck-viewport">
<main class="deck-stage" id="deckStage">
  <!-- Deck chrome: logo (brand) · current section · slide counter · progress dots -->
  <header class="deck-nav">
    <div class="deck-logo">atlas<span>.review</span></div>
    <div class="deck-meta"><div class="deck-section" id="deckSection"></div><div class="deck-count" id="deckCount"></div></div>
  </header>
  <nav class="deck-dots" id="deckDots" aria-label="Slides"></nav>
  <!-- Icon sheet: use with <svg class="ico" aria-hidden="true"><use href="#i-NAME"/></svg>. Add a <symbol> for any new icon. -->
  <svg class="sprite" aria-hidden="true">
    <symbol id="i-bolt" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 10V3L4 14h7v7l9-11h-7z"/></symbol>
    <symbol id="i-shield" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></symbol>
    <symbol id="i-layers" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></symbol>
    <symbol id="i-users" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></symbol>
    <symbol id="i-chart" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></symbol>
    <symbol id="i-trend" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></symbol>
    <symbol id="i-search" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></symbol>
    <symbol id="i-eye" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0zM2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></symbol>
    <symbol id="i-chat" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z"/></symbol>
    <symbol id="i-server" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01"/></symbol>
    <symbol id="i-database" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"/></symbol>
    <symbol id="i-globe" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></symbol>
    <symbol id="i-cube" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/></symbol>
    <symbol id="i-cash" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"/></symbol>
    <symbol id="i-flag" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9"/></symbol>
    <symbol id="i-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13l4 4L19 7"/></symbol>
  </svg>

```

## Document shell (end) + Controller JS (copy verbatim)

```html
</main>
</div>
<script>
/* ==========================================================
   NICE-PRESENTATION CONTROLLER
   Stage scaling · navigation · reveal/counters · FAQ ·
   phone carousel · inline editing (E) · fullscreen (F)
   ========================================================== */
(() => {
  const stage  = document.getElementById('deckStage');
  const slides = Array.from(stage.querySelectorAll('.slide'));
  const sectionEl = document.getElementById('deckSection');
  const countEl   = document.getElementById('deckCount');
  const dotsEl    = document.getElementById('deckDots');
  let current = 0, wheelLock = false, editing = false;

  /* --- Fixed 16:9 stage scaling --- */
  function scaleStage() {
    const f = Math.min(innerWidth / 1920, innerHeight / 1080);
    const x = (innerWidth - 1920 * f) / 2, y = (innerHeight - 1080 * f) / 2;
    stage.style.transform = `translate(${x}px, ${y}px) scale(${f})`;
  }
  addEventListener('resize', scaleStage); scaleStage();

  /* --- Progress dots --- */
  slides.forEach((_, i) => {
    const d = document.createElement('button');
    d.className = 'deck-dot'; d.setAttribute('aria-label', `Go to slide ${i + 1}`);
    d.addEventListener('click', () => go(i));
    dotsEl.appendChild(d);
  });

  /* --- Per-slide entrance effects --- */
  function animateCounter(el) {
    const target = parseFloat(el.dataset.count);
    const dec = (el.dataset.count.split('.')[1] || '').length;
    const fmt = new Intl.NumberFormat(document.documentElement.lang || undefined, { minimumFractionDigits: dec, maximumFractionDigits: dec });
    const t0 = performance.now(), dur = 1800;
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) { el.textContent = fmt.format(target); return; }
    el.textContent = fmt.format(0);
    const step = now => {
      const p = Math.min((now - t0) / dur, 1), e = 1 - Math.pow(1 - p, 4);
      el.textContent = fmt.format(e * target);
      if (p < 1) requestAnimationFrame(step); else el.textContent = fmt.format(target);
    };
    requestAnimationFrame(step);
  }
  function enter(slide) {
    slide.querySelectorAll('[data-count]').forEach(animateCounter);
  }

  /* --- Show a slide --- */
  function go(i) {
    i = Math.max(0, Math.min(i, slides.length - 1));
    slides.forEach((s, k) => { s.classList.toggle('active', k === i); if (k !== i) s.classList.remove('visible'); });
    const s = slides[i];
    requestAnimationFrame(() => requestAnimationFrame(() => s.classList.add('visible')));
    current = i;
    enter(s);
    stage.classList.toggle('on-dark', s.classList.contains('dark'));
    if (sectionEl) { sectionEl.textContent = s.dataset.section || ''; sectionEl.style.opacity = s.dataset.section ? 1 : 0; }
    if (countEl) countEl.textContent = `${String(i + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`;
    dotsEl.querySelectorAll('.deck-dot').forEach((d, k) => { d.classList.toggle('active', k === i); k === i ? d.setAttribute('aria-current', 'step') : d.removeAttribute('aria-current'); });
    if (location.hash !== `#${i + 1}`) history.replaceState(null, '', `#${i + 1}`);
  }
  const next = () => go(current + 1), prev = () => go(current - 1);

  /* --- Keyboard --- */
  document.addEventListener('keydown', e => {
    if (e.target.isContentEditable) return;
    if ((e.key === ' ' || e.key === 'Enter') && e.target.closest?.('button, a, [role="button"]')) return; /* let a focused control handle its own key */
    if (e.key === 'e' || e.key === 'E') { toggleEdit(); return; }
    if (e.key === 'f' || e.key === 'F') { document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen?.(); return; }
    if (['ArrowRight', 'ArrowDown', 'PageDown', ' ', 'Enter'].includes(e.key)) { e.preventDefault(); next(); }
    else if (['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace'].includes(e.key)) { e.preventDefault(); prev(); }
    else if (e.key === 'Home') go(0);
    else if (e.key === 'End') go(slides.length - 1);
  });
  /* --- Wheel (throttled) --- */
  addEventListener('wheel', e => {
    if (editing || wheelLock || Math.abs(e.deltaY) < 20) return;
    wheelLock = true; setTimeout(() => wheelLock = false, 700);
    e.deltaY > 0 ? next() : prev();
  }, { passive: true });
  /* --- Touch swipe --- */
  let tx = 0, ty = 0;
  addEventListener('touchstart', e => { tx = e.touches[0].clientX; ty = e.touches[0].clientY; }, { passive: true });
  addEventListener('touchend', e => {
    const dx = e.changedTouches[0].clientX - tx, dy = e.changedTouches[0].clientY - ty;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) dx < 0 ? next() : prev();
  }, { passive: true });

  /* --- FAQ accordion --- */
  stage.querySelectorAll('.faq-q').forEach(q => q.addEventListener('click', () => {
    if (editing) return;
    const open = q.parentElement.classList.toggle('open');
    q.setAttribute('aria-expanded', String(open));
  }));

  /* --- 3D phone carousel(s) --- */
  stage.querySelectorAll('.phones').forEach(wrap => {
    const cards = Array.from(wrap.querySelectorAll('.phone'));
    const cfg = { center: [0, 0, 1, 1], left1: [-1, 28, .82, 1], right1: [1, -28, .82, 1], left2: [-2, 45, .64, .55], right2: [2, -45, .64, .55], hidden: [0, 0, .4, 0] };
    const gap = 260;
    cards.forEach(card => { card.tabIndex = 0; card.setAttribute('role', 'button'); card.addEventListener('keydown', ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); card.click(); } }); });
    let c = Math.floor(cards.length / 2);
    function layout() {
      cards.forEach((card, i) => {
        let off = i - c; const n = cards.length;
        if (off > n / 2) off -= n; if (off < -n / 2) off += n;
        const pos = off === 0 ? 'center' : off === -1 ? 'left1' : off === 1 ? 'right1' : off === -2 ? 'left2' : off === 2 ? 'right2' : 'hidden';
        const [m, r, s, o] = cfg[pos];
        card.dataset.pos = pos;
        card.style.zIndex = 10 - Math.abs(off);
        card.style.transform = `translateX(${(pos === 'left2' || pos === 'right2') ? m * gap * 0.9 : m * gap}px) rotateY(${r}deg) scale(${s})`;
        card.style.opacity = o;
      });
    }
    cards.forEach((card, i) => card.addEventListener('click', () => { c = i; layout(); }));
    const ctl = wrap.nextElementSibling;
    if (ctl && ctl.classList.contains('phones-ctl')) {
      ctl.querySelector('[data-dir="prev"]')?.addEventListener('click', () => { c = (c - 1 + cards.length) % cards.length; layout(); });
      ctl.querySelector('[data-dir="next"]')?.addEventListener('click', () => { c = (c + 1) % cards.length; layout(); });
    }
    layout();
  });

  /* --- Inline editing (E / top-left hotzone · Ctrl+S saves an edited copy) --- */
  const EDITABLE = '.title,.statement,.lead,.body,.label,.kicker,.h3,.check span,.card-title,.card-desc,.card-tier,.card-big,.stat-label,.stat-sub,.quote-text,.author-name,.author-role,.wstep-when,.wstep-t,.wstep-d,.point-k,.point-d,.panel-text,.panel-cta,.panel-sub,.note-band-k,.note-band-d,.chart-k,.hbar-label,.hbar-val,.dc-k,.dc-v,.dc-d,.dc-big,.dc-cap,.meter-val,.meter-k,.meter-d,.lc-y span,.lc-x span,.lc-end b,.lc-k,.lc-d,.lc-v,.pnode-k,.pnode-d,.tnode-k,.tnode-t,.tnode-d,.faq-q span:first-child,.faq-a > div,.fv-label,.fv-val,.tag-pill,.caption,.badge span,.trust-item span,td,th,.deck-logo';
  const toggleBtn = document.getElementById('editToggle');
  const hotzone = document.querySelector('.edit-hotzone');
  const toast = document.getElementById('editToast');
  const storeKey = 'nice-presentation:' + location.pathname;
  function say(msg) { toast.textContent = msg; toast.classList.add('show'); clearTimeout(say.t); say.t = setTimeout(() => toast.classList.remove('show'), 1800); }
  function toggleEdit() {
    editing = !editing;
    document.body.classList.toggle('editing', editing);
    toggleBtn.classList.toggle('active', editing);
    document.querySelectorAll(EDITABLE).forEach(el => editing ? el.setAttribute('contenteditable', 'true') : el.removeAttribute('contenteditable'));
    if (!editing) { try { localStorage.setItem(storeKey, stage.innerHTML); } catch (_) {} say('Edits saved in this browser · Ctrl+S to download'); }
    else say('Edit mode · click any text · E to finish');
  }
  function download() {
    const clone = document.documentElement.cloneNode(true);
    clone.querySelectorAll('[contenteditable]').forEach(el => el.removeAttribute('contenteditable'));
    clone.querySelector('body').classList.remove('editing');
    clone.querySelectorAll('.slide').forEach(s => s.classList.remove('active', 'visible'));
    const html = '<!DOCTYPE html>\n' + clone.outerHTML;
    const a = Object.assign(document.createElement('a'), { href: URL.createObjectURL(new Blob([html], { type: 'text/html' })), download: (location.pathname.split('/').pop() || 'presentation.html') });
    a.click(); say('Downloaded edited copy');
  }
  document.addEventListener('keydown', e => { if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 's') { e.preventDefault(); download(); } });
  let hideT;
  const show = () => { clearTimeout(hideT); toggleBtn.classList.add('show'); };
  const hide = () => { hideT = setTimeout(() => { if (!editing) toggleBtn.classList.remove('show'); }, 400); };
  hotzone.addEventListener('mouseenter', show); hotzone.addEventListener('mouseleave', hide);
  toggleBtn.addEventListener('mouseenter', show); toggleBtn.addEventListener('mouseleave', hide);
  hotzone.addEventListener('click', toggleEdit); toggleBtn.addEventListener('click', toggleEdit);
  try {
    const saved = localStorage.getItem(storeKey);
    if (saved && new URLSearchParams(location.search).get('fresh') === null) { /* restore text edits; open with ?fresh to ignore them */
      const tmp = document.createElement('div'); tmp.innerHTML = saved;
      const a = tmp.querySelectorAll(EDITABLE), b = stage.querySelectorAll(EDITABLE);
      if (a.length === b.length) b.forEach((el, i) => el.innerHTML = a[i].innerHTML);
    }
  } catch (_) {}

  addEventListener('hashchange', () => { const n = parseInt(location.hash.slice(1), 10); if (Number.isFinite(n) && n - 1 !== current) go(n - 1); });

  /* --- Start --- */
  const fromHash = parseInt(location.hash.slice(1), 10);
  go(Number.isFinite(fromHash) ? fromHash - 1 : 0);
})();
</script>
</body>
</html>
```