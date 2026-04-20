# What We Learned Deploying AI within Bloomberg’s Engineering Organization – Lei Zhang, Bloomberg

## Key Takeaways

### 1. Embracing AI for Productivity
**Quote:** "Unless we deploy and try, we wouldn't know what's the best way to benefit from all the awesome work."  
**Why it matters:** Bloomberg recognized the need to experiment with AI tools to enhance productivity. By forming a dedicated team to explore AI capabilities, they aimed to leverage these tools effectively, leading to quicker proof of concepts and improved developer productivity.

### 2. Implementing Uplift Agents
**Quote:** "Wouldn't it be cool the day you get a ticket saying hey, this piece of software needs patched at the same time you have a pull request with the fix?"  
**Why it matters:** The introduction of uplift agents to scan the codebase for applicable patches represents a significant advancement in automating software maintenance. This approach not only streamlines the patching process but also enhances the overall efficiency of software engineering.

### 3. Establishing a Pay Path for AI Tools
**Quote:** "We want to make easy things extremely easy to do... and we want to make sure the wrong thing is ridiculously hard to do."  
**Why it matters:** By creating a structured pay path for AI tool deployment, Bloomberg ensures that teams can efficiently experiment with and implement AI solutions. This framework helps maintain quality control while encouraging innovation and collaboration across teams.

## Practical Tips & Procedures

### Implementing Uplift Agents
**What it does:** Automates the process of identifying and applying software patches.  
**Steps:**
1. Form a dedicated team to develop uplift agents that scan the codebase.
2. Integrate the uplift agents with existing tools to identify applicable patches.
3. Monitor the effectiveness of the patches and gather feedback for continuous improvement.  
**Quote:** "We did have a reg based refraction tool... but we are able to see very much better results from the uplift agents."  
**When to use:** When needing to automate software maintenance and improve patch management efficiency.

### Establishing a Pay Path for AI Tools
**What it does:** Provides a structured framework for teams to experiment with and deploy AI solutions.  
**Steps:**
1. Create a centralized hub for teams to discover existing AI models and tools.
2. Develop a standard platform service for tool creation and deployment.
3. Facilitate collaboration between teams to avoid duplication of efforts.  
**Quote:** "We created a pay path in partnership with our AI organization."  
**When to use:** When multiple teams are interested in deploying similar AI tools to ensure coordination and efficiency.

## Tools & Technologies Mentioned
- **Uplift Agents:** Tools designed to automate the identification and application of software patches, improving maintenance efficiency.

## Important Warnings/Risks
- **Increased Pull Requests:** "The average open pull requests increased and time to merge also increased." - This can lead to bottlenecks in the development process if not managed properly.