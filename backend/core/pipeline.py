from __future__ import annotations

from typing import Iterable, List, Sequence, Dict
from datetime import datetime

from backend.core.automata.state_inference import infer_states
from backend.core.clustering.cluster import cluster_embeddings
from backend.core.confidence.scoring import compute_confidence
from backend.core.features.structural import extract_structural_features
from backend.core.ingestion.chunking import chunk_text

from backend.core.schemas import (
    Automata,
    AutomataState,
    AutomataTransition,
    Chunk,
    Cluster,
    Confidence,
    Feature,
    FeatureVector,
    Input,
    Interpretation,
    Report,
    VersionInfo,
)

FEATURE_FIELDS = (
    "information_density",
    "logical_operator_ratio",
    "hedging_frequency",
    "abstraction_level",
    "ordering_strength",
    "topic_drift",
)

FEATURES_VERSION = "0.1.0"
AUTOMATA_VERSION = "0.1.0"
INTERPRETATION_VERSION = "0.1.0"


# ---------- Normalization ----------

def _normalize_inputs(documents: Iterable[Input | dict]) -> List[Input]:
    inputs: List[Input] = []
    for document in documents:
        if isinstance(document, Input):
            inputs.append(document)
        else:
            if hasattr(Input, "model_validate"):
                inputs.append(Input.model_validate(document))
            else:
                inputs.append(Input.parse_obj(document))
    return inputs


# ---------- Chunking ----------

def _build_chunks(documents: Sequence[Input]) -> List[Chunk]:
    chunks: List[Chunk] = []
    for document in documents:
        for index, content in enumerate(chunk_text(document.content)):
            chunks.append(
                Chunk(
                    chunk_id=f"{document.document_id}:{index}",
                    document_id=document.document_id,
                    content=content,
                    index=index,
                    timestamp=document.timestamp,
                )
            )
    return chunks


# ---------- Features ----------

def _build_features(chunks: Sequence[Chunk]) -> List[Feature]:
    features: List[Feature] = []
    for chunk in chunks:
        structural = extract_structural_features(chunk.content)
        vector = FeatureVector(
            information_density=structural.get("information_density", 0.0),
            logical_operator_ratio=structural.get("logical_operator_ratio", 0.0),
            hedging_frequency=0.0,
            abstraction_level=0.0,
            ordering_strength=0.0,
            topic_drift=0.0,
        )
        features.append(Feature(chunk_id=chunk.chunk_id, features=vector))
    return features


def _feature_embeddings(features: Sequence[Feature]) -> List[List[float]]:
    embeddings: List[List[float]] = []
    for feature in features:
        vector = feature.features
        embeddings.append(
            [float(getattr(vector, field) or 0.0) for field in FEATURE_FIELDS]
        )
    return embeddings


# ---------- Clustering ----------

def _build_clusters(
    chunks: Sequence[Chunk],
    embeddings: Sequence[List[float]],
) -> List[Cluster]:
    clusters: List[Cluster] = []
    assignments = cluster_embeddings(list(embeddings))
    if not assignments:
        return clusters

    total_chunks = max(len(chunks), 1)

    for cluster_id, member_indices in assignments.items():
        member_chunks = [
            chunks[idx].chunk_id
            for idx in member_indices
            if 0 <= idx < len(chunks)
        ]
        if not member_chunks:
            continue

        coherence_score = min(len(member_chunks) / total_chunks, 1.0)

        clusters.append(
            Cluster(
                cluster_id=f"cluster_{cluster_id}",
                label=f"Cluster {cluster_id}",
                member_chunks=member_chunks,
                coherence_score=round(coherence_score, 2),
            )
        )

    return clusters


def _select_primary_cluster(clusters: Sequence[Cluster]) -> Cluster:
    if not clusters:
        return Cluster(
            cluster_id="cluster_noise",
            label="Noise / Unclustered",
            member_chunks=[],
            coherence_score=0.0,
        )

    return max(
        clusters,
        key=lambda c: ((c.coherence_score or 0.0), len(c.member_chunks)),
    )


# ---------- Automata ----------

def _build_automata(cluster_sequence: Sequence[str]) -> Automata:
    states_raw, transitions_raw = infer_states(list(cluster_sequence))

    states = [AutomataState(**state) for state in states_raw]
    transitions = [
        AutomataTransition(
            from_state=t["from"],
            to_state=t["to"],
            probability=t["probability"],
        )
        for t in transitions_raw
    ]

    return Automata(states=states, transitions=transitions)


# ---------- Pipeline ----------

def run_pipeline(
    subject_id: str,
    documents: Iterable[Input | dict],
    enable_interpretation: bool = True,
) -> Report:
    inputs = _normalize_inputs(documents)
    chunks = _build_chunks(inputs)

    if len(chunks) < 5:
        interpretation = Interpretation(
            summary="Insufficient text volume to infer stable communication patterns.",
            guidance=["Provide more written material for analysis."],
            failure_modes=["Too few chunks for reliable clustering."],
            non_claims=["This analysis does not assess personality, intent, or mental state."],
        )

        return Report(
            subject_id=subject_id,
            patterns=[],
            primary_cluster_id=None,
            automata=Automata(states=[], transitions=[]),
            interpretation=interpretation,
            confidence=Confidence(
                overall=0.2,
                notes="Insufficient usable text for inference.",
            ),
            version=VersionInfo(
                features=FEATURES_VERSION,
                automata=AUTOMATA_VERSION,
                interpretation=INTERPRETATION_VERSION,
            ),
        )

    # Order chunks by time before sequencing
    chunks = sorted(chunks, key=lambda c: c.timestamp)

    features = _build_features(chunks)
    embeddings = _feature_embeddings(features)
    clusters = _build_clusters(chunks, embeddings)

    # Map every chunk to its assigned cluster
    chunk_to_cluster: Dict[str, str] = {}
    for cluster in clusters:
        for cid in cluster.member_chunks:
            chunk_to_cluster[cid] = cluster.cluster_id

    cluster_sequence = [
        chunk_to_cluster.get(chunk.chunk_id, "cluster_noise")
        for chunk in chunks
    ]

    automata = _build_automata(cluster_sequence)

    primary_cluster = _select_primary_cluster(clusters)
    coherence = primary_cluster.coherence_score or 0.0
    confidence_value = compute_confidence(
        num_chunks=len(chunks),
        num_states=len(automata.states),
        coherence_score=coherence,
    )

    interpretation = None
    if enable_interpretation:
        interpretation = Interpretation(
            summary=(
                f"Observed {len(chunks)} text chunks grouped into "
                f"{len(clusters)} communication pattern clusters."
            ),
            guidance=[
                "Present high-level intent before detailed constraints.",
                "Clarify ownership when transitioning between topics.",
            ],
            failure_modes=[
                "Sparse data reduces detectable structure.",
                "Mixed topics may weaken clustering coherence.",
            ],
            non_claims=[
                "This analysis does not assess personality or intent.",
                "It models observable communication structure only.",
            ],
        )

    return Report(
        subject_id=subject_id,
        patterns=clusters,
        primary_cluster_id=primary_cluster.cluster_id,
        automata=automata,
        interpretation=interpretation,
        confidence=Confidence(
            overall=confidence_value,
            notes="Confidence reflects chunk volume, state variety, and cluster coherence.",
        ),
        version=VersionInfo(
            features=FEATURES_VERSION,
            automata=AUTOMATA_VERSION,
            interpretation=INTERPRETATION_VERSION,
        ),
    )