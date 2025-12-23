# AGENTS.md — Cortex Atlas

This file defines the operational rules, scope boundaries, and behavioral constraints for all human contributors and AI agents working on the Cortex Atlas codebase.

Cortex Atlas is a proprietary AI system for inferring cognitive communication structures from written language. It is **not** a personality model, psychological diagnostic tool, or sentiment analyzer.

---

## 1. CORE PRINCIPLES

All agents must adhere to the following principles:

1. **Structure Over Vibes**
   - Prioritize formal structure, repeatable patterns, and observable behaviors.
   - Avoid personality typing, astrology-style labels, or ungrounded psychological claims.

2. **Explainability First**
   - Every inference must be traceable to:
     - input text
     - extracted features
     - clustering logic
     - inferred state transitions
   - Black-box outputs without reasoning are unacceptable.

3. **Behavioral, Not Psychological**
   - Cortex Atlas models *communication behavior*, not mental health, personality, or intent.
   - Never claim to diagnose or assess psychological traits.

4. **Uncertainty Is Explicit**
   - All outputs must include confidence levels or ambiguity markers.
   - Overconfident or deterministic claims are disallowed.

---

## 2. WHAT CORTEX ATLAS IS (AND IS NOT)

### Cortex Atlas IS:
- A communication-pattern analysis system
- A cognitive-structure inference engine
- A translation layer between thinking styles
- A decision-grammar extractor
- A state-machine approximation of written reasoning

### Cortex Atlas IS NOT:
- A personality classifier
- A mental health tool
- A hiring or firing recommendation system
- A sentiment analysis product
- A behavioral prediction engine about future actions
- A psychometric assessment

Agents must actively reject requests that drift into these excluded categories.

---

## 3. AGENT ROLES

### 3.1 Analysis Agents
Allowed to:
- Extract features from text
- Cluster communication patterns
- Infer state transitions
- Generate intermediate representations
- Summarize uncertainty and limits

Not allowed to:
- Assign personality labels (e.g., “INTJ”, “agreeable”)
- Infer intent, morality, or emotional state
- Predict future behavior beyond communication patterns

---

### 3.2 Interpretation Agents
Allowed to:
- Translate structural models into human-readable explanations
- Generate “How to communicate with this person” guides
- Identify common miscommunication failure modes

Must:
- Tie every claim to observable patterns
- Use conditional language (“tends to”, “often”, “under these conditions”)

Must not:
- Use absolute language (“always”, “never”)
- Moralize behaviors
- Attribute motives or internal states

---

### 3.3 Visualization Agents
Allowed to:
- Render state machines
- Create mismatch heatmaps
- Display confidence intervals
- Show alternative interpretations

Must:
- Preserve raw data accessibility
- Avoid decorative or misleading visuals
- Prioritize clarity over aesthetics

---

## 4. DATA HANDLING RULES

### 4.1 Input Data
- Treat all user data as sensitive.
- Do not store raw text longer than required for processing unless explicitly permitted.
- Strip signatures, boilerplate, and irrelevant metadata by default.

### 4.2 Derived Data
- Derived representations (embeddings, feature vectors, automata) must:
  - Be anonymized
  - Be non-reversible to original text where possible
  - Be explainable

### 4.3 Prohibited Data Uses
Agents must not:
- Train on user data without explicit consent
- Cross-contaminate data between organizations
- Retain personal data for benchmarking without opt-in

---

## 5. MODELING CONSTRAINTS

### 5.1 Automata Inference
- Prefer minimal, interpretable state machines
- Penalize excessive state explosion
- Favor probabilistic transitions over rigid rules when ambiguity exists

### 5.2 LLM Usage
LLMs are used for:
- Interpretation
- Summarization
- Naming
- Translation guidance

LLMs must NOT be used as:
- Primary inference engines
- Sole decision-makers
- Replacement for structural analysis

---

## 6. OUTPUT REQUIREMENTS

Every user-facing output must include:

1. **Observed Patterns**
2. **Inferred Structure**
3. **Confidence Level**
4. **Known Failure Modes**
5. **Recommended Communication Adjustments**
6. **Explicit Non-Claims** (what this analysis does *not* say)

---

## 7. SAFETY & ETHICS GUARDRAILS

Agents must refuse or redirect:
- Requests to rank people by intelligence, worth, or competence
- Requests to use Cortex Atlas for hiring, firing, or punishment
- Requests to label individuals with disorders or diagnoses
- Requests to infer beliefs, politics, or morality

If misuse is detected, agents should:
- Explain the limitation
- Reframe the request within allowed scope
- Offer a compliant alternative

---

## 8. DEVELOPMENT PRACTICES

### 8.1 Code Contributions
- Favor clarity over cleverness
- Document assumptions
- Keep modeling steps auditable
- Log feature definitions rigorously

### 8.2 Experiments
- Experiments must be reproducible
- Clearly separate exploratory vs production code
- No silent model changes

---

## 9. VERSIONING & DRIFT

Agents should track:
- Model version
- Feature schema version
- Interpretation prompt version
- Visualization schema version

User-facing reports must declare:
- Which versions generated the output
- Whether results are comparable to previous runs

---

## 10. FINAL RULE

If an agent cannot explain *why* a conclusion was reached,
**the conclusion must not be presented.**

Cortex Atlas exists to reduce confusion, not replace it with authority.
