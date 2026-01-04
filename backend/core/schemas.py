from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional, Literal

from pydantic import BaseModel, Field


class Input(BaseModel):
    document_id: str
    author_id: str
    source: Optional[Literal["email", "chat", "doc", "ticket", "note"]] = None
    content: str
    timestamp: datetime


class Chunk(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    index: int


class FeatureVector(BaseModel):
    information_density: Optional[float] = None
    logical_operator_ratio: Optional[float] = None
    hedging_frequency: Optional[float] = None
    abstraction_level: Optional[float] = None
    ordering_strength: Optional[float] = None
    topic_drift: Optional[float] = None


class Feature(BaseModel):
    chunk_id: str
    features: FeatureVector


class Cluster(BaseModel):
    cluster_id: str
    label: Optional[str] = None
    member_chunks: List[str]
    coherence_score: Optional[float] = None


class AutomataState(BaseModel):
    state_id: str
    label: str
    support: Optional[float] = None


class AutomataTransition(BaseModel):
    from_state: str = Field(..., alias="from")
    to: str
    probability: float


class Automata(BaseModel):
    states: List[AutomataState]
    transitions: List[AutomataTransition]


class Interpretation(BaseModel):
    summary: str
    guidance: List[str]
    failure_modes: List[str]
    non_claims: Optional[List[str]] = None


class Confidence(BaseModel):
    overall: float
    notes: str


class VersionInfo(BaseModel):
    features: str
    automata: str
    interpretation: str


class Report(BaseModel):
    subject_id: str
    patterns: Cluster
    automata: Automata
    interpretation: Interpretation
    confidence: Confidence
    version: VersionInfo

    class Config:
        allow_population_by_field_name = True
