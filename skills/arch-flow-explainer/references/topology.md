# Topology + numbered call flows

Pattern for static architecture diagrams. The SVG shows components grouped into functional containers; numbered arrows show calls between them; the legend below explains each call's purpose, protocol, and scale.

Read `references/styling.md` first for the shared CSS, color palette, and arrow marker definitions.

## When to use this pattern

- "How are these microservices wired together?"
- "Show the call flow when a request hits the API"
- "Diagram the architecture of this multi-rack system"
- "Who calls whom in this system?"

If the answer involves **time order** (step 1 must happen before step 2 before step 3), use the sequence pattern instead — see `sequence.md`.

## Anatomy of a topology diagram

```
┌─────────────────────────────────────────────────────────────┐
│  CONTAINER A (functional grouping)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Node 1     │  │   Node 2     │  │   Node 3     │       │
│  └──────┬───────┘  └──────────────┘  └──────────────┘       │
└─────────┼───────────────────────────────────────────────────┘
          │ ① call (protocol)
          ▼
┌─────────────────────────────────────────────────────────────┐
│  CONTAINER B (functional grouping)                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Node group with sub-components                        │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │ │
│  │  │ sub-box  │  │ sub-box  │  │ sub-box  │              │ │
│  │  └──────────┘  └──────────┘  └──────────┘              │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

Two-level hierarchy is the sweet spot: containers (light gray) → node boxes (colored) → optional sub-boxes (white inside colored). Going deeper than three levels usually means the diagram should be split.

## Standard layout

The most reusable layout has a **left column for one logical zone** (often the management plane / orchestrator) and a **right area for the system being managed**, with arrows flowing left-to-right or wrapping around. This works for management-plane / data-plane systems, control / worker patterns, and orchestrator / target patterns.

Alternative layouts:

- **Top-down stack**: orchestrator at top, layers below. Use when there's a clear hierarchical control flow.
- **Hub and spokes**: central component in the middle, peripherals around. Use for systems with one obvious coordinator and many peers.
- **Side-by-side peers**: two equal-weight subsystems with arrows crossing between. Use for federation or peering patterns.

Avoid free-form layouts where components float without clear grouping — they read as visual noise.

## Building the SVG

### 1. Set viewBox and add defs

```svg
<svg viewBox="0 0 1280 1080" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="...">
  <defs>
    <!-- arrow markers from styling.md -->
    <marker id="arrow-blue" .../>
    <marker id="arrow-amber" .../>
    <marker id="arrow-teal" .../>
    <marker id="arrow-purple" .../>
    <marker id="arrow-green" .../>

    <style>
      /* SVG-internal CSS from styling.md */
    </style>
  </defs>
  ...
</svg>
```

### 2. Place containers (functional groupings)

```svg
<rect class="container" x="20" y="20" width="400" height="900" rx="14"/>
<text class="label-th" x="220" y="48" text-anchor="middle">Container header</text>
<text class="label-tn" x="220" y="66" text-anchor="middle">subtitle / scope note</text>
```

### 3. Place node boxes inside containers

```svg
<rect class="node-blue" x="40" y="90" width="360" height="120" rx="10"/>
<text class="label-th" x="220" y="118" text-anchor="middle">Node name</text>
<text class="label-tn" x="220" y="136" text-anchor="middle">role / scope</text>
<text class="label-ts" x="60" y="162" text-anchor="start">• Bullet about responsibility</text>
<text class="label-ts" x="60" y="182" text-anchor="start">• Another bullet</text>
```

### 4. Add sub-boxes for component detail (optional)

```svg
<rect class="sub-box" x="480" y="135" width="195" height="115" rx="6"/>
<text class="label-th" x="577" y="158" text-anchor="middle">Sub-component</text>
<text class="label-tn" x="577" y="178" text-anchor="middle">detail line</text>
```

### 5. Draw arrows with numbered circles

Arrows are drawn as `<path>` elements (preferred over `<line>` because curves route around obstacles better):

```svg
<!-- Arrow from source to target -->
<path class="arr-blue" d="M 400 130 C 430 130, 460 145, 480 165"
      marker-end="url(#arrow-blue)"/>

<!-- Numbered circle near the destination side of the arrow -->
<circle cx="470" cy="160" r="12" fill="#0ea5e9" class="num-circle"/>
<text class="num-text" x="470" y="164">1</text>
```

Path conventions:
- Use cubic Bezier (`C x1 y1, x2 y2, x y`) for curved arrows; pick control points that make the curve clear of other elements
- Use `M x y L x y` (straight line) for short arrows between adjacent boxes
- Place the numbered circle near the destination side, not the midpoint — it reads as "what's being received here"
- The number's `y` text coordinate should be circle `cy + 4` to look visually centered

### 6. Annotate scale (multi-rack / multi-instance systems)

For diagrams of systems that scale, annotate flows with their multiplication factor. Use a small pill near the arrow:

```svg
<rect class="scale-pill" x="412" y="115" width="34" height="14" rx="7"/>
<text class="label-scale" x="429" y="125" text-anchor="middle">×N</text>
```

with CSS:
```css
.scale-pill { fill: #f4ebd9; stroke: #d9be8a; stroke-width: 0.8; }
.label-scale { font: 600 10px -apple-system, sans-serif; fill: #6b5325; }
```

Common scale values:
- `×N` — once per top-level unit (rack, region, cluster)
- `×18N` — once per leaf unit across all top-level units
- `site-wide` — single connection total
- `ad-hoc` — happens on demand, not on a fixed schedule

### 7. Show in-band / data-plane arrows differently

Arrows for traffic that doesn't cross the management network use **dashed teal** to visually separate them:

```svg
<path class="arr-teal" d="M ..." marker-end="url(#arrow-teal)"/>
```

The `.arr-teal` class already includes `stroke-dasharray: 5,4`. This pattern is critical for systems where the management plane and data plane are separate concerns — the diagram needs to make the separation obvious at a glance.

## The numbered legend below the SVG

Each numbered flow gets an entry in the `.flows` grid. Categorize each flow by class (`ctrl`, `tele`, `inband`, `scout`, `live`):

```html
<div class="flows">
  <div class="flow ctrl">
    <span class="num">1</span>
    <div><b>NICo → NMX-C</b> · <code>gRPC</code> <span class="scale">×N</span><br>
    One gRPC session per rack to that rack's NMX-C VIP. Per-rack aggregator means NICo doesn't fan out to individual switch trays.</div>
  </div>

  <div class="flow ctrl">
    <span class="num">2</span>
    <div><b>NICo → BMC</b> · <code>Redfish HTTPS</code> <span class="scale">×18N</span><br>
    Unicast Redfish per compute tray. For 4 racks that's 72 BMC sessions; for 40 racks it's 720. No BMC aggregator.</div>
  </div>
  ...
</div>
```

Format conventions:
- **Bold** the actor → target identifier
- Use `<code>` for the protocol name (gRPC, Redfish HTTPS, DOCA SDN, etc.)
- Use a `<span class="scale">` pill for the scale annotation when relevant
- One or two sentences explaining what the flow does — be specific about the purpose, not just the mechanics

## Closing prose — the "what this makes visible" section

After the legend, add three or four observations that the diagram makes possible. This is the analytical payoff:

> Three things the diagram makes visible that are easy to miss in prose:
>
> **Flow 2 vs Flow 1**: NICo fans out 18 individual Redfish sessions to BMCs but only 1 gRPC session to NMX-C — that's the per-rack aggregation NMX-C provides "for free."
>
> **Flows 4 → 5 → 6 are sequential**: NICo never touches FRR or the DPU SDN agent directly. It goes through the SDN Controller every time. This matters for failure-mode analysis: if the SDN Controller is down, NICo can still do NVLink ops (flow 1) and BMC ops (flow 2) but cannot move tenant network state.
>
> **Flows 10 and 11 are dashed**: in-band NVLink traffic stays entirely inside the rack. Your management network firewall rules don't need to handle any of it.

This section is what turns the diagram from documentation into analysis. Aim for observations that:
- Note something quantitative the diagram now makes obvious (call counts, scale factors)
- Highlight a sequencing or dependency consequence (e.g., what fails when X is down)
- Distinguish similar-looking elements (e.g., why some arrows are dashed)
- Call out a non-obvious boundary (e.g., what does and doesn't cross a firewall)

## Worked example structure

See `assets/topology-example.html` for a complete real-world topology diagram (NICo multi-rack call flows). The structure is:

1. Page header (h1 + sub)
2. Reading-instructions banner (orange/amber-tinted)
3. SVG with two main containers (mgmt server on left, rack on right) plus an inter-rack hint section
4. Five color categories in legend-cats row
5. 14 numbered flows in the .flows grid, categorized by ctrl/tele/inband/scout
6. Final prose observations (in the page response, not the file) calling out scale and isolation

## Common topology layouts and their use cases

**Management plane + managed system** (most common)
- Left: management server / orchestrator with multiple service boxes stacked vertically
- Right: managed system with internal hierarchy
- Arrows: left-to-right with numbered circles near destinations
- Examples: NICo + NVL72, K8s control plane + worker nodes, Hashicorp Vault + clients

**Pipeline / dataflow**
- Top to bottom: data sources → processing stages → sinks
- Arrows: vertical with numbers along the flow
- Examples: Kafka producer → broker → consumer, ETL pipelines

**Hub-and-spoke**
- Center: single coordinator
- Around: peers / leaf services
- Arrows: radiate outward with numbered call types
- Examples: Service mesh control plane, fleet management

**Federated peers**
- Two or more side-by-side equal-weight subsystems
- Arrows: cross between them
- Examples: Multi-region DBs, federated identity, replication topologies
