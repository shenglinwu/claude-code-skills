# claude-code-skills

Personal Claude Code skills and output styles, kept in one repository so they can be versioned and copied to a new machine.

A **skill** is a folder of instructions that Claude Code loads when the task matches. An **output style** changes how Claude writes its replies to you. Neither is program code. Both are Markdown files that Claude reads.

## What is in here

| Folder | Name | What it does |
| --- | --- | --- |
| `skills/arch-flow-explainer/` | arch-flow-explainer | Draws system architecture and call flows as a single self-contained HTML file with an inline SVG picture. |
| `skills/cortex-palette/` | cortex-palette | The default brand colors for anything visual: pages, slides, charts, diagrams. |
| `skills/prompt-clarity/` | prompt-clarity (`pc`) | Rewrites only the unclear wording of your prompt, then asks whether to run it. |
| `skills/prompt-optimization/` | prompt-optimization (`po`) | Does a fuller prompt rewrite (success criteria, structure, scope), then asks whether to run it. |
| `output-styles/plain/` | Plain | Makes Claude answer in simple, short, everyday English for a non-native reader. |
| `output-styles/eli5/` | eli5 | Makes Claude explain everything as if you know nothing about the topic, with big pictures and very few words. |

Each folder has its own `README.md` with the details.

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
                                                    cortex-palette
```

An output style is always on once you select it, and only one style is active at a time. The two prompt skills run only when you ask for them. The `cortex-palette` skill feeds colors to any visual skill, including `arch-flow-explainer`.

## Install

Claude Code reads skills and output styles from your home configuration folder, which is `~/.claude`. This repository is the source, and you copy or link the files there.

```bash
# skills: one folder per skill
ln -s "$PWD/skills/arch-flow-explainer"  ~/.claude/skills/arch-flow-explainer
ln -s "$PWD/skills/cortex-palette"       ~/.claude/skills/cortex-palette
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

Two skills contain absolute paths that only exist on the author's machine. Fix them after copying to a new computer, or the skill will fail at that step.

| File | Path inside it | What it is for |
| --- | --- | --- |
| `skills/prompt-clarity/SKILL.md` | `/root/.claude/skills/prompt-clarity/clarity-prompt.md` | The instruction file the subagent reads. |
| `skills/prompt-clarity/SKILL.md` | `/mnt/c/Program Files/Vim/vim92/gvim.exe` | The editor opened by the "Edit for next prompt" choice. |
| `skills/prompt-optimization/SKILL.md` | `/mnt/c/Program Files/Vim/vim92/gvim.exe` | Same editor, same choice. |
| `output-styles/plain/hooks/settings.json` | `/root/.claude/hooks/style-reminder.sh` | The hook script that injects the active style's checklist before every reply. |

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

Skills that describe a habit rather than a command, such as `cortex-palette`, are meant to start on their own and are never typed. The two prompt skills are meant to be typed with a slash.

One detail to know: in this session Claude Code lists a skill under its **folder** name, not the `name:` field in the header. The two prompt skills set `name: pc` and `name: po` but sit in folders called `prompt-clarity` and `prompt-optimization`. If typing `/pc` does not find the skill, type `/prompt-clarity` instead, or rename the folder to match the header.
