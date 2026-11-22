---
name: "nice-presentation"
description: "Create colourful ClearWave-style HTML slide decks: blue-green base with mint, orange, grape and other side colours, DM Sans + Playfair italic, 16:9 stage. Optional argument: base colour hex or preset."
---

# Nice Presentation

Generates single-file, zero-dependency HTML presentations that all share one design system, ported from the ClearWave template (TemplateMo 622): blue-green (#0D98BA) tinted light surfaces, a dark ink accent surface, DM Sans for everything with **one italic Playfair Display phrase per headline**, glow orbs, a faint noise texture, and slow "silk" easing (`cubic-bezier(0.16,1,0.3,1)`).

Text, tables, charts, diagrams, timelines, panels and cards use a bold **business-infographic** build: three slanted colour dashes above every label, a three-colour strip along the bottom of each slide, solid icon circles with a white ring and soft shadow, thick coloured bars on light gray rails, tinted colour blocks for key numbers, and diagrams drawn as rings, waves and connected boxes. Every repeated item takes its own side colour, so slides are full and colourful rather than sparse.

There is **no style-discovery phase**. The look is fixed; your job is content, structure, and choosing the right layout for each slide. Never swap in other fonts, gradients-on-white, neon, or "creative" alternatives. The only allowed variations are the base colour, set by the palette argument (see Palette argument), and how the side colours are spread across items (see Colour system).

## Non-negotiables

1. **One self-contained HTML file.** Inline CSS + JS. Only external resource: the Google Fonts link. Images go in an `assets/` folder next to the file (or base64 if the user wants a single file).
2. **Fixed 1920×1080 stage**, scaled as a whole by JS. Never reflow content per device, never use media-query breakpoints for slide content. Author every size in px at 1920×1080.
3. **Copy the Base CSS and Controller JS below verbatim.** Only edit the `:root` tokens and add small slide-specific rules in a clearly marked `/* === DECK-SPECIFIC === */` block at the end of the `<style>`.
4. **Slide switching** uses `.active`/`.visible` (visibility + opacity). Never `display:none`.
5. **No overflow, no overlap, no scrolling.** Content must sit between y≈150 (below the deck nav) and y≈960 (above the progress dots). If it doesn't fit, split the slide.
6. Never put workflow text on slides ("template", "layout", "option A" as a design label, file names).

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
5. **Brand** (optional) — deck short name for the top-left logo, base colour (skip if a palette argument was given; default blue-green `#0D98BA`), logo image if any.

Skip questions the user already answered. If the user gave content up front and is clearly in a hurry, assume Medium + Speaker-led and say so.

### Phase 2 — Outline
Map the content to layouts from the catalog. A good default arc:
Title (hero) → Agenda → [Section divider → Feature / Points / Stats / Chart / Diagram / Cards …]×N → Statement → Table/Timeline → Q&A → Closing CTA → Thank-you (dark).
Rules: alternate `slide` and `slide alt` backgrounds so neighbours differ; use a section divider every 4–6 slides in long decks; at most one dark full slide (usually the last) and one CTA box; use the featured dark card only for the recommended item. For decks over ~12 slides, show the outline (one line per slide: layout + headline) and get a quick OK before generating.

### Phase 3 — Generate
If a palette argument (or a colour from Phase 1) was given, generate the tokens first (see Palette argument) and replace the matching lines in the Base CSS `:root`; otherwise keep the blue-green default.

Assemble: `Document shell (head)` → Base CSS → (deck-specific CSS) → `Document shell (body start)` → slides → `Document shell (end)` with the Controller JS.

Writing rules for this style:
- Every slide headline gets **one** `<em>` phrase (2–4 words) — it renders in Playfair italic in the accent colour. Not more than one per headline.
- Each content slide opens with a `.label` (1–3 words, uppercased, with the three colour dashes above it) or a `.kicker` ("01 — Topic") above the `.title`.
- `data-section` on each `<section>` fills the pill in the top-right nav. Use short chapter names; reuse the same name for slides in one chapter.
- Add `reveal` + stagger classes `d1`…`d6` to elements in reading order. Containers like `.stats`, `.panel`, `.window` get one reveal, not every child.
- Numbers that should count up: `<span data-count="34">34</span>` (keep the real value as text so print/PDF is correct). Bars/progress fills: `style="--h:75%"` / `style="--w:72%"`.
- Speaker notes: `<div class="notes">…</div>` inside the slide (never displayed).
- Icons: inline SVG, stroke `currentColor`, `stroke-width 2–2.5` (Heroicons-outline style). The body-start shell has an icon sheet (`<svg class="sprite">` with `<symbol id="i-…">`); use one with `<svg class="ico" aria-hidden="true"><use href="#i-bolt"/></svg>` and add a `<symbol>` for any other icon you need. Put icons inside the circle holders (`.point-icon`, `.card-icon`, `.hbar-icon`, `.wstep-dot`, `.pnode-ring`, `.tnode-icon`, `.meter-knob`, `.lc-icon`), which size them. No emoji except the ✦ glyph used by the template and ✓ in checks.
- Infographic parts: give every repeated item an icon that matches its meaning; keep each circle's text to a caps label (1–3 words) plus one short sentence; let the automatic colour cycle colour the items, and mark the current or recommended item (`.now`, `tr.hl`, `.card.featured`) rather than adding more colours.
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

Fix anything flagged, then **look at the PNGs** (contact sheets of 4 help) for overlap, cramped text, orphaned single words in headlines, and empty-looking slides. Also load once at 390×844 to confirm the stage letterboxes rather than reflows.

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
- **Base colour** (blue-green by default) is the structure: headline `<em>` words, labels, buttons, navigation, links, featured card, dark slides. Never put side colours on these.
- **Side colours** decorate repeated items: Mint `#00AB78`, Dark Orange `#FF8C00`, Cinnabar `#E34234`, Gold `#FFD700`, Grape `#6F2DA8`, Amber Brown `#A6674C`, and Metallic Gray `#999B9B` for neutral items. Each has a `-ink` shade that is readable as text on the light backgrounds. Components use the exact colour for fills and the `-ink` shade for text, so gold and orange stay legible.

How items get a colour:
- **Automatic.** Children of `.stats`, `.grid-2/3/4`, `.wave`, `.quotes`, `.checklist`, `.tags`, `.mini-stats`, `.fv-row`, `.ticker-track`, `.points`, `.hbars`, `.meters`, `.process`, `.tree-kids` and table rows (`.data > tbody`) cycle base → orange → grape → mint → cinnabar → gold → amber-brown. This colours stat blocks, card columns and icon circles, check circles, point and timeline circles, bars, meters, process rings, tree nodes, table row dots, quote marks and avatars, highlighted tags, mini-stat tops and progress fills. Donut segments and line series take an explicit `.tone-*` each, matching their callout or legend key.
- **Explicit.** Add `.tone-mint`, `.tone-orange`, `.tone-cinnabar`, `.tone-gold`, `.tone-grape`, `.tone-amber-brown`, `.tone-gray` or `.tone-base` to any item to choose its colour. Use this when colour carries meaning, such as a risk in cinnabar or the same team always in grape across slides.
- **Single colour.** Add `.mono` to a slide to keep all its items in the base colour (for example a sober financial slide).
- **Semantic pills and table marks.** `.pill.green` (mint, done), `.pill.warn` (orange), `.pill.red` (cinnabar, failed), `.pill.gold`, `.pill.grape`, `.pill.blue` (base), `.pill.dim` (gray). In tables, `.yes` is mint and `.bad` is cinnabar.
- **Extras.** `.card.tinted` adds a top border in the card's colour. `.orb-d` is a soft orange glow that pairs with `.orb-a`. `.kicker` text is orange unless a tone is set. `.float-icon` is grape.

Keep it calm: one slide shows at most about four side colours (the cycle does this for normal item counts). Don't add colours to body text or headlines.

## Palette argument
The skill takes one optional argument: a **base colour**, either a hex code or a preset name. Examples: `/nice-presentation #0D98BA`, `/nice-presentation blue-green`, or in prose ("use blue-green #0D98BA"). With no argument, use the default blue-green `#0D98BA` that is already in the Base CSS.

Presets: `blue-green` #0D98BA (default) · `steel-blue` #4682B4 · `teal` #2A9D8F (original ClearWave) · `plum` #9A4A9A · `amber` #C27530. Any other hex is accepted.

The base colour becomes `--accent-mid`. Everything else is derived from it: a darker `--accent` checked for at least 4.5:1 contrast on the background (used for text, buttons and italic headline words), a lighter `--accent-light`, tinted backgrounds, a near-black ink in the same hue, muted text colours, the letterbox colour and the phone frame. Never hand-pick these values. Run this script and paste its output over the same-named lines in `:root`:

```python
import colorsys, sys
PRESETS = {'steel-blue': '#4682B4', 'blue-green': '#0D98BA', 'teal': '#2A9D8F', 'plum': '#9A4A9A', 'amber': '#C27530'}
def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def hx(c): return '#%02X%02X%02X' % tuple(round(max(0, min(255, v))) for v in c)
def mix(a, b, t): return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))
def hsl(h, s, l): return tuple(v * 255 for v in colorsys.hls_to_rgb(h, l, s))
def lum(c):
    f = lambda v: (v / 255) / 12.92 if v / 255 <= 0.03928 else ((v / 255 + 0.055) / 1.055) ** 2.4
    r, g, b = map(f, c); return 0.2126 * r + 0.7152 * g + 0.0722 * b
def contrast(a, b): la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)
def palette(base):
    base = rgb(PRESETS.get(base.lower(), base))
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
    t, shell = palette(sys.argv[1] if len(sys.argv) > 1 else 'blue-green')
    for k, v in t.items(): print(f'  {k}: {v};')
    print(f'  --shell: {shell};')
```

Run it as `python3 palette.py blue-green` or `python3 palette.py "#0D98BA"`. The generator only sets the base colour; side colours stay the same. If the base colour is close to a side colour (for example a mint base), give the clashing items an explicit `.tone-*` instead. For a very light or very dark base (yellow, near-black), check the Phase 4 screenshots for washed-out or muddy surfaces and tell the user if the colour doesn't suit this style. Mention the base colour used when delivering.

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
- **Structure**: `.slide` (`.alt` lighter bg, `.dark` ink bg, `.center` centred), `.head` (+`.center`) wrapper for label/title/lead, `.split` 2-col (`.wide-left`, `.reverse`), `.grid-2/3/4`, `.row`, decorative `.orb .orb-a|b|c|d` (first children of the slide), tones `.tone-*` and `.mono` (see Colour system).
- **Type**: `.label` (three colour dashes + caps), `.kicker`, `.title` (`.hero` bigger), `.h3`, `.lead`, `.body`, `.statement`, `em` accent. `.points` > `.point` (`.point-icon`, `.point-k`, `.point-d`) for an icon list.
- **Panels**: `.side-panel` (first child of the slide: tinted block over the right 44%, holds `.panel-text`, `.panel-cta`, `.panel-sub`; the next element is the left content), `.note-band` (`.note-band-k` + `.note-band-d`), `.panel` (feature panel, see Visuals).
- **Hero bits**: `.badge` (+`.badge-dot`), `.trust` > `.trust-item` + `.trust-divider`, `.btn .btn-primary|.btn-outline|.btn-ghost-dark`.
- **Visuals**: `.window` (`.window-bar` with three `<i>`, `.window-body`, or a direct `<img>`), `.bars` > `.bar[.on]` with `--h`, `.mini-stats`, `.visual` + `.float` / `.float.solid` floating badges, `.panel` > `.fv-row` / `.fv-card[.wide]` / `.fv-track > .fv-fill` / `.fv-list > .fv-item` + `.pill .green|.blue|.dim|.warn|.red|.gold|.grape`, `.figure` + `.caption`.
- **Content**: `.checklist[.two-col]` > `.check` (`.check-icon` ✓ or 01…), `.stats[.three]` > `.stat`, `.card[.featured|.tinted]` (`.card-flag`, `.card-tier`, `.card-big`, `.card-title`, `.card-desc`, `.card-icon`, `.card-divider`), `.quotes` > `.quote[.tall]`, `.tags` > `.tag-pill[.hl]`, `.ticker` (items listed twice for a seamless loop), `.faq` > `.faq-item[.open]` (`button.faq-q`), `.phones` + `.phones-ctl`, `.cta-box` + `.cta-actions`, `.contact`.
- **Tables**: `.table-wrap > table.data` (`tr.hl`, `.num`, `.yes`, `.no`, `.bad`). The first column is the row label and gets a coloured dot.
- **Charts**: `.chart-k` caps caption, then `.hbars` > `.hbar` (`style="--v:72%"`; `.hbar-icon`, `.hbar-label`, `.hbar-track > .hbar-fill`, `.hbar-val`) · `.donut-chart` = `.donut-side` + `.donut` (SVG with `.dn-track` and one `.dn-seg.tone-*` per segment, `pathLength="100"`, `style="--p:58;--o:0"` = length and start in %, + `.donut-center` > `.dc-big` + `.dc-cap`) + `.donut-side.right`; each side holds `.dc` (`.dc-head` > `.dc-k` + `.dc-v`, `.dc-d`) · `.meters` > `.meter` (`style="--v:72%"`; `.meter-val`, `.meter-track > .meter-fill > .meter-knob`, `.meter-k`, `.meter-d`) · `.line-chart` = `.lc-plot` + `.lc-legend`. The plot holds `.lc-y` (axis numbers, top to bottom), `.lc-area` and `.lc-x` (labels with `style="--x:40%"`). `.lc-area` holds one SVG (`viewBox="0 0 100 100" preserveAspectRatio="none"`) with a `g.lc-series.tone-*` per line: `.lc-fill` (area under the line, closed to y=100), `.lc-line`, and `.lc-pts` (`M x,y h0` per point, drawn as round dots). Then one `.lc-end.tone-*` per line (`style="--x:100%;--y:16%"`) with the last value in `<b>`. Coordinates: x = 0–100 across, y = 100 − value ÷ axis max × 100. The legend holds `.lc-key.tone-*` (`.lc-icon`, `div` > `.lc-k` + `.lc-d`, `.lc-v`).
- **Diagrams**: `.process` (set `style="--n:5"`) > `.pnode` (`.pnode-text` > `.pnode-k` + `.pnode-d`, `.pnode-ring` with an icon) · `.tree` > `.tree-root > .tnode` + `.tree-kids` (set `style="--n:3"`) > `.tree-kid > .tnode` (`.tnode-icon`, `.tnode-k`, `.tnode-t`, `.tnode-d`).
- **Timelines**: `.wave` (set `style="--n:5"`) > `.wstep[.now|.later]` (`.wstep-text` > `.wstep-when` + `.wstep-t` + `.wstep-d`, `.wstep-dot` with an icon). Odd steps sit high with text above; even steps sit low with text below.

The full example deck below uses every layout. Copy the structure of the layout you need, **never the demo wording or numbers**.

### Example deck — every layout (slides go inside `<main class="deck-stage">`)

```html
  <!-- ================= 01 · TITLE (hero) ================= -->
  <section class="slide" data-section="Overview">
    <div class="orb orb-a"></div><div class="orb orb-b"></div>
    <div class="split wide-left">
      <div style="display:flex;flex-direction:column">
        <div class="badge reveal"><div class="badge-dot">✦</div><span>Platform Review · <strong>November 2026</strong></span></div>
        <h1 class="title hero reveal d1">Your platform,<br><em>finally clear.</em></h1>
        <p class="lead reveal d2">How Atlas unified twelve internal tools into one calm, observable surface — and what we ship next.</p>
        <div class="trust reveal d3">
          <div class="trust-item"><svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></svg><span>Platform Engineering</span></div>
          <div class="trust-divider"></div>
          <div class="trust-item"><svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg><span>Q4 All-Hands</span></div>
        </div>
      </div>
      <div class="visual reveal d2">
        <div class="window">
          <div class="window-bar"><i></i><i></i><i></i></div>
          <div class="window-body">
            <div class="win-head"><div class="win-title">Cluster Utilization</div><div class="tag">Live</div></div>
            <div class="bars">
              <div class="bar" style="--h:35%"></div><div class="bar" style="--h:55%"></div><div class="bar" style="--h:42%"></div><div class="bar on" style="--h:75%"></div>
              <div class="bar" style="--h:60%"></div><div class="bar on" style="--h:88%"></div><div class="bar" style="--h:70%"></div><div class="bar on" style="--h:92%"></div>
            </div>
            <div class="mini-stats">
              <div class="mini-stat"><div class="mini-val">94<small>%</small></div><div class="mini-label">GPU usage</div><div class="mini-chg">+12%</div></div>
              <div class="mini-stat"><div class="mini-val">2.4<small>k</small></div><div class="mini-label">Workloads</div><div class="mini-chg">+8%</div></div>
              <div class="mini-stat"><div class="mini-val">18<small>h</small></div><div class="mini-label">Saved / wk</div><div class="mini-chg">+24%</div></div>
            </div>
          </div>
        </div>
        <div class="float" style="bottom:-28px;left:-44px"><div class="float-icon">✦</div><div class="float-text"><strong>Autoscaler on</strong><span>prod-east · just now</span></div></div>
        <div class="float solid" style="top:40px;right:-36px"><div class="fv">↑ 34%</div><div class="fl">Throughput this quarter</div></div>
      </div>
    </div>
    <div class="notes">Open with the headline number; the dashboard is illustrative.</div>
  </section>

  <!-- ================= 02 · AGENDA (checklist two-col) ================= -->
  <section class="slide alt" data-section="Agenda">
    <div class="head">
      <div class="label reveal">Agenda</div>
      <h2 class="title reveal d1">What we’ll <em>cover</em> today</h2>
    </div>
    <div class="checklist two-col">
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
      <div class="label reveal">Why it matters</div>
      <h2 class="title reveal d1">Three things <em>changed</em></h2>
      <div class="points reveal d2" style="margin-top:52px">
        <div class="point"><div class="point-icon"><svg class="ico" aria-hidden="true"><use href="#i-eye"/></svg></div><div><div class="point-k">Visibility</div><p class="point-d">Every team sees its own cost and capacity, live.</p></div></div>
        <div class="point"><div class="point-icon"><svg class="ico" aria-hidden="true"><use href="#i-bolt"/></svg></div><div><div class="point-k">Speed</div><p class="point-d">New clusters arrive in minutes instead of days.</p></div></div>
        <div class="point"><div class="point-icon"><svg class="ico" aria-hidden="true"><use href="#i-shield"/></svg></div><div><div class="point-k">Safety</div><p class="point-d">Policy runs before anything reaches production.</p></div></div>
      </div>
    </div>
  </section>

  <!-- ================= 04 · SECTION DIVIDER ================= -->
  <section class="slide alt center" data-section="Chapter 1">
    <div class="orb orb-c"></div>
    <div class="head center" style="margin:0">
      <div class="label reveal">Chapter 01</div>
      <h2 class="title hero reveal d1">Built for <em>clarity</em><br>at every scale</h2>
      <p class="lead reveal d2">Every feature reduces friction and surfaces what matters. No bloat, no configuration maze.</p>
    </div>
  </section>

  <!-- ================= 05 · FEATURE (content + panel) ================= -->
  <section class="slide" data-section="What we built">
    <div class="split">
      <div>
        <div class="kicker reveal">01 — Unified Dashboard</div>
        <h2 class="title reveal d1">Every metric, one <em>calm</em> surface</h2>
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

  <!-- ================= 06 · FEATURE (reverse, with screenshot window) ================= -->
  <section class="slide alt" data-section="What we built">
    <div class="split reverse">
      <div>
        <div class="kicker reveal">02 — Smart Automation</div>
        <h2 class="title reveal d1">Routines that run <em>themselves</em></h2>
        <p class="lead reveal d2">Describe the intent in plain language; Atlas proposes the flow and keeps an audit trail of every action.</p>
        <div class="checklist">
          <div class="check reveal d3"><div class="check-icon">✓</div><span>Natural-language flow builder</span></div>
          <div class="check reveal d4"><div class="check-icon">✓</div><span>500+ trigger templates</span></div>
        </div>
      </div>
      <div class="window reveal d2">
        <div class="window-bar"><i></i><i></i><i></i></div>
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
      <div class="label reveal">Results</div>
      <h2 class="title reveal d1">Twelve months, <em>measured</em></h2>
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
      <div class="label reveal">Cost by team</div>
      <h2 class="title reveal d1">Search spends <em>twice</em> what anyone else does</h2>
    </div>
    <div class="reveal d2">
      <div class="chart-k">Monthly GPU spend · US$ thousands · October 2026</div>
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
      <div class="label reveal">Where the money goes</div>
      <h2 class="title reveal d1">Compute is <em>most</em> of the bill</h2>
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
        <div class="label reveal">Adoption</div>
        <h2 class="title reveal d1">Most teams are <em>already in</em></h2>
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
      <div class="label reveal">Delivery</div>
      <h2 class="title reveal d1">Deploys <em>tripled</em> in six months</h2>
    </div>
    <div class="reveal d2">
      <div class="chart-k">Production deploys per week · May – October 2026</div>
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
      <div class="label reveal">Options for 2027</div>
      <h2 class="title reveal d1">Three paths, one <em>recommendation</em></h2>
    </div>
    <div class="grid-3" style="align-items:stretch">
      <div class="card reveal d2">
        <div class="card-tier">Option A · Hold</div>
        <div class="card-big">$1.2<small>M / yr</small></div>
        <p class="card-desc">Keep today’s footprint and focus on reliability work.</p>
        <div class="card-divider"></div>
        <div class="checklist"><div class="check"><div class="check-icon">✓</div><span>Lowest risk</span></div><div class="check"><div class="check-icon">✓</div><span>No new hiring</span></div><div class="check"><div class="check-icon">✓</div><span>Growth capped at 15%</span></div></div>
      </div>
      <div class="card featured reveal d3">
        <div class="card-flag">Recommended</div>
        <div class="card-tier">Option B · Expand</div>
        <div class="card-big">$2.0<small>M / yr</small></div>
        <p class="card-desc">Add a second GPU region and self-service onboarding.</p>
        <div class="card-divider"></div>
        <div class="checklist"><div class="check"><div class="check-icon">✓</div><span>2× capacity by Q3</span></div><div class="check"><div class="check-icon">✓</div><span>Payback in 14 months</span></div><div class="check"><div class="check-icon">✓</div><span>Four new hires</span></div></div>
      </div>
      <div class="card reveal d4">
        <div class="card-tier">Option C · Rebuild</div>
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
      <div class="label reveal">Principles</div>
      <h2 class="title reveal d1">How we <em>decide</em></h2>
    </div>
    <div class="grid-3">
      <div class="card reveal d2"><div class="card-icon"><svg class="ico" aria-hidden="true"><use href="#i-shield"/></svg></div><div class="card-title">Safe by default</div><p class="card-desc">Every change is reversible, reviewed and observable before it reaches production.</p></div>
      <div class="card reveal d3"><div class="card-icon"><svg class="ico" aria-hidden="true"><use href="#i-bolt"/></svg></div><div class="card-title">Fast feedback</div><p class="card-desc">Teams see the cost and performance of a change within minutes, not at month-end.</p></div>
      <div class="card reveal d4"><div class="card-icon"><svg class="ico" aria-hidden="true"><use href="#i-layers"/></svg></div><div class="card-title">One layer</div><p class="card-desc">A single control plane over compute, storage and network — no parallel tooling.</p></div>
    </div>
  </section>

  <!-- ================= 14 · STATEMENT ================= -->
  <section class="slide alt center" data-section="Insight">
    <div class="orb orb-c"></div>
    <div class="center" style="display:flex;flex-direction:column">
      <div class="label reveal">Key insight</div>
      <p class="statement reveal d1">The bottleneck was never compute. It was <em>knowing what we already had.</em></p>
      <div class="author statement-by reveal d2" style="justify-content:center"><div class="avatar">SW</div><div style="text-align:left"><div class="author-name">Platform team retro</div><div class="author-role">September 2026</div></div></div>
    </div>
  </section>

  <!-- ================= 15 · QUOTES ================= -->
  <section class="slide" data-section="Feedback">
    <div class="head">
      <div class="label reveal">What teams say</div>
      <h2 class="title reveal d1">Teams that <em>love</em> the change</h2>
    </div>
    <div class="quotes">
      <div class="quote tall reveal d2"><div class="quote-mark">“</div><p class="quote-text">We replaced three separate tools and actually have fewer meetings now. The automation handles the hand-offs we used to sort out every morning.</p><div class="author"><div class="avatar">SL</div><div><div class="author-name">Sarah Lin</div><div class="author-role">Head of Operations · Data</div></div></div></div>
      <div class="quote reveal d3"><div class="quote-mark">“</div><p class="quote-text">I can review capacity and approve changes between meetings.</p><div class="author"><div class="avatar">MR</div><div><div class="author-name">Marcus Reyes</div><div class="author-role">Product Director</div></div></div></div>
      <div class="quote reveal d4"><div class="quote-mark">“</div><p class="quote-text">Onboarding a 30-person team took one afternoon.</p><div class="author"><div class="avatar">PK</div><div><div class="author-name">Priya Kapoor</div><div class="author-role">Engineering Lead</div></div></div></div>
      <div class="quote reveal d4"><div class="quote-mark">“</div><p class="quote-text">We show stakeholders live data instead of preparing decks.</p><div class="author"><div class="avatar">TW</div><div><div class="author-name">Tom Wang</div><div class="author-role">Finance</div></div></div></div>
      <div class="quote reveal d5"><div class="quote-mark">“</div><p class="quote-text">Support answered an integration question in two hours.</p><div class="author"><div class="avatar">AN</div><div><div class="author-name">Aiko Nakamura</div><div class="author-role">CTO · Labs</div></div></div></div>
    </div>
  </section>

  <!-- ================= 16 · PHONE SHOWCASE ================= -->
  <section class="slide alt" data-section="Mobile">
    <div class="head center" style="margin-bottom:0">
      <div class="label reveal">Mobile app</div>
      <h2 class="title reveal d1">Your cluster, <em>in your pocket</em></h2>
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
      <div class="label reveal">Comparison</div>
      <h2 class="title reveal d1">Before and <em>after</em> Atlas</h2>
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
      <div class="label reveal">Roadmap</div>
      <h2 class="title reveal d1">The next <em>five</em> quarters</h2>
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
    <div class="head center" style="margin-bottom:0">
      <div class="label reveal">Request path</div>
      <h2 class="title reveal d1">From request to running job in <em>five steps</em></h2>
    </div>
    <div class="process reveal d2" style="--n:5">
      <div class="pnode"><div class="pnode-text"><div class="pnode-k">1 · Request</div><p class="pnode-d">Ask for capacity in plain terms.</p></div><div class="pnode-ring"><svg class="ico" aria-hidden="true"><use href="#i-chat"/></svg></div></div>
      <div class="pnode"><div class="pnode-text"><div class="pnode-k">2 · Check</div><p class="pnode-d">Quota, budget and security rules run.</p></div><div class="pnode-ring"><svg class="ico" aria-hidden="true"><use href="#i-shield"/></svg></div></div>
      <div class="pnode"><div class="pnode-text"><div class="pnode-k">3 · Place</div><p class="pnode-d">Pick the cheapest region that fits.</p></div><div class="pnode-ring"><svg class="ico" aria-hidden="true"><use href="#i-globe"/></svg></div></div>
      <div class="pnode"><div class="pnode-text"><div class="pnode-k">4 · Run</div><p class="pnode-d">The job starts with metrics wired in.</p></div><div class="pnode-ring"><svg class="ico" aria-hidden="true"><use href="#i-bolt"/></svg></div></div>
      <div class="pnode"><div class="pnode-text"><div class="pnode-k">5 · Bill</div><p class="pnode-d">Cost lands on the team’s budget.</p></div><div class="pnode-ring"><svg class="ico" aria-hidden="true"><use href="#i-cash"/></svg></div></div>
    </div>
  </section>

  <!-- ================= 20 · DIAGRAM — TREE (org / architecture) ================= -->
  <section class="slide alt" data-section="How it works">
    <div class="head center" style="margin-bottom:76px">
      <div class="label reveal">Architecture</div>
      <h2 class="title reveal d1">One control plane over <em>every layer</em></h2>
    </div>
    <div class="tree reveal d2">
      <div class="tree-root"><div class="tnode"><span class="tnode-icon"><svg class="ico" aria-hidden="true"><use href="#i-cube"/></svg></span><div class="tnode-k">Control</div><div class="tnode-t">Atlas control plane</div><p class="tnode-d">Policy · scheduling · cost tagging</p></div></div>
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
      <div class="label reveal">Integrations</div>
      <h2 class="title reveal d1">Connects with your <em>existing stack</em></h2>
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
        <div class="label reveal">Q&amp;A</div>
        <h2 class="title reveal d1">Questions,<br><em>answered</em></h2>
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
        <div class="label">Decision needed</div>
        <h2 class="title">Ready for a<br><em>clearer platform?</em></h2>
        <p class="lead">Approve Option B today and we start the second region in January.</p>
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
      <div class="label reveal">Thank you</div>
      <h2 class="title hero reveal d1">Less noise,<br><em>more done.</em></h2>
      <div class="contact reveal d2" style="margin-top:56px;align-items:center"><span><b>Presenter Name</b> · Team</span><span>contact@example.com</span></div>
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
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Playfair+Display:ital,wght@0,700;1,600;1,700&display=swap" rel="stylesheet">
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
  --bg:           #E2F3F7;
  --bg-alt:       #D3ECF3;
  --surface:      #F0F9FB;
  --surface-2:    #FFFFFF;
  --accent:       #0A748D;
  --accent-mid:   #0D98BA;
  --accent-light: #62BCD2;
  --accent-rgb:   10,116,141;          /* = --accent as r,g,b */
  --mid-rgb:      13,152,186;          /* = --accent-mid as r,g,b */
  --light-rgb:    98,188,210;          /* = --accent-light as r,g,b */
  --accent-ghost: rgba(var(--accent-rgb),0.08);
  --accent-border:rgba(var(--accent-rgb),0.15);
  --ink:          #0E2025;             /* dark surfaces (CTA, featured card) */
  --ink-rgb:      14,32,37;            /* = --ink as r,g,b */
  --text-1:       #0E2025;
  --text-2:       #3A5C64;
  --text-3:       #6C8B93;
  --border:       rgba(var(--ink-rgb),0.08);
  --track:        rgba(var(--ink-rgb),0.08);   /* light gray rails, tracks and the timeline ribbon */
  --badge-shadow: 0 8px 22px rgba(var(--ink-rgb),0.16);   /* soft drop shadow under icon circles */
  --shadow-sm:    0 3px 18px rgba(var(--ink-rgb),0.06);
  --shadow-md:    0 12px 48px rgba(var(--ink-rgb),0.10);
  --shadow-lg:    0 36px 96px rgba(var(--ink-rgb),0.13);
  --silk:         cubic-bezier(0.16, 1, 0.3, 1);
  --silk-dur:     0.8s;
  --radius:       24px;
  --radius-lg:    36px;
  --font-sans:    'DM Sans', sans-serif;
  --font-serif:   'Playfair Display', serif;
  /* Type scale, authored at 1920×1080 */
  --fs-hero:      112px;
  --fs-title:     76px;
  --fs-h3:        52px;
  --fs-lead:      30px;
  --fs-body:      26px;
  --fs-small:     21px;
  --fs-label:     17px;
  --letterbox:    #C2E5EE;             /* color around the stage on non-16:9 screens */
  --shell:        #BCCED2;             /* phone frame */
  /* Side colours: decorate repeated items. Exact colour for fills; -ink = darker shade readable as text on light bg */
  --c-mint:     #00AB78; --c-mint-rgb:     0,171,120;  --c-mint-ink:     #007653;
  --c-orange:   #FF8C00; --c-orange-rgb:   255,140,0;  --c-orange-ink:   #9B5500;
  --c-cinnabar: #E34234; --c-cinnabar-rgb: 227,66,52;  --c-cinnabar-ink: #BD372B;
  --c-gold:     #FFD700; --c-gold-rgb:     255,215,0;  --c-gold-ink:     #796600;
  --c-gray:     #999B9B; --c-gray-rgb:     153,155,155; --c-gray-ink:    #6A6B6B;
  --c-grape:    #6F2DA8; --c-grape-rgb:    111,45,168; --c-grape-ink:    #6F2DA8;
  --c-amber-brown: #A6674C; --c-amber-brown-rgb: 166,103,76; --c-amber-brown-ink: #935B43;
  --pad-x:        128px;
  --pad-top:      150px;
  --pad-bottom:   120px;
}

/* === 1b. TONES — per-item colour. Components read --tone (fill), --tone-rgb, --tone-ink (text).
   Repeated items cycle automatically; add .tone-<name> to any element to set it explicitly. === */
.tone-base     { --tone: var(--accent-mid); --tone-rgb: var(--mid-rgb); --tone-ink: var(--accent); }
.tone-mint     { --tone: var(--c-mint);     --tone-rgb: var(--c-mint-rgb);     --tone-ink: var(--c-mint-ink); }
.tone-orange   { --tone: var(--c-orange);   --tone-rgb: var(--c-orange-rgb);   --tone-ink: var(--c-orange-ink); }
.tone-cinnabar { --tone: var(--c-cinnabar); --tone-rgb: var(--c-cinnabar-rgb); --tone-ink: var(--c-cinnabar-ink); }
.tone-gold     { --tone: var(--c-gold);     --tone-rgb: var(--c-gold-rgb);     --tone-ink: var(--c-gold-ink); }
.tone-gray     { --tone: var(--c-gray);     --tone-rgb: var(--c-gray-rgb);     --tone-ink: var(--c-gray-ink); }
.tone-grape    { --tone: var(--c-grape);    --tone-rgb: var(--c-grape-rgb);    --tone-ink: var(--c-grape-ink); }
.tone-amber-brown { --tone: var(--c-amber-brown); --tone-rgb: var(--c-amber-brown-rgb); --tone-ink: var(--c-amber-brown-ink); }
/* auto-cycle: base → orange → grape → mint → cinnabar → gold → amber-brown (gray is for explicit/neutral use) */
:is(.stats,.grid-2,.grid-3,.grid-4,.wave,.quotes,.checklist,.tags,.mini-stats,.fv-row,.ticker-track,.points,.hbars,.meters,.process,.tree-kids,.data > tbody) > :nth-child(7n+1):not([class*="tone-"]) { --tone: var(--accent-mid); --tone-rgb: var(--mid-rgb); --tone-ink: var(--accent); }
:is(.stats,.grid-2,.grid-3,.grid-4,.wave,.quotes,.checklist,.tags,.mini-stats,.fv-row,.ticker-track,.points,.hbars,.meters,.process,.tree-kids,.data > tbody) > :nth-child(7n+2):not([class*="tone-"]) { --tone: var(--c-orange); --tone-rgb: var(--c-orange-rgb); --tone-ink: var(--c-orange-ink); }
:is(.stats,.grid-2,.grid-3,.grid-4,.wave,.quotes,.checklist,.tags,.mini-stats,.fv-row,.ticker-track,.points,.hbars,.meters,.process,.tree-kids,.data > tbody) > :nth-child(7n+3):not([class*="tone-"]) { --tone: var(--c-grape); --tone-rgb: var(--c-grape-rgb); --tone-ink: var(--c-grape-ink); }
:is(.stats,.grid-2,.grid-3,.grid-4,.wave,.quotes,.checklist,.tags,.mini-stats,.fv-row,.ticker-track,.points,.hbars,.meters,.process,.tree-kids,.data > tbody) > :nth-child(7n+4):not([class*="tone-"]) { --tone: var(--c-mint); --tone-rgb: var(--c-mint-rgb); --tone-ink: var(--c-mint-ink); }
:is(.stats,.grid-2,.grid-3,.grid-4,.wave,.quotes,.checklist,.tags,.mini-stats,.fv-row,.ticker-track,.points,.hbars,.meters,.process,.tree-kids,.data > tbody) > :nth-child(7n+5):not([class*="tone-"]) { --tone: var(--c-cinnabar); --tone-rgb: var(--c-cinnabar-rgb); --tone-ink: var(--c-cinnabar-ink); }
:is(.stats,.grid-2,.grid-3,.grid-4,.wave,.quotes,.checklist,.tags,.mini-stats,.fv-row,.ticker-track,.points,.hbars,.meters,.process,.tree-kids,.data > tbody) > :nth-child(7n+6):not([class*="tone-"]) { --tone: var(--c-gold); --tone-rgb: var(--c-gold-rgb); --tone-ink: var(--c-gold-ink); }
:is(.stats,.grid-2,.grid-3,.grid-4,.wave,.quotes,.checklist,.tags,.mini-stats,.fv-row,.ticker-track,.points,.hbars,.meters,.process,.tree-kids,.data > tbody) > :nth-child(7n+7):not([class*="tone-"]) { --tone: var(--c-amber-brown); --tone-rgb: var(--c-amber-brown-rgb); --tone-ink: var(--c-amber-brown-ink); }
.mono :is(.stats,.grid-2,.grid-3,.grid-4,.wave,.quotes,.checklist,.tags,.mini-stats,.fv-row,.ticker-track,.points,.hbars,.meters,.process,.tree-kids,.data > tbody) > * { --tone: var(--accent-mid); --tone-rgb: var(--mid-rgb); --tone-ink: var(--accent); } /* .mono on a slide = single colour */

/* === 2. RESET === */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 100%; height: 100%; overflow: hidden; background: var(--letterbox); }
html { touch-action: manipulation; }
body { font-family: var(--font-sans); color: var(--text-1); -webkit-font-smoothing: antialiased; }
a { color: inherit; text-decoration: none; }
img { display: block; max-width: 100%; }
button { cursor: pointer; border: none; background: none; font-family: inherit; color: inherit; }
:is(button, a, [tabindex]):focus-visible { outline: 3px solid var(--accent-mid); outline-offset: 4px; border-radius: 6px; }
.sprite { position: absolute; width: 0; height: 0; overflow: hidden; }   /* icon <symbol> sheet */
.ico { width: 46%; height: 46%; flex-shrink: 0; }                         /* <svg class="ico" aria-hidden="true"><use href="#i-bolt"/></svg> */
em { font-style: italic; font-family: var(--font-serif); color: var(--accent); font-weight: 600; }

/* === 3. FIXED STAGE (do not change) === */
.deck-viewport { position: fixed; inset: 0; overflow: hidden; background: var(--letterbox); }
.deck-stage {
  position: absolute; left: 0; top: 0; width: 1920px; height: 1080px;
  overflow: hidden; transform-origin: 0 0; background: var(--bg);
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
  background: var(--bg);
  transition: opacity 0.6s var(--silk), visibility 0s linear 0.6s;
}
.slide.active { visibility: visible; opacity: 1; pointer-events: auto; z-index: 1; transition: opacity 0.6s var(--silk); }
.slide.alt     { background: var(--surface); }
.slide:not(.dark)::after { content: ''; position: absolute; left: 0; right: 0; bottom: 0; height: 14px; z-index: 2; pointer-events: none;
  background: linear-gradient(105deg, var(--accent-mid) 0 33%, transparent 33% 33.5%, var(--c-mint) 33.5% 66.5%, transparent 66.5% 67%, var(--c-orange) 67%); }
.slide > *     { position: relative; z-index: 1; }

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
.deck-logo { font-size: 30px; font-weight: 700; letter-spacing: -0.04em; color: var(--text-1); }
.deck-logo span { color: var(--accent); }
.deck-meta { display: flex; align-items: center; gap: 18px; }
.deck-section {
  font-size: 18px; font-weight: 500; color: var(--text-2); padding: 10px 24px; border-radius: 100px;
  background: var(--accent-ghost); box-shadow: inset 0 0 0 1px var(--accent-border);
  transition: opacity 0.4s var(--silk);
}
.deck-count { font-size: 18px; font-weight: 600; color: var(--text-3); font-variant-numeric: tabular-nums; min-width: 72px; text-align: right; }
.deck-dots {
  position: absolute; bottom: 44px; left: 50%; transform: translateX(-50%); z-index: 40;
  display: flex; gap: 12px; align-items: center;
}
.deck-dot { width: 12px; height: 12px; border-radius: 50%; background: var(--accent-border); cursor: pointer; transition: width 0.4s var(--silk), background-color 0.4s var(--silk); }
.deck-dot.active { background: var(--accent); width: 40px; border-radius: 6px; }
.deck-stage.on-dark .deck-logo { color: #fff; }
.deck-stage.on-dark .deck-section { color: rgba(255,255,255,0.7); background: rgba(255,255,255,0.06); box-shadow: inset 0 0 0 1px rgba(255,255,255,0.12); }
.deck-stage.on-dark .deck-dot { background: rgba(255,255,255,0.18); }
.deck-stage.on-dark .deck-dot.active { background: var(--accent-light); }

/* === 5. TYPOGRAPHY PRIMITIVES === */
.label {
  display: flex; flex-direction: column; align-self: flex-start; width: max-content;
  font-size: var(--fs-label); font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--accent); margin-bottom: 26px;
}
/* three slanted colour dashes above every label: base · mint · orange */
.label::before { content: ''; width: 116px; height: 10px; margin: 0 0 18px 4px; transform: skewX(-32deg);
  background: linear-gradient(90deg, var(--accent-mid) 0 30%, transparent 30% 35%, var(--c-mint) 35% 65%, transparent 65% 70%, var(--c-orange) 70%); }
.center .label { align-self: center; align-items: center; }
.title { font-size: var(--fs-title); font-weight: 700; letter-spacing: -0.035em; line-height: 1.1; color: var(--text-1); text-wrap: balance; }
.title.hero { font-size: var(--fs-hero); letter-spacing: -0.045em; line-height: 1.04; }
.h3 { font-size: var(--fs-h3); font-weight: 700; letter-spacing: -0.03em; line-height: 1.15; text-wrap: balance; }
.lead { font-size: var(--fs-lead); line-height: 1.6; color: var(--text-2); max-width: 1000px; margin-top: 28px; }
.body { font-size: var(--fs-body); line-height: 1.65; color: var(--text-2); }
.kicker { font-size: 18px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: var(--tone-ink, var(--c-orange-ink)); margin-bottom: 22px; }
.center { text-align: center; align-items: center; }
.center .lead { margin-left: auto; margin-right: auto; }
.head { margin-bottom: 64px; display: flex; flex-direction: column; }
.head.center .lead { text-align: center; }

/* === 6. REVEAL ANIMATION (fires when a slide becomes active) === */
.reveal { opacity: 0; transform: translateY(36px); transition: opacity 0.8s var(--silk), transform 0.8s var(--silk); }
.slide.visible .reveal { opacity: 1; transform: none; }
.d1 { transition-delay: 0.10s; } .d2 { transition-delay: 0.20s; } .d3 { transition-delay: 0.30s; }
.d4 { transition-delay: 0.40s; } .d5 { transition-delay: 0.50s; } .d6 { transition-delay: 0.60s; }

/* === 7. COMPONENTS === */

/* 7a. Badge pill (hero) */
.badge {
  display: inline-flex; align-items: center; gap: 14px; align-self: flex-start;
  background: var(--surface-2); border: 1.5px solid var(--accent-border); border-radius: 100px;
  padding: 9px 26px 9px 10px; margin-bottom: 40px; box-shadow: var(--shadow-sm);
  font-size: 21px; font-weight: 500; color: var(--text-2);
}
.badge-dot { width: 38px; height: 38px; border-radius: 50%; background: var(--accent); color: #fff;
  display: flex; align-items: center; justify-content: center; font-size: 17px; font-weight: 700; }
.badge strong { color: var(--accent); }

/* 7b. Buttons / chips */
.btn { display: inline-flex; align-items: center; gap: 14px; font-size: 24px; font-weight: 600; padding: 22px 46px; border-radius: 100px; }
.btn-primary { color: #fff; background: var(--accent); box-shadow: 0 10px 36px rgba(var(--accent-rgb),0.30); }
.btn-outline { color: var(--accent); border: 2px solid var(--accent-border); }
.row { display: flex; align-items: center; gap: 20px; flex-wrap: wrap; }

/* 7c. Trust / meta row */
.trust { display: flex; align-items: center; gap: 30px; margin-top: 64px; }
.trust-item { display: flex; align-items: center; gap: 12px; font-size: 20px; font-weight: 500; color: var(--text-3); }
.trust-item svg { color: var(--accent); width: 24px; height: 24px; flex-shrink: 0; }
.trust-divider { width: 1.5px; height: 30px; background: var(--border); }

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
  background: var(--tone, var(--accent)); box-shadow: var(--badge-shadow);
  display: flex; align-items: center; justify-content: center; color: #fff; font-size: 18px; font-weight: 700; font-variant-numeric: tabular-nums;
}
.check b { color: var(--text-1); font-weight: 600; }
.checklist.two-col { display: grid; grid-template-columns: 1fr 1fr; column-gap: 72px; row-gap: 30px; }

/* 7e-2. Points — icon circle + coloured caps label + text (template "mind map" column) */
.points { display: flex; flex-direction: column; gap: 34px; }
.point { display: grid; grid-template-columns: 84px 1fr; column-gap: 28px; align-items: center; }
.point-icon { width: 84px; height: 84px; border-radius: 50%; background: var(--tone, var(--accent)); color: #fff; border: 6px solid var(--surface-2);
  box-shadow: var(--badge-shadow); display: flex; align-items: center; justify-content: center; }
.point-k { font-size: 18px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--tone-ink, var(--accent)); margin-bottom: 6px; }
.point-d { font-size: 22px; line-height: 1.5; color: var(--text-2); text-wrap: pretty; }

/* 7e-3. Side panel — tinted block filling the right part of the slide, big text (template quote panel) */
.slide > .side-panel { position: absolute; top: 0; right: 0; bottom: 0; width: 44%; z-index: 0;
  background: rgba(var(--mid-rgb),0.14); padding: var(--pad-top) var(--pad-x) var(--pad-bottom) 96px;
  display: flex; flex-direction: column; justify-content: center; }
.side-panel + * { max-width: 48%; }
.panel-text { font-size: 48px; line-height: 1.3; font-weight: 400; letter-spacing: -0.015em; color: var(--text-1); text-wrap: pretty; }
.panel-cta { margin-top: 48px; font-size: 64px; font-weight: 700; letter-spacing: -0.03em; color: var(--accent); }
.panel-sub { font-size: 24px; color: var(--text-2); margin-top: 8px; }

/* 7e-4. Note band — gray strip: big label | divider | text (template footer band) */
.note-band { display: grid; grid-template-columns: auto 1fr; align-items: center; column-gap: 40px; margin-top: 48px;
  background: var(--track); padding: 30px 44px; }
.note-band-k { font-size: 34px; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; line-height: 1.1; color: var(--text-1);
  padding-right: 40px; border-right: 3px solid var(--accent-mid); }
.note-band-d { font-size: 21px; line-height: 1.55; color: var(--text-2); text-wrap: pretty; }

/* 7f. Window / dashboard card (hero visual, screenshots) */
.window { background: var(--surface-2); border-radius: var(--radius-lg); border: 1.5px solid var(--border); box-shadow: var(--shadow-lg); overflow: hidden; }
.window-bar { background: var(--bg-alt); padding: 18px 24px; display: flex; gap: 12px; border-bottom: 1.5px solid var(--border); }
.window-bar i { width: 15px; height: 15px; border-radius: 50%; display: block; }
.window-bar i:nth-child(1) { background: #FF5F57; } .window-bar i:nth-child(2) { background: #FFBD2E; } .window-bar i:nth-child(3) { background: #28CA41; }
.window-body { padding: 40px; }
.window img { width: 100%; height: auto; display: block; }
.win-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; }
.win-title { font-size: 24px; font-weight: 600; }
.tag { font-size: 16px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--accent);
  background: var(--accent-ghost); border: 1.5px solid var(--accent-border); padding: 5px 16px; border-radius: 100px; }
.bars { height: 150px; display: flex; align-items: flex-end; gap: 12px; margin-bottom: 32px; }
.bar { flex: 1; border-radius: 6px 6px 0 0; background: var(--accent-ghost); border: 1.5px solid var(--accent-border); height: 0; transition: height 1.2s var(--silk) 0.2s; }
.slide.visible .bar { height: var(--h); }
.bar.on { background: var(--accent); border-color: var(--accent); }
.mini-stats { display: grid; grid-template-columns: repeat(3,1fr); gap: 18px; }
.mini-stat { background: var(--bg); border-radius: var(--radius); padding: 22px; border: 1.5px solid var(--border); }
.mini-val { font-size: 36px; font-weight: 700; letter-spacing: -0.03em; }
.mini-val small { font-size: 22px; color: var(--tone-ink, var(--accent)); }
.mini-label { font-size: 17px; color: var(--text-3); margin-top: 4px; }
.mini-chg { font-size: 17px; font-weight: 600; color: var(--tone-ink, var(--accent)); margin-top: 6px; }
.mini-stat { border-top: 3px solid var(--tone, var(--accent)) !important; }

/* Floating badges on a visual */
.visual { position: relative; }
.float { position: absolute !important; display: flex; align-items: center; gap: 16px; background: var(--surface-2);
  border: 1.5px solid var(--border); border-radius: var(--radius); padding: 18px 24px; box-shadow: var(--shadow-md);
  animation: floaty 4s ease-in-out infinite; z-index: 2; }
.float-icon { width: 54px; height: 54px; border-radius: 15px; background: var(--tone, var(--c-grape)); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 24px; }
.float-text { font-size: 18px; line-height: 1.35; } .float-text strong { display: block; color: var(--text-1); } .float-text span { color: var(--text-3); }
.float.solid { background: var(--accent); border-color: var(--accent); box-shadow: 0 14px 40px rgba(var(--accent-rgb),0.35); display: block; animation-delay: 2s; }
.float.solid .fv { font-size: 38px; font-weight: 700; color: #fff; letter-spacing: -0.03em; }
.float.solid .fl { font-size: 17px; color: rgba(255,255,255,0.75); margin-top: 2px; }
@keyframes floaty { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-9px); } }

/* 7g. Feature panel (fv-cards) */
.panel { background: rgba(var(--mid-rgb),0.13); padding: 52px; display: flex; flex-direction: column; gap: 22px; }
.fv-row { display: flex; gap: 22px; }
.fv-card { flex: 1; background: var(--surface-2); border-radius: 4px; padding: 26px 28px; box-shadow: 0 6px 20px rgba(var(--ink-rgb),0.07); }
.fv-row > .fv-card { border-top: 6px solid var(--tone, var(--accent)); }
.fv-card.wide { flex: 2; }
.fv-label { font-size: 16px; color: var(--tone-ink, var(--text-3)); font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 10px; }
.fv-val { font-size: 44px; font-weight: 700; letter-spacing: -0.03em; font-variant-numeric: tabular-nums; }
.fv-track { height: 10px; border-radius: 5px; margin-top: 16px; background: var(--track); overflow: hidden; }
.fv-fill { height: 100%; border-radius: 4px; background: var(--tone, var(--accent)); width: 0; transition: width 1.4s var(--silk) 0.3s; }
.slide.visible .fv-fill { width: var(--w); }
.fv-list { display: flex; flex-direction: column; gap: 12px; margin-top: 8px; }
.fv-item { display: flex; align-items: center; justify-content: space-between; padding: 14px 0; border-bottom: 1.5px solid var(--border); font-size: 20px; }
.fv-item:last-child { border-bottom: none; }
.fv-item span:first-child { color: var(--text-2); font-weight: 500; }
.pill { font-size: 16px; font-weight: 600; padding: 5px 16px; border-radius: 100px; }
.pill.green { background: rgba(var(--c-mint-rgb),0.14); color: var(--c-mint-ink); }
.pill.red   { background: rgba(var(--c-cinnabar-rgb),0.12); color: var(--c-cinnabar-ink); }
.pill.gold  { background: rgba(var(--c-gold-rgb),0.22); color: var(--c-gold-ink); }
.pill.grape { background: rgba(var(--c-grape-rgb),0.12); color: var(--c-grape-ink); }
.pill.blue  { background: rgba(var(--mid-rgb),0.12); color: var(--accent-mid); }
.pill.dim   { background: var(--border); color: var(--text-3); }
.pill.warn  { background: rgba(var(--c-orange-rgb),0.14); color: var(--c-orange-ink); }

/* 7h. Stats */
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 40px; }
.stats.three { grid-template-columns: repeat(3, 1fr); }
.stat { display: flex; flex-direction: column; }
.stat-value { align-self: flex-start; display: flex; align-items: baseline; gap: 4px; margin-bottom: 26px;
  font-size: 96px; font-weight: 700; letter-spacing: -0.05em; line-height: 1; font-variant-numeric: tabular-nums;
  padding: 22px 32px 18px 26px; color: var(--tone-ink, var(--accent));
  background: rgba(var(--tone-rgb, var(--accent-rgb)),0.13); border-left: 10px solid var(--tone, var(--accent)); }
.stat-suffix { font-size: 50%; font-weight: 600; letter-spacing: -0.02em; }
.stat-label { font-size: 18px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--tone-ink, var(--accent)); margin-bottom: 10px; }
.stat-sub { font-size: 21px; color: var(--text-2); line-height: 1.5; }

/* 7i. Cards (pricing-card style) — options, comparisons, pillars */
/* a card is a tinted column between two thick tone rules (template pricing columns); text is centred */
.card { position: relative; display: flex; flex-direction: column; align-items: center; text-align: center;
  padding: 46px 40px 44px; background: rgba(var(--tone-rgb, var(--accent-rgb)),0.07);
  border-top: 7px solid rgba(var(--tone-rgb, var(--accent-rgb)),0.55); border-bottom: 7px solid rgba(var(--tone-rgb, var(--accent-rgb)),0.55); }
.card-tier { font-size: 18px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: var(--tone-ink, var(--accent)); margin-bottom: 16px; }
.card-big { font-size: 84px; font-weight: 700; letter-spacing: -0.04em; line-height: 1; margin-bottom: 4px; display: flex; flex-direction: column; align-items: center; gap: 8px; font-variant-numeric: tabular-nums; }
.card-big small { font-family: var(--font-serif); font-style: italic; font-size: 26px; font-weight: 600; color: var(--text-3); letter-spacing: 0; }
.card-title { font-size: 32px; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 14px; text-wrap: balance; }
.card-desc { font-size: 21px; color: var(--text-2); line-height: 1.55; margin-top: 14px; text-wrap: pretty; }
.card-divider { align-self: stretch; height: 2px; background: rgba(var(--tone-rgb, var(--accent-rgb)),0.22); margin: 28px 0 26px; }
.card .checklist { margin-top: 0; gap: 16px; align-self: stretch; text-align: left; }
.card .check { font-size: 21px; gap: 16px; }
.card .check-icon { width: 30px; height: 30px; font-size: 14px; box-shadow: none; }
.card-icon { width: 112px; height: 112px; border-radius: 50%; background: var(--tone, var(--accent)); color: #fff; border: 7px solid var(--surface-2);
  box-shadow: var(--badge-shadow); display: flex; align-items: center; justify-content: center; margin-bottom: 28px; }
.card-icon svg { width: 46px; height: 46px; }
.card.tinted { background: rgba(var(--tone-rgb, var(--accent-rgb)),0.13); }
/* featured = the recommended option: solid base-colour column */
.card.featured { background: var(--accent); border-color: var(--accent); }
.card.featured :is(.card-tier, .card-big, .card-title) { color: #fff; }
.card.featured :is(.card-big small, .card-desc, .check) { color: rgba(255,255,255,0.82); }
.card.featured .card-divider { background: rgba(255,255,255,0.22); }
.card.featured .check-icon { background: #fff; color: var(--accent); }
.card.featured .card-icon { background: #fff; color: var(--accent); }
.card-flag { position: absolute; top: -7px; left: 50%; transform: translate(-50%, -100%); background: var(--c-orange); color: var(--ink);
  font-size: 16px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; padding: 9px 26px; white-space: nowrap; }

/* 7j. Quotes (testimonials) */
.quotes { display: grid; grid-template-columns: 1.15fr 1fr 1fr; grid-template-rows: auto auto; gap: 32px; }
.quote { background: var(--surface-2); border-radius: var(--radius-lg); border: 1.5px solid var(--border); padding: 44px; box-shadow: var(--shadow-sm); display: flex; flex-direction: column; }
.quote.tall { grid-row: span 2; justify-content: space-between; }
.quote-mark { font-family: var(--font-serif); font-size: 96px; line-height: 0.6; color: var(--tone, var(--accent-light)); height: 40px; }
.quote-text { font-size: 23px; line-height: 1.6; color: var(--text-2); font-style: italic; margin: 18px 0 30px; flex: 1; }
.quote.tall .quote-text { font-size: 30px; }
.author { display: flex; align-items: center; gap: 16px; }
.avatar { width: 58px; height: 58px; border-radius: 50%; flex-shrink: 0; border: 2px solid rgba(var(--tone-rgb, var(--accent-rgb)),0.30); background: rgba(var(--tone-rgb, var(--accent-rgb)),0.10);
  display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 20px; color: var(--tone-ink, var(--accent)); }
.author-name { font-size: 21px; font-weight: 600; }
.author-role { font-size: 18px; color: var(--text-3); margin-top: 2px; }

/* 7k. Statement (big quote slide) */
.statement { font-size: 84px; font-weight: 700; letter-spacing: -0.035em; line-height: 1.15; max-width: 1500px; }
.statement-by { margin-top: 56px; }

/* 7l. Tag cloud (integration pills) */
.tags { display: flex; flex-wrap: wrap; gap: 18px; justify-content: center; max-width: 1400px; margin: 0 auto; }
.tag-pill { background: var(--surface-2); border-radius: 100px; border: 1.5px solid var(--border); padding: 18px 36px; box-shadow: var(--shadow-sm);
  font-size: 24px; font-weight: 600; color: var(--text-2); white-space: nowrap; letter-spacing: -0.01em; }
.tag-pill.hl { border-color: rgba(var(--tone-rgb, var(--accent-rgb)),0.30); background: rgba(var(--tone-rgb, var(--accent-rgb)),0.10); color: var(--tone-ink, var(--accent)); }

/* 7m. Ticker (logo strip) */
.ticker { border-top: 1.5px solid var(--border); border-bottom: 1.5px solid var(--border); background: var(--surface); padding: 34px 0; overflow: hidden;
  margin: 0 calc(-1 * var(--pad-x)); }
.ticker-label { text-align: center; font-size: 17px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-3); font-weight: 600; margin-bottom: 26px; }
.ticker-track { display: flex; align-items: center; gap: 90px; width: max-content; animation: ticker 32s linear infinite; }
.ticker:hover .ticker-track { animation-play-state: paused; }
.ticker-item { display: flex; align-items: center; gap: 14px; font-size: 27px; font-weight: 700; letter-spacing: -0.03em; color: var(--text-3); white-space: nowrap; }
.ticker-item i { width: 44px; height: 44px; border-radius: 12px; background: rgba(var(--tone-rgb, var(--accent-rgb)),0.14); border: 1.5px solid rgba(var(--tone-rgb, var(--accent-rgb)),0.32); display: block; }
.ticker-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--accent-light); opacity: 0.5; }
@keyframes ticker { from { transform: translateX(0); } to { transform: translateX(-50%); } }

/* 7n. FAQ / Q&A accordion */
.faq { display: grid; grid-template-columns: 1fr 1.6fr; gap: 110px; align-items: start; }
.faq-item { border-bottom: 1.5px solid var(--border); }
.faq-item:first-child { border-top: 1.5px solid var(--border); }
.faq-q { width: 100%; text-align: left; display: flex; justify-content: space-between; align-items: center; gap: 24px; padding: 30px 0; cursor: pointer; font-size: 27px; font-weight: 600; transition: color 0.3s; }
.faq-q:hover { color: var(--accent); }
.faq-icon { width: 44px; height: 44px; border-radius: 50%; border: 2px solid var(--accent-border); flex-shrink: 0; display: flex; align-items: center; justify-content: center;
  color: var(--accent); font-size: 26px; font-weight: 300; transition: transform 0.5s var(--silk), background 0.4s, color 0.4s; }
.faq-item.open .faq-icon { transform: rotate(45deg); background: var(--accent); color: #fff; border-color: var(--accent); }
.faq-a { display: grid; grid-template-rows: 0fr; transition: grid-template-rows 0.5s var(--silk); }
.faq-item.open .faq-a { grid-template-rows: 1fr; }
.faq-a > div { overflow: hidden; font-size: 23px; line-height: 1.65; color: var(--text-2); transition: padding-bottom 0.5s var(--silk); }
.faq-item.open .faq-a > div { padding-bottom: 30px; }

/* 7o. Wave timeline — icon circles alternate high/low along a wide gray ribbon; text sits above high
   circles and below low ones (template "timeline planning"). Set --n to the number of steps. */
.wave { --row: 176px; --band: 270px; --dot: 132px; display: grid; grid-template-columns: repeat(var(--n, 5), 1fr); position: relative; }
.wave::before { content: ''; position: absolute; left: 0; right: 0; z-index: 0;
  top: calc(var(--row) + var(--dot) / 2 - (var(--band) - var(--dot)) / 8); height: calc((var(--band) - var(--dot)) * 1.25);
  background: var(--track);
  -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 100' preserveAspectRatio='none'%3E%3Cpath d='M0 50 C18 22 32 10 50 10 C68 10 82 22 100 50 C118 78 132 90 150 90 C168 90 182 78 200 50' fill='none' stroke='black' stroke-width='34' vector-effect='non-scaling-stroke'/%3E%3C/svg%3E") repeat-x 0 0 / calc(200% / var(--n, 5)) 100%;
          mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 100' preserveAspectRatio='none'%3E%3Cpath d='M0 50 C18 22 32 10 50 10 C68 10 82 22 100 50 C118 78 132 90 150 90 C168 90 182 78 200 50' fill='none' stroke='black' stroke-width='34' vector-effect='non-scaling-stroke'/%3E%3C/svg%3E") repeat-x 0 0 / calc(200% / var(--n, 5)) 100%; }
.wstep { display: grid; grid-template-rows: var(--row) var(--band) var(--row); justify-items: center; text-align: center; position: relative; z-index: 1; padding: 0 10px; }
.wstep-text { grid-row: 1; align-self: end; padding-bottom: 20px; max-width: 290px; }
.wstep:nth-child(even) .wstep-text { grid-row: 3; align-self: start; padding: 20px 0 0; }
.wstep-dot { grid-row: 2; align-self: start; width: var(--dot); height: var(--dot); border-radius: 50%;
  background: var(--tone, var(--accent)); color: #fff; border: 8px solid var(--surface-2); box-shadow: var(--badge-shadow);
  display: flex; align-items: center; justify-content: center; }
.wstep:nth-child(even) .wstep-dot { align-self: end; }
.wstep.later .wstep-dot { background: var(--surface-2); color: var(--tone-ink, var(--accent)); border: 6px solid var(--tone, var(--accent)); }
.wstep.now .wstep-dot { box-shadow: var(--badge-shadow), 0 0 0 12px rgba(var(--tone-rgb, var(--accent-rgb)),0.22); }
.wstep-when { font-size: 18px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--tone-ink, var(--accent)); font-variant-numeric: tabular-nums; }
.wstep.now .wstep-when::after { content: ' · Now'; color: var(--text-1); }
.wstep-t { font-size: 30px; font-weight: 700; letter-spacing: -0.02em; margin: 6px 0 6px; }
.wstep-d { font-size: 20px; line-height: 1.45; color: var(--text-2); text-wrap: pretty; }

/* 7o-2. Process diagram — a row of thick toothed rings (template "process gear"); text alternates above/below */
.process { display: grid; grid-template-columns: repeat(var(--n, 5), 1fr); }
.pnode { display: grid; grid-template-rows: 186px auto 186px; justify-items: center; text-align: center; }
.pnode-ring { grid-row: 2; position: relative; width: min(268px, calc(100% - 26px)); aspect-ratio: 1; border-radius: 50%;
  background: var(--surface-2); border: 24px solid var(--tone, var(--accent)); outline: 15px dashed var(--tone, var(--accent)); outline-offset: -2px;
  box-shadow: var(--badge-shadow); color: var(--tone-ink, var(--accent)); display: flex; align-items: center; justify-content: center; margin: 15px 0; }
.pnode-ring::before { content: ''; position: absolute; inset: -66px; border-radius: 50%; border: 3px solid var(--track); clip-path: inset(0 0 58% 0); }
.pnode:nth-child(even) .pnode-ring::before { clip-path: inset(58% 0 0 0); }
.pnode-text { grid-row: 1; align-self: end; padding-bottom: 54px; max-width: 280px; position: relative; }
.pnode-text::after { content: ''; position: absolute; left: 50%; bottom: 0; width: 3px; height: 36px; background: var(--track); }
.pnode:nth-child(even) .pnode-text { grid-row: 3; align-self: start; padding: 54px 0 0; }
.pnode:nth-child(even) .pnode-text::after { top: 0; bottom: auto; }
.pnode-k { font-size: 18px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--tone-ink, var(--accent)); margin-bottom: 8px; }
.pnode-d { font-size: 20px; line-height: 1.45; color: var(--text-2); text-wrap: pretty; }

/* 7o-3. Tree diagram — org chart / architecture: boxed nodes with an icon circle on top, joined by lines */
.tree { display: flex; flex-direction: column; align-items: center; --gap: 48px; --stem: 50px; }
.tree-root { position: relative; padding-bottom: var(--stem); }
.tree-root::after { content: ''; position: absolute; left: 50%; bottom: 0; width: 3px; height: var(--stem); background: var(--accent-mid); transform: translateX(-50%); }
.tree-kids { display: grid; grid-template-columns: repeat(var(--n, 3), 1fr); column-gap: var(--gap); width: 100%; }
.tree-kid { position: relative; padding-top: calc(var(--stem) + 50px); display: flex; justify-content: center; }
.tree-kid::before { content: ''; position: absolute; top: 0; left: calc(var(--gap) / -2); right: calc(var(--gap) / -2); height: 3px; background: var(--accent-mid); }
.tree-kid:first-child::before { left: 50%; } .tree-kid:last-child::before { right: 50%; }
.tree-kid::after { content: ''; position: absolute; top: 0; left: 50%; width: 3px; height: var(--stem); background: var(--tone, var(--accent-mid)); transform: translateX(-50%); }
.tnode { position: relative; width: 100%; max-width: 440px; text-align: center; background: var(--surface-2); border: 3px solid var(--tone, var(--accent)); border-radius: 10px;
  padding: 64px 28px 26px; box-shadow: 0 10px 28px rgba(var(--ink-rgb),0.08); }
.tree-root .tnode { min-width: 520px; }
.tnode-icon { position: absolute; top: 0; left: 50%; transform: translate(-50%, -50%); width: 100px; height: 100px; border-radius: 50%;
  background: var(--tone, var(--accent)); color: #fff; border: 6px solid var(--surface-2); box-shadow: var(--badge-shadow); display: flex; align-items: center; justify-content: center; }
.tnode-k { font-size: 17px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--tone-ink, var(--accent)); }
.tnode-t { font-size: 28px; font-weight: 700; letter-spacing: -0.02em; margin: 6px 0 6px; }
.tnode-d { font-size: 19px; line-height: 1.45; color: var(--text-2); }

/* 7p. Table */
.table-wrap { background: var(--track); padding: 20px 26px; }
table.data { width: 100%; border-collapse: separate; border-spacing: 10px 10px; font-size: 22px; font-variant-numeric: tabular-nums; }
table.data th { text-align: left; font-size: 16px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-2);
  background: var(--surface-2); padding: 16px 26px; border-bottom: 4px solid var(--accent-mid); box-shadow: 0 3px 10px rgba(var(--ink-rgb),0.06); }
table.data td { padding: 18px 26px; background: var(--surface-2); color: var(--text-2); border-radius: 4px; }
table.data :is(th, td):first-child { background: transparent; box-shadow: none; border-bottom: none; padding-left: 4px; }
table.data td:first-child { color: var(--text-1); font-weight: 700; display: flex; align-items: center; gap: 16px; }
table.data td:first-child::before { content: ''; width: 18px; height: 18px; border-radius: 50%; flex-shrink: 0; background: var(--tone, var(--accent)); box-shadow: 0 0 0 5px rgba(var(--tone-rgb, var(--accent-rgb)),0.18); }
table.data tr.hl td:not(:first-child) { background: rgba(var(--tone-rgb, var(--accent-rgb)),0.16); color: var(--text-1); font-weight: 700; }
table.data .num { text-align: right; }

/* 7p-2. Charts */
.chart-k { font-size: 18px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-2); margin-bottom: 26px; }
/* horizontal bars: icon circle · caps label · thick bar on a light rail · value (template "bar chart") */
.hbars { display: grid; grid-template-columns: auto max-content 1fr auto; column-gap: 24px; row-gap: 20px; align-items: center; }
.hbar { display: contents; }
.hbar-icon, .lc-icon { width: 60px; height: 60px; border-radius: 50%; background: var(--surface-2); color: var(--tone-ink, var(--accent)); border: 3px solid var(--tone, var(--accent));
  box-shadow: var(--badge-shadow); display: flex; align-items: center; justify-content: center; }
.hbar-label { font-size: 18px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-2); }
.hbar-track { height: 34px; background: var(--track); border-radius: 0 8px 8px 0; }
.hbar-fill { height: 100%; width: 0; border-radius: 0 8px 8px 0; background: var(--tone, var(--accent)); transition: width 1.2s var(--silk) 0.3s;
  box-shadow: 0 4px 12px rgba(var(--tone-rgb, var(--accent-rgb)),0.30); }
.slide.visible .hbar-fill { width: var(--v); }
.hbar-val { font-size: 26px; font-weight: 700; color: var(--tone-ink, var(--accent)); font-variant-numeric: tabular-nums; min-width: 84px; text-align: right; }
/* donut: ring of segments in the middle, callouts with dashed leader lines on both sides (template "line and bar chart") */
.donut-chart { display: grid; grid-template-columns: 1fr auto 1fr; column-gap: 40px; align-items: center; }
.donut { position: relative; width: 500px; aspect-ratio: 1; }
.donut svg { width: 100%; height: 100%; transform: rotate(-90deg); overflow: visible; }
.dn-track { fill: none; stroke: var(--track); stroke-width: 26; }
.dn-seg { fill: none; stroke: var(--tone, var(--accent-mid)); stroke-width: 26; stroke-dasharray: 0 100; stroke-dashoffset: calc(-1 * var(--o)); transition: stroke-dasharray 1.4s var(--silk) 0.3s; }
.slide.visible .dn-seg { stroke-dasharray: var(--p) 100; }
.donut-center { position: absolute; inset: 22%; border-radius: 50%; background: var(--surface-2); box-shadow: var(--badge-shadow);
  display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 24px; }
.dc-big { font-size: 64px; font-weight: 700; letter-spacing: -0.04em; color: var(--text-1); font-variant-numeric: tabular-nums; line-height: 1; }
.dc-cap { font-size: 16px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-3); margin-top: 10px; }
.donut-side { display: flex; flex-direction: column; gap: 52px; }
.dc { position: relative; padding-bottom: 18px; border-bottom: 2.5px dashed rgba(var(--tone-rgb, var(--accent-rgb)),0.55); }
.dc::after { content: ''; position: absolute; bottom: -7px; right: -6px; width: 12px; height: 12px; border-radius: 50%; background: var(--tone, var(--accent)); }
.donut-side.right .dc { text-align: right; } .donut-side.right .dc::after { right: auto; left: -6px; }
.dc-head { display: flex; align-items: baseline; justify-content: space-between; gap: 20px; }
.donut-side.right .dc-head { flex-direction: row-reverse; }
.dc-k { font-size: 18px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--tone-ink, var(--accent)); }
.dc-v { font-size: 44px; font-weight: 700; letter-spacing: -0.03em; color: var(--tone-ink, var(--accent)); font-variant-numeric: tabular-nums; }
.dc-d { font-size: 20px; line-height: 1.45; color: var(--text-2); margin-top: 6px; }
/* line chart: soft gridlines, one coloured line + tint per series, end-value bubbles, tinted icon legend on the right */
.line-chart { display: grid; grid-template-columns: 1fr 420px; column-gap: 140px; align-items: center; }
.lc-plot { display: grid; grid-template-columns: auto 1fr; grid-template-rows: 440px auto; column-gap: 26px; row-gap: 22px; padding-top: 30px; }
.lc-y { display: flex; flex-direction: column; justify-content: space-between; text-align: right; font-size: 17px; font-weight: 700; color: var(--text-3); font-variant-numeric: tabular-nums; }
.lc-y span { line-height: 0; }
.lc-area { position: relative; background: linear-gradient(rgba(var(--ink-rgb),0.09) 2px, transparent 2px) 0 0 / 100% 33.333%; border-bottom: 3px solid rgba(var(--ink-rgb),0.22); }
.lc-area svg { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; clip-path: inset(-30px 100% -30px -30px); transition: clip-path 1.6s var(--silk) 0.3s; }
.slide.visible .lc-area svg { clip-path: inset(-30px -30px -30px -30px); }
.lc-fill { fill: var(--tone, var(--accent)); fill-opacity: 0.07; }
.lc-line { fill: none; stroke: var(--tone, var(--accent)); stroke-width: 6; stroke-linejoin: round; stroke-linecap: round; vector-effect: non-scaling-stroke; }
.lc-pts { fill: none; stroke: var(--tone, var(--accent)); stroke-width: 18; stroke-linecap: round; vector-effect: non-scaling-stroke; }
.lc-end { position: absolute; left: var(--x); top: var(--y); width: 34px; height: 34px; margin: -17px 0 0 -17px; border-radius: 50%; background: var(--surface-2);
  border: 7px solid var(--tone, var(--accent)); box-shadow: var(--badge-shadow); opacity: 0; transition: opacity 0.5s ease 1.5s; }
.lc-end b { position: absolute; left: calc(100% + 14px); top: 50%; transform: translateY(-50%); padding: 6px 16px; border-radius: 10px; white-space: nowrap;
  background: var(--surface-2); border: 3px solid var(--tone, var(--accent)); box-shadow: var(--badge-shadow);
  font-size: 24px; font-weight: 700; color: var(--tone-ink, var(--accent)); font-variant-numeric: tabular-nums; }
.slide.visible .lc-end { opacity: 1; }
.lc-x { grid-column: 2; position: relative; height: 22px; }
.lc-x span { position: absolute; left: var(--x); transform: translateX(-50%); font-size: 17px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-3); }
.lc-legend { display: flex; flex-direction: column; gap: 22px; }
.lc-key { display: grid; grid-template-columns: auto 1fr auto; column-gap: 20px; align-items: center; padding: 22px 26px;
  background: rgba(var(--tone-rgb, var(--accent-rgb)),0.08); border-left: 10px solid var(--tone, var(--accent)); border-radius: 0 14px 14px 0; }
.lc-k { font-size: 18px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--tone-ink, var(--accent)); }
.lc-d { font-size: 18px; line-height: 1.4; color: var(--text-2); margin-top: 4px; }
.lc-v { font-size: 48px; font-weight: 700; letter-spacing: -0.03em; color: var(--tone-ink, var(--accent)); font-variant-numeric: tabular-nums; }
/* vertical meters: rounded rails with a coloured fill and an icon knob on top (template "comparison") */
.meters { display: flex; justify-content: center; align-items: flex-end; gap: 64px; }
.meter { display: flex; flex-direction: column; align-items: center; width: 170px; text-align: center; }
.meter-val { font-size: 52px; font-weight: 700; letter-spacing: -0.03em; color: var(--tone-ink, var(--accent)); font-variant-numeric: tabular-nums; }
.meter-track { width: 44px; height: 400px; border-radius: 22px; background: var(--track); display: flex; align-items: flex-end; margin: 52px 0 26px; }
.meter-fill { position: relative; width: 100%; height: 0; border-radius: 22px; background: var(--tone, var(--accent)); transition: height 1.3s var(--silk) 0.3s; }
.slide.visible .meter-fill { height: var(--v); }
.meter-knob { position: absolute; top: 0; left: 50%; transform: translate(-50%, -50%); width: 66px; height: 66px; border-radius: 50%;
  background: var(--tone, var(--accent)); color: #fff; border: 6px solid var(--surface-2); box-shadow: var(--badge-shadow); display: flex; align-items: center; justify-content: center; }
.meter-k { font-size: 17px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-2); }
.meter-d { font-size: 19px; line-height: 1.45; color: var(--text-3); margin-top: 6px; }
.yes { color: var(--c-mint-ink); font-weight: 700; } .no { color: var(--text-3); } .bad { color: var(--c-cinnabar-ink); font-weight: 700; }

/* 7q. Phone showcase (3D carousel) */
.phones { position: relative; height: 600px; perspective: 1800px; display: flex; align-items: center; justify-content: center; }
.phone { position: absolute; width: 228px; transition: transform 0.7s var(--silk), opacity 0.7s var(--silk); cursor: pointer; }
.phone-shell { background: var(--shell); border-radius: 40px; padding: 6px;
  box-shadow: 0 0 0 1px rgba(150,166,184,0.5), 0 32px 72px rgba(var(--ink-rgb),0.18), inset 0 1px 0 rgba(255,255,255,0.6); }
.phone-screen { background: var(--bg); border-radius: 34px; overflow: hidden; aspect-ratio: 9 / 19.5; }
.phone-screen img { width: 100%; height: 100%; object-fit: cover; }
.phone-cap { text-align: center; margin-top: 16px; font-size: 20px; font-weight: 600; color: var(--text-2); opacity: 0; transition: opacity 0.4s; }
.phone[data-pos="center"] .phone-cap { opacity: 1; }
.phones-ctl { display: flex; align-items: center; justify-content: center; gap: 28px; margin-top: 4px; }
.round-btn { width: 60px; height: 60px; border-radius: 50%; border: 2px solid var(--accent-border); background: var(--surface-2); color: var(--accent);
  display: flex; align-items: center; justify-content: center; font-size: 24px; transition: background-color 0.4s var(--silk), color 0.4s var(--silk), border-color 0.4s var(--silk); }
.round-btn:hover { background: var(--accent); color: #fff; border-color: var(--accent); }
/* drawn mock screen (when no screenshot available) */
.mock { height: 100%; display: flex; flex-direction: column; padding: 30px 18px 0; gap: 12px; }
.mock-h { font-size: 19px; font-weight: 700; padding: 0 4px; }
.mock-card { background: var(--surface-2); border-radius: 16px; border: 1px solid var(--border); padding: 16px; }
.mock-line { height: 9px; border-radius: 5px; background: var(--bg-alt); margin-top: 8px; }
.mock-line.a { background: var(--accent); width: 45%; } .mock-line.s { width: 70%; }
.mock-big { font-size: 30px; font-weight: 700; letter-spacing: -0.03em; }
.mock-nav { margin-top: auto; display: flex; justify-content: space-around; padding: 14px 0 20px; border-top: 1px solid var(--border); background: var(--surface-2); margin-left: -18px; margin-right: -18px; }
.mock-nav i { width: 24px; height: 24px; border-radius: 50%; background: var(--bg-alt); display: block; } .mock-nav i.on { background: var(--accent); }

/* 7r. Dark CTA / closing banner */
.slide.dark { background: var(--ink); color: #fff; }
.slide.dark .title, .slide.dark .statement { color: #fff; }
.slide.dark em { color: var(--accent-light); }
.slide.dark .lead, .slide.dark .body { color: rgba(255,255,255,0.62); }
.slide.dark .label { color: var(--accent-light); background: transparent; border-color: rgba(var(--light-rgb),0.3); }
.slide.dark .orb-a { background: radial-gradient(ellipse at center, rgba(var(--light-rgb),0.16) 0%, transparent 70%); }
.slide.dark .orb-b { background: radial-gradient(ellipse at center, rgba(var(--light-rgb),0.08) 0%, transparent 70%); }
.cta-box { background: var(--ink); border-radius: var(--radius-lg); padding: 110px; display: flex; align-items: center; justify-content: space-between; gap: 80px; position: relative; overflow: hidden; }
.cta-box::before { content: ''; position: absolute; top: -40%; right: -5%; width: 820px; height: 820px; border-radius: 50%;
  background: radial-gradient(ellipse at center, rgba(var(--light-rgb),0.17) 0%, transparent 70%); }
.cta-box > * { position: relative; }
.cta-box .title { color: #fff; } .cta-box em { color: var(--accent-light); }
.cta-box .lead { color: rgba(255,255,255,0.62); }
.cta-box .label { color: var(--accent-light); background: transparent; border-color: rgba(var(--light-rgb),0.3); }
.cta-actions { display: flex; flex-direction: column; gap: 18px; flex-shrink: 0; }
.btn-ghost-dark { color: rgba(255,255,255,0.7); border: 1.5px solid rgba(255,255,255,0.14); justify-content: center; }
.contact { display: flex; flex-direction: column; gap: 14px; font-size: 22px; color: rgba(255,255,255,0.6); }
.contact b { color: #fff; font-weight: 600; }

/* 7s. Image figure */
.figure { border-radius: var(--radius-lg); overflow: hidden; border: 1.5px solid var(--border); box-shadow: var(--shadow-md); background: var(--surface-2); }
.figure img { width: 100%; height: 100%; object-fit: cover; }
.caption { font-size: 18px; color: var(--text-3); margin-top: 16px; }

/* Speaker notes are never shown */
.notes { display: none !important; }

/* === 8. INLINE EDITING === */
.edit-hotzone { position: fixed; top: 0; left: 0; width: 80px; height: 80px; z-index: 10000; cursor: pointer; }
.edit-toggle { position: fixed; top: 18px; left: 18px; z-index: 10001; width: 48px; height: 48px; border-radius: 50%;
  background: #fff; color: var(--accent); border: 1.5px solid var(--accent-border); box-shadow: 0 6px 20px rgba(var(--ink-rgb),0.12);
  font-size: 20px; display: flex; align-items: center; justify-content: center;
  opacity: 0; pointer-events: none; transition: opacity 0.3s, background 0.3s, color 0.3s; }
.edit-toggle.show, .edit-toggle.active { opacity: 1; pointer-events: auto; }
.edit-toggle.active { background: var(--accent); color: #fff; }
.edit-toast { position: fixed; bottom: 24px; left: 50%; transform: translate(-50%, 20px); z-index: 10002; opacity: 0; pointer-events: none;
  background: var(--ink); color: #fff; font-size: 14px; font-weight: 500; padding: 10px 20px; border-radius: 100px; transition: opacity 0.4s var(--silk), transform 0.4s var(--silk); }
.edit-toast.show { opacity: 1; transform: translate(-50%, 0); }
body.editing [contenteditable="true"] { outline: 2px dashed rgba(var(--accent-rgb),0.35); outline-offset: 6px; border-radius: 6px; cursor: text; }
body.editing [contenteditable="true"]:focus { outline-color: var(--accent); }

/* === 9. PRINT (one slide per page) & REDUCED MOTION === */
@page { size: 1920px 1080px; margin: 0; }
@media print {
  html, body { width: 1920px; height: auto; overflow: visible; background: #fff; }
  .deck-viewport { position: static; overflow: visible; }
  .deck-stage { position: static; width: 1920px; height: auto; transform: none !important; overflow: visible; }
  .deck-stage::after, .deck-nav, .deck-dots, .edit-hotzone, .edit-toggle, .edit-toast, .phones-ctl { display: none !important; }
  .slide { position: relative; visibility: visible !important; opacity: 1 !important; break-after: page; page-break-after: always; }
  .slide:last-child { break-after: auto; page-break-after: auto; }
  .reveal { opacity: 1 !important; transform: none !important; transition: none !important; }
  .bar { height: var(--h) !important; } .fv-fill { width: var(--w) !important; }
  .hbar-fill { width: var(--v) !important; } .meter-fill { height: var(--v) !important; } .dn-seg { stroke-dasharray: var(--p) 100 !important; }
  .lc-area svg { clip-path: none !important; } .lc-end { opacity: 1 !important; transition: none !important; }
  * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.2s !important; }
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
    if ((e.key === ' ' || e.key === 'Enter') && e.target.closest?.('button, a')) return; /* let a focused control handle its own key */
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