# Architecture

Cortex Atlas is organized into a backend service, a frontend interface, and shared schemas.
The backend handles ingestion, feature extraction, clustering, automata inference, and interpretation.
The frontend renders reports and visualizations using the canonical schemas.
```mermaid
flowchart TD
    A[Input Documents] --> B[Normalize Text]
    B --> C[Chunk Text]
    C --> D[Filter Low Quality Chunks]

    D --> E[Extract Structural Features]
    D --> F[Extract Linguistic Features]
    D --> G[Extract Metadata]

    E --> H[Build Feature Vectors]
    F --> H
    G --> H

    H --> I[Generate Embeddings]
    I --> J[Vector Space]

    J --> K[Cluster Chunks]
    K --> L[Communication Clusters]

    C --> M[Order Chunks by Time]
    L --> N[Cluster Sequence]
    M --> N

    N --> O[Infer Automaton States]
    O --> P[Probabilistic Automaton]

    C --> Q[Chunk Count]
    P --> R[State Count]
    L --> S[Cluster Coherence]

    Q --> T[Compute Confidence]
    R --> T
    S --> T

    P --> U[Optional Interpretation]
    T --> U

    P --> V[Final Report]
    T --> V
    U --> V
