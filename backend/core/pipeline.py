from __future__ import annotations

from typing import Iterable, List, Sequence

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
                )
            )
    return chunks


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


def _build_clusters(chunks: Sequence[Chunk], embeddings: Sequence[List[float]]) -> List[Cluster]:
    clusters: List[Cluster] = []
    assignments = cluster_embeddings(list(embeddings))
    if not assignments:
        return clusters

    total_chunks = max(len(chunks), 1)
    for cluster_id, member_indices in assignments.items():
        member_chunks = [chunks[idx].chunk_id for idx in member_indices]
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
        return Cluster(cluster_id="cluster_0", label="Cluster 0", member_chunks=[], coherence_score=0.0)

    return max(
        clusters,
        key=lambda cluster: (cluster.coherence_score or 0.0, len(cluster.member_chunks)),
    )


def _build_automata(cluster_sequence: Sequence[str]) -> Automata:
    states, transitions = infer_states(list(cluster_sequence))
    return Automata(
        states=[AutomataState(**state) for state in states],
        transitions=[
            AutomataTransition(from_state=transition["from"], to=transition["to"], probability=transition["probability"])
            for transition in transitions
        ],
    )


def run_pipeline(documents: Iterable[Input | dict]) -> Report:
    inputs = _normalize_inputs(documents)
    chunks = _build_chunks(inputs)
    if not chunks:
        interpretation = Interpretation(
            summary="No usable chunks were available for analysis.",
            guidance=["Provide more text to infer stable patterns."],
            failure_modes=["Insufficient volume prevents reliable clustering."],
            non_claims=["This analysis does not assess personality, intent, or mental state."],
        )
        return Report(
            subject_id=inputs[0].author_id if inputs else "unknown",
            patterns=Cluster(cluster_id="cluster_0", label="Cluster 0", member_chunks=[], coherence_score=0.0),
            automata=Automata(states=[], transitions=[]),
            interpretation=interpretation,
            confidence=Confidence(overall=0.0, notes="Insufficient text volume for inference."),
            version=VersionInfo(features="0.1.0", automata="0.1.0", interpretation="0.1.0"),
        )

    features = _build_features(chunks)
    embeddings = _feature_embeddings(features)
    clusters = _build_clusters(chunks, embeddings)
    primary_cluster = _select_primary_cluster(clusters)

    cluster_by_chunk = {chunk_id: primary_cluster.cluster_id for chunk_id in primary_cluster.member_chunks}
    cluster_sequence = [
        cluster_by_chunk.get(chunk.chunk_id, primary_cluster.cluster_id) for chunk in chunks
    ]

    automata = _build_automata(cluster_sequence)
    coherence_score = primary_cluster.coherence_score or 0.0
    confidence_value = compute_confidence(len(chunks), len(automata.states), coherence_score)

    interpretation = Interpretation(
        summary=(
            f"Observed {len(chunks)} text chunks grouped into {len(clusters) or 1} communication pattern cluster(s)."
        ),
        guidance=[
            "Provide clear structure when introducing new topics.",
            "Confirm shared assumptions before moving into details.",
        ],
        failure_modes=[
            "Sparse text limits detectable structure.",
            "Mixed topics may reduce clustering coherence.",
        ],
        non_claims=[
            "This analysis does not assess personality, intent, or mental state.",
            "It only summarizes observable communication patterns.",
        ],
    )

    return Report(
        subject_id=inputs[0].author_id if inputs else "unknown",
        patterns=primary_cluster,
        automata=automata,
        interpretation=interpretation,
        confidence=Confidence(
            overall=confidence_value,
            notes="Confidence is based on chunk volume, state variety, and clustering coherence.",
        ),
        version=VersionInfo(features="0.1.0", automata="0.1.0", interpretation="0.1.0"),
    )
