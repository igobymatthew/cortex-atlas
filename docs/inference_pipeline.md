# Inference Pipeline

1. Ingest documents and normalize text.
2. Chunk text into analysis units.
3. Extract structural features and embed them.
4. Cluster feature embeddings into communication patterns.
5. Infer automata states and transitions from cluster sequences.
6. Generate interpretations, confidence, and non-claims.

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Queue
    participant Worker
    participant Pipeline
    participant Storage
    participant LLM

    Client->>API: Submit analysis request
    API->>API: Validate input
    API->>Storage: Create job record
    API->>Queue: Enqueue job
    API-->>Client: Return analysis id

    Queue->>Worker: Dequeue job
    Worker->>Pipeline: Run pipeline

    Pipeline->>Pipeline: Normalize text
    Pipeline->>Pipeline: Chunk documents
    Pipeline->>Pipeline: Order chunks by timestamp

    Pipeline->>Pipeline: Assign cluster per chunk
    Note over Pipeline: Example sequence A A B B B A

    Pipeline->>Pipeline: Group contiguous clusters
    Note over Pipeline: Intervals A then B then A

    Pipeline->>Pipeline: Infer automaton states
    Pipeline->>Pipeline: Detect state transitions
    Pipeline->>Pipeline: Compute state support

    Pipeline->>Pipeline: Compute confidence score

    alt confidence sufficient
        Pipeline->>LLM: Generate interpretation
        LLM-->>Pipeline: Interpretation
    else confidence insufficient
        Pipeline->>Pipeline: Skip interpretation
    end

    Pipeline-->>Worker: Final report
    Worker->>Storage: Persist report

    Client->>API: Request results
    API->>Storage: Fetch report
    Storage-->>API: Report
    API-->>Client: Report payload
