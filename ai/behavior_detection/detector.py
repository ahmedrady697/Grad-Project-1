"""Module 1 - Student Behavior Detection (entry point).

Replace the body of `process_frame` with your real pipeline:
    frame -> person detection/tracking -> pose / classifier -> list[Event]
"""
from __future__ import annotations

import numpy as np

from ai.shared.schemas import Event


class BehaviorDetector:
    def __init__(self, weights_path: str | None = None):
        self.weights_path = weights_path
        # TODO: load YOLO model here

    def process_frame(self, frame: np.ndarray) -> list[Event]:
        # TODO: run inference and convert detections to Event objects
        return []
