# prompt-optimization

Rewrites a prompt into a better version before it is run, then asks you whether to run it. It works on how the request is expressed, never on what the request asks for.

Its smaller sibling `prompt-clarity` in this repository only removes double meanings. This skill can also add success criteria, reorder sections, set the scope, and define what "done" means for an agent.

## How to run it

```
/prompt-optimization add caching to the user lookup endpoint
```

Everything you type after the skill name becomes the prompt to work on.

Note on the name: the header inside `SKILL.md` says `name: po`, but Claude Code lists the skill under its folder name. If `/po` is not found, type `/prompt-optimization`, or rename the folder to `po` so the two match.

## The three steps

```
step 1  judge how broken the prompt is, and where it is going
step 2  apply only the fixes that match, and print the result
step 3  ask you: run it, save it, edit it, or keep it
```

Step 3 is not optional. A run that prints a perfect prompt and then stops counts as a failed run, because you are left with no way to say "now run it".

## Step 1: how much to change

The size of the edit has to match the size of the problem. Rewriting a prompt that already worked is as harmful as leaving a broken one alone.

| Verdict | What the prompt looks like | What the skill does |
| --- | --- | --- |
| Sound | Intent, success criteria, and output format are already clear | Return it unchanged, or make one or two small fixes. No restructuring. |
| Fixable gaps | Intent is clear but something is missing | Patch only the gap. Keep the author's wording everywhere else. |
| Genuinely unclear | Ambiguous, contradictory, or a wall of text | A full rewrite is justified. |

The skill also works out where the prompt is heading, because that changes which fixes apply: a one-shot answer, a document or creative piece, or an agent task such as changing code across several steps.

## Step 2: the eleven techniques

| # | Technique | The short version |
| --- | --- | --- |
| 1 | Explicit success criteria | Say what a good result looks like in checkable terms: scope, audience, length, format. |
| 2 | Motivation over mandate | Add a short "why" to a rule, so the model follows the spirit and not just the letter. |
| 3 | Specificity | Replace "good", "proper", "clean" with real criteria. Say what to produce, not what to avoid. |
| 4 | Structure and ordering | Separate parts with tags or headings. Long reference material goes first, the actual question goes last. |
| 5 | Right degree of freedom | For open or agent work, state the outcome and the hard limits, then leave the method alone. Script exact steps only when the steps truly must be fixed. |
| 6 | Surface missing context, never invent it | Insert a marker like `[specify: deployment target]` instead of guessing the stack or the scale. |
| 7 | Escape hatch for facts | Allow the answer "the information is not available" instead of a guess. This is the single strongest guard against invented facts. |
| 8 | Examples that match | Models copy every detail of an example, including the accidental ones. Fix any example that does not match the wanted behavior. |
| 9 | No thinking scaffolding | Never add "think step by step" or `<thinking>` blocks. Modern models already reason on their own, so this is noise that can fight the harness. Existing boilerplate of this kind gets removed. |
| 10 | Agent tasks: define done | Add a finish test ("done when `pytest tests/x` passes"), a check step ("run the tests and show the output"), and a boundary ("only touch files under `src/api/`"). |
| 11 | Role framing only when it matters | Add a role when the audience or the lens really changes the answer. Skip "you are a world-class expert", because it adds nothing on modern models. |

Technique 7 has one trap worth knowing. A rule like "include the deadline if one was given" must not become filler such as "Deadline: none stated". Your conditional already covered the missing case, so turning it into mandatory text changes your format.

## The four choices in step 3

| Choice | What happens |
| --- | --- |
| Yes, execute it | Claude runs the improved prompt right away, as if you had typed it yourself. |
| Save for next prompt | The text is written to `/tmp/.claude.saved_prompt.txt`. In your next message you write `@saved` and it is replaced by that text. |
| Edit for next prompt | Same as saving, and then your editor opens on the file. The prompt is not run yet. |
| No, just keep the prompt | Nothing else happens. |

## What always survives untouched

Technical terms, proper names, exact format contracts, conditional phrasing of the form "if X then Y", and every example or template you supplied. When two readings are both possible, the skill keeps your wording rather than picking one.

## Install and machine-specific path

```bash
ln -s "$PWD/skills/prompt-optimization" ~/.claude/skills/prompt-optimization
```

`SKILL.md` names one editor from the author's computer: `/mnt/c/Program Files/Vim/vim92/gvim.exe`, which is a Windows program reached from WSL. Only the "Edit for next prompt" choice needs it, so the other three choices work anywhere. Replace it with your own editor command on a plain Linux or Mac machine.

Unlike `prompt-clarity`, this skill keeps all its instructions in one file and does not start a subagent. That costs more room in your session, and in exchange it can act on the result immediately with your full context available.
