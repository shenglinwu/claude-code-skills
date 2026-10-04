---
name: po
description: Optimize a prompt for clarity and effectiveness before execution
---

You are optimizing the prompt below before it is sent to an AI assistant. Assume the reader is a current frontier model. Such a model follows instructions closely and literally, thinks and plans without being told to, and can carry a long task through on its own. That changes what a good prompt looks like: it says plainly what is wanted, supplies what only the author knows, and leaves out anything written to push or steer a weaker model.

The skill has three steps: triage, print the optimized prompt, then call the `AskUserQuestion` tool in the same turn so the user can choose what happens to the prompt.

<original_prompt>
$ARGUMENTS
</original_prompt>

## Step 1: Triage before rewriting

The reader infers intent well, so over-editing a prompt does as much harm as leaving it vague. Pick an intervention level first:

- **Sound**: intent, success criteria, and output format are already clear. Return it unchanged, or with one or two small fixes. A prompt that works stays as written; restructuring or expanding it to look optimized makes it worse.
- **Fixable**: intent is clear, but something is missing (success criteria, format, scope) or is left over from older models (shouting, "think step by step", hype, scripted steps). Fix only that, and keep the author's wording and structure everywhere else.
- **Unclear**: ambiguous intent, a wall of text, or asks that contradict each other. A full rewrite is justified.

Then identify where the prompt is going, because that decides which techniques apply: a one-shot answer, a document or creative deliverable, an **agentic task** (code changes, multi-step tool work), or a **brief for another model** (a subagent brief or a system prompt).

## Step 2: Apply the techniques that fit

<techniques>

### Add what is missing

1. **Success criteria.** State what a good result looks like in checkable terms: scope, audience, format, and the order of priorities. The reader does what the words say, so state exactly what is wanted and no more. For length, describe the reader and the purpose ("an executive will skim this on a phone"); use a number only when the author gave one.

2. **Purpose.** The reader does better work when it knows who the result is for and what it will be used for, because it can then make the small judgment calls the prompt did not cover. If the author stated a purpose or a reason for a rule, keep it and place it where it is seen early. A reason the author did not give is missing context (technique 3), not something to write for them.

3. **Missing context: surface it, never invent it.** If the prompt depends on information the author did not provide (stack, scale, environment, audience, preferences), insert a bracketed placeholder for the author to fill in (`[specify: deployment target]`), or add an instruction for the reader ("State any assumptions you make about X before answering"). Invented specifics silently corrupt the answer.

4. **Room to say "I don't know".** For factual, analytical, or extraction tasks, permit uncertainty: "If the information isn't available or isn't enough, say so rather than guessing." When the task turns on facts that change quickly (versions, prices, current products), also ask the reader to check a current source if it has one. This governs the reader's factual claims only and leaves the author's output format alone: a conditional such as "include the deadline if one was stated" stays a conditional, and does not become filler such as "Deadline: none stated".

### Take out what no longer helps

5. **Thinking scaffolds.** Remove "think step by step", "take a deep breath", `<thinking>`/`<scratchpad>` sections, and prose that steers thinking depth ("think harder", "don't overthink"). The reader reasons on its own, and how deeply it thinks is a setting of the harness, so these lines are noise. Replace a demand to show the full reasoning with a request for a short explanation of the answer, because the newest models can decline to reproduce their raw reasoning. Asking for a plan stays when the plan is itself a deliverable ("outline the migration steps before writing the code").

6. **Pressure and hedges.** Rewrite capitals, `MUST`/`CRITICAL`/`IMPORTANT` markers, and exclamation runs as plain statements; a shouted rule gets applied too widely and too rigidly. Remove effort boosters ("be thorough", "don't be lazy"), which describe what the reader already does. The reverse also holds: "try to" or "if possible" attached to a real requirement is read as permission to skip it, so state the requirement plainly. When you cannot tell whether the author meant it as optional, keep the author's words.

7. **Hype and padding.** Remove capability personas ("you are a world-class expert"), generic virtues ("be accurate and clear"), and reminders that repeat an earlier line. Keep or add a role only when a domain lens, audience, or tone changes the answer ("explain for a non-technical executive").

8. **Scripted steps for judgment work.** If the original walks the reader through steps for work that needs judgment (read, then list, then write, then double-check), restate it as the outcome, the constraints, and how to check the result; the reader's own plan is usually better than a script. Keep exact steps where the order is the requirement or only one sequence is safe (destructive commands, compliance procedures, exact formats). Never turn an outcome-oriented ask into a recipe.

9. **Style prohibitions.** Rewrite "don't do X" style rules as what to produce instead, since naming a failure can pull the reader toward it. Keep prohibitions that are real constraints (scope limits, safety, business rules), with their reason beside them when the author gave one.

### Shape it for the reader

10. **Structure.** When the prompt carries long reference material or data, separate it from the instructions with XML tags (`<report>`, `<data>`) and put it first, with the ask last. Otherwise write the prompt as plain prose in the style the answer should take: the reader mirrors the prompt's formatting, and bullet lists cut rules off from their reasons. A short prompt does not need headings. If the original is already well structured, keep its structure exactly.

11. **Examples.** The reader copies examples closely, including length, tone, and incidental details. Check that the author's examples match the behavior they ask for and fix mismatches. Do not write an example of your own, since its content would be invented; when the format matters and no example exists, describe the format or give a skeleton with placeholders.

### Fit it to where it is going

12. **Agentic tasks.** These matter more than any wording polish:
    - *Done and verified.* Say what finished looks like, using checks the author named ("done when `npm test` passes"). If the author named none, ask for a real check that exercises the change (the project's tests, build, or the changed command itself) with its output shown, without making up command names or paths.
    - *Scope.* Keep the change to what was asked. Other problems the reader notices are reported at the end, not fixed.
    - *A question stays a question.* If the author is asking something or describing a problem, the deliverable is an assessment. Do not turn it into a request to change things.
    - *Report.* Ask for the outcome first, then what was verified and what was not.
    - *Unattended runs.* Only when the author says the task runs without them: name the actions that still need their go-ahead (destructive ones, anything outside the scope) and say the rest proceeds without check-ins.

13. **Briefs for another model.** A subagent or a system-prompted model knows only what the brief says. Check that it carries the goal and what the result is for, what is already known or ruled out, the constraints, and what to send back and in what form. Use what the author gave and add placeholders for the rest.

14. **Visual and frontend work.** Vague taste words ("nice", "modern", "not generic") do not steer the reader; it falls back on its default look. Do not add more of them. Ask for the direction with a placeholder (`[specify: look and feel, or a site to take cues from]`).

</techniques>

<rules>

- Preserve the original intent. Optimize how the request is expressed, not what it asks for. When two readings are possible, keep the author's wording.
- Preserve domain terms, proper nouns, technical details, numbers, exact format contracts, and conditional phrasing ("if X, then Y") exactly. A precise contract stays the same contract.
- Preserve the author's examples, templates, and sample formats.
- Preserve anything the harness acts on: slash commands, `@` mentions, file paths, and keywords that switch a mode. They are configuration, not wording.
- Add no facts, context, or assumptions the author did not state (technique 3).
- Keep the edit proportional to the defects found in step 1. A short, clear prompt comes back short and clear.
- Step 2 only rewrites. The task inside the prompt is not carried out until the user chooses that in step 3.
- Print only the optimized prompt, as plain text ready to paste: no code fence, no JSON, and no notes about what changed.

</rules>

## Step 3: Ask what to do next (same turn)

Right after printing the optimized prompt, call the `AskUserQuestion` tool with these four options: "Yes, execute it", "Save for next prompt", "Edit for next prompt", and "No, just keep the prompt".

Printing the prompt does not end the turn. Without this call the user has no way to say "run it", so a run that stops after step 2 has failed even if the prompt is perfect. Use the tool itself rather than a plain-text question, and call it in this turn rather than the next.

If the user selects "Yes, execute it", execute the optimized prompt faithfully, following all relevant skills and instructions as if the user had typed the optimized prompt directly.

If the user selects "Save for next prompt", silently delete the file `/tmp/.claude.saved_prompt.txt` if it exists and write the full optimized prompt text to the file `/tmp/.claude.saved_prompt.txt`, confirm to the user that the prompt has been saved, and inform the user that they can reference the saved prompt in their next message by using the placeholder `@saved` (e.g., `/pc @saved`).

If the user selects "Edit for next prompt", silently delete the file `/tmp/.claude.saved_prompt.txt` if it exists and write the full optimized prompt text to the file `/tmp/.claude.saved_prompt.txt`, run `! /mnt/c/Program\ Files/Vim/vim92/gvim.exe /tmp/.claude.saved_prompt.txt` command, don't execute the modified prompt yet, and inform the user that they can reference the saved prompt in their next message by using the placeholder `@saved` (e.g., `/po @saved`).

If the user selects "No, just keep the prompt", stop and do nothing further.
