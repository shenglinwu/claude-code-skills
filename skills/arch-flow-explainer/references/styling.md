# Styling reference

Shared visual language for all diagrams produced by this skill. Read this first regardless of which diagram type you're generating — it covers the page-level CSS, color palette, typography, and structural conventions both patterns rely on.

## Page structure

Every diagram is wrapped in this skeleton:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>...</title>
<style>
  /* ...page styles below... */
</style>
</head>
<body>
<div class="wrap">
  <h1>Title</h1>
  <div class="sub">One-line description</div>

  <div class="scale-banner">
    <b>Reading this diagram:</b> One- or two-sentence orientation for the reader.
  </div>

  <svg viewBox="0 0 W H" ...> ... </svg>

  <div class="legend-cats"> ... </div>

  <h2>Numbered ...</h2>
  <div class="flows"> ... </div>

  <!-- Optional final result/artifact box -->
  <div class="result-box"> ... </div>
</div>
</body>
</html>
```

## Page CSS (verbatim, copy into the `<style>` block)

```css
body {
  margin: 0;
  padding: 28px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: #fafafa;
  color: #0e2025;
}
.wrap { max-width: 1320px; margin: 0 auto; }
h1 { font-size: 22px; font-weight: 600; margin: 0 0 6px; }
.sub { color: #666; font-size: 13px; margin-bottom: 20px; }
h2 { font-size: 15px; font-weight: 600; margin: 22px 0 10px; }

svg {
  width: 100%; height: auto; display: block;
  background: #fff;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
}

/* Banner — orient the reader before they look at the diagram */
.scale-banner {
  background: #e2f3f7;             /* or #f7f1ef for amber-themed banners */
  border: 1px solid #62bcd2;       /* matches background */
  color: #0a748d;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  margin-bottom: 16px;
}
.scale-banner b { color: #0a748d; }

/* Legend categories row (under the SVG) */
.legend-cats { margin-top: 8px; font-size: 12px; color: #555; display: flex; gap: 18px; flex-wrap: wrap; align-items: center; }
.legend-cats span { display: inline-flex; align-items: center; gap: 6px; }
.legend-cats i { width: 18px; height: 3px; display: inline-block; border-radius: 2px; }

/* Numbered flow grid */
.flows { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px 36px; font-size: 13px; line-height: 1.5; }
.flow { display: grid; grid-template-columns: 30px 1fr; gap: 12px; align-items: start; }
.flow .num {
  width: 26px; height: 26px; border-radius: 50%;
  display: inline-flex; align-items: center; justify-content: center;
  font-weight: 600; font-size: 12px; color: #fff;
  flex-shrink: 0;
}
.flow.ctrl   .num { background: #0d98ba; }
.flow.tele   .num { background: #6f2da8; }
.flow.inband .num { background: #999b9b; }
.flow.scout  .num { background: #a6674c; }
.flow.live   .num { background: #00ab78; }
.flow b { font-weight: 600; }
.flow code { font-size: 12px; color: #475569; background: #f1f5f9; padding: 1px 6px; border-radius: 4px; }

/* Inline scale pill (×N, site-wide, etc.) */
.scale {
  display: inline-block; font-size: 11px;
  background: #f3eae6; color: #935b43;
  padding: 1px 7px; border-radius: 10px;
  margin-left: 4px; font-weight: 600;
}

/* Optional result/artifact box at the bottom */
.result-box {
  margin-top: 28px;
  background: #ebf8f4;
  border: 1px solid #99ddc9;
  padding: 14px 18px;
  border-radius: 10px;
  font-size: 13px;
}
.result-box h3 { margin: 0 0 8px; font-size: 14px; color: #007653; }
.result-box pre {
  background: #fff;
  border: 1px solid #c7ede1;
  border-radius: 6px;
  padding: 10px 12px;
  font-size: 12px;
  color: #007653;
  margin: 0;
  overflow-x: auto;
}
```

## SVG-internal CSS (in `<defs><style>...</style></defs>`)

These classes are referenced inside the SVG by SVG elements. Put them in a `<style>` block inside `<defs>`:

```css
/* Typography */
.label-th    { font: 600 14px -apple-system, "Segoe UI", Roboto, sans-serif; fill: #0e2025; }
.label-ts    { font: 13px -apple-system, "Segoe UI", Roboto, sans-serif; fill: #333; }
.label-tn    { font: 11px -apple-system, "Segoe UI", Roboto, sans-serif; fill: #666; }
.label-msg   { font: 600 11px -apple-system, sans-serif; fill: #1f2937; }
.label-state { font: italic 600 11px -apple-system, sans-serif; fill: #6f2da8; }
.label-ph    { font: 700 13px -apple-system, sans-serif; fill: #1e293b; letter-spacing: 0.4px; }

/* Container boxes (large outer groupings) */
.container { fill: #f7f7f7; stroke: #d0d0d0; stroke-width: 1; }

/* Node boxes (categorized by role) */
.node-blue   { fill: #e2f3f7; stroke: #0d98ba; stroke-width: 1.2; }
.node-purple { fill: #eee6f5; stroke: #6f2da8; stroke-width: 1.2; }
.node-coral  { fill: #ffefdb; stroke: #ff8c00; stroke-width: 1.2; }
.node-teal   { fill: #ededed; stroke: #999b9b; stroke-width: 1.2; }
.node-amber  { fill: #f3eae6; stroke: #a6674c; stroke-width: 1.2; }
.node-green  { fill: #e0f5ef; stroke: #00ab78; stroke-width: 1.2; }

/* Sub-boxes inside node boxes (for component detail) */
.sub-box { fill: #ffffff; stroke: #94a3b8; stroke-width: 1; }
.ghost   { fill: #f8fafc; stroke: #cbd5e1; stroke-width: 1; stroke-dasharray: 4,3; }

/* Arrows */
.arr-blue   { stroke: #0d98ba; stroke-width: 1.7; fill: none; }
.arr-purple { stroke: #6f2da8; stroke-width: 1.7; fill: none; }
.arr-amber  { stroke: #a6674c; stroke-width: 1.7; fill: none; }
.arr-teal   { stroke: #999b9b; stroke-width: 1.7; fill: none; stroke-dasharray: 5,4; }
.arr-green  { stroke: #00ab78; stroke-width: 1.7; fill: none; }

/* Numbered circles on arrows */
.num-circle { stroke: #fff; stroke-width: 1.5; }
.num-text   { font: 700 12px -apple-system, sans-serif; fill: #fff; text-anchor: middle; }
```

## Arrow markers

Define one marker per arrow color in `<defs>`. The arrowhead colors must match the arrow strokes:

```html
<defs>
  <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M2 1L9 5L2 9" fill="none" stroke="#0d98ba" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
  </marker>
  <!-- repeat for amber, teal, purple, green with matching strokes -->
</defs>
```

Apply with `marker-end="url(#arrow-blue)"` on the path/line element.

## Color palette — choosing colors

This skill ships with the **nice palette** (the `nice-palette` skill) as its default theme — all the hex values in the CSS above are drawn from it, so a diagram produced verbatim already uses the user's default colors. Blue Green (`#0d98ba`), the base color, is reserved for the primary/origin role. Only deviate if the user explicitly asks for a different theme (e.g. "use the existing project palette", "make it monochrome"). The CSS class names (`.node-blue`, `.arr-blue`, …) are **stable semantic slot names** kept consistent across every diagram in a document set — keep the class names even though each now maps to a nice-palette color (the names come from the older Cortex palette, so `teal` is now gray and `green` is mint).

Six slots cover all roles. Pick by **semantic role**, not by component name. The same component can be a different color in different diagrams depending on what's being illustrated.

| Slot (class) | Nice-palette color | Node fill / stroke | Use for |
|---|---|---|---|
| **blue** | Blue Green | `#e2f3f7` / `#0d98ba` | Primary orchestrator, control-plane services, control flows over admin Ethernet |
| **purple** | Grape | `#eee6f5` / `#6f2da8` | Telemetry / aggregation services, secondary controllers, registration / correlation flows |
| **coral** | Dark Orange | `#ffefdb` / `#ff8c00` | Compute, hosts, tenant-facing components, end-user systems |
| **teal** | Metallic Gray | `#ededed` / `#999b9b` | Fabric / data plane, in-band traffic that doesn't cross the management network. Arrows are typically **dashed** (`stroke-dasharray: 5,4`) |
| **amber** | Amber Brown | `#f3eae6` / `#a6674c` | Bootstrap / discovery / pre-staging services, site-local services |
| **green** | Mint | `#e0f5ef` / `#00ab78` | Steady-state daemons, success states, post-provisioning operations |

Need a seventh or eighth role? Use the remaining nice-palette side colors: Gold (fill `#ffd700`, stroke `#e6c200`, text `#796600`) and Cinnabar (`#e34234`, text `#bd372b`). Keep Cinnabar for errors and failures when the diagram shows status. Use solid fills only — **no gradients and no colored glow effects** anywhere.

### Flow-color legend categories

The legend below the diagram has small colored bars for each category. Standard categorization (nice-palette color in parentheses):

- 🟦 **Blue** (Blue Green) — Control plane (admin Ethernet) — the everyday RPCs
- 🟪 **Purple** (Grape) — Telemetry / registration / correlation
- 🟧 **Amber** (Amber Brown) — Bootstrap / discovery / pre-staging
- 🟢 **Green** (Mint) — Steady-state / lifecycle / operational
- ⬜ **Teal, dashed** (Metallic Gray) — In-band traffic, never on management network

Adapt the categories to match the system being diagrammed — these are the most common ones, but a security-focused diagram might use different categories (e.g. authn, authz, data, audit). The principle: each numbered arrow's color matches a category, and each category appears in the legend.

## Typography conventions

- **`.label-th`** (14px, 600) — primary labels for components, container headers
- **`.label-ts`** (13px, regular) — secondary content inside boxes
- **`.label-tn`** (11px, #666) — tertiary / hint text, field annotations
- **`.label-msg`** (11px, 600) — message labels on arrows in sequence diagrams
- **`.label-state`** (11px, italic, purple) — state-change notes in sequence diagrams
- **`.label-ph`** (13px, 700, letterspacing) — phase headers in sequence diagrams

## Numbered circles

The single most distinctive element. Every numbered call flow has a colored circle on the arrow line near the destination side, with bold white text inside. The circle's **fill color matches the flow category** (blue/purple/amber/teal/green).

```svg
<circle cx="X" cy="Y" r="11" fill="#0d98ba" class="num-circle"/>
<text class="num-text" x="X" y="Y+4">1</text>
```

Radius 11–12 works well at 1200-wide viewBox. The text needs a slight `+4` y-offset to sit visually centered (because of the SVG text baseline).

## Sizing principles

- **Topology diagrams**: viewBox typically `1200×~900` to `1280×~1100` depending on detail. Container boxes get 700–1000 wide; node boxes get 200–400 wide.
- **Sequence diagrams**: viewBox typically `1280×~1300` to `1280×~1400`. Lane width 130–280; phase bands 200–250 tall each.
- **Padding**: keep ≥20px between nested boxes and ≥40px in the outer container. Cramped diagrams read worse than spacious ones at the same total size.
- **Don't mix viewBox units with explicit pixel widths.** Set `width="100%"` on the SVG and let the viewBox define the coordinate system — this lets the SVG scale to any container width.

## What to copy verbatim, what to customize

**Copy verbatim:**
- All CSS (page-level and SVG-internal)
- Marker definitions
- Legend grid structure
- Numbered circle pattern

**Customize per diagram:**
- viewBox dimensions
- Component layout coordinates
- Component names and labels
- Flow numbering and routing
- Legend categories (if standard ones don't fit the system)
- Banner and prose insights
