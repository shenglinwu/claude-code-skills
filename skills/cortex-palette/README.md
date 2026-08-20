# cortex-palette

The default set of colors for anything Claude draws for you: web pages, slides, charts, dashboards, diagrams, reports. Claude applies it by itself and does not stop to ask you to choose colors.

The point is that every visual thing you get looks like it came from the same place, without you repeating your color preferences in each request.

## The two colors that carry the identity

| Color | Hex | Where it goes |
| --- | --- | --- |
| Cortex Blue | `#0EA5E9` | The core color. Every H1, H2, H3, slide title, page masthead, table column header, card title, brand mark, primary link, and active tab. |
| Companion Cyan | `#22D3EE` | The second accent. Smaller headings, title underlines, hover and focus states, second chart series, dividers. |

Twelve more named accents fill in the rest: Fern Green, Dried Herb, Desert Sage, Stormy Weather, Oak Buff, Marsala, Biscay Bay, Lavender Mist, Cashmere Rose, Cadmium Orange, Reflecting Pond, Amethyst Orchid. `SKILL.md` lists the hex value, the color family, and the normal job of each one.

## Style rules that never bend

- **Solid fills only.** Each hex value is painted flat.
- **No gradients anywhere.** No `linear-gradient`, `radial-gradient`, `conic-gradient`, no SVG gradient tags, no fade-to-transparent overlays. This covers backgrounds, buttons, headings, hero sections, chart fills, and decorative shapes.
- **No glow effects.** No glowing text shadows, no colored box shadows used as a halo, no blur filters, no neon. A plain gray drop shadow to lift a card off the page is fine, because that reads as depth rather than light.
- **Build contrast by putting blocks next to each other.** Where you would normally reach for a gradient, use two solid blocks side by side or stacked instead.

The reason for these three rules is that gradients and glows drift. Two people generating two pages get two slightly different fades, and the set stops looking like one family. Flat colors reproduce exactly.

## What you get out of `SKILL.md`

| Section | What it gives you |
| --- | --- |
| Full palette tables | Token name, friendly name, hex value, and the job of each of the 14 colors. |
| Drop-in CSS | A `:root` block with all the custom properties, plus heading rules, a hero block, a dark surface, and a neutral shadow. Paste it and go. |
| Forbidden CSS | The exact patterns not to write, so the gradient and glow rules are checkable rather than a matter of taste. |
| Chart palettes | Three ready lists: `CORTEX_CATEGORICAL` for series colors, `CORTEX_SEQUENTIAL` for heatmaps, `CORTEX_DIVERGING` for surplus and deficit. |
| Pairing guidance | Which combinations work for a hero slide, an editorial section, a dense dashboard, and dark mode. |
| Pairs to avoid | Seven combinations that read as mud or as one flat block, such as Fern Green next to Desert Sage. |
| Tailwind config | A `theme.extend.colors.cortex` block if the project uses Tailwind. |

## How it works with other visual skills

This skill supplies color only. It does not choose fonts and it does not choose layout, so it can sit on top of any design skill without fighting it.

When another visual skill is running, the Cortex colors win, unless you explicitly asked for that other skill's theme.

| Other skill | What this skill overrides |
| --- | --- |
| theme-factory | Do not pick a preset theme. Hand it the Cortex hex values as a custom theme. |
| nvidia-presentation | Replace the NVIDIA green accent with Cortex Blue. Keep the dark background. |
| vizro-analytics, frontend-design, frontend-slides | Pass `CORTEX_CATEGORICAL` as the chart series list and Cortex Blue as the primary brand color. |
| drawio, excalidraw-diagram, arch-flow-explainer | Color the boxes and arrows from this palette, and keep Cortex Blue for the main or starting box. |

## Turning it off

Name another theme in your request and this skill steps aside. "Use NVIDIA green", "make it monochrome", "match the existing site palette", and "use Solarized" all work. The skill is a default, not a rule.

## Install

```bash
ln -s "$PWD/skills/cortex-palette" ~/.claude/skills/cortex-palette
```

Start a new Claude Code session afterward. You never type this skill by hand. It is written to start on its own whenever visual output is about to be produced.
