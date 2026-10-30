"""Video input shared by all modules (webcam index, video file, or RTSP URL)."""
from __future__ import annotations

from collections.abc import Iterator

import cv2
import numpy as np


def read_frames(source: int | str = 0, skip: int = 0) -> Iterator[np.ndarray]:
    """Yield BGR frames from a webcam index, video file path, or stream URL.

    skip: number of frames to drop between yielded frames (speeds up processing).
    """
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video source: {source!r}")
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            yield frame
            for _ in range(skip):
                cap.grab()
    finally:
        cap.release()
