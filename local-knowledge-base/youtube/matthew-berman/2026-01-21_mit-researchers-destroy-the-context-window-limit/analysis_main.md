# MIT Researchers DESTROY the Context Window Limit
**Channel:** Matthew Berman  
**URL:** https://youtu.be/huszaaJPjU8?si=__tnCmKX9rAOrUlg

## Key Takeaways

### 1. Recursive Language Models (RLMs) Enhance Context Windows
**Quote:** "With our new recursive language model strategy, we can see the quality stays pretty consistent over time, even up to 1 million tokens."
**Why it matters:** RLMs allow for processing of significantly longer prompts without degrading performance, which is crucial for tasks requiring extensive context, such as deep research or analyzing large codebases.

### 2. Limitations of Traditional Context Windows
**Quote:** "The more information you put into that context window, the harder time the model has finding things... This is called context rot."
**Why it matters:** Traditional models struggle with long inputs due to context rot, where the quality of responses declines as the context length increases. RLMs address this limitation by enabling deeper searches within the context.

### 3. Cost Efficiency of RLMs
**Quote:** "The cost of GPT5 Mini ingesting 6 to 11 million input tokens is $150 to 275... RLM GBT5 has an average cost of 99."
**Why it matters:** RLMs not only improve performance but also reduce costs associated with processing long contexts, making them a more economical choice for complex tasks.

## Practical Tips & Procedures

### Implementing Recursive Language Models
**What it does:** Allows for processing of long prompts by enabling recursive querying within a larger context.
**Steps:**
1. Create an environment code that stores the long prompt in a text file.
2. Provide the model with tools to search through the stored prompt.
3. Enable recursive querying to dig deeper into relevant sections of the prompt.
**Quote:** "When the model finds a piece of the context that it thinks is relevant, it can actually do a query again on it and go deeper and deeper."
**When to use:** Use this approach for tasks requiring extensive context, such as deep research or analyzing large datasets.

## Tools & Technologies Mentioned
- **Zapier:** A platform for automating workflows and integrating various tools. It allows users to connect over 7,000 different applications for streamlined processes.

## Important Warnings/Risks
- **Cost Variability:** "RLMs iteratively interact with their context until they find a suitable answer leading to large differences in iteration length depending on task complexity." - This can lead to unpredictable costs if the model goes deep into recursive queries, potentially increasing expenses significantly.