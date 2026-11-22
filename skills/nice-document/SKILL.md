---
name: "nice-document"
description: "Create high-quality A4 documents (white papers, business reports, research briefs, executive summaries) as one HTML file that prints cleanly to PDF: dark section bands, stat tiles, charts, tables, pull quotes and process flows in nice-palette colours, DM Sans + Playfair. Use when the user asks for a white paper, report, brief or other polished multi-page document. Optional argument: base colour hex or preset."
---

# Nice Document

Generates single-file HTML documents laid out as fixed **A4 pages (210 × 297 mm)** that look finished on screen and print to PDF one page per sheet. The look is a corporate white-paper style: a full-width dark header band on every page with the section name and number, light rounded panels, big-number stat tiles, simple bar and line charts, dark-header tables, dark pull-quote panels with Playfair Display text, arrow process flows and one-line takeaway banners. Colours come from the **nice-palette** skill, and the DM Sans + Playfair italic accent words, icon circles and side-colour cycle make it a sibling of **nice-presentation**. Colour never appears as a stripe or edge: no multi-colour strips, no coloured top borders, no short bars above titles.

There is **no style-discovery phase**. The look is fixed; your job is content, structure and choosing the right page pattern for each page. The only variations are the base colour (palette argument) and how side colours are spread across items.

## Files in this skill

- `nice-document-sample.html`: a complete 9-page sample that uses every component. **It is the source of the Base CSS and the self-check script.** Read it before generating.
- `palette.py`: generates base-colour tokens for a different base colour (same script as nice-presentation).

## Non-negotiables

1. **One self-contained HTML file.** Inline CSS and JS. The only external resource is the Google Fonts link. Images go in an `assets/` folder next to the file, or are inlined as base64 if the user wants one file.
2. **Copy the whole `<style>` block and the closing `<script>` from `nice-document-sample.html` verbatim.** Edit only `:root` tokens, and put any document-specific rules in a `/* === DOCUMENT-SPECIFIC === */` block at the end of the `<style>`.
3. **Every page is a `<section class="page">` inside `<main class="doc">`.** Pages have a fixed height. Nothing flows from one page to the next: when content does not fit, you move blocks to a new page yourself.
4. **Author sizes in mm and pt**, never px or vw. Never set fixed heights on panels, cards, stats or table cells; let them grow to fit their text. Charts and figures are the only blocks with a set height (`--lc-h`, `--h`, `--fig-h`).
5. **No overflow, no clipped text.** Text must never run outside its card or panel, and tables must never be cut off at the bottom. The self-check script outlines any block that spills (see Verify).
6. Never put workflow text in the document ("template", "layout", "placeholder", file names). Never invent statistics: use the user's numbers, or label sample figures as illustrative.

## Workflow

### Phase 1: Content discovery
Ask together, in one structured question round, only what the user has not already said:
1. **Document type**: White paper / Business report / Research brief / Executive summary / Other.
2. **Length**: Short (3 to 5 pages) / Medium (6 to 10) / Long (11+).
3. **Content**: Full draft ready / Notes and data / Topic only (you research and write).
4. **Branding**: organisation name, document title, date or edition, website, base colour (default blue-green `#0D98BA`).

If the user gave content and is clearly in a hurry, assume Medium and say so.

### Phase 2: Outline
Plan page by page: band title, band number and the blocks on each page. Default arc:

Cover → Contents → Executive summary → [section pages]×N → Conclusion and references.

Rules: one section per page in short papers; a long section may take two pages with the same band title and number. Every content page has 3 to 6 blocks and opens with the main point (a panel with a `.key` line, a `.lead` paragraph or a stat row), then shows the evidence. Use a dark `.quote` or `.banner` at most once per page. For documents over 8 pages, show the outline (one line per page) and get a quick OK before generating.

### Phase 3: Generate
Assemble: head (title + fonts link) → copied `<style>` → `<body><main class="doc">` → pages → `</main>` → copied `<script>` → `</body></html>`. If a palette argument was given, run `python3 palette.py <hex or preset>` from this skill folder and paste its token lines over the same-named lines in `:root` (ignore `--letterbox` and `--shell`).

Copy the structure of the patterns you need from the sample, **never its wording or numbers**.

### Phase 4: Verify (do not skip)
Open the file in headless Chromium and check three things: the self-check result, a picture of every page, and the printed PDF.

```python
import asyncio, sys
from playwright.async_api import async_playwright
async def main(path, outdir):
    async with async_playwright() as p:
        try: b = await p.chromium.launch()
        except Exception: b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = await b.new_page(viewport={'width': 900, 'height': 1200}, device_scale_factor=1.5); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file://' + path); await pg.wait_for_timeout(1500)
        print('overflow blocks:', await pg.evaluate("document.documentElement.dataset.overflow"))
        print('under-filled pages:', await pg.evaluate("document.documentElement.dataset.underfilled") or 'none')
        pages = await pg.query_selector_all('.page')
        for i, el in enumerate(pages): await el.screenshot(path=f'{outdir}/page-{i+1:02d}.png')
        await pg.emulate_media(media='print')
        await pg.pdf(path=f'{outdir}/document.pdf', prefer_css_page_size=True, print_background=True)
        pdf = open(f'{outdir}/document.pdf', 'rb').read()
        print('html pages:', len(pages), 'pdf pages:', pdf.count(b'/MediaBox'))
        print('JS errors:', errs); await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2]))
```

Without Playwright, any Chrome or Edge can do the PDF part: `chrome --headless=new --no-pdf-header-footer --virtual-time-budget=8000 --print-to-pdf=out.pdf file:///path/doc.html`, and `--dump-dom` shows the `data-overflow` and `data-underfilled` attributes on `<html>`. Every PDF page should have `/MediaBox [0 0 595 842]` (A4 in points, give or take a fraction).

Pass criteria:
- `overflow blocks: 0`. If not, the flagged block has a dashed red outline on screen: shorten it, move a block to another page, or split the page.
- `pdf pages` equals `html pages`. One more PDF page than HTML pages means a page overflowed in print.
- No page under 70% full (`data-underfilled`). Fix by enlarging charts (`--lc-h`, `--h`, `--fig-h`), adding a block that carries real content, merging with the next page, or adding `.spread` to `.content` to share the spare room evenly.
- Look at every page picture for cramped text, single orphan words in headings, tables with one-word columns, and empty-looking areas.

### Phase 5: Deliver
Save `<document-name>.html` (plus `assets/` if any) where the user asked, or next to their files. Tell the user the page count, that **Ctrl+P → Save as PDF** with margins "None" and "Background graphics" on gives the PDF (A4 is set by the page), and offer to export the PDF yourself with the script above. Mention the base colour used.

## Colour system

Colours come from **nice-palette**. If that skill is available and its values differ from the `:root` tokens in the sample (it was updated later), its colours win: copy its values over the matching tokens.

How the template's colours map to the palette:

| Template colour | Role | nice-palette token |
|---|---|---|
| Navy header band, table header, quote and banner panels | Dark structure | `--ink` `#0E2025` |
| Bright blue big numbers, bold key lines | Accent text | `--accent` `#0A748D` |
| Blue and cyan chart bars and lines | Data fills | `--accent-mid` `#0D98BA`, then the side-colour cycle |
| Light cyan highlighted tile or card | Highlighted item | solid `--accent` stat (`.stat.hl`), stronger tint card (`.card.hl`) |
| Light gray panels and cards | Panels | `--surface` `#F0F9FB` |
| Teal cover band | Cover | `--accent-mid` with `--bg` above it |

Rules:
- **Base colour carries the structure**: band numbers, accent text, key lines, single-series charts, highlights. Side colours only decorate repeated items: the tint and number colour of stat tiles, card tints and icon circles, flow step circles, second and later chart series. Never mark a tile or card with a coloured top edge or a short bar above its title; colour comes from the tint and the icon circle, as in nice-presentation. Never use side colours for headings or body text.
- **Four colours at most.** A document uses the base colour plus three side colours, dark orange, grape and mint, and nothing else. nice-palette also defines gold and amber brown; this skill does not use them. Cinnabar red is the one exception: it marks failed, negative or high-risk status only (`.pill.bad`) and never decorates items. Neutrals (white, `--ink`, the text grays and metallic gray for inactive items) do not count as colours. If the base colour is close to one of the three (for example a plum or mint base), use the other two side colours instead of bringing in a new one.
- **`.tone-cycle`** on a container colours its children in order: blue-green → orange → grape → mint, then repeat. Add it to rows of stats, cards and flows. Use an explicit `.tone-*` class when colour carries meaning.
- **Charts**: one series is blue-green only; never colour each bar differently just for decoration. A second series is orange (`.tone-orange`). Mark one bar as special with `.tone-ink` or a `.tone-*` that means something.
- **Status pills** have fixed meanings: `.pill.ok` mint (done, good), `.pill.warn` orange (in progress, medium), `.pill.bad` cinnabar red (failed, high risk; the one colour allowed outside the four), `.pill.info` blue-green (planned, active), `.pill.off` gray (queued, inactive).

## Palette argument

One optional argument: a base colour as a hex code or preset name (`blue-green` #0D98BA default, `steel-blue` #4682B4, `teal` #2A9D8F, `plum` #9A4A9A, `amber` #C27530). Run `python3 palette.py "#4682B4"` and paste its output over the matching `:root` lines; side colours stay the same. If the base is close to a side colour, give clashing items an explicit `.tone-*`.

## Page patterns (from the reference templates)

Each pattern below is used in the sample; find it by the comment above each `<section>`.

1. **Cover** (`.page.cover`, sample page 1): the page is split, light `--bg` on top and the base colour below. A white rounded card floats across the split. Inside the card: a spaced caps eyebrow (`.cover-eyebrow`, series or organisation), a large Playfair title (`.cover-title`, with one `<em>` word), the document kind in spaced caps at the bottom of the card (`.cover-kind`, for example "White paper"), and a 2 to 3 sentence abstract (`.cover-abstract`). Under the card, white text on the base colour: organisation and website on the left, date and edition on the right (`.cover-foot`). The cover has no band and no footer.
2. **Section page shell** (every other page): `header.band` with `.band-t` (section name, set in spaced caps) and `.band-n` (two-digit section number), then `.content` with the blocks, then `footer.foot` with "Document title · Year". The page number is added automatically and counts the cover as page 1.
3. **Contents** (sample page 2): `ol.toc` rows with section number, title, a short description and page number, followed by an "About this paper" panel.
4. **Executive summary** (sample page 3): a 2 × 2 grid of stat tiles beside a horizontal bar chart, then a table beside a text panel that ends in a bold `.key` finding, then a dark pull quote.
5. **Text page** (sample page 4): a `.lead` paragraph, two-column prose (`.prose.cols-2` with `.h3` subheads, paragraphs and lists), a small chart or panel, and a `.note` summary. Use this for narrative sections; the reference templates have no long prose, so this page keeps the same components around the text.
6. **Landscape page** (sample page 5): text panel and figure on the left, line chart on the right, then a full-width table with a highlighted row, a note, and a row of three stats.
7. **Model page** (sample page 6): a centred panel with a big arrow chain (`.big-line`) beside stacked cards, a dark process flow (`.flow.dark`), a row of four centred cards, then a table with status pills beside a dark checklist panel.
8. **Metrics page** (sample page 7): four stat tiles, a line chart beside a column chart, three cards (success factors, quick wins, common mistakes) and a dark banner.
9. **Roadmap page** (sample page 8): trend list panel beside a priority bar chart, a phased flow (`.flow.phases`, Now / Next / Later), three time-horizon cards, a status table and a best-practice note.
10. **Conclusion page** (sample page 9): a large Playfair closing statement (`.closing-h`), a centred summary panel, numbered takeaways (`ol.steps`) beside a quote, a references table and a closing banner.

## Components

- **Layout**: `.row` two equal columns (`.c3`, `.c4`, `.c5`, `.wide-l` 3:2, `.wide-r` 2:3, `.top` to stop equal heights), `.stack` vertical group, `.center`, `.content.spread` to share spare height between blocks.
- **Type**: `.h2`, `.h3`, `.lead`, `.muted`, `.small`, `em` (Playfair italic in accent, one short phrase per heading at most), `.prose`, `.cols-2`.
- **Panels**: `.panel` (`.tint`, `.dark`, `.center`, `.mid` to centre vertically) with `.panel-t` title and `.key` bold accent line, `.big-line` arrow chain with `<span class="arr">→</span>`, `.quote` (`<p>` + `<cite>`), `.banner` (`<b>` for the accent words), `.note` (left-border callout, `<b>` for accent words).
- **Lists**: `ul.ticks` mint check circles, `ol.steps` numbered circles, plain `ul`/`ol` inside `.prose` or `.panel`.
- **Stats**: `.stat` is a tile tinted in its tone, with `.stat-v` (big number in the tone's -ink), `.stat-k` (short caps label in the same colour) and optional `.stat-d` (detail line). `.stat.hl` makes the one featured number a solid base-colour tile with white text; use it at most once per row.
- **Cards**: `.card` is tinted in its tone and starts with an icon circle: `<div class="card-icon"><svg class="ico" aria-hidden="true"><use href="#i-NAME"/></svg></div>`, then `.card-t` and `.card-d`. `.card.hl` is a stronger tint. `.card.row-icon` puts the icon beside the title and text, which saves height in stacked cards or full pages. Pick an icon that matches the meaning. The icon sheet (`<svg class="sprite">` right after `<body>`) holds `bolt shield layers users chart trend search eye chat server database globe cube cash flag check alert`; copy it from the sample and add a `<symbol>` (24 × 24, stroke `currentColor`, outline style) for any other icon.
- **Process flows**: `.flow` with `span.step` items (numbered circles and arrows are automatic; `.dark` for the navy version, `.phases` for "<b>Now:</b> text" steps, optional `span.flow-cap` caption).
- **Tables**: `table.data` with `thead`; `tr.hl` highlighted row, `.num` right-aligned numbers, `.pill` status marks; `.cap` caption under a table or chart.
- **Charts** (all with a `.chart-t` title, units in a `<span>`):
  - Horizontal bars: `.hbars` > `.hbar` with `style="--v:72%"` (value ÷ axis max), `.hbar-k` label, `.hbar-track > .hbar-fill`, `.hbar-v` value. Set `--hbar-k` on `.hbars` to change the label column width.
  - Columns: `.vbars` (`style="--h:60mm"`) > `.vbar` with `--v`, holding `.vbar-col > .vbar-v`; labels go in a following `.vbars-x` with one `span` per column.
  - Line chart: `.lc` (`style="--lc-h:60mm"`) holding `.lc-y` (axis labels top to bottom), `.lc-plot` with an SVG `viewBox="0 0 100 100" preserveAspectRatio="none"` (a `g.lc-grid` of lines, then one `g.lc-s.tone-*` per series with `.lc-line`, optional `.lc-area`, and `.lc-pts` written as `M x,y h0` per point), and `.lc-x` (labels, evenly spaced). Coordinates: x runs 0 to 100 across evenly spaced labels; y = 100 − (value − axis min) ÷ (axis max − axis min) × 100. Add `.lc-legend` with one `span.tone-*` per series.
- **Figures**: `figure.figure` with an `<img>` (or an inline SVG illustration) and `figcaption`; `--fig-h` sets the height, and images are cropped to fill it with rounded corners. Use the user's own images. When there are none, draw a simple SVG illustration in palette colours or leave the figure out; never use fake stock photos or images of real people.
- **Tones**: `.tone-cycle`, `.tone-base`, `.tone-orange`, `.tone-grape`, `.tone-mint`, `.tone-gray`, `.tone-ink`.

## Fit guide (A4 content area is about 182 × 245 mm)

Rough heights to plan a page: band and footer are fixed; stat row 25 to 35 mm; a card row 35 to 45 mm; a table with 4 rows 40 mm; a chart 55 to 90 mm; a quote 35 to 45 mm; a banner or note 15 mm; gaps 6 mm. Limits per block: tables up to 8 rows and 5 columns; up to 7 bars, 8 columns or 2 to 3 line series with up to 8 points; 3 to 6 flow steps; card and stat rows of 2 to 5 items; panel text up to about 90 words. Keep labels short so table columns and stat labels do not break into one word per line.

## Writing rules

- Each page opens with its main point. Put the single most important sentence of a section in a `.key` line, `.note` or `.banner`, not buried in a paragraph.
- Band titles are 1 to 5 words. Card titles are 1 to 4 words. Stat labels are 2 to 6 words.
- Stat values carry their unit (`$4.2M`, `-18%`, `3.1x`). Every chart title says what is measured and the unit.
- Quotes need a real attribution from the user's material; otherwise attribute them to the document itself ("Closing note, 2026") or use a `.banner` instead.
- Keep body text left-aligned (no justified text) and in sentence case. Spaced caps are only for band titles, the cover eyebrow and kind, and flow steps.
