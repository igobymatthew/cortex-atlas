from typing import List
import re

MIN_CHUNK_LENGTH = 40
MAX_CHUNK_LENGTH = 500

def chunk_text(text: str) -> List[str]:
    """
    Split text into semantically meaningful chunks.
    Prefers paragraph boundaries, falls back to sentences.
    """
    if not text or not text.strip():
        return []

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: List[str] = []

    for p in paragraphs:
        if len(p) <= MAX_CHUNK_LENGTH:
            if len(p) >= MIN_CHUNK_LENGTH:
                chunks.append(p)
        else:
            # fallback to sentence split
            sentences = re.split(r"(?<=[.!?])\s+", p)
            buffer = ""
            for s in sentences:
                if len(buffer) + len(s) < MAX_CHUNK_LENGTH:
                    buffer += " " + s
                else:
                    if len(buffer.strip()) >= MIN_CHUNK_LENGTH:
                        chunks.append(buffer.strip())
                    buffer = s
            if len(buffer.strip()) >= MIN_CHUNK_LENGTH:
                chunks.append(buffer.strip())

    return chunks
