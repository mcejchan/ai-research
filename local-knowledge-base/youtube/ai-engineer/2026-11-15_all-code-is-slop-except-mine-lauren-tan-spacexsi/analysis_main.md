## Key Takeaways (3-5 main points)

### 1. Codebase Quality Dictates Agent Output Quality
**Quote:** "Since code is the biggest input for agents, it means that any workarounds, um anti-patterns, deprecated code, tech debt, it's now likely to be just copied by the next agent since it looks like the established pattern in your codebase."
**Why it matters:** Agents learn from existing code patterns. If your codebase contains "weeds" like anti-patterns or tech debt, agents will replicate them at scale. Maintaining a pristine codebase is no longer just about human readability; it is the primary mechanism for ensuring agent-generated code is high-quality.

### 2. Replace Prose Instructions with Deterministic Constraints
**Quote:** "Whenever you're correcting your agent, think about how you can make that a deterministic check instead of adding another line to your rules or your agents.md because it's far more reproducible when it's in code and it lets you trust it more."
**Why it matters:** Natural language instructions (rules, markdown files) are ambiguous and prone to misinterpretation. Converting corrections into lint rules, type system constraints, or architectural boundaries ensures agents cannot violate them, creating a "concrete foundation" that forces correct behavior by default.

### 3. Verification is the New Code Review
**Quote:** "Our code review process has now really shrunk into looking at verification artifacts instead. So things like videos, screenshots, diagrams, formal verification."
**Why it matters:** As agent volume increases (e.g., 3,000 PRs/month), manual line-by-line review becomes impossible. Trust shifts from reading code to verifying outcomes through runtime checks, visual artifacts, and formal proofs. This allows engineers to manage high-velocity output without becoming a bottleneck.

### 4. Ban Nuanced APIs to Eliminate Slop
**Quote:** "Anything that requires nuance to use well often leads to slop... our solution has been to just ban it in product code... effectively, this problem has now been categorically eliminated, and we never need to catch that during code review again."
**Why it matters:** Agents struggle with APIs that require deep contextual judgment (like `useEffect` in React). By banning these APIs entirely in product code and enforcing strict architectural boundaries, teams eliminate entire categories of bugs and reduce the cognitive load required for review.

## Practical Tips & Procedures

### The "Garden" Maintenance Workflow
**What it does:** Transforms the codebase into a high-trust environment where agents can operate autonomously by enforcing deterministic constraints.
**Steps:**
1.  **Identify Anti-Patterns:** When an agent makes a mistake or produces slop, identify the root cause (e.g., misuse of `useEffect`, importing main thread code into renderer).
2.  **Encode as Deterministic Checks:** Instead of adding a rule to `agents.md`, create a lint rule, type constraint, or dependency graph analyzer rule that physically prevents the error.
3.  **Clean Up Legacy Code:** Remove existing instances of the anti-pattern so agents don't copy the "bad" examples.
4.  **Ban Nuanced APIs:** If an API is frequently misused by agents, ban it in product code and provide a safer, constrained wrapper or alternative.
5.  **Iterate:** Repeat this process until there are "nothing left to review" in standard code paths.
**Quote:** "Every time we correct our agents, it turns into one of these deterministic checks or we think about how to categorically eliminate that problem in the code through better API design, through better architecture."
**When to use:** Whenever you find yourself repeatedly correcting the same type of agent error or reviewing similar "slop" in pull requests.

### Runtime Verification with Feature Maps
**What it does:** Gives agents a shared vocabulary and tools to verify their own work against user-facing features.
**Steps:**
1.  **Create a Feature Map:** Build a "site map" of all features available in the application from the user's perspective.
2.  **Define Shared Vocabulary:** Use this map to give agents precise terms for UI elements (e.g., "the thingy in the left sidebar" becomes a specific ID or name).
3.  **Implement Custom CLIs:** Create command-line interfaces within skills that allow agents to run the code and use debugging tools (like Chrome DevTools protocol) consistently.
4.  **Execute Verification:** Agents use these tools to run the app, interact with features, and capture artifacts (videos/screenshots) to prove functionality.
**Quote:** "With this, agents don't need to guess when you say, you know, the thingy in the left sidebar, it gives you some shared vocabulary."
**When to use:** For UI-heavy applications where agents need to verify visual and functional correctness without human intervention.

### Formal Verification for Critical Flows
**What it does:** Uses mathematical proofs to ensure system invariants and prevent subtle logic bugs.
**Steps:**
1.  **Identify Critical Flows:** Select major user flows or complex algorithms (e.g., notifications across devices, virtualization logic).
2.  **Model the System:** Use tools like TLA+ to model the state machine of the flow.
3.  **Prove Properties:** Use tools like Lean to prove specific properties (e.g., no flickering/jittering in a virtualization library).
4.  **Integrate into CI:** Run these checks as part of the verification pipeline to catch bugs before merge.
**Quote:** "We now use TLA Plus to do some model checking of major user flows... we use a lean as well for proving certain algorithms."
**When to use:** For high-stakes logic, concurrency issues, or performance-critical algorithms where runtime testing might miss edge cases.

## Tools & Technologies Mentioned
*   **Dune:** A client framework for Electron apps (similar to Next.js) that enforces organic architecture and lint rules.
*   **Grokbot:** The AI agent platform used by the speaker's team at SpaceX SI.
*   **TLA+:** Used for model checking major user flows and system invariants.
*   **Lean:** Used for proving specific algorithms and properties (e.g., virtualization logic).
*   **Bombadil:** A library used for property-based testing of UIs.
*   **Chrome DevTools Protocol:** Used by agents for runtime verification and debugging.
*   **P Stack (Potato Stack):** A plugin/skill set that includes tools like "state chart" for visualizing state machines.

## Important Warnings/Risks
*   **Automating Slop:** "If your inner coding loop produces slop, then automating that loop just produces more slop and you need to throw more and more and more tokens at the problem, which we all know is very expensive." - Automating a bad process amplifies errors and costs.
*   **Comments as Escape Hatches:** "The worst part about comments though is that they're not enforceable... it gives an agent an escape hatch to justify not doing the right thing because it's hard." - Relying on comments for guidance is dangerous because agents may ignore them or use them to justify poor architecture.
*   **Nuanced APIs:** "Agents are not good at using it [useEffect]... anything that requires nuance to use well often leads to slop." - Allowing agents to use complex, judgment-heavy APIs without strict constraints leads to widespread performance and logic issues.