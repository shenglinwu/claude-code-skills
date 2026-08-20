# arch-flow-explainer

Turns a system you are trying to explain into one self-contained HTML file: a hand-drawn SVG picture, a numbered legend under it, and a few sentences of analysis.

Self-contained means everything lives inside the single `.html` file. There is no separate stylesheet, no JavaScript, and no image files. You can open it in any browser, paste it into a wiki page, or mail it to someone, and it still looks the same.

## When Claude uses it

It starts on its own when you ask to draw, diagram, or visualize how parts of a system talk to each other. Example requests: "diagram the architecture", "show the call flow when a request hits the API", "explain the bootstrap process step by step".

It stays out of the way when:

- The system is tiny, meaning three parts or fewer with no interesting call order. A short table says it better.
- You asked for Mermaid, an image, or a slide. Those are different tools.
- The question is about an idea, not a system. "What is OAuth?" is prose, not a picture.

## The two kinds of picture

| | Topology with numbered flows | Swim-lane sequence |
| --- | --- | --- |
| Shows | Which part calls which part, over what protocol | Messages in time order, top to bottom |
| Good for | "How are these services wired together?" | "How does the login handshake work?" |
| The numbers mean | Reference labels for the legend | The order things happen in |
| Layout | Boxes grouped into labeled containers | One vertical lane per role, grouped into phases |

If you cannot decide within half a minute, the skill picks topology, because it fits more situations. When a system needs both, the skill writes two files that share the same colors and legend format, so you can read them side by side.

## What the finished file contains

```
┌─────────────────────────────────────────┐
│  Title and one-line summary             │
├─────────────────────────────────────────┤
│                                         │
│   inline SVG picture                    │
│   boxes, arrows, numbered circles       │
│                                         │
├─────────────────────────────────────────┤
│  Legend: one entry per numbered arrow   │
│  who → whom, protocol, what it does     │
├─────────────────────────────────────────┤
│  Prose insights: 3 or 4 things the      │
│  picture now makes obvious              │
└─────────────────────────────────────────┘
```

The prose at the bottom is the part that matters most. Without it the file is decoration. With it the file is analysis, usually about scale, about what breaks when one part fails, or about a data path nobody noticed.

## Files in this skill

| File | What it holds |
| --- | --- |
| `SKILL.md` | The main instructions: when to trigger, which pattern to pick, the seven work steps, and the quality bar. |
| `references/styling.md` | Read this one first for any diagram. It holds the CSS to copy, the color slots, the fonts, and the sizing rules. |
| `references/topology.md` | How to build the topology picture, step by step, with the SVG snippets. |
| `references/sequence.md` | How to build the swim-lane sequence picture, step by step. |
| `assets/topology-example.html` | A complete real diagram. Copy it and edit, rather than starting from an empty file. |
| `assets/sequence-example.html` | The same, for the sequence pattern. |

Claude only loads `SKILL.md` at first. It reads the reference files when it actually needs them, which keeps the session small.

## Colors

The skill ships with the Cortex palette already applied, so a diagram built straight from the reference files is on brand with no extra work. See the `cortex-palette` skill in this repository for the full color list.

Six color slots cover every role. You pick a slot by what the part **does** in this particular picture, not by its name. The same service can be blue in one diagram and orange in another.

| Slot | Color | Used for |
| --- | --- | --- |
| blue | Cortex Blue `#0ea5e9` | The main coordinator and control traffic |
| purple | Amethyst Orchid `#9b5bb6` | Telemetry, registration, second-level controllers |
| coral | Cadmium Orange `#e78a5c` | Compute, hosts, anything the end user touches |
| teal | Biscay Bay `#3f7c8a` | Data plane traffic that never crosses the management network. Its arrows are dashed. |
| amber | Oak Buff `#c9a66b` | Bootstrap, discovery, pre-staging, site-local services |
| green | Fern Green `#659157` | Steady-state daemons and success states |

Fills are always solid. The skill never emits gradients or colored glow effects.

## Rules the skill will not break

- Every numbered arrow has a matching numbered entry in the legend. An arrow with no explanation is an unfinished diagram.
- Boxes sit inside labeled containers. Boxes floating on an empty canvas are not allowed.
- No JavaScript in the output. CSS animation is allowed but almost never needed.
- No Mermaid. The SVG is laid out by hand on purpose, because automatic routing tools cannot reach this quality.
- Three boxes stacked on top of each other is not a diagram from this skill. That is a table wearing a costume.

## File names it produces

The pattern is `<system>_<scope>_<type>.html`, all lowercase with underscores, where type is `topology`, `flows`, `sequence`, or `bootstrap`. For example `oauth_bootstrap_sequence.html` or `kafka_consumer_topology.html`.

## Install

```bash
ln -s "$PWD/skills/arch-flow-explainer" ~/.claude/skills/arch-flow-explainer
```

Then start a new Claude Code session. The skill needs no settings and no machine-specific paths, so it works as-is on any computer.
