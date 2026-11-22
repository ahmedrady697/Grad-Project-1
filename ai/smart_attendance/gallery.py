"""Gallery of enrolled face embeddings with cosine-similarity matching.

Only embeddings are stored, never photos. Numpy is the only dependency, so this
file can be tested without any face-recognition model installed.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np


def _normalize(vec: np.ndarray) -> np.ndarray:
    vec = np.asarray(vec, dtype=np.float32).ravel()
    norm = float(np.linalg.norm(vec))
    if norm == 0.0:
        raise ValueError("embedding has zero length")
    return vec / norm


class Gallery:
    """student_id -> several normalized embeddings (one per enrollment photo)."""

    def __init__(self) -> None:
        self._embeddings: dict[str, np.ndarray] = {}  # student_id -> (n, dim)

    def __len__(self) -> int:
        return len(self._embeddings)

    @property
    def student_ids(self) -> list[str]:
        return sorted(self._embeddings)

    def add(self, student_id: str, embedding: np.ndarray) -> None:
        vec = _normalize(embedding)[None, :]
        if student_id in self._embeddings:
            self._embeddings[student_id] = np.vstack([self._embeddings[student_id], vec])
        else:
            self._embeddings[student_id] = vec

    def match(self, embedding: np.ndarray, threshold: float) -> tuple[str | None, float]:
        """Return (student_id, similarity) of the best match.

        student_id is None when the best similarity is below the threshold
        (an unknown face). The similarity is still returned for logging.
        """
        if not self._embeddings:
            return None, 0.0
        query = _normalize(embedding)
        best_id: str | None = None
        best_sim = -1.0
        for student_id, embs in self._embeddings.items():
            sim = float(np.max(embs @ query))
            if sim > best_sim:
                best_id, best_sim = student_id, sim
        if best_sim < threshold:
            return None, best_sim
        return best_id, best_sim

    def save(self, path: str | Path) -> None:
        """Save to a .npz file (embeddings only)."""
        ids = self.student_ids
        arrays = {f"emb_{i}": self._embeddings[sid] for i, sid in enumerate(ids)}
        np.savez_compressed(Path(path), ids=np.array(ids, dtype=str), **arrays)

    @classmethod
    def load(cls, path: str | Path) -> Gallery:
        gallery = cls()
        with np.load(Path(path), allow_pickle=False) as data:
            for i, sid in enumerate(data["ids"].tolist()):
                gallery._embeddings[str(sid)] = data[f"emb_{i}"]
        return gallery
