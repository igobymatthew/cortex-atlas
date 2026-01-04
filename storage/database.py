from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

import psycopg
from psycopg.rows import dict_row

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/cortex_atlas"
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def get_connection() -> psycopg.Connection[Dict[str, Any]]:
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def init_db() -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS analysis_jobs (
                    analysis_id UUID PRIMARY KEY,
                    subject_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    documents JSONB NOT NULL,
                    options JSONB,
                    report JSONB,
                    error TEXT,
                    created_at TIMESTAMPTZ NOT NULL,
                    updated_at TIMESTAMPTZ NOT NULL
                );
                """
            )
            cur.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_analysis_jobs_status
                ON analysis_jobs(status, created_at);
                """
            )
        conn.commit()


def enqueue_analysis_job(
    subject_id: str,
    documents: Iterable[Dict[str, Any]],
    options: Optional[Dict[str, Any]] = None,
) -> str:
    analysis_id = str(uuid.uuid4())
    payload_documents = list(documents)
    created_at = _utc_now()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO analysis_jobs (
                    analysis_id,
                    subject_id,
                    status,
                    documents,
                    options,
                    created_at,
                    updated_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    analysis_id,
                    subject_id,
                    "queued",
                    json.dumps(payload_documents),
                    json.dumps(options) if options is not None else None,
                    created_at,
                    created_at,
                ),
            )
        conn.commit()
    return analysis_id


def claim_next_job() -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE analysis_jobs
                SET status = 'running', updated_at = %s
                WHERE analysis_id = (
                    SELECT analysis_id
                    FROM analysis_jobs
                    WHERE status = 'queued'
                    ORDER BY created_at
                    FOR UPDATE SKIP LOCKED
                    LIMIT 1
                )
                RETURNING analysis_id, subject_id, documents, options;
                """,
                (_utc_now(),),
            )
            row = cur.fetchone()
        conn.commit()
    return row


def update_job_status(
    analysis_id: str,
    status: str,
    *,
    report: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None,
) -> None:
    updated_at = _utc_now()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE analysis_jobs
                SET status = %s,
                    report = %s,
                    error = %s,
                    updated_at = %s
                WHERE analysis_id = %s
                """,
                (
                    status,
                    json.dumps(report) if report is not None else None,
                    error,
                    updated_at,
                    analysis_id,
                ),
            )
        conn.commit()


def fetch_job(analysis_id: str) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT analysis_id, subject_id, status, documents, options, report, error,
                       created_at, updated_at
                FROM analysis_jobs
                WHERE analysis_id = %s
                """,
                (analysis_id,),
            )
            row = cur.fetchone()
    return row
