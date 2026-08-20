---
name: arch-flow-explainer
description: Generate self-contained HTML/SVG explainers for software and system architectures, call flows, and bootstrap sequences. Use this skill whenever the user asks to draw, diagram, visualize, or explain how a system's components interact — including phrases like "create a diagram", "show the call flow", "diagram the architecture", "explain how X talks to Y", "visualize the bootstrap process", "make a sequence diagram", "show who calls whom", or "produce an HTML diagram". Also trigger after reading code or documentation when a visual summary would be more useful than prose, or when the user complains that a stack diagram is "too simple". Produces a single self-contained HTML file with embedded SVG, numbered call flows, color-coded legend, and prose insights — opens in any browser, embeds in any wiki. Two diagram patterns: topology with numbered call flows for static architecture, and swim-lane sequence diagrams for time-ordered processes. Do not use this skill for Mermaid output, simple stack diagrams, or single-component explanations where prose suffices.
---

# Architecture & Flow Explainer

Generates self-contained HTML files containing SVG diagrams and a numbered legend that explain how a system's components interact. Output is a single `.html` file with no external dependencies — it opens in any browser, embeds in any wiki page, and survives being copy-pasted around.

## Default theme: Cortex palette

This skill defaults to the **Cortex palette** — the user's brand colors. Every hex value in `references/styling.md` and the example assets is already a Cortex color, so a diagram built from them is on-brand with no extra work. Cortex Blue (`#0ea5e9`) is reserved for the primary/origin role; the other roles map to named Cortex accents (Amethyst Orchid, Cadmium Orange, Biscay Bay, Oak Buff, Fern Green). Use **solid fills only — no gradients, no colored glow effects**. Only deviate if the user explicitly requests a different theme (e.g. "match this project's existing palette", "make it monochrome").

## Two diagram patterns

Both patterns share the same color palette, numbering convention, and legend format, so a system documented with one can be supplemented with the other.

**1. Topology + numbered call flows.** Static architecture (components in functional groups) with numbered arrows showing the calls between them. Best for explaining steady-state architecture and answering "who calls whom over what protocol, and how does that scale". See `references/topology.md`.

**2. Swim-lane sequence diagram.** Time-ordered messages between roles, organized into phases. Best for explaining bootstrap, handshake, or lifecycle flows where order matters. See `references/sequence.md`.

If both apply (e.g. a system doc covering both architecture and bootstrap), produce two files. They're designed to share the same visual language so the reader can flip between them seamlessly.

## When to use this skill

Trigger this skill when:

- The user asks for a **diagram** of an architecture, system, call flow, sequence, handshake, or bootstrap process
- The user asks how components in a system **interact** or **call** each other
- After reading code or documentation, a **visual summary** would convey the answer better than prose (use judgment — propose a diagram if the system has 4+ interacting components or non-trivial call ordering)
- The user explicitly asks for an **HTML file** they can open or share

Skip this skill when:

- A simple stack diagram or markdown table is sufficient (≤3 components, no call flows)
- The user explicitly wants a **Mermaid** diagram, an **image**, or a **slide**
- The question is conceptual — "what is OAuth?" — not architectural

## Choosing the pattern

The choice depends on whether time order is essential.

| Use topology + numbered flows | Use swim-lane sequence |
|---|---|
| "How are these microservices wired together?" | "How does authentication happen step by step?" |
| "Show the call flow when a request hits the API" | "Diagram the OAuth handshake" |
| "Diagram the architecture of this multi-rack system" | "Explain the bootstrap process" |
| Multiple components, parallel calls | Strict happens-before ordering |
| Numbered flows are reference labels | Numbered flows are time order |

If you can't decide in 30 seconds, pick topology — it's the more general pattern. Sequence is specifically for time-ordered processes.

## Workflow

1. **Identify the diagram type.** Topology or sequence? If genuinely ambiguous, ask one short question and proceed.

2. **Read the relevant references.** Always read `references/styling.md` first — it covers the shared CSS, color palette, and structural conventions. Then read either `topology.md` or `sequence.md` depending on what you're generating.

3. **Look at the example.** The matching file in `assets/` is a complete working diagram from a real system (NVIDIA NCX Infra Controller). Skim it for the exact patterns: how containers nest, where numbered circles sit, how the legend is structured.

4. **Identify components and flows from source material.** From the user's code, docs, or prior conversation:
   - For each **component**, decide which color category fits its role (see `styling.md`).
   - For each **interaction**, decide its category (control plane, telemetry, in-band, bootstrap, steady-state) and assign a number.
   - For sequences, determine **phases** — natural groupings of related messages.

5. **Lay out the SVG by hand.** Don't try to auto-route. Pick coordinates deliberately. Topology diagrams group components into functional containers; sequence diagrams have lanes left-to-right with lifelines top-to-bottom.

6. **Write the legend.** Each numbered flow gets a paragraph in the legend grid: actor → target with the protocol in `<code>`, an optional scale annotation (`×N`, `×18N`, `site-wide`, `ad-hoc`), and one or two sentences explaining what the flow does and why.

7. **Add prose insights below.** The most valuable part of the explainer. Three or four observations the diagram now makes obvious — usually about scale, fault isolation, or non-obvious data paths. Without these, the diagram is decoration; with them, it's analysis.

## Quality bar

A good diagram from this skill has:

- **Numbered flows colored consistently** by category from the Cortex palette — control-plane is always Cortex Blue, in-band is always Biscay Bay teal-dashed, etc., across all diagrams in the same document set
- **Components grouped in functional containers** with role labels — never floating boxes on a blank canvas
- **A complete legend below the diagram** — every numbered arrow has a corresponding legend entry; no arrows without explanation
- **Prose insights** — at minimum three observations the visual makes possible
- **A self-contained HTML file** — no external CSS, no JavaScript, no external images; the SVG is inline and the styles are in a `<style>` block in `<head>`

## Anti-patterns

- **Don't make stack diagrams.** Three colored boxes stacked vertically isn't this skill — that's a markdown table dressed up. The skill exists for the numbered-flow + legend combination.
- **Don't crowd the SVG.** If readability is suffering, split into two diagrams (one topology, one sequence) rather than cramming.
- **Don't skip the legend.** A numbered arrow without a numbered legend entry is incomplete.
- **Don't use Mermaid syntax.** This skill produces hand-laid SVG specifically because auto-routing tools can't produce diagrams of this quality. If the user wants Mermaid, that's a different request.
- **Don't add JavaScript.** The output is a static, self-contained HTML file. CSS-only animations are acceptable but rarely needed.
- **Don't be afraid of size.** A 1200×1200 viewBox is fine. Bigger SVGs with breathing room read better than cramped ones.

## File naming

Save outputs with snake_case names that describe both the system and the diagram type:

- `oauth_bootstrap_sequence.html`
- `microservice_call_flows.html`
- `kafka_consumer_topology.html`
- `nico_multirack_call_flows.html`

Pattern: `<system>_<scope>_<diagram-type>.html` where diagram-type is one of `topology`, `flows`, `sequence`, or `bootstrap`.

## What's in this skill

```
arch-flow-explainer/
├── SKILL.md                            ← you are here
├── references/
│   ├── styling.md                      ← CSS, colors, typography, layout conventions
│   ├── topology.md                     ← topology + numbered flows pattern
│   └── sequence.md                     ← swim-lane sequence pattern
└── assets/
    ├── topology-example.html           ← complete real-world topology example
    └── sequence-example.html           ← complete real-world sequence example
```

Always read `references/styling.md` for any diagram. Read `topology.md` or `sequence.md` based on which pattern you're producing. Use the matching `assets/` file as a working starting template — copy it, then edit.
