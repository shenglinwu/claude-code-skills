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

By default, write a tutorial document: an HTML page that reads from top to bottom like a guided lesson. Build it with the nice-document skill, then give the user the link.

Write it as paragraphs under section headings. Each section opens with a sentence that ties it to the one before. A good default order:

1. **What it is**: a short paragraph on what it is and why it exists.
2. **The big picture**: a text diagram of the parts or the flow, with a paragraph that walks through it.
3. **How it works**: the theory, in paragraphs, with the key implementation details.
4. **Using it**: one small real example, as code or a command. Say what the example shows before it, and explain the result after it.
5. **Common mistakes**: 1 to 3, each with what goes wrong and how to avoid it.

Add a key terms table (term | meaning) where it helps most, for example after the section that brings in most of the terms. Move the diagram or the table to another place if it makes the explanation clearer.

If the topic says the goal is a presentation or another kind of document (for example slides or a cheatsheet), keep the same teaching content and all the rules above, and shape the output as that type.
