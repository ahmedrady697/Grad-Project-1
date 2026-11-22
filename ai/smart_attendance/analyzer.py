"""Face detection + embedding.

`FaceAnalyzer` is the small interface the rest of the module depends on, so the
matching logic can be tested with a fake analyzer and the real model can be
swapped later. `InsightFaceAnalyzer` is the real implementation (CPU only).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np


@dataclass
class DetectedFace:
    bbox: tuple[int, int, int, int]  # x1, y1, x2, y2 in pixels
    embedding: np.ndarray
    score: float = 1.0               # detector confidence, 0..1

    @property
    def area(self) -> int:
        x1, y1, x2, y2 = self.bbox
        return max(0, x2 - x1) * max(0, y2 - y1)


class FaceAnalyzer(Protocol):
    def analyze(self, frame: np.ndarray) -> list[DetectedFace]:
        """Detect all faces in a BGR frame and return one embedding per face."""
        ...


class InsightFaceAnalyzer:
    """InsightFace detector + ArcFace-style embeddings, forced onto the CPU.

    The model is loaded on first use. The first run downloads the model files
    (internet needed once); later runs work offline.

    model_name: "buffalo_s" is the small model (best for old laptops),
                "buffalo_l" is more accurate but slower.
    det_size:   a smaller detection size is faster but misses small faces.
                Raise it (for example (640, 640)) if students at the back are missed.
    """

    def __init__(
        self,
        model_name: str = "buffalo_s",
        det_size: tuple[int, int] = (320, 320),
        min_det_score: float = 0.5,
    ) -> None:
        self.model_name = model_name
        self.det_size = det_size
        self.min_det_score = min_det_score
        self._app = None

    def _load(self) -> None:
        from insightface.app import FaceAnalysis  # imported late: heavy

        app = FaceAnalysis(
            name=self.model_name,
            allowed_modules=["detection", "recognition"],
            providers=["CPUExecutionProvider"],
        )
        app.prepare(ctx_id=-1, det_thresh=self.min_det_score, det_size=self.det_size)
        self._app = app

    def analyze(self, frame: np.ndarray) -> list[DetectedFace]:
        if self._app is None:
            self._load()
        faces = []
        for face in self._app.get(frame):
            x1, y1, x2, y2 = (int(v) for v in face.bbox)
            faces.append(
                DetectedFace(
                    bbox=(x1, y1, x2, y2),
                    embedding=np.asarray(face.embedding, dtype=np.float32),
                    score=float(face.det_score),
                )
            )
        return faces
