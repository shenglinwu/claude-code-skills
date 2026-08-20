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

Each folder has its own `README.md` with the details.

## How the pieces fit together

```
                    ┌──────────────────────┐
  you type a task → │  Claude Code session │
                    └───────────┬──────────┘
                                │
        ┌───────────────────────┼────────────────────────┐
        │                       │                        │
   Plain style            prompt-clarity /          arch-flow-explainer
   (how replies           prompt-optimization       (builds the HTML
    are written)          (rewrite the task          diagram)
                           before running it)              │
                                                           │ takes its
                                                           │ colors from
                                                           ▼
                                                    cortex-palette
```

The Plain output style is always on once you select it. The two prompt skills run only when you ask for them. The `cortex-palette` skill feeds colors to any visual skill, including `arch-flow-explainer`.

## Install

Claude Code reads skills and output styles from your home configuration folder, which is `~/.claude`. This repository is the source, and you copy or link the files there.

```bash
# skills: one folder per skill
ln -s "$PWD/skills/arch-flow-explainer"  ~/.claude/skills/arch-flow-explainer
ln -s "$PWD/skills/cortex-palette"       ~/.claude/skills/cortex-palette
ln -s "$PWD/skills/prompt-clarity"       ~/.claude/skills/prompt-clarity
ln -s "$PWD/skills/prompt-optimization"  ~/.claude/skills/prompt-optimization

# output style: the file itself, not the folder
ln -s "$PWD/output-styles/plain/Plain.md" ~/.claude/output-styles/Plain.md

# the reminder text used by the Plain style hook
ln -s "$PWD/output-styles/plain/hooks/plain-reminder.txt" ~/.claude/hooks/plain-reminder.txt
```

Use `cp -r` instead of `ln -s` if you prefer real copies over links. After that, start a new Claude Code session so the files are picked up, and run `/output-style Plain` once to turn the writing style on.

The Plain style also needs a hook entry in `~/.claude/settings.json`. See `output-styles/plain/README.md` for the exact block to merge in.

## Machine-specific paths to check

Two skills contain absolute paths that only exist on the author's machine. Fix them after copying to a new computer, or the skill will fail at that step.

| File | Path inside it | What it is for |
| --- | --- | --- |
| `skills/prompt-clarity/SKILL.md` | `/root/.claude/skills/prompt-clarity/clarity-prompt.md` | The instruction file the subagent reads. |
| `skills/prompt-clarity/SKILL.md` | `/mnt/c/Program Files/Vim/vim92/gvim.exe` | The editor opened by the "Edit for next prompt" choice. |
| `skills/prompt-optimization/SKILL.md` | `/mnt/c/Program Files/Vim/vim92/gvim.exe` | Same editor, same choice. |
| `output-styles/plain/hooks/settings.json` | `/root/.claude/hooks/plain-reminder.txt` | The checklist text injected before every reply. |

The Vim path is a Windows program reached from WSL, which is Linux running inside Windows. On a plain Linux or Mac machine, replace it with your own editor command.

## Repository layout

```
claude-code-skills/
├── README.md                       ← you are here
├── output-styles/
│   └── plain/
│       ├── README.md
│       ├── Plain.md                ← the style itself
│       └── hooks/
│           ├── settings.json       ← sample ~/.claude/settings.json
│           └── plain-reminder.txt  ← checklist injected on every prompt
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
