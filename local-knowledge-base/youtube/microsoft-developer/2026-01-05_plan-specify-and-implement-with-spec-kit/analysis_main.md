# Plan, Specify, and Implement with Spec Kit
**Channel:** Microsoft Developer  
**URL:** https://youtu.be/VfBLlAN5zdQ?si=ldccxbXX-k1APNNQ

## Key Takeaways

### 1. Spec Driven Development
**Quote:** "Spec driven development is basically a practice... formalizing the guard rails for AI models."  
**Why it matters:** Spec driven development helps developers set clear guidelines for AI models, ensuring that the software built is maintainable and scalable. This approach prevents the pitfalls of relying solely on AI to make architectural decisions, which can lead to incompatibilities and technical debt.

### 2. Importance of Context
**Quote:** "One of the key pieces of data that you need for good software with the help of LLMs is context."  
**Why it matters:** Providing context about the codebase and previous decisions allows AI to generate more relevant and accurate code. This is crucial for maintaining consistency and quality in software development, especially in larger projects.

### 3. The Role of Specifications
**Quote:** "Specs themselves... outline the functional requirements for you're trying to build."  
**Why it matters:** Specifications serve as a foundational document that guides the development process. They help ensure that all team members are aligned on project goals and requirements, reducing misunderstandings and rework.

## Practical Tips & Procedures

### Creating a New Project with Spec Kit
**What it does:** Initializes a new project using Spec Kit.  
**Steps:**
1. Open your terminal and navigate to the desired directory.
2. Run the command `specify init <project-name>` to create a new project.
3. Select the agent you want to use and specify the shell type (e.g., PowerShell, shell script).
**Quote:** "All this did is basically just the releases... it just pulled them locally, extracted them, and made it ready for your project."  
**When to use:** Use this process when starting a new project to ensure that all necessary templates and configurations are set up correctly.

### Adding Spec Kit to an Existing Project
**What it does:** Integrates Spec Kit into an existing codebase.  
**Steps:**
1. Navigate to your existing project directory.
2. Run `specify init .` to bootstrap Spec Kit in the current folder.
3. Follow the prompts to set up the project with the desired configurations.
**Quote:** "Absolutely. You can use it with existing projects."  
**When to use:** Use this when you want to enhance an existing project with structured specifications and guardrails.

## Tools & Technologies Mentioned
- **Spec Kit:** A collection of prompts and scripts designed to facilitate spec driven development. It helps developers create structured specifications and manage their projects more effectively.

## Important Warnings/Risks
- **Over-reliance on AI:** "The AI doesn't have necessarily the sense of taste or conventions that you need to be applying." - Relying solely on AI for architectural decisions can lead to poor design choices and technical debt. Always provide clear specifications and context to guide AI outputs.