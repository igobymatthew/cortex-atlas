from typing import Dict
import re

LOGICAL_OPERATORS = ["if", "then", "because", "therefore", "however", "but"]

def extract_structural_features(text: str) -> Dict[str, float]:
    words = text.split()
    word_count = max(len(words), 1)

    logical_hits = sum(
        1 for w in words if w.lower().strip(",.") in LOGICAL_OPERATORS
    )

    sentences = re.split(r"[.!?]", text)
    avg_sentence_length = (
        sum(len(s.split()) for s in sentences if s.strip()) / max(len(sentences), 1)
    )

    return {
        "information_density": word_count / max(len(text), 1),
        "logical_operator_ratio": logical_hits / word_count,
        "avg_sentence_length": avg_sentence_length,
    }
