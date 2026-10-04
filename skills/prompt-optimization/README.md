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
| Fixable | Intent is clear, but something is missing, or something is left over from older models (shouting, "think step by step", hype, scripted steps) | Fix only that. Keep the author's wording everywhere else. |
| Unclear | Ambiguous, contradictory, or a wall of text | A full rewrite is justified. |

The skill also works out where the prompt is heading, because that changes which fixes apply: a one-shot answer, a document or creative piece, an agent task such as changing code across several steps, or a brief for another model (a subagent brief or a system prompt).

## Step 2: the fourteen techniques

The skill assumes the reader is a current frontier model: one that follows instructions closely and literally, thinks and plans on its own, and can carry a long task through alone. So a good prompt says plainly what is wanted, supplies what only the author knows, and drops anything written to push a weaker model.

| # | Technique | The short version |
| --- | --- | --- |
| | **Add what is missing** | |
| 1 | Success criteria | Say what a good result looks like in checkable terms: scope, audience, format. For length, describe the reader. Use a number only if the author gave one. |
| 2 | Purpose | Keep the author's "who is this for" and "why" near the top, so the model can make the small calls the prompt did not cover. |
| 3 | Surface missing context, never invent it | Insert a marker like `[specify: deployment target]` instead of guessing the stack or the scale. |
| 4 | Room to say "I don't know" | Allow the answer "the information is not available" instead of a guess. For facts that change quickly, ask for a check against a current source. |
| | **Take out what no longer helps** | |
| 5 | Thinking scaffolds | Remove "think step by step", `<thinking>` blocks, and "think harder". A demand to show the full reasoning becomes a request for a short explanation, because the newest models can decline to reproduce raw reasoning. |
| 6 | Pressure and hedges | Capitals, `MUST`, and "don't be lazy" become plain statements, because a shouted rule gets applied too widely. "Try to" on a real requirement becomes the requirement. |
| 7 | Hype and padding | Skip "you are a world-class expert" and "be accurate and clear". Keep a role only when the audience or the lens changes the answer. |
| 8 | Scripted steps for judgment work | Replace "first read, then list, then write" with the outcome, the limits, and how to check it. Keep exact steps only where the order is the requirement. |
| 9 | Style prohibitions | Say what to produce instead of what to avoid. Real limits (scope, safety, business rules) stay as limits. |
| | **Shape it for the reader** | |
| 10 | Structure | Long reference material goes first inside tags, the actual question goes last. Everything else is plain prose, because the model mirrors the prompt's formatting. |
| 11 | Examples | Models copy every detail of an example. Fix the author's examples if they do not match. Never write a new one; describe the format instead. |
| | **Fit it to where it is going** | |
| 12 | Agent tasks | Define done with a real check, keep the change to what was asked, keep a question a question, and ask for a report that leads with the outcome. |
| 13 | Briefs for another model | The other model knows only what the brief says: the goal, what is already known, the limits, and what to send back. |
| 14 | Visual and frontend work | Words like "nice" or "modern" do not steer the model. Ask the author for a direction with a marker. |

Technique 4 has one trap worth knowing. A rule like "include the deadline if one was given" must not become filler such as "Deadline: none stated". Your conditional already covered the missing case, so turning it into mandatory text changes your format.

## The four choices in step 3

| Choice | What happens |
| --- | --- |
| Yes, execute it | Claude runs the improved prompt right away, as if you had typed it yourself. |
| Save for next prompt | The text is written to `/tmp/.claude.saved_prompt.txt`. In your next message you write `@saved` and it is replaced by that text. |
| Edit for next prompt | Same as saving, and then your editor opens on the file. The prompt is not run yet. |
| No, just keep the prompt | Nothing else happens. |

## What always survives untouched

Technical terms, proper names, numbers, exact format contracts, conditional phrasing of the form "if X then Y", every example or template you supplied, and anything Claude Code itself acts on (slash commands, `@` mentions, file paths, mode keywords). When two readings are both possible, the skill keeps your wording rather than picking one.

## Install and machine-specific path

```bash
ln -s "$PWD/skills/prompt-optimization" ~/.claude/skills/prompt-optimization
```

`SKILL.md` names one editor from the author's computer: `/mnt/c/Program Files/Vim/vim92/gvim.exe`, which is a Windows program reached from WSL. Only the "Edit for next prompt" choice needs it, so the other three choices work anywhere. Replace it with your own editor command on a plain Linux or Mac machine.

Unlike `prompt-clarity`, this skill keeps all its instructions in one file and does not start a subagent. That costs more room in your session, and in exchange it can act on the result immediately with your full context available.
