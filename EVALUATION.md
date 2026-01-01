# EVALUATION.md — Cortex Atlas

## Purpose

This document describes how Cortex Atlas is evaluated, validated, and monitored.

Cortex Atlas does not produce a single numeric “accuracy score.”  
Evaluation focuses on **structural validity, interpretability, and stability**.

---

## What Is Evaluated

Cortex Atlas evaluates **communication structure inference**, not truth, intent, or personality.

Primary evaluation dimensions:
- Pattern consistency
- Structural coherence
- Interpretability
- Reproducibility
- Robustness to noise

---

## Evaluation Components

### 1. Feature Extraction Validation
- Features must map to observable text properties
- Feature definitions are versioned and documented
- Changes require regression checks

Metrics:
- Feature presence consistency
- Sensitivity to formatting changes
- Noise resistance

---

### 2. Clustering & Mode Detection
Evaluation focuses on:
- Semantic coherence of clusters
- Stability across runs
- Resistance to over-fragmentation

Methods:
- Human expert review
- Intra-cluster similarity scores
- Perturbation testing (small text edits)

---

### 3. Automata Inference Evaluation
State machines are evaluated for:
- Minimality (no unnecessary states)
- Interpretability
- Plausible transition logic

Checks include:
- State explosion detection
- Transition probability sanity bounds
- Re-run consistency on identical inputs

---

### 4. Interpretation Layer Evaluation
LLM-generated explanations are evaluated for:
- Faithfulness to underlying structures
- Absence of unsupported claims
- Proper use of uncertainty language

Interpretation must never introduce:
- New inferred traits
- Psychological claims
- Deterministic judgments

---

## Human Review

Human-in-the-loop evaluation is critical.

Reviewers assess:
- Whether outputs align with observable inputs
- Whether explanations remain within scope
- Whether failure modes are acknowledged

Disagreements are logged and used to refine guardrails, not to force consensus.

---

## Reproducibility

Cortex Atlas emphasizes reproducibility over raw performance.

Each output references:
- Feature schema version
- Clustering algorithm version
- Automata inference version
- Interpretation prompt version

Results generated under different versions are explicitly flagged as non-comparable.

---

## Drift Monitoring

Drift is monitored across:
- Input distributions
- Feature activation patterns
- Cluster composition
- Interpretation language

If drift is detected:
- Confidence thresholds are adjusted
- Outputs may be withheld or marked unstable

---

## Failure Modes

Known limitations include:
- Sparse or low-quality input text
- Highly templated or boilerplate-heavy data
- Mixed authorship within a single dataset
- Domain-specific jargon without sufficient context

These are surfaced to users explicitly.

---

## What Is Not Evaluated

Cortex Atlas does not evaluate:
- User correctness
- Communication effectiveness outcomes
- Productivity improvements
- Psychological accuracy

Such claims are out of scope.

---

## Continuous Improvement

Evaluation findings are used to:
- Refine feature definitions
- Improve clustering heuristics
- Tighten interpretation constraints
- Strengthen guardrails against misuse

No silent changes are made to inference logic.

---

## Final Note

Cortex Atlas prioritizes **epistemic humility**.

If a structure cannot be evaluated clearly,
it is not promoted as insight.