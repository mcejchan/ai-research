# How to build a software factory that improves itself (Zach Lloyd, Warp)

## Key Takeaways (3-5 main points)

### 1. Move from Interactive Prompting to Cloud-Sandboxed Factories
**Quote:** "The solution uh to both these problems is to sand box your agents and move them to the cloud. And the product category that is emerging to support this uh is what um you know, we call a cloud software factory."
**Why it matters:** Local agents create security risks because a compromised agent can take over the user's laptop. Furthermore, local setups are difficult to govern, audit, or control costs across an organization. Moving to the cloud allows for centralized governance and security.

### 2. Define Your Factory as Code for Version Control and Automation
**Quote:** "And then finally, defining code means like your factory should be a thing uh that has like a strict definition. And that definition should include like what are the workflows? What are the skills? What are the MCPs? Where do these run? And when you define it in code and version control it, then you get the ability to like test different versions of your factory."
**Why it matters:** Treating the factory configuration as code allows teams to test different versions, roll back changes, and enable coding agents to update the factory itself. It ensures that the entire automation stack is reproducible and auditable.

### 3. Implement a Self-Improvement Loop Using Agent-Generated Scores
**Quote:** "And so the idea behind a self-improvement loop is that agents will go and they'll look at all these failure modes. They'll aggregate them. They will look for patterns. And then they will come up with ideas for how do you improve the underlying factory definition so that going forward you don't have this same failure mode."
**Why it matters:** Instead of manual review, use LLM-as-a-judge to score agent runs (e.g., detecting redundant tests). These scores feed into an improvement loop where agents propose PRs to fix the factory definition, closing the gap between failure and resolution automatically.

### 4. Build Custom Benchmarks from Real Past Runs, Not Public Leaderboards
**Quote:** "But the world that you want to get to um as you automate more development is actually being measurement first on your own data. And so you should whatever factory model you approach have the ability to score meaning like eval how your coding agents are doing uh feed those scores into agents that can improve your factory and then also create your own benchmarks."
**Why it matters:** Public benchmarks (like SWE-bench) do not reflect your specific codebase or stack. By replaying real past tasks against different models, you can generate cost-vs-quality trade-off graphs specific to your organization, enabling data-driven model routing.

## Practical Tips & Procedures

### Setting Up the Self-Improvement Loop
**What it does:** Automates the identification of agent failure modes and proposes fixes to the factory configuration.
**Steps:**
1.  **Record All Traces:** Ensure every agent run, conversation, and artifact is stored centrally in your factory infrastructure.
2.  **Define Scoring Agents:** Create specific agents (LLM-as-a-judge) that review these traces for known failure modes (e.g., "writing redundant tests").
3.  **Aggregate Patterns:** Have a meta-agent analyze the scores to identify recurring issues (e.g., "Agent failed to read matching positive skills 37 times").
4.  **Generate Fix PRs:** The meta-agent proposes a change to the factory definition (e.g., updating a skill or prompt) to prevent the failure in the future.
**Quote:** "So, this is like closing the loop where the agent has identified a problem and it's suggesting a change to actually drive a better result in the factory."
**When to use:** When you have a steady stream of agent tasks and want to reduce manual debugging of agent behavior.

### Creating Custom Model Benchmarks
**What it does:** Determines the best model for specific tasks based on your actual codebase rather than generic benchmarks.
**Steps:**
1.  **Curate Tasks:** Select representative past runs from your system (either manually or by asking the factory to identify interesting sessions).
2.  **Replay Tasks:** Run these specific tasks against various model configurations (e.g., GLM, GPT-4o, etc.).
3.  **Score Results:** Use your defined scoring agents to evaluate correctness and quality.
4.  **Analyze Trade-offs:** Generate a cost vs. quality graph to determine which model offers the best value for specific task types (e.g., front-end vs. backend).
**Quote:** "And so, in in this case, for example, like we could see GLM 53 flash uh was 93% correct on these tasks at a cost of $2. GPT 56 saw was like 95% correct, but it cost three times as much."
**When to use:** When optimizing costs or selecting models for specific parts of your development pipeline.

### Verification Strategy for Factory Output
**What it does:** Reduces the code review burden by automating verification before human review.
**Steps:**
1.  **Spec-Driven Development:** Ensure changes adhere to a predefined specification before implementation.
2.  **Computer Use Verification:** Deploy agents that interact with the running application to produce evidence (screenshots, logs) that the feature works from a user standpoint.
**Quote:** "The big things that I advise are spec-driven development, so you could actually test um make sure that the changes are adherent to a spec. And the other thing is computer use verification... if you can have agents that verify or produce evidence from the user standpoint that the thing works, that can go a long way in terms of like lessening the code review burden."
**When to use:** When facing a "pile up of PRs" generated by automated agents.

## Tools & Technologies Mentioned
*   **Warp Factories:** A platform for building internal software factories, managing agent workflows, and handling self-improvement loops.
*   **Warp Terminal:** An open-source agentic terminal with ~65k GitHub stars.
*   **Linear/Jira:** Task trackers used to input agentic work into the factory.
*   **Slack/GitHub:** Interfaces where engineers interact with the factory (e.g., responding to PR comments).
*   **LLM-as-a-Judge:** A technique used to score agent outputs automatically.

## Important Warnings/Risks
*   **Local Agent Security Risks:** "if there is a problem or a compromise of a local agent, then it's basically has the ability to take over whatever the user who's signed in on the their laptop is, and so that's not a good thing." - Local agents lack sandboxing, posing significant security threats to user machines and corporate data.
*   **Governance Blind Spots:** "right now, we're in this situation where you know, everyone is kind of configuring their own MCPs, their own skills, their own tools, and it's like you can't see what's going on, you can't audit it." - Decentralized agent setups make it impossible to audit costs, security, or compliance.
*   **Misleading Public Benchmarks:** "you can't really trust the public benchmarks [clears throat] as like a way of understanding how good a certain model or harness is going to be on your own workflows." - Relying on generic benchmarks can lead to suboptimal model selection for your specific codebase and stack.