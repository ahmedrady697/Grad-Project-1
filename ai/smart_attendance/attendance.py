"""Module 3 - Smart Attendance (entry point).

Suggested pipeline:
    enroll():        photos of a student -> embeddings stored with student_id
    process_frame(): frame -> detect faces -> embeddings -> cosine match -> list[Event]
"""
from __future__ import annotations

import numpy as np

from ai.shared.schemas import Event


class AttendanceSystem:
    def __init__(self, similarity_threshold: float = 0.4):
        self.similarity_threshold = similarity_threshold
        self.gallery: dict[str, list[np.ndarray]] = {}  # student_id -> embeddings
        # TODO: load InsightFace model

    def enroll(self, student_id: str, images: list[np.ndarray]) -> None:
        # TODO: compute embeddings for each image and store them
        raise NotImplementedError

    def process_frame(self, frame: np.ndarray) -> list[Event]:
        # TODO: detect faces, match against gallery, emit STUDENT_PRESENT / UNKNOWN_FACE
        return []
