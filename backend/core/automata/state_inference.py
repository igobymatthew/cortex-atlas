from typing import List, Dict, Tuple
from collections import defaultdict

def infer_states(
    cluster_sequence: List[str]
) -> Tuple[List[Dict], List[Dict]]:
    """
    Infers a probabilistic state machine from an ordered cluster sequence.
    """
    state_counts = defaultdict(int)
    transition_counts = defaultdict(int)

    for state in cluster_sequence:
        state_counts[state] += 1

    for a, b in zip(cluster_sequence, cluster_sequence[1:]):
        transition_counts[(a, b)] += 1

    states = [
        {
            "state_id": state,
            "label": state,
            "support": count / len(cluster_sequence)
        }
        for state, count in state_counts.items()
    ]

    transitions = []
    for (a, b), count in transition_counts.items():
        total = state_counts[a]
        transitions.append({
            "from": a,
            "to": b,
            "probability": count / total
        })

    return states, transitions
