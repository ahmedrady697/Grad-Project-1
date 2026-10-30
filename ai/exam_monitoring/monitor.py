"""Module 2 - Exam Monitoring (entry point).

Suggested pipeline:
    frame -> face/head pose (MediaPipe) + phone detection (YOLO)
          -> temporal rules (e.g. yaw beyond threshold for N seconds) -> list[Event]
"""
from __future__ import annotations

import numpy as np

from ai.shared.schemas import Event


class ExamMonitor:
    def __init__(self, yaw_threshold_deg: float = 35.0, hold_seconds: float = 2.0):
        self.yaw_threshold_deg = yaw_threshold_deg
        self.hold_seconds = hold_seconds
        # TODO: load face mesh + phone detector

    def process_frame(self, frame: np.ndarray) -> list[Event]:
        # TODO: estimate head pose, detect phones, apply rules
        return []
