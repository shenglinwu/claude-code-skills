---
name: pc
description: Optimize a prompt for clarity before execution
---

The prompt to enhance is provided as `$ARGUMENTS`.

If `$ARGUMENTS` is `@saved`, or contains `@saved`, read `/tmp/.claude.saved_prompt.txt` and use its text in place of `@saved`. If that file does not exist, tell the user no prompt is saved and stop.

To keep this session's context small, run the clarity enhancement in a subagent: the heavy instruction block and the optimization reasoning stay in the subagent's isolated context, and only the finished enhanced prompt returns here. The interactive choice and any execution stay in THIS session.

## Step 1 — Offload the optimization to a subagent

Call the `Agent` tool (`subagent_type: "general-purpose"`, `model: "sonnet"`) with a **short** prompt (keep it short so the heavy instructions are not loaded into this session's context — the subagent reads them from file itself):

> Read `${CLAUDE_SKILL_DIR}/clarity-prompt.md` and follow it exactly to clarity-enhance the prompt below. Return ONLY the clarity-enhanced prompt as plain text — no preamble, no code fences, no explanation.
>
> `<original_prompt>`
> *(the `$ARGUMENTS` content, verbatim, with `@saved` already replaced)*
> `</original_prompt>`

The subagent's returned message is the clarity-enhanced prompt.

## Step 2 — Present and offer choices (in this session)

First print the full clarity-enhanced prompt as your visible reply text, so the user can read it before deciding. Do not skip it, shorten it, or put it only inside a tool call. Only after the prompt is printed, use the `AskUserQuestion` tool to ask whether to execute it, with these four options: "Yes, execute it", "Save for next prompt", "Edit for next prompt", and "No, just keep the prompt". The question dialog can hide text printed earlier in the turn, so also put the full clarity-enhanced prompt in the `preview` field of each option.

If the user selects **"Yes, execute it"**, execute the clarity-enhanced prompt faithfully in this session, following all relevant skills and instructions as if the user had typed the enhanced prompt directly.

If the user selects **"Save for next prompt"**, silently delete the file `/tmp/.claude.saved_prompt.txt` if it exists and write the full clarity-enhanced prompt text to the file `/tmp/.claude.saved_prompt.txt`, confirm to the user that the prompt has been saved, and inform the user that they can reference the saved prompt in their next message by using the placeholder `@saved` (e.g., `/pc @saved`).

If the user selects **"Edit for next prompt"**, silently delete the file `/tmp/.claude.saved_prompt.txt` if it exists and write the full clarity-enhanced prompt text to the file `/tmp/.claude.saved_prompt.txt`, open the file for the user by running `/mnt/c/Program\ Files/Vim/vim92/gvim.exe /tmp/.claude.saved_prompt.txt` with the Bash tool, don't execute the modified prompt yet, and inform the user that they can reference the saved prompt in their next message by using the placeholder `@saved` (e.g., `/pc @saved`).

If the user selects **"No, just keep the prompt"**, stop and do nothing further.
