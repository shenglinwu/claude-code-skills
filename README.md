# claude-code-skills

Personal Claude Code skills and output styles, kept in one repository so they can be versioned and copied to a new machine.

A **skill** is a folder of instructions that Claude Code loads when the task matches. An **output style** changes how Claude writes its replies to you. Neither is program code. Both are Markdown files that Claude reads.

## What is in here

| Folder | Name | What it does |
| --- | --- | --- |
| `skills/arch-flow-explainer/` | arch-flow-explainer | Draws system architecture and call flows as a single self-contained HTML file with an inline SVG picture. |
| `skills/cortex-palette/` | cortex-palette The older brand colors (Cortex Blue plus named accents). Used only when you ask for Cortex colors by name. `nice-palette` is the default. |
| `skills/daily-briefing/` | daily-briefing | Reads a list of news feeds, picks 40 tech items from the past 24 hours, summarizes and translates them, and builds one HTML page with the source links. It can also publish that page to Vercel. |
| `skills/eli8/` | eli8 | A thin wrapper around an `eli5` skill for engineers: same simple explainer, but it keeps the real technical terms instead of everyday comparisons. |
| `skills/nice-document/` | nice-document | Builds polished A4 documents (white papers, reports, briefs) as one HTML file. On screen it is one long web page with a linked contents list and a contents sidebar that stays in view. A PDF with A4 pages is optional and made only when asked. Uses the nice-palette base color plus orange, grape and mint only, with red kept for problem tags. Ships with a 9-page sample and a small color script. |
| `skills/nice-palette/` | nice-palette | The default colors: a blue-green base color (`#0D98BA`) with mint, orange, cinnabar, gold, grape, amber-brown, and gray side colors, for any HTML Claude builds. You can pick another named palette: `steel-blue`, `galaxy` (slate base with sage, ochre, terracotta), or `natural` (gray-blue base with copper, mauve, taupe). |
| `skills/nice-presentation/` | nice-presentation | Builds colorful 16:9 HTML slide decks in the nice-palette colors. Takes an optional base color or palette name (such as `galaxy` or `natural`), and ships with three sample decks and a small color script. |
| `skills/prompt-clarity/` | prompt-clarity (`pc`) | Rewrites only the unclear wording of your prompt, then asks whether to run it. |
| `skills/prompt-optimization/` | prompt-optimization (`po`) | Does a fuller prompt rewrite (success criteria, structure, scope), then asks whether to run it. |
| `output-styles/plain/` | Plain | Makes Claude answer in simple, short, everyday English for a non-native reader. |
| `output-styles/eli5/` | eli5 | Makes Claude explain everything as if you know nothing about the topic, with big pictures and very few words. |

The older folders have their own `README.md` with the details. For `daily-briefing`, `eli8`, `nice-document`, `nice-palette`, and `nice-presentation`, the `SKILL.md` file is the only documentation so far.

## How the pieces fit together

```
                    ┌──────────────────────┐
  you type a task → │  Claude Code session │
                    └───────────┬──────────┘
                                │
        ┌───────────────────────┼────────────────────────┐
        │                       │                        │
   Plain or eli5          prompt-clarity /          arch-flow-explainer
   style (how replies     prompt-optimization       (builds the HTML
   are written)           (rewrite the task          diagram)
                           before running it)              │
                                                           │ takes its
                                                           │ colors from
                                                           ▼
                                                     nice-palette
                                                           ▲
   nice-presentation ── takes its colors from ─────────────┤
   nice-document ────── takes its colors from ─────────────┘
   cortex-palette ── only when you ask for Cortex colors
   eli8 ── hands the topic to ──▶ eli5 skill (not in this repo)
   daily-briefing ── works on its own, can publish to Vercel
```

An output style is always on once you select it, and only one style is active at a time. The two prompt skills run only when you ask for them. The `nice-palette` skill is the default color source for anything visual. `arch-flow-explainer`, `nice-presentation` and `nice-document` take their colors from it. The presentation and document skills use only four of its colors (the base color plus orange, grape and mint), with red kept for problem tags. The older `cortex-palette` starts only when you ask for Cortex colors by name.

## Install

Claude Code reads skills and output styles from your home configuration folder, which is `~/.claude`. This repository is the source, and you copy or link the files there.

```bash
# skills: one folder per skill
ln -s "$PWD/skills/arch-flow-explainer"  ~/.claude/skills/arch-flow-explainer
ln -s "$PWD/skills/cortex-palette"       ~/.claude/skills/cortex-palette
ln -s "$PWD/skills/daily-briefing"       ~/.claude/skills/daily-briefing
ln -s "$PWD/skills/eli8"                 ~/.claude/skills/eli8
ln -s "$PWD/skills/nice-document"        ~/.claude/skills/nice-document
ln -s "$PWD/skills/nice-palette"         ~/.claude/skills/nice-palette
ln -s "$PWD/skills/nice-presentation"    ~/.claude/skills/nice-presentation
ln -s "$PWD/skills/prompt-clarity"       ~/.claude/skills/prompt-clarity
ln -s "$PWD/skills/prompt-optimization"  ~/.claude/skills/prompt-optimization

# output styles: the file itself, not the folder
ln -s "$PWD/output-styles/plain/Plain.md" ~/.claude/output-styles/Plain.md
ln -s "$PWD/output-styles/eli5/eli5.md"   ~/.claude/output-styles/eli5.md

# the checklists and the hook script that sends the active style's checklist
ln -s "$PWD/output-styles/plain/hooks/plain-reminder.txt" ~/.claude/hooks/plain-reminder.txt
ln -s "$PWD/output-styles/eli5/hooks/eli5-reminder.txt"   ~/.claude/hooks/eli5-reminder.txt
ln -s "$PWD/output-styles/eli5/hooks/style-reminder.sh"   ~/.claude/hooks/style-reminder.sh
```

Use `cp -r` instead of `ln -s` if you prefer real copies over links. After that, start a new Claude Code session so the files are picked up, and pick Plain or eli5 in `/config` once to turn a writing style on.

Both styles share one hook entry in `~/.claude/settings.json`. See `output-styles/eli5/README.md` for the exact block to merge in and for how the script picks the right checklist.

## Machine-specific paths to check

Some skills contain absolute paths that only exist on the author's machine. Fix them after copying to a new computer, or the skill will fail at that step.

| File | Path inside it | What it is for |
| --- | --- | --- |
| `skills/prompt-clarity/SKILL.md` | `/mnt/c/Program Files/Vim/vim92/gvim.exe` | The editor opened by the "Edit for next prompt" choice. |
| `skills/prompt-optimization/SKILL.md` | `/mnt/c/Program Files/Vim/vim92/gvim.exe` | Same editor, same choice. |
| `output-styles/plain/hooks/settings.json` | `/root/.claude/hooks/style-reminder.sh` | The hook script that injects the active style's checklist before every reply. |
| `skills/daily-briefing/briefing-config.md` | Vercel project `daily-briefing` and `https://daily-briefing-puce.vercel.app` | Where the finished page is published. The first run copies this file into the working folder; set your own project there, or set "Publish to Vercel" to no. |
| `skills/daily-briefing/news-sources.lst` | `web-proxy-smoky.vercel.app` | The author's own feed proxy. The end of `SKILL.md` shows how to deploy your own. |

The Vim path is a Windows program reached from WSL, which is Linux running inside Windows. On a plain Linux or Mac machine, replace it with your own editor command.

## Repository layout

```
claude-code-skills/
├── README.md                       ← you are here
├── output-styles/
│   ├── plain/
│   │   ├── README.md
│   │   ├── Plain.md                ← the style itself
│   │   └── hooks/
│   │       ├── settings.json       ← sample ~/.claude/settings.json
│   │       └── plain-reminder.txt  ← checklist sent while Plain is active
│   └── eli5/
│       ├── README.md
│       ├── eli5.md                 ← the style itself
│       └── hooks/
│           ├── eli5-reminder.txt   ← checklist sent while eli5 is active
│           └── style-reminder.sh   ← hook script shared by both styles
└── skills/
    ├── arch-flow-explainer/
    │   ├── README.md
    │   ├── SKILL.md
    │   ├── references/             ← styling, topology, sequence guides
    │   └── assets/                 ← two complete example HTML diagrams
    ├── cortex-palette/
    │   ├── README.md
    │   └── SKILL.md
    ├── daily-briefing/
    │   ├── SKILL.md
    │   ├── news-sources.lst        ← starter feed list, copied on first run
    │   └── briefing-config.md      ← starter settings, copied on first run
    ├── eli8/
    │   └── SKILL.md
    ├── nice-document/
    │   ├── SKILL.md
    │   ├── palette.py              ← makes document colors from one base color
    │   └── nice-document-sample.html  ← 9-page sample, source of the CSS
    ├── nice-palette/
    │   └── SKILL.md
    ├── nice-presentation/
    │   ├── SKILL.md
    │   ├── palette.py              ← makes deck colors from one base color
    │   └── nice-presentation-sample*.html  ← three sample decks
    ├── prompt-clarity/
    │   ├── README.md
    │   ├── SKILL.md
    │   └── clarity-prompt.md       ← instructions read by the subagent
    └── prompt-optimization/
        ├── README.md
        └── SKILL.md
```

## How a skill is written

Every `SKILL.md` starts with a small header block between two `---` lines. Claude reads the `description` to decide whether the skill applies to what you asked.

```markdown
---
name: cortex-palette
description: When to use this skill, written so Claude can match it to a request.
---

The instructions Claude follows once the skill is loaded.
```

Skills that describe a habit rather than a command, such as `nice-palette`, are meant to start on their own and are never typed. `cortex-palette` starts only when you name it in a request. The two prompt skills and `eli8` are meant to be typed with a slash.

One detail to know: in this session Claude Code lists a skill under its **folder** name, not the `name:` field in the header. The two prompt skills set `name: pc` and `name: po` but sit in folders called `prompt-clarity` and `prompt-optimization`. If typing `/pc` does not find the skill, type `/prompt-clarity` instead, or rename the folder to match the header.
