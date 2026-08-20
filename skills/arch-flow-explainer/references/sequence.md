# Swim-lane sequence diagrams

Pattern for time-ordered processes — bootstrap, handshake, lifecycle. The SVG shows roles as vertical lanes, time as the y-axis, and messages as horizontal arrows between lanes. Phase bands group related messages.

Read `references/styling.md` first for the shared CSS, color palette, and arrow markers.

## When to use this pattern

- "Explain how authentication happens step by step"
- "Show the bootstrap process"
- "Diagram the OAuth handshake"
- "What's the order of operations during X?"

If the answer is about **who calls whom in steady state** (not about the order of a specific scenario), use the topology pattern instead — see `topology.md`.

## Anatomy of a sequence diagram

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  Lane A  │  │  Lane B  │  │  Lane C  │  │  Lane D  │   ← lane headers
└────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │             │       ← lifelines (dashed)
═════│═════════════│═════════════│═════════════│════   ← phase band background
     │             │             │             │
PHASE 0 — pre-staging                                  ← phase header
     │ ① message label                          │
     │────────────▶│             │             │       ← message arrow
     │             │ ② another message         │
     │             │────────────▶│             │
═════│═════════════│═════════════│═════════════│════   ← next phase band
     │             │             │             │
PHASE 1 — startup                                      
     │             │             │ ③ ...      │
     │             │             │────────────▶│
     ⌐             ⌐             ⌐             ⌐       ← bottom of lifelines
```

Time flows top-to-bottom. Lanes are columns. Messages are horizontal arrows. Phase bands are wide colored backgrounds grouping related messages.

## Identifying lanes and phases

**Lanes** = roles, not necessarily processes. A single physical server might have two lanes if it has two distinct services (e.g. `NICo DHCP` and `NICo API`). Conversely, a cluster of three identical machines is usually one lane.

Pick lanes by asking: **who is the actor?** for each message. Each distinct actor is a lane.

Common lane patterns:
- 3-lane: client / server / database
- 4-lane: user / frontend / backend / external service
- 5-6 lane: more than that means the diagram is probably too dense — split it

**Phases** = natural time-order groupings. A phase has a single conceptual purpose ("BMCs come up", "user authenticates", "session establishes"). Within a phase, messages happen close in time; between phases, there's a logical break or wait.

3–5 phases is typical. Fewer than 3 means the diagram doesn't need phases (just label messages 1, 2, 3...). More than 5 means the process is too big and should be split.

## Building the SVG

### 1. Set viewBox and add defs

```svg
<svg viewBox="0 0 1280 1380" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="...">
  <defs>
    <!-- arrow markers for each color -->
    <marker id="arrow-blue" .../>
    <marker id="arrow-amber" .../>
    <marker id="arrow-teal" .../>
    <marker id="arrow-purple" .../>
    <marker id="arrow-green" .../>

    <style>
      /* SVG-internal CSS from styling.md, plus phase-band classes below */
      .phase-band-0 { fill: #f7f1e4; }
      .phase-band-1 { fill: #fbe6db; }
      .phase-band-2 { fill: #dceaee; }
      .phase-band-3 { fill: #f3ecf7; }
      .phase-band-4 { fill: #eef2ea; }

      .lane-header { fill: #f1f5f9; stroke: #94a3b8; stroke-width: 1; }
      .lane-header.operator { fill: #f7f1e4; stroke: #d9be8a; }
      /* ... per-lane variants */

      .lifeline { stroke: #cbd5e1; stroke-width: 1; stroke-dasharray: 3,3; fill: none; }
      .activation { fill: #ffffff; stroke: #64748b; stroke-width: 1; }
    </style>
  </defs>
  ...
</svg>
```

### 2. Lay out phase bands (background)

Phase bands span the full width of the diagram and group all messages happening in that phase. Place them **first** so they sit underneath everything else:

```svg
<rect class="phase-band-0" x="20" y="140" width="1240" height="130" rx="8"/>
<rect class="phase-band-1" x="20" y="290" width="1240" height="240" rx="8"/>
...

<text class="label-ph" x="40" y="160">PHASE 0  ·  Pre-staging  (...)</text>
<text class="label-ph" x="40" y="310">PHASE 1  ·  BMCs power on  (...)</text>
...
```

Phase header text goes inside the band, top-left, with a brief parenthetical context note.

### 3. Place lane headers at the top

```svg
<rect class="lane-header operator" x="30" y="30" width="140" height="90" rx="8"/>
<text class="label-th" x="100" y="65" text-anchor="middle">Operator</text>
<text class="label-tn" x="100" y="85" text-anchor="middle">human, before</text>
<text class="label-tn" x="100" y="100" text-anchor="middle">site cutover</text>
```

Each lane gets its own header tinted with its category color (use the node-* color palette: blue for control, amber for boot/site services, etc.). The header has the role name plus 1-2 lines of scope/identity.

Lane width 130-280 depending on how much identity text the role needs. Center-align text in the header.

### 4. Draw lifelines

Vertical dashed lines from the bottom of each lane header down through all the phase bands:

```svg
<line class="lifeline" x1="100"  y1="125" x2="100"  y2="1280"/>
<line class="lifeline" x1="330"  y1="125" x2="330"  y2="1280"/>
<line class="lifeline" x1="560"  y1="125" x2="560"  y2="1280"/>
...
```

The x-coordinate of each lifeline is the **center** of its lane — this is the anchor for all message arrows landing on or originating from that role.

### 5. Draw messages between lifelines

Each message is an arrow between two lifelines, with a numbered circle and a label:

```svg
<!-- Message label above arrow -->
<text class="label-msg" x="445" y="340" text-anchor="middle">DHCPDISCOVER (broadcast, mac=aa:bb:..:07:01)</text>

<!-- Arrow from source lifeline to destination lifeline -->
<path class="arr-blue" d="M 550 350 L 340 350" marker-end="url(#arrow-blue)"/>

<!-- Numbered circle on the arrow midpoint -->
<circle cx="445" cy="350" r="11" fill="#0ea5e9" class="num-circle"/>
<text class="num-text" x="445" y="354">3</text>
```

Conventions:
- Message label sits **above** the arrow, centered between the two lanes
- Arrow is a straight horizontal line — `M sourceX y L destX y` works
- For long-distance arrows that cross multiple lanes, use a slight curve to avoid overlapping unrelated lifelines
- Numbered circle sits at the arrow's midpoint (or slightly offset to avoid overlap with the message label)
- Number's text y-coord is `cy + 4` for visual centering

### 6. Use activation rectangles for internal work

When a role does internal processing between receiving and sending messages, show it with an activation rectangle on its lifeline:

```svg
<rect class="activation" x="320" y="225" width="20" height="30"/>
<text class="label-msg" x="350" y="244" text-anchor="start">internal action description</text>
```

Activation rect width is ~20px; it sits centered on the lifeline (`x = lifelineX - 10`). Internal action text appears to the right of the rectangle.

### 7. Use state notes for state changes

When a role transitions to a different mode (e.g. a DPU finishes booting and is now running a different image), use an italic state note:

```svg
<rect class="activation" x="935" y="755" width="20" height="25"/>
<text class="label-state" x="965" y="772" text-anchor="start">forge-scout running on DPU's Arm cores</text>
```

The `.label-state` class makes it italic and purple, distinguishing it from regular messages.

## Color coding messages

Match the arrow color to the message category, same convention as topology:

- **Blue (`.arr-blue`)** — control plane messages (DHCP, Redfish, gRPC over admin network)
- **Amber (`.arr-amber`)** — pre-staging actions, manual ops by humans
- **Teal dashed (`.arr-teal`)** — in-band signals (LLDP, hardware events on a single link)
- **Purple (`.arr-purple`)** — registration / correlation / metadata operations
- **Green (`.arr-green`)** — steady-state operational messages (post-boot, in-production)

The numbered circle's fill color must match the arrow color.

## Phase band colors

Phase bands use very pale fills so they don't overpower the foreground content:

| Phase position | Class | Hex | Suggested role |
|---|---|---|---|
| 0 (first) | `.phase-band-0` | `#f7f1e4` (pale Oak Buff) | Pre-staging / setup |
| 1 | `.phase-band-1` | `#fbe6db` (pale Cadmium Orange) | Initial boot / power-on |
| 2 | `.phase-band-2` | `#dceaee` (pale Biscay Bay) | Network / discovery |
| 3 | `.phase-band-3` | `#f3ecf7` (pale Amethyst Orchid) | Registration / handoff |
| 4 (last) | `.phase-band-4` | `#eef2ea` (pale Fern Green) | Steady state / success |

If the system has fewer or more phases, adapt — but use pale tints throughout (saturated phase backgrounds compete with the message arrows).

## The numbered legend below

Same format as topology diagrams. Each numbered message gets a row in the `.flows` grid, categorized by its role:

```html
<div class="flows">
  <div class="flow scout">
    <span class="num">1</span>
    <div><b>Operator → NICo</b> · import rack inventory<br>
    Operator loads the L11 factory inventory file: a list of MACs for every BMC and DPU in the rack.</div>
  </div>

  <div class="flow ctrl">
    <span class="num">3</span>
    <div><b>Host BMC → NICo</b> · <code>DHCPDISCOVER</code><br>
    BMC has standby power and comes up first. Sends a normal DHCP broadcast.</div>
  </div>
  ...
</div>
```

For sequence diagrams, omit the scale annotation (×N pills) since each flow is a single time-ordered event, not a fan-out.

## Result / artifact box

Sequence diagrams especially benefit from a closing **result box** showing the concrete artifact that the process produces. This makes the abstract sequence land:

```html
<div class="result-box">
  <h3>Result: the ManagedHost row in Postgres</h3>
  <pre>ManagedHost {
  rack:           2
  slot:           7
  serial:         SN-12345
  host_bmc_ip:    10.10.2.71   ← DHCP-reserved (step 4)
  dpu_bmc_ip:     10.10.2.72   ← DHCP-reserved (step 7)
  dpu_oob_ip:     10.10.2.73   ← self-registered (step 14)
  state:          READY
}</pre>
</div>
```

Reference back to the step numbers (← step 4) so the reader can trace each field to where it was set in the sequence.

## Worked example structure

See `assets/sequence-example.html` for a complete real-world sequence diagram (NICo bootstrap). The structure is:

1. Page header (h1 + sub)
2. Reading-instructions banner (blue-tinted)
3. SVG with 6 lanes (operator, NICo, host BMC, DPU BMC, DPU, ToR), 5 phase bands, 17 numbered messages
4. Five color categories in legend-cats row
5. 17 numbered messages in the .flows grid
6. Result box at the bottom showing the ManagedHost Postgres row

## Sizing guidance for sequence diagrams

- viewBox typically `1280 × 1300–1400` — sequence diagrams are taller than they are wide
- Lane width 130–280 depending on header content
- Phase band height: ~120 for short phases (2-3 messages), ~250 for longer phases (4-6 messages)
- Message vertical spacing: ~30-40px between consecutive messages within a phase
- Lifelines extend from y = lane-header bottom (~125) to y = bottom of last phase band (~1280)

## Common sequence patterns and their use cases

**Bootstrap / power-on sequence**
- Lanes: operator, orchestrator, hardware components (BMCs, devices)
- Phases: pre-staging → boot → discovery → handoff → steady-state
- Examples: NICo bootstrap, K8s node join, container startup

**Authentication handshake**
- Lanes: user, client, identity provider, resource server
- Phases: initiation → redirect → token exchange → resource access
- Examples: OAuth, OIDC, SAML

**Distributed transaction**
- Lanes: coordinator, participants
- Phases: prepare → vote → commit / abort
- Examples: 2PC, Saga pattern

**Failure / recovery**
- Lanes: leader, followers, monitor
- Phases: normal → detect → elect → reconcile
- Examples: Raft leader election, MySQL replication failover
