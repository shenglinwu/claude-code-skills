# eli5 output style

Makes Claude explain everything as if you know nothing about the topic. Replies start with a big, simple picture and use very few words.

It is based on the `eli5` skill from the `claude-community` plugin marketplace. That skill builds one HTML page of big pictures when you type `/eli5 <topic>`. This style turns the same idea into rules for every reply, so you do not have to ask each time.

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

## The five rules

| # | Rule | What it means |
| --- | --- | --- |
| 1 | Assume you know nothing | Every term, tool, file name, and function name gets a few everyday words or a place in the picture, even names from earlier in the conversation. |
| 2 | Picture first, words second | Anything with a shape (parts that connect, steps, before and after, choices) starts with a text diagram or a Markdown table. It has about 7 boxes at most, with one to three words per label. |
| 3 | Very few words | Each picture gets a caption of one or two short sentences. The one reason that matters stays, written as "this happens, so that happens". |
| 4 | Big explanations get a page | A "how does X work" question, or any answer that needs more than one picture, becomes an HTML artifact built like a picture book. The terminal gets the link and a two or three line summary. |
| 5 | Lead with the answer | The first line is the thing you would repeat to someone else. No warm-up, no recap, and nothing said twice. |

An HTML artifact is a web page that Claude Code publishes for you on claude.ai. Only big explanations get one, because a page for every short status update would be slow and noisy.

## The same answer, both ways

Bad:

> DNS resolution involves a recursive resolver querying the root, TLD, and authoritative nameservers to map a hostname to an IP address, and the result is cached according to its TTL.

Good:

DNS is the internet's phone book. It turns a name into a number that computers can call.

```
  you type          phone book           computer calls
 example.com  -->  "whose number?"  -->  1.2.3.4
                        |
                  remembers it
                  for a while
```

Your computer asks the phone book once and then remembers the number, so your next visit starts faster.

## Files here

| File | What it is |
| --- | --- |
| `eli5.md` | The style itself. This is the file Claude Code loads. |
| `hooks/eli5-reminder.txt` | A short version of the five rules, sent in front of every reply while eli5 is active. |
| `hooks/style-reminder.sh` | The hook script. It finds the active style and sends that style's checklist. The Plain style uses it too. |

## Why there is a hook as well

Over a long session, and especially in the wrap-up after a big task, the style rules fade. The hook fixes that by pasting a short checklist in front of every reply, so the rules are always the most recent thing Claude read.

The hook has one more job. Plain and eli5 each have their own checklist, and Claude Code does not tell a hook which style is active. If both checklists were sent every time, they would disagree. So the script looks up the style itself, like a mail sorter reading the address on each letter:

```
you send a message
        │
        ▼
UserPromptSubmit hook runs style-reminder.sh
        │  takes "outputStyle" from the first settings file that has it:
        │    1. /etc/claude-code/managed-settings.json
        │    2. <project>/.claude/settings.local.json
        │    3. <project>/.claude/settings.json
        │    4. ~/.claude/settings.json
        ▼
"eli5"   →  sends eli5-reminder.txt
"Plain"  →  sends plain-reminder.txt
other    →  sends nothing
        │
        ▼
Claude writes the reply
```

A style named `<Name>` maps to `<name>-reminder.txt`, in lower case, in the folder where the script is linked. So a new style gets its own checklist once you add that one file.

When you pick a style in `/config`, Claude Code saves it to the project's `.claude/settings.local.json`. The script reads that file on your next message, so a switch in the middle of a session works. One limit: a style passed on the command line with `claude --settings` never reaches a file, so the script cannot see it.

The script needs `jq`, a small command line program for reading and building JSON. It reads the settings files with `jq`, and it also uses `jq` to wrap the checklist in the JSON shape the hook must return. `suppressOutput: true` keeps that text off your screen, so you never see the checklist itself.

## Install

Three pieces have to be in place. The paths below are for a machine where the home configuration folder is `/root/.claude`. Adjust them if yours is elsewhere.

```bash
# 1. the style file
ln -s "$PWD/output-styles/eli5/eli5.md" ~/.claude/output-styles/eli5.md

# 2. the checklist and the hook script that sends it
ln -s "$PWD/output-styles/eli5/hooks/eli5-reminder.txt" ~/.claude/hooks/eli5-reminder.txt
ln -s "$PWD/output-styles/eli5/hooks/style-reminder.sh" ~/.claude/hooks/style-reminder.sh
```

3. Merge this block into `~/.claude/settings.json`. One hook serves both Plain and eli5. If you still have the older Plain hook that runs `jq ... < plain-reminder.txt`, replace it with this one, because keeping both would send the Plain checklist even while eli5 is active.

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/root/.claude/hooks/style-reminder.sh"
          }
        ]
      }
    ]
  },
  "outputStyle": "eli5"
}
```

The `outputStyle` line turns eli5 on for every session. If you prefer to switch it on by hand instead, leave that line out and pick eli5 in `/config` when you want it.

Start a new Claude Code session after any of these changes.

## Keeping the two files in step

`eli5.md` and `eli5-reminder.txt` say the same five rules, one in full and one in short form. When you change one, change the other in the same commit, or Claude will get two slightly different sets of rules and follow whichever it read last.
