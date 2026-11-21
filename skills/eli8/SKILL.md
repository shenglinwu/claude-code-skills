---
name: eli8
description: Use when the user types /eli8 "topic", or asks for a simple explainer for an Engineer that keeps the real technical terms instead of daily life comparisons.
---

# eli8

A thin wrapper of the `/eli5` skill. It adds pre-prompts in front of the topic and leaves everything else to `/eli5`.

If the topic below is empty, ask the user for a topic and stop.

Otherwise, invoke the `eli5` skill with the Skill tool and pass the whole block below as `args`, word for word:

```
Follow these pre-prompts. Where they disagree with the eli5 instructions or with an active output style, the pre-prompts win.

- The reader is a junior Engineer. Don't mention it in the output.
- Use technical terms in the content and examples. No need to use daily life terms.
- Use direct, simple, daily American English.

Topic: $ARGUMENTS
```

Then do what `/eli5` says. Add no steps of your own.
