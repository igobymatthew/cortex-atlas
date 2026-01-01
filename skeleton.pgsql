cortex-atlas/
├── backend/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── analysis.py          # Run analysis jobs
│   │   │   ├── results.py           # Fetch reports & artifacts
│   │   │   ├── health.py
│   │   │   └── __init__.py
│   │   └── deps.py                  # Auth, db deps
│   ├── core/
│   │   ├── ingestion/
│   │   │   ├── normalize.py         # Cleaning, boilerplate stripping
│   │   │   ├── chunking.py
│   │   │   └── filters.py
│   │   ├── features/
│   │   │   ├── structural.py        # ordering, logic, density
│   │   │   ├── linguistic.py
│   │   │   └── metadata.py
│   │   ├── clustering/
│   │   │   ├── embed.py
│   │   │   ├── cluster.py
│   │   │   └── validate.py
│   │   ├── automata/
│   │   │   ├── state_inference.py
│   │   │   ├── transitions.py
│   │   │   └── simplify.py
│   │   ├── interpretation/
│   │   │   ├── prompts.py
│   │   │   ├── explain.py
│   │   │   └── guardrails.py
│   │   └── confidence/
│   │       ├── scoring.py
│   │       └── uncertainty.py
│   ├── models/                      # Serialized / versioned
│   │   ├── embeddings/
│   │   ├── automata/
│   │   └── prompts/
│   ├── storage/
│   │   ├── database.py
│   │   ├── vectors.py
│   │   └── files.py
│   ├── schemas/                     # ⬅️ see below
│   ├── workers/
│   │   └── analysis_job.py
│   ├── config.py
│   └── main.py
│
├── frontend/
│   ├── app/
│   │   ├── dashboard/
│   │   ├── reports/
│   │   └── visualizations/
│   ├── components/
│   │   ├── StateMachine.tsx
│   │   ├── ConfidenceBadge.tsx
│   │   └── Heatmap.tsx
│   └── lib/
│       └── api.ts
│
├── schemas/                         # SHARED SCHEMAS (CANONICAL)
│   ├── input.schema.json
│   ├── feature.schema.json
│   ├── cluster.schema.json
│   ├── automata.schema.json
│   ├── interpretation.schema.json
│   ├── report.schema.json
│   └── confidence.schema.json
│
├── docs/
│   ├── architecture.md
│   ├── inference_pipeline.md
│   └── versioning.md
│
├── experiments/
│   ├── clustering_playground.ipynb
│   └── automata_prototypes/
│
├── AGENTS.md
├── MODEL_CARD.md
├── MODEL_LIMITATIONS.md
├── DATA_USAGE.md
├── SECURITY.md
├── EVALUATION.md
├── README.md
└── pyproject.toml
