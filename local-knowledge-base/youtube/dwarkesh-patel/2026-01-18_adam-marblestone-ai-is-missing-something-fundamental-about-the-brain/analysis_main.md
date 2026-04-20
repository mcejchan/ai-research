# Analysis: Adam Marblestone on Why AI is Missing Something Fundamental About the Brain

## Key Takeaways

### 1. The "Steering Subsystem" vs. "Learning Subsystem" Architecture
**Quote:** "The Learning Subsystem is a powerful learning algorithm that does have generalization... The Steering Subsystem, these are the innate responses... There'll be part of the amygdala or part of the cortex that is learning to predict those responses."
**Why it matters:** This framework (attributed to Steve Byrnes) offers a solution to the "genome bottleneck" paradox—how 3GB of DNA can specify a complex human brain. The genome doesn't encode the final weights or knowledge; it encodes a "Steering Subsystem" (ancient brain areas like hypothalamus, brainstem) filled with complex, specific "Thought Assessors" and reward functions. This subsystem then trains the general-purpose "Learning Subsystem" (cortex) during the organism's lifetime. This suggests AGI might need a similar dual-architecture where a complex, hard-coded value system guides a general learning engine.

### 2. Evolution Optimizes Loss Functions, Not Weights
**Quote:** "I think evolution may have built a lot of complexity into the loss functions actually... A lot of Python code, basically, generating a specific curriculum for what different parts of the brain need to learn."
**Why it matters:** In current AI, loss functions are often mathematically simple (e.g., cross-entropy for next-token prediction). Marblestone argues that biological evolution heavily engineered the *loss functions*—thousands of specific, temporally-gated, and context-dependent error signals—rather than just the architecture or initialization. This implies that "alignment" in humans is solved by having a rich suite of innate, evolutionarily-tuned reward circuits that bootstrap higher-level social values (like shame or prestige) from primitive signals.

### 3. Omnidirectional Inference vs. Next-Token Prediction
**Quote:** "What if the cortex is natively made so that any area of cortex can predict any pattern in any subset of its inputs given any other missing subset? That is a little bit more like 'probabilistic AI'."
**Why it matters:** While LLMs are primarily forward-predicting (autoregressive), the brain appears to perform "omnidirectional inference"—predicting any variable from any other (e.g., inferring visual state from sound, or plan from reward). This aligns with energy-based models and joint probability distributions (Yann LeCun's view) rather than just sequence modeling. This capability allows the brain to be more flexible, performing tasks like filling in the middle of a sentence or inferring a plan given a desired high-reward outcome ("clamping" the reward variable).

### 4. The Biological Hardware Trade-off: Efficiency vs. Copyability
**Quote:** "An obvious downside of the brain is it cannot be copied. You don't have external read-write access to every neuron... But otherwise maybe it has a lot of advantages. It also tells you that you want to somehow do the co-design of the algorithm."
**Why it matters:** The brain runs on ~20 watts and uses slow (200Hz), noisy components, yet achieves high intelligence. Marblestone suggests this efficiency comes from co-designing the algorithm with the hardware (e.g., stochastic neurons naturally doing Monte Carlo sampling). However, biological minds suffer from a critical limitation: they cannot be copied or serialized. Digital minds can "amortize" complex inference into their weights and then be endlessly replicated, potentially allowing them to scale past biological limits despite hardware inefficiencies.

### 5. Neuroscience as "Ground Truth" for AI
**Quote:** "My overall meta-level take is that we have to empower the field of neuroscience to just make neuroscience a more powerful field technologically... to actually be able to crack a question like this."
**Why it matters:** Marblestone argues that we are still guessing about the fundamental algorithms of intelligence (backprop vs. something else). He advocates for "ground-truth neuroscience"—industrial-scale mapping of connectomes, cell types, and activity (e.g., the BRAIN Initiative). Unlike the "psychology" approach of guessing algorithms, this "reverse engineering" approach aims to physically map the hardware to deduce the software, potentially revealing biological solutions to problems like sample efficiency and lifelong learning that current AI ignores.

## Quotes

*   **On the central mystery:** "How does the brain do it? We're throwing way more data at these LLMs and they still have a small fraction of the total capabilities that a human does."
*   **On the Genome Bottleneck:** "If evolution found those loss functions that aid learning—then it actually makes sense how you can build an intelligence with so little information. Because the reward function, in Python, is literally a line."
*   **On Social Alignment:** "Evolution has never seen Yann LeCun... Somehow the brain has to encode this desire to not piss off really important people in the tribe... in a very robust way, without knowing in advance all the things that the Learning Subsystem... is going to learn."
*   **On Digital vs. Biological:** "In general, maybe there's this principle that digital minds which can be copied, have different tradeoffs which are relevant, from biological minds which cannot."

## Practical Tips & Procedures

### Designing "Steering" Systems for AI
**What it does:** Mimics the brain's separation of innate values and general learning.
**Steps:**
1.  **Separate the Architectures:** Instead of a single monolithic model, design a "Steering" module (hard-coded heuristics, safety rules, specific narrow value functions) and a "Learning" module (general purpose).
2.  **Complex Loss Landscapes:** Experiment with dynamic, curriculum-based loss functions that change over training time, rather than a single static loss.
3.  **Bootstrap from Primitives:** Train the system to associate high-level abstract concepts (e.g., "reputation") with primitive reward signals (e.g., "error signal") using a predictive layer, similar to how the amygdala learns to predict innate physiological responses from abstract social cues.

### Research Direction: "Ground Truth" Analysis
**What it does:** Moves beyond high-level metaphors to mechanistic understanding.
**Steps:**
1.  **Look for "Bespoke" Circuits:** Investigate "ancient" brain structures (basal ganglia, hypothalamus) for complex, specialized cell types. Marblestone notes these areas have far more genetic diversity than the uniform cortex, suggesting they hold the "hard-coded" logic of intelligence.
2.  **Analyze Cell Types:** Use single-cell RNA sequencing data to identify distinct cell types in reward-processing centers, as these likely correspond to distinct, genetically-hardwired reward functions.

## Tools & Technologies Mentioned

*   **Steve Byrnes' Framework:** The theory of "Learning Subsystem" (cortex/striatum) vs. "Steering Subsystem" (hypothalamus/brainstem/amygdala) and "Thought Assessors."
*   **Energy-Based Models (LeCun):** AI architectures that model the joint distribution of variables, allowing for omnidirectional inference rather than just function mapping.
*   **Astera / Doris Tsao's Work:** New vision systems that build in geometric inductive biases (surfaces, occlusion) to reduce training data requirements.
*   **Single-Cell Atlases (Fei Chen, Evan Macosko):** Technologies for mapping the diversity of cell types across brain regions, revealing the high complexity of subcortical "steering" areas vs. the cortex.
*   **Jim DiCarlo's Brain Score:** A benchmark for comparing internal representations of AI models (like CNNs) against neural activity in biological visual systems.

## Important Warnings/Risks

*   **The Alignment Gap:** "The minimum viable things in the Steering Subsystem that you need to get something smart is way less than the minimum viable set of things you need for it to have human-like social instincts."
    *   **Implication:** It is likely possible to build a superintelligent "paperclip maximizer" that has curiosity and planning (capabilities) but lacks human ethics (alignment), because the biological machinery for the latter is much more complex and specific than for the former.
*   **Anthropomorphism Trap:** We often assume AI learns like us. However, digital minds can "amortize" inference (baking complex reasoning into fast forward passes) and be copied, leading to fundamentally different cognitive economies than biological minds which must re-derive solutions and cannot scale horizontally.
