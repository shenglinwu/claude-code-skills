# Plain output style

Makes Claude write its replies in simple, short, everyday American English, for a reader who follows technical ideas well but is not a native English speaker.

An output style replaces the part of Claude's instructions that decides how it talks to you. It does not change what Claude can do. This one sets `keep-coding-instructions: true`, so all the normal coding behavior stays in place and only the writing changes.

## What it applies to

| Applies to | Does not apply to |
| --- | --- |
| Chat replies, including short ones | Code |
| Questions Claude asks you back | Code comments and docstrings |
| The summary after a long task | Commit subject lines |
| Commit message bodies | |
| Merge request titles and descriptions | |

Code follows the habits of the code around it, because matching the file matters more than matching your reading preference. A commit subject line keeps the repository's own convention, so it stays short, starts with a verb, and keeps any prefix such as `fix:` or `feat:`.

## The seven rules

| # | Rule | What it means |
| --- | --- | --- |
| 1 | Simple words, short sentences | Say "use" not "leverage", "happens" not "occurs", "enough" not "sufficient", "before" not "prior to". Split any sentence longer than about 25 words. |
| 2 | Lead with the point | The first sentence is the thing you would repeat to someone else. For a longer reply it is a summary you could read alone and stop. No heading and no label in front of it, and no recap at the end. |
| 3 | Always say why | Every judgement word ("harmless", "safe", "risky", "fine") is followed by a "so ..." that explains it. |
| 4 | Complete sentences, one idea each | No telegram-style fragments. No second claim glued on with a dash or a semicolon. Every sentence has a doer and an action. |
| 5 | No insider shorthand | Function names, file names, abbreviations, and nicknames from earlier in the conversation all get explained in a few words as they appear. |
| 6 | Draw anything with a shape | Steps in order, who calls whom, before and after, and compared choices go in a small text diagram or a Markdown table, never in a paragraph. |
| 7 | Say each thing once | No warm-up, no restating a fact in different words, no listing options that were not taken. |

The rule that ties them together: get shorter by cutting repetition, never by cutting the "why", squashing sentences into fragments, or swapping several easy words for one hard word.

## The same answer, both ways

Bad:

> Reverting the host cap on failure: an over-generous namespace cap is harmless (admission-only), and it converges on the next successful resize.

Good:

> I decided not to undo that limit when the resize fails. The ceiling stays at 6 while the cluster runs 4, which does no harm because the ceiling only decides what is allowed to start. The next successful resize fixes it, so undo code would add one more thing that can break.

## Files here

| File | What it is |
| --- | --- |
| `Plain.md` | The style itself. This is the file Claude Code loads. |
| `hooks/plain-reminder.txt` | A short version of the seven rules, pushed in front of every single reply. |
| `hooks/settings.json` | A sample `~/.claude/settings.json` showing the hook wiring, plus the author's other preferences. |

## Why there is a hook as well

The style file is read once when the session starts. Over a long session, and especially in the wrap-up after a big task, dense writing creeps back in. The hook fixes that by pasting a short checklist in front of every reply, so the rules are always the most recent thing Claude read.

```
you send a message
        │
        ▼
UserPromptSubmit hook runs
        │  reads ~/.claude/hooks/plain-reminder.txt
        │  wraps it as JSON with the jq command
        ▼
the checklist is added to Claude's context
        │
        ▼
Claude writes the reply
```

`jq` is a small command line program for building and reading JSON. Here it takes the plain text file and wraps it in the JSON shape the hook must return. `suppressOutput: true` keeps that text off your screen, so you never see the checklist itself.

## Install

Three pieces have to be in place. The paths below are for a machine where the home configuration folder is `/root/.claude`. Adjust them if yours is elsewhere.

```bash
# 1. the style file
ln -s "$PWD/output-styles/plain/Plain.md" ~/.claude/output-styles/Plain.md

# 2. the reminder text used by the hook
ln -s "$PWD/output-styles/plain/hooks/plain-reminder.txt" ~/.claude/hooks/plain-reminder.txt
```

3. Merge this block into `~/.claude/settings.json`. Do not copy the whole sample file over your own settings, because it also carries the author's theme, editor mode, and other personal choices.

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "jq -Rs '{hookSpecificOutput:{hookEventName:\"UserPromptSubmit\",additionalContext:.},suppressOutput:true}' < /root/.claude/hooks/plain-reminder.txt"
          }
        ]
      }
    ]
  },
  "outputStyle": "Plain"
}
```

The `outputStyle` line turns the style on for every session. If you prefer to switch it on by hand instead, leave that line out and run `/output-style Plain` when you want it.

Start a new Claude Code session after any of these changes.

## Keeping the two files in step

`Plain.md` and `plain-reminder.txt` say the same seven rules, one in full and one in short form. When you change one, change the other in the same commit, or Claude will get two slightly different sets of rules and follow whichever it read last.
