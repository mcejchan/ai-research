# The end of MCP for AI agents?
**Channel:** Arseny Shatokhin  
**URL:** https://youtu.be/D4ImbDGFgIM?si=Ih_vaHdqbx8x-Eqr

## Key Takeaways

### 1. Shift from MCPs to Code Execution
**Quote:** "The difference in performance was striking. The agent not only produced significantly better results and worked more autonomously, but it also consumed 98% less tokens.

**Why it matters:** This shift indicates that traditional Model Context Protocols (MCPs) may not be the most efficient way to build AI agents. By moving to a code execution model, developers can achieve better performance and lower costs.

### 2. Problems with MCPs
**Quote:** "As the number of connected tools grows, loading all tool definitions up front... slows down the agents and increases the cost."  
**Why it matters:** The excessive token consumption and latency caused by MCPs can hinder the efficiency of AI agents. Understanding these limitations is crucial for developers looking to optimize their systems.

### 3. Benefits of Code Execution
**Quote:** "Using this approach we don't pass all these tools into the agent's context window. We only pass one tool that the agent actually needs to use."  
**Why it matters:** This method allows for more efficient resource use and better performance. It also enables agents to evolve by creating and saving functions as needed, enhancing their capabilities over time.

## Practical Tips & Procedures

### Implementing Code Execution for AI Agents
**What it does:** This process allows AI agents to call MCP servers dynamically, improving performance and reducing token consumption.  
**Steps:**
1. Create separate folders for each MCP server.
2. Inside each folder, create subfolders for specific tools as TypeScript files.
3. When the agent needs a tool, import it from the folder and call it in code.
**Quote:** "The agent can simply take this transcript and without even reading it, send it to Salesforce MCP server."  
**When to use:** Use this approach for complex tasks where efficiency and autonomy are critical, particularly when dealing with multiple MCPs.

## Tools & Technologies Mentioned
- **TypeScript:** A programming language that can be used to structure tools for AI agents, allowing for dynamic execution and improved performance.

## Important Warnings/Risks
- **Reliability Issues:** "If your agent has to generate code every single time it needs to call a tool, then there are more chances that it's going to make a mistake." - This highlights the potential for errors in code generation, which could affect the agent's performance and reliability.