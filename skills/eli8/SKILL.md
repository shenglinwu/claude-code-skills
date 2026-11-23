---
name: eli8
description: Explain a technical topic to an engineer who is new to it, keeping real technical terms and no everyday-life analogies. Use for /eli8 <topic>, or "explain X to an engineer", "engineer-level intro to X".
argument-hint: "<topic>"
---

# eli8

Topic: $ARGUMENTS
If the topic is empty, use the topic from the user's message. If there is none, ask for one and stop.

Reader: an engineer who is new to this topic. Never mention the reader.

Rules (these win over any active output style):
- Use the real technical terms. Define each new term once, in a short clause, where it first appears.
- No everyday-life analogies. Compare to engineering ideas instead (hash map, queue, HTTP request).
- Short, direct American English.
- If the topic is code, a file, or an error in this repo, read it first.

Answer shape:
1. One line: what it is.
2. A text diagram of the parts or the flow.
3. How it works: 3 to 6 short steps.
4. Key terms: table of term | meaning.
5. One small real example (code or command).
6. Common mistakes: 1 to 3.
