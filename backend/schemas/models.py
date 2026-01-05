from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal
from datetime import datetime

SourceType = Literal["email", "chat", "doc", "ticket", "note"]

class DocumentIn(BaseModel):
    document_id: str
    author_id: str
    source: SourceType = "doc"
    content: str
    timestamp: datetime

class AnalysisOptions(BaseModel):
    language: str = "en"
    retain_raw_text: bool = False
    confidence_threshold: float = 0.65
    enable_llm_interpretation: bool = False

class AnalysisRequest(BaseModel):
    subject_id: str
    documents: List[DocumentIn]
    options: AnalysisOptions = Field(default_factory=AnalysisOptions)

class Chunk(BaseModel):
    chunk_id: str
    document_id: str
    author_id: str
    text: str
    timestamp: datetime

class FeatureVector(BaseModel):
    chunk_id: str
    features: Dict[str, float]

class Cluster(BaseModel):
    cluster_id: str
    label: str
    member_chunks: List[str]
    coherence_score: float

class AutomataState(BaseModel):
    state_id: str
    label: str
    support: float

class AutomataTransition(BaseModel):
    from_state: str = Field(alias="from")
    to_state: str = Field(alias="to")
    probability: float

class Automata(BaseModel):
    states: List[AutomataState]
    transitions: List[AutomataTransition]

class Interpretation(BaseModel):
    summary: str
    guidance: List[str]
    failure_modes: List[str]
    non_claims: List[str]

class Confidence(BaseModel):
    overall: float
    notes: str

class VersionInfo(BaseModel):
    features: str
    automata: str
    interpretation: str

class Report(BaseModel):
    subject_id: str
    patterns: List[Cluster]
    automata: Automata
    interpretation: Optional[Interpretation] = None
    confidence: Confidence
    version: VersionInfo