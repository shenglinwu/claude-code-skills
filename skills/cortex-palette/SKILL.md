---
name: cortex-palette
description: User's default brand color palette — Cortex Blue + companion cyan + 12 named accents. Use whenever generating HTML pages, presentation slides, decks, dashboards, charts, data visualizations, infographics, landing pages, reports, or any visual artifact that requires a color scheme. Apply automatically without asking the user to pick colors. Also use to override the default theme tokens of design/slide/chart skills such as frontend-design, frontend-slides, vizro-analytics, nvidia-presentation, theme-factory, visual-explainer, arch-flow-explainer, code-explainer, drawio, and excalidraw-diagram when the user has not explicitly requested a different theme.
---

# Cortex Palette

The user's standardized color palette for all visual output. Apply this palette by default — do not ask the user to pick colors. Only deviate if the user explicitly requests a different theme (e.g. "use NVIDIA green", "make it monochrome", "use the existing theme of this project").

## Style rules (non-negotiable)

- **Use solid colors only.** Apply each hex value as a flat fill — no gradients, no color interpolation between palette entries.
- **No gradients anywhere.** No `linear-gradient`, `radial-gradient`, `conic-gradient`, SVG `<linearGradient>` / `<radialGradient>`, multi-stop fills, or fade-to-transparent overlays. This applies to backgrounds, buttons, headings, hero sections, chart fills, dividers, and decorative shapes.
- **No glow effects.** No `text-shadow` glows, no `box-shadow` with colored spread used as a glow, no SVG `<filter>` blur halos, no neon/bloom effects. Plain drop shadows for elevation (subtle black/gray, low opacity) are fine; colored glows are not.
- **Composition via adjacency, not blending.** If you would normally reach for a gradient (hero section, two-tone divider, transition between sections), use two solid color blocks side-by-side or stacked instead.

## When to invoke this skill

Auto-apply when you are about to generate any of:
- HTML pages, landing pages, marketing pages, or web components
- Presentation slides, decks, or pitch documents
- Charts, dashboards, KPI cards, data visualizations
- Infographics, diagrams, architecture explainers
- Reports, one-pagers, executive summaries
- Any artifact rendered visually (drawio, excalidraw, mermaid, SVG)

When invoking another visual skill (frontend-design, frontend-slides, vizro-analytics, nvidia-presentation, theme-factory, etc.), pass these hex values as the theme override.

## Core rule

**Cortex Blue `#0EA5E9` is the core color for titles, headers, and section headings.** It is the dominant identity color — use it for:
- H1, H2, H3, slide titles, page mastheads, deck cover headlines
- Table column headers, card titles, panel titles
- Brand marks, logos, primary links
- Active navigation states, tab labels

**Companion Cyan `#22D3EE`** is the secondary accent — use it as a **solid fill** for:
- Sub-headers (H4–H6), title underlines (solid bar, not gradient)
- Highlights, hover states, focus rings
- Secondary chart series, decorative dividers
- Companion blocks adjacent to Cortex Blue panels (side-by-side solid fills, never blended)

## Full palette

### Primary
| Token | Name | Hex | Role |
|---|---|---|---|
| `--cortex-blue` | Cortex Blue | `#0EA5E9` | **Core color** — titles, headers, brand. Tailwind sky-500. |
| `--cortex-cyan` | Companion Cyan | `#22D3EE` | Secondary accent (solid fill only — no gradients). Tailwind cyan-400. |

### Supporting (12 named accents)
| Token | Name | Hex | Family | Typical use |
|---|---|---|---|---|
| `--fern-green` | Fern Green | `#659157` | mid green | nature/growth accent, distinct chart series, "success" semantic |
| `--dried-herb` | Dried Herb | `#87864F` | olive | tag, category accent |
| `--desert-sage` | Desert Sage | `#B7BFA9` | sage green | soft surface tint, light section bg |
| `--stormy-weather` | Stormy Weather | `#58656D` | slate | borders, secondary text, muted chrome |
| `--oak-buff` | Oak Buff | `#C9A66B` | mustard / tan | warning-adjacent, warm accent |
| `--marsala` | Marsala | `#8A4E51` | burgundy | deep warm accent, emphasis |
| `--biscay-bay` | Biscay Bay | `#3F7C8A` | teal | secondary cool accent, alt-series |
| `--lavender-mist` | Lavender Mist | `#AAA1C8` | soft lavender | soft surface tint, light section bg, editorial accent |
| `--cashmere-rose` | Cashmere Rose | `#B690A0` | mauve | soft accent, editorial section |
| `--cadmium-orange` | Cadmium Orange | `#E78A5C` | coral | CTA, warm emphasis, contrast |
| `--reflecting-pond` | Reflecting Pond | `#2A2C42` | deep navy | dark backgrounds, dark-mode surfaces |
| `--amethyst-orchid` | Amethyst Orchid | `#9B5BB6` | purple | category accent, distinct series |

## Drop-in CSS

```css
:root {
  /* Primary */
  --cortex-blue: #0EA5E9;
  --cortex-cyan: #22D3EE;

  /* Supporting */
  --fern-green: #659157;
  --dried-herb: #87864F;
  --desert-sage: #B7BFA9;
  --stormy-weather: #58656D;
  --oak-buff: #C9A66B;
  --marsala: #8A4E51;
  --biscay-bay: #3F7C8A;
  --lavender-mist: #AAA1C8;
  --cashmere-rose: #B690A0;
  --cadmium-orange: #E78A5C;
  --reflecting-pond: #2A2C42;
  --amethyst-orchid: #9B5BB6;

  /* Semantic aliases */
  --color-title:    var(--cortex-blue);     /* H1/H2/H3, slide titles */
  --color-subtitle: var(--cortex-cyan);     /* sub-headers, underlines */
  --color-primary:  var(--cortex-blue);
  --color-accent:   var(--cortex-cyan);
  --color-bg-dark:  var(--reflecting-pond);
  --color-text:     #1A1A1A;
  --color-muted:    var(--stormy-weather);
  --color-border:   #E5E7EB;
}

/* Headings — Cortex Blue is the core title color */
h1, h2, h3,
.slide-title, .page-title, .deck-title, .card-title, .panel-title {
  color: var(--color-title);
}
h4, h5, h6, .subtitle { color: var(--color-subtitle); }

/* Hero section — two solid blocks, not a gradient */
.hero {
  background: var(--cortex-blue);
  color: #FFFFFF;
}
.hero__accent {
  background: var(--cortex-cyan); /* adjacent solid block, e.g. side panel or bottom band */
}

/* Dark-mode surface */
.surface-dark {
  background: var(--color-bg-dark);
  color: #F5F5F5;
}

/* Elevation — neutral drop shadow only (no colored glow) */
.elevated {
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06);
}
```

**Forbidden CSS patterns** (do not emit these):
```css
/* ❌ gradients */
background: linear-gradient(...);
background: radial-gradient(...);
background-image: linear-gradient(...);

/* ❌ glow effects */
text-shadow: 0 0 12px var(--cortex-cyan);
box-shadow: 0 0 24px var(--cortex-blue);   /* colored spread used as glow */
filter: drop-shadow(0 0 8px #0EA5E9);
```

## Chart / data viz

**Categorical series order** (Plotly, Chart.js, Vizro, ECharts) — the first colors maximize contrast against Cortex Blue:

```js
const CORTEX_CATEGORICAL = [
  '#0EA5E9', // Cortex Blue
  '#E78A5C', // Cadmium Orange
  '#659157', // Fern Green
  '#9B5BB6', // Amethyst Orchid
  '#3F7C8A', // Biscay Bay
  '#C9A66B', // Oak Buff
  '#8A4E51', // Marsala
  '#22D3EE', // Companion Cyan
  '#AAA1C8', // Lavender Mist
  '#B7BFA9', // Desert Sage
  '#B690A0', // Cashmere Rose
  '#87864F', // Dried Herb
  '#58656D', // Stormy Weather
];
```

**Sequential (single-hue)** — for heatmaps, choropleths, intensity maps:
```js
const CORTEX_SEQUENTIAL = ['#E0F2FE', '#7DD3FC', '#38BDF8', '#0EA5E9', '#0369A1', '#0C4A6E'];
```

**Diverging** — for variance / surplus-deficit:
```js
const CORTEX_DIVERGING = ['#8A4E51', '#B690A0', '#F5F5F5', '#7DD3FC', '#0EA5E9'];
```

## Pairing guidance

| Section type | Recommended combination (all solid fills, no gradients) |
|---|---|
| Hero / cover slide | Solid Reflecting Pond background, Cortex Blue title, optional Companion Cyan solid band/sidebar — never blended |
| Two-tone section accent | Cortex Blue block + Cadmium Orange block (cool/warm) **or** Cortex Blue + Marsala — adjacent solid panels |
| Soft / editorial section | Desert Sage + Cashmere Rose + Lavender Mist + Oak Buff (each as its own solid panel or tag) |
| Data-dense dashboard | Cortex Blue (primary KPI) + Biscay Bay + Amethyst Orchid + Cadmium Orange + Fern Green as flat series colors |
| Status semantics | Fern Green = success/positive · Cadmium Orange = warn/attention · Marsala = error/negative · Stormy Weather = neutral/disabled |
| Dark mode | Reflecting Pond bg, Cortex Blue titles, Companion Cyan accents (solid), Stormy Weather borders |

**Avoid:**
- Amethyst Orchid adjacent to Cashmere Rose (muddy purple/mauve clash)
- Amethyst Orchid adjacent to Lavender Mist (both purple — pick one)
- Lavender Mist adjacent to Cashmere Rose (both soft pastels, low separation)
- Fern Green adjacent to Dried Herb (both mid-greens, reads as one block)
- Fern Green adjacent to Desert Sage (green-on-green, low separation — use one as background, the other as accent only if value contrast is high)
- Dried Herb adjacent to Oak Buff (too close in hue, reads as one block)
- Marsala on Reflecting Pond (low contrast — use Cadmium Orange or Companion Cyan instead)

## Tailwind integration

If the project uses Tailwind, extend the config:

```js
// tailwind.config.js
theme: {
  extend: {
    colors: {
      cortex: {
        blue: '#0EA5E9',
        cyan: '#22D3EE',
        fern: '#659157',
        herb: '#87864F',
        sage: '#B7BFA9',
        slate: '#58656D',
        buff: '#C9A66B',
        marsala: '#8A4E51',
        bay: '#3F7C8A',
        lavender: '#AAA1C8',
        rose: '#B690A0',
        orange: '#E78A5C',
        pond: '#2A2C42',
        orchid: '#9B5BB6',
      },
    },
  },
}
```

Then headings: `<h1 class="text-cortex-blue">…</h1>`.

## Override behavior for sibling skills

When another visual skill is also active, this skill's palette wins for color tokens unless the user explicitly opted into the other skill's theme. Specifically:

- **theme-factory** — do not pick a preset theme; supply the Cortex hex values as a custom theme.
- **nvidia-presentation** — override the NVIDIA green accent with Cortex Blue; keep dark Reflecting Pond background.
- **vizro-analytics** / **frontend-design** / **frontend-slides** — pass `CORTEX_CATEGORICAL` as the series palette and `--cortex-blue` as the primary brand token.
- **drawio** / **excalidraw-diagram** / **arch-flow-explainer** — color nodes/edges from this palette; reserve Cortex Blue for primary/origin nodes.

## What this skill is NOT

- Not a font/typography spec — only colors. Pair with whatever typography the active design skill chooses.
- Not a layout system — only color tokens. Layout decisions belong to the host skill.
- Not mandatory — if the user names another theme ("Solarized", "the existing site palette", "monochrome"), defer to their choice.
