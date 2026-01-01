# DATA_USAGE.md — Cortex Atlas

## Purpose

This document defines how Cortex Atlas collects, processes, stores, and deletes data.

Cortex Atlas is designed to analyze **written communication behavior**, not personal identity, psychology, or intent. Data usage is intentionally constrained to support this scope.

---

## Data Collected

### 1. User-Provided Content
Cortex Atlas may process:
- Text documents
- Emails or message exports
- Tickets, notes, or written artifacts
- Metadata necessary for processing (timestamps, source identifiers)

Cortex Atlas does **not** require:
- Audio
- Video
- Biometric data
- Behavioral telemetry unrelated to text analysis

---

### 2. Automatically Generated Data
During processing, Cortex Atlas generates:
- Feature vectors
- Embeddings
- Cluster assignments
- State-machine representations
- Inference metadata (confidence, ambiguity markers)

These are considered **derived data**.

---

## Data Usage Principles

Cortex Atlas follows these principles:

1. **Purpose Limitation**
   - Data is used solely to generate communication-structure analysis for the requesting user or organization.

2. **Data Minimization**
   - Only the minimum data required for analysis is processed.
   - Boilerplate, signatures, and irrelevant text are removed by default.

3. **Isolation**
   - Data is isolated by user and organization.
   - No cross-user or cross-organization analysis occurs.

4. **Explainability**
   - Derived data must remain traceable to its source input.
   - No hidden aggregation or secondary use.

---

## Training & Model Improvement

### Default Policy
- User data is **not** used for training or fine-tuning models.

### Optional Opt-In
If explicitly enabled by a user or organization:
- Data may be anonymized and aggregated
- Used to improve clustering robustness or interpretation quality
- Never used to create identifiable profiles

Opt-in consent must be explicit, documented, and reversible.

---

## Data Retention

### Raw Text
- Retained only for the duration required to complete analysis
- Deleted automatically unless retention is explicitly configured

### Derived Data
- May be retained longer to support:
  - Re-analysis
  - Version comparison
  - Longitudinal tracking (if enabled)

Retention durations are configurable per organization.

---

## Data Deletion

Users and organizations may request:
- Deletion of raw inputs
- Deletion of derived representations
- Full account data removal

Deletion requests are honored within a reasonable timeframe and propagate across backups where applicable.

---

## Data Sharing

Cortex Atlas does **not**:
- Sell user data
- Share user data with third parties
- Use user data for advertising
- Expose data to other customers

Third-party services (e.g. LLM providers) receive only:
- The minimum information required
- Sanitized, segmented inputs
- No identifying metadata where possible

---

## Security & Protection

Data protection measures include:
- Encryption in transit and at rest
- Access controls and least-privilege policies
- Logical separation between customers
- Regular security reviews

For vulnerability handling, see `SECURITY.md`.

---

## Regulatory Compliance

Cortex Atlas is designed to support:
- GDPR (data access, deletion, purpose limitation)
- CCPA
- Enterprise privacy reviews

This document supplements formal legal agreements and DPAs.

---

## Explicit Non-Claims

Cortex Atlas does not:
- Infer personal beliefs, intent, or morality
- Diagnose mental health conditions
- Perform personality classification
- Make evaluative judgments about individuals

Data usage beyond the scope described here is unsupported.

---

## Contact

For data handling or privacy questions:
- Refer to `SECURITY.md`
- Contact the Cortex Atlas maintainers

---

## Final Note

User data exists to serve user understanding — not model ambition.

If a use case requires more data, it must justify itself.