Below is a **clean, production-grade API contract** for **Cortex Atlas**.
This is written as if you’re shipping a real SaaS: explicit inputs, explicit outputs, versioned, auditable.

No speculative endpoints. No hand-wavy “AI does stuff.”

---

# Cortex Atlas — API Contract (v1)

**Base URL**

```
/api/v1
```

**Auth**

* Bearer token (JWT / OAuth2)
* Org-scoped by default

```
Authorization: Bearer <token>
```

---

## 1. CREATE ANALYSIS JOB

### `POST /analysis`

Starts an asynchronous analysis job.

### Request Body

```json
{
  "subject_id": "user_123",
  "documents": [
    {
      "document_id": "doc_001",
      "author_id": "user_123",
      "source": "email",
      "content": "Here’s what I think we should do next...",
      "timestamp": "2026-01-10T15:04:05Z"
    }
  ],
  "options": {
    "language": "en",
    "retain_raw_text": false,
    "confidence_threshold": 0.65
  }
}
```

### Required

* `subject_id`
* ≥5 documents recommended (hard minimum configurable)

### Response — 202 Accepted

```json
{
  "analysis_id": "analysis_abc123",
  "status": "queued",
  "estimated_time_seconds": 45
}
```

---

## 2. CHECK ANALYSIS STATUS

### `GET /analysis/{analysis_id}`

Returns job status and progress.

### Response — 200 OK

```json
{
  "analysis_id": "analysis_abc123",
  "status": "running",
  "progress": {
    "stage": "automata_inference",
    "percent_complete": 62
  }
}
```

### Status Values

* `queued`
* `running`
* `completed`
* `failed`

---

## 3. FETCH FINAL REPORT

### `GET /reports/{analysis_id}`

Returns the **final canonical report artifact**.

### Response — 200 OK

```json
{
  "subject_id": "user_123",

  "patterns": {
    "cluster_id": "cluster_planning",
    "label": "Planning & Decomposition",
    "member_chunks": ["chunk_12", "chunk_19", "chunk_27"],
    "coherence_score": 0.81
  },

  "automata": {
    "states": [
      {
        "state_id": "S1",
        "label": "Exploratory Planning",
        "support": 0.42
      },
      {
        "state_id": "S2",
        "label": "Detail Expansion",
        "support": 0.35
      }
    ],
    "transitions": [
      {
        "from": "S1",
        "to": "S2",
        "probability": 0.67
      },
      {
        "from": "S2",
        "to": "S1",
        "probability": 0.21
      }
    ]
  },

  "interpretation": {
    "summary": "This subject tends to reason by first outlining broad intent, then expanding details once constraints appear.",
    "guidance": [
      "Present high-level intent before requesting specifics.",
      "Avoid interrupting exploratory phases with granular questions."
    ],
    "failure_modes": [
      "Premature detail requests may cause defensive over-explanation.",
      "Ambiguous ownership can stall progress."
    ],
    "non_claims": [
      "This analysis does not assess personality or intent."
    ]
  },

  "confidence": {
    "overall": 0.78,
    "notes": "Sufficient text volume with consistent authorship."
  },

  "version": {
    "features": "1.0.0",
    "automata": "1.0.0",
    "interpretation": "1.0.0"
  }
}
```

---

## 4. FETCH STATE MACHINE (VISUALIZATION-READY)

### `GET /reports/{analysis_id}/automata`

Returns **graph-optimized** automata data for frontend rendering.

### Response — 200 OK

```json
{
  "nodes": [
    { "id": "S1", "label": "Exploratory Planning", "weight": 0.42 },
    { "id": "S2", "label": "Detail Expansion", "weight": 0.35 }
  ],
  "edges": [
    { "from": "S1", "to": "S2", "probability": 0.67 },
    { "from": "S2", "to": "S1", "probability": 0.21 }
  ]
}
```

---

## 5. FETCH RAW OBSERVATIONS (AUDIT MODE)

### `GET /reports/{analysis_id}/evidence`

Returns traceable evidence linking outputs → inputs.

**Enterprise / audit-only endpoint.**

### Response — 200 OK

```json
{
  "states": [
    {
      "state_id": "S1",
      "supporting_chunks": [
        {
          "chunk_id": "chunk_12",
          "excerpt": "Let’s start by framing the problem broadly..."
        }
      ]
    }
  ]
}
```

---

## 6. LIST REPORTS (ORG / USER)

### `GET /reports`

Query parameters:

* `subject_id`
* `limit`
* `offset`

### Response — 200 OK

```json
{
  "reports": [
    {
      "analysis_id": "analysis_abc123",
      "subject_id": "user_123",
      "created_at": "2026-01-10T15:05:12Z",
      "confidence": 0.78
    }
  ]
}
```

---

## 7. DELETE DATA (GDPR / CCPA)

### `DELETE /reports/{analysis_id}`

Deletes report + derived artifacts.

### Response — 204 No Content

---

## 8. ERROR FORMAT (STANDARDIZED)

All errors use the same structure.

```json
{
  "error": {
    "code": "INSUFFICIENT_DATA",
    "message": "Not enough unique text to infer stable patterns.",
    "details": {
      "minimum_documents": 5,
      "provided": 2
    }
  }
}
```

---

## 9. ERROR CODES (NON-EXHAUSTIVE)

| Code                   | Meaning                   |
| ---------------------- | ------------------------- |
| `INVALID_INPUT`        | Schema validation failed  |
| `INSUFFICIENT_DATA`    | Too little usable text    |
| `MIXED_AUTHORSHIP`     | Multiple authors detected |
| `LOW_CONFIDENCE`       | Output withheld           |
| `UNSUPPORTED_LANGUAGE` | Language not supported    |
| `INTERNAL_ERROR`       | Server failure            |

---

## 10. DESIGN DECISIONS (IMPORTANT)

* **Async by default** → predictable performance
* **No streaming inference** → auditability
* **No freeform LLM endpoint** → guardrail integrity
* **Explicit evidence endpoint** → trust + compliance
* **Versioned artifacts** → reproducibility

---

## NEXT BUILD STEPS (PICK ONE)

1. **Pydantic models for these schemas**
2. **FastAPI route implementations**
3. **Automata inference stub (code)**
4. **Confidence scoring logic**
5. **Frontend graph consumption spec**

Say the number and I’ll drop straight into code.

