"""Module 4 - Dashboard backend (FastAPI).

Run:  uvicorn backend.main:app --reload
Docs: http://127.0.0.1:8000/docs

Events are kept in memory for now. Replace EVENTS with a real database
(SQLite/PostgreSQL) once the event format is stable.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from ai.shared.schemas import EventType, Module

app = FastAPI(title="Smart Classroom Monitoring API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_methods=["*"],
    allow_headers=["*"],
)


class EventIn(BaseModel):
    """Mirrors ai/shared/schemas/event.py. Invalid events are rejected with HTTP 422."""

    module: Module
    type: EventType
    confidence: float = Field(ge=0.0, le=1.0)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    camera_id: str = "cam0"
    track_id: int | None = None
    student_id: str | None = None
    bbox: tuple[int, int, int, int] | None = None
    meta: dict[str, Any] = Field(default_factory=dict)


EVENTS: list[dict[str, Any]] = []


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/events")
def add_event(event: EventIn) -> dict[str, int]:
    """Modules post events here (see ai/shared/schemas/event.py for the format)."""
    EVENTS.append(event.model_dump(mode="json"))
    return {"count": len(EVENTS)}


@app.get("/events")
def list_events(
    module: str | None = None,
    event_type: str | None = Query(default=None, alias="type"),
    student_id: str | None = None,
    limit: int = Query(default=100, ge=1, le=1000),
) -> list[dict[str, Any]]:
    items = [
        e
        for e in EVENTS
        if (module is None or e["module"] == module)
        and (event_type is None or e["type"] == event_type)
        and (student_id is None or e["student_id"] == student_id)
    ]
    return items[-limit:]


@app.get("/attendance")
def attendance(
    date: str | None = Query(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$"),
) -> dict[str, Any]:
    """Students marked present, first sighting only.

    date: optional YYYY-MM-DD in UTC (timestamps are stored in UTC).
    """
    first_seen: dict[str, dict[str, Any]] = {}
    for e in EVENTS:
        if e["type"] != EventType.STUDENT_PRESENT.value or not e["student_id"]:
            continue
        if date is not None and not e["timestamp"].startswith(date):
            continue
        first_seen.setdefault(
            e["student_id"],
            {
                "student_id": e["student_id"],
                "first_seen": e["timestamp"],
                "confidence": e["confidence"],
            },
        )
    present = sorted(first_seen.values(), key=lambda r: r["first_seen"])
    return {"date": date, "count": len(present), "present": present}
