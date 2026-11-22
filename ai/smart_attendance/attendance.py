"""Module 3 - Smart Attendance (entry point).

    enroll():        photos of a student -> embeddings stored with student_id
    process_frame(): frame -> detect faces -> embeddings -> cosine match -> list[Event]

A student is marked present only after `min_consistent` consecutive processed
frames recognize them, and is reported once per session. Unknown faces are
reported at most once every `unknown_cooldown` seconds, so the dashboard is not
flooded.
"""
from __future__ import annotations

import time
from collections.abc import Callable
from pathlib import Path

import numpy as np

from ai.shared.schemas import Event, EventType, Module

from .analyzer import DetectedFace, FaceAnalyzer, InsightFaceAnalyzer
from .gallery import Gallery


class AttendanceSystem:
    def __init__(
        self,
        similarity_threshold: float = 0.4,
        *,
        analyzer: FaceAnalyzer | None = None,
        min_consistent: int = 3,
        unknown_cooldown: float = 10.0,
        camera_id: str = "cam0",
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.similarity_threshold = similarity_threshold
        self.min_consistent = min_consistent
        self.unknown_cooldown = unknown_cooldown
        self.camera_id = camera_id
        self._clock = clock
        self._analyzer = analyzer
        self.gallery = Gallery()
        self.present: dict[str, str] = {}  # student_id -> timestamp first marked present
        self._streak: dict[str, int] = {}  # student_id -> consecutive frames recognized
        self._last_unknown: float | None = None

    @property
    def analyzer(self) -> FaceAnalyzer:
        if self._analyzer is None:
            self._analyzer = InsightFaceAnalyzer()
        return self._analyzer

    # ------------------------------------------------------------------ enroll
    def enroll(self, student_id: str, images: list[np.ndarray]) -> int:
        """Add embeddings for a student. Uses the largest face in each image.

        Returns how many images produced an embedding. Raises ValueError when
        no image contains a face, so a bad enrollment is never silent.
        """
        added = 0
        for image in images:
            faces = self.analyzer.analyze(image)
            if not faces:
                continue
            largest = max(faces, key=lambda f: f.area)
            self.gallery.add(student_id, largest.embedding)
            added += 1
        if added == 0:
            raise ValueError(f"no face found in any enrollment image for {student_id!r}")
        return added

    def save_gallery(self, path: str | Path) -> None:
        self.gallery.save(path)

    def load_gallery(self, path: str | Path) -> None:
        self.gallery = Gallery.load(path)

    # ----------------------------------------------------------------- session
    def reset_session(self) -> None:
        """Forget who is present (call at the start of each class)."""
        self.present.clear()
        self._streak.clear()
        self._last_unknown = None

    def attendance_report(self) -> dict[str, str]:
        """student_id -> timestamp first marked present."""
        return dict(self.present)

    # ------------------------------------------------------------------- frame
    def process_frame(self, frame: np.ndarray) -> list[Event]:
        events: list[Event] = []
        seen_now: set[str] = set()

        for face in self.analyzer.analyze(frame):
            student_id, similarity = self.gallery.match(face.embedding, self.similarity_threshold)
            if student_id is None:
                unknown = self._unknown_event(face, similarity)
                if unknown is not None:
                    events.append(unknown)
                continue

            seen_now.add(student_id)
            if student_id in self.present:
                continue
            self._streak[student_id] = self._streak.get(student_id, 0) + 1
            if self._streak[student_id] >= self.min_consistent:
                event = Event(
                    module=Module.ATTENDANCE,
                    type=EventType.STUDENT_PRESENT,
                    confidence=min(1.0, max(0.0, similarity)),
                    camera_id=self.camera_id,
                    student_id=student_id,
                    bbox=face.bbox,
                    meta={"similarity": round(similarity, 4)},
                )
                self.present[student_id] = event.timestamp
                events.append(event)

        # a student must be recognized in consecutive frames, so reset the others
        self._streak = {sid: n for sid, n in self._streak.items() if sid in seen_now}
        return events

    def _unknown_event(self, face: DetectedFace, similarity: float) -> Event | None:
        now = self._clock()
        if self._last_unknown is not None and now - self._last_unknown < self.unknown_cooldown:
            return None
        self._last_unknown = now
        return Event(
            module=Module.ATTENDANCE,
            type=EventType.UNKNOWN_FACE,
            confidence=min(1.0, max(0.0, face.score)),
            camera_id=self.camera_id,
            bbox=face.bbox,
            meta={"best_similarity": round(similarity, 4)},
        )
