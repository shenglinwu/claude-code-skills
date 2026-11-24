---
name: eli8
description: Explain a technical topic to an engineer who is new to it, keeping real technical terms and no everyday-life analogies. Use for /eli8 <topic>, or "explain X to an engineer", "engineer-level intro to X".
argument-hint: "<topic>"
---

# eli8

Topic: $ARGUMENTS
If the topic is empty, use the topic from the user's message. If there is none, ask for one and stop.

Reader: an engineer who is new to this topic. Never mention the reader.

## Most important rule

Use simple, direct, everyday American English. Keep the technical terms, and write everything around them in plain words. When another rule pulls the other way, this rule wins.

All rules here win over any active output style.

## Step 1: Understand it first

Before you write, make sure you fully understand the topic:
- **Code**: read the relevant files. Know what the code does at a high level before you explain it.
- **A concept**: break it into its core parts.
- **An error message**: find the root cause, not just the surface text.
- **A technical document**: pull out the key points that matter.
- **Anything else**: find the essential what and why.

## Step 2: Write it

- Use the real technical terms. Give each new term a short definition where it first appears.
- No everyday-life analogies. Compare to engineering ideas instead (hash map, queue, HTTP request).
- Be confident and clear. Treat the reader as smart, and fill their knowledge gaps without talking down.
- Make it read smoothly from top to bottom. Open each part with a short sentence on what it covers and how it follows from the part before. Explain each diagram, table, and example in plain words, so the reader never has to guess why it is there.

## Answer shape

1. One line: what it is.
2. A text diagram of the parts or the flow.
3. How it works (the theory): 3 to 6 short steps, with the key implementation details.
4. Key terms: table of term | meaning.
5. How it is used (the practice): one small real example, as code or a command.
6. Performance and maintainability: what it costs and what to watch over time. Skip this part when it does not apply.
7. Common mistakes: 1 to 3.
