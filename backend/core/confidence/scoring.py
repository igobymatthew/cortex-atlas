from typing import List

def compute_confidence(
    num_chunks: int,
    num_states: int,
    coherence_score: float
) -> float:
    """
    Conservative confidence calculation.
    """
    if num_chunks < 5:
        return 0.2

    base = min(num_chunks / 20, 1.0)
    state_penalty = max(0.0, 1.0 - (num_states * 0.1))

    confidence = base * state_penalty * coherence_score
    return round(min(confidence, 1.0), 2)
