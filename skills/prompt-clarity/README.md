# prompt-clarity

Sharpens only the unclear wording in a prompt, then asks you what to do with the result. It changes how the request is worded, never what the request asks for.

This is the light version. Its bigger sibling `prompt-optimization` in this repository also adds success criteria, restructures sections, and defines what "done" means. Use this one when your prompt is already the right shape and only a few sentences could be read two ways.

## How to run it

```
/prompt-clarity fix the tests so they pass and clean up that file
```

Whatever you type after the skill name becomes the prompt to work on.

Note on the name: the header inside `SKILL.md` says `name: pc`, but Claude Code lists the skill under its folder name. If `/pc` is not found, type `/prompt-clarity`, or rename the folder to `pc` so the two match.

## What happens, step by step

```
you type /prompt-clarity <your prompt>
        │
        ▼
1. a subagent is started
   it reads clarity-prompt.md by itself and does the rewriting
   in its own separate memory
        │
        ▼
2. only the finished prompt comes back to your session
        │
        ▼
3. the prompt is shown to you, then you pick one of four choices
```

The subagent exists to keep your session small. The long instruction file and all the thinking about the rewrite stay in the subagent's own memory, and your session only ever sees the short finished result.

## The four choices

| Choice | What happens |
| --- | --- |
| Yes, execute it | Claude runs the improved prompt right away, as if you had typed it yourself. |
| Save for next prompt | The text is written to `/tmp/.claude.saved_prompt.txt`. In your next message you write `@saved` and it is replaced by that text. |
| Edit for next prompt | Same as saving, and then your editor opens on the file so you can change it first. |
| No, just keep the prompt | Nothing else happens. You keep the text on screen. |

## The five things it fixes

The rewriting rules live in `clarity-prompt.md`. Only these five edits are allowed:

| Problem | Example fix |
| --- | --- |
| A vague "it", "this", or "that" | Replace the word with the actual thing it points at. |
| No stated doer | "should be validated" becomes "the API should validate the input". |
| Unclear scope | Make clear whether "all", "some", or "each" is meant. |
| A phrase with two readings | Rewrite so only the meaning you intended survives. |
| Fuzzy conditions | "as needed" becomes a real if-then rule. |

## The two guard rails

**It edits sentence by sentence and copies the rest exactly.** Modern models guess intent well, so rewording a sentence that was already clear is pure drift away from what you asked. If nothing in your prompt is ambiguous, the skill hands your prompt back unchanged. That is the correct answer, not a failure.

**It never guesses an answer it does not have.** If clearing up "as needed" would need information you did not give, the skill keeps your wording or inserts a marker like `[specify: which tests]` for you to fill in. A guessed answer quietly changes what the prompt asks for, which is worse than the original vagueness.

## What it deliberately leaves alone

| Left alone | Why |
| --- | --- |
| Headings, bullet order, sections | Structure is not clarity. |
| Vague words like "good" or "appropriate" | That is a question of detail, not of double meaning. |
| Missing background | Adding it would mean inventing facts. |
| Filler and polite phrases | Trimming is a question of length, not clarity. |
| Technical terms, names, examples, templates | These carry meaning that must survive untouched. |

## Files

| File | What it is |
| --- | --- |
| `SKILL.md` | The three steps run in your session: start the subagent, show the result, ask the four questions. |
| `clarity-prompt.md` | The rewriting rules. Only the subagent reads this, never your main session. |

## Install and machine-specific paths

```bash
ln -s "$PWD/skills/prompt-clarity" ~/.claude/skills/prompt-clarity
```

Two absolute paths inside `SKILL.md` come from the author's computer. Fix both on a new machine.

| Path | What it is | If it is wrong |
| --- | --- | --- |
| `/root/.claude/skills/prompt-clarity/clarity-prompt.md` | The rules file the subagent opens | The subagent cannot read the rules, so step 1 fails. |
| `/mnt/c/Program Files/Vim/vim92/gvim.exe` | A Windows editor reached from WSL | Only the "Edit for next prompt" choice breaks. The other three still work. |
