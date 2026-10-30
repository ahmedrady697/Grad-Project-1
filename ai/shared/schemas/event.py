"""Event schema: the contract between the modules and the dashboard.

Every module (behavior, exam, attendance) turns frames into a list of Event
objects. The dashboard backend only understands this format, so each module can
be developed and tested independently.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class Module(str, Enum):
    BEHAVIOR = "behavior"
    EXAM = "exam"
    ATTENDANCE = "attendance"


class EventType(str, Enum):
    # Module 1 - behavior
    HAND_RAISED = "hand_raised"
    WRITING = "writing"
    READING = "reading"
    USING_PHONE = "using_phone"
    SLEEPING = "sleeping"
    TALKING = "talking"
    LOOKING_AWAY = "looking_away"
    # Module 2 - exam
    SUSPICIOUS_HEAD_TURN = "suspicious_head_turn"
    PHONE_DETECTED = "phone_detected"
    LEFT_SEAT = "left_seat"
    # Module 3 - attendance
    STUDENT_PRESENT = "student_present"
    UNKNOWN_FACE = "unknown_face"


@dataclass
class Event:
    module: Module
    type: EventType
    confidence: float
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    camera_id: str = "cam0"
    track_id: int | None = None          # tracker id inside the video
    student_id: str | None = None        # only when known (attendance)
    bbox: tuple[int, int, int, int] | None = None  # x1, y1, x2, y2 in pixels
    meta: dict[str, Any] = field(default_factory=dict)  # anything module-specific

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["module"] = self.module.value
        d["type"] = self.type.value
        return d
