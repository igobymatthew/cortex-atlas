from typing import List, Dict
import numpy as np

def cluster_embeddings(
    embeddings: List[List[float]],
    min_cluster_size: int = 3
) -> Dict[int, List[int]]:
    """
    Simple placeholder clustering.
    Replace internals with HDBSCAN later without changing signature.
    """
    if not embeddings:
        return {}

    clusters: Dict[int, List[int]] = {}
    cluster_id = 0

    for idx, _ in enumerate(embeddings):
        clusters.setdefault(cluster_id, []).append(idx)
        if len(clusters[cluster_id]) >= min_cluster_size:
            cluster_id += 1

    return clusters