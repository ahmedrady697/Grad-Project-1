"""Module 4 - Dashboard backend (FastAPI).

Run:  uvicorn backend.main:app --reload
Docs: http://127.0.0.1:8000/docs

This is a minimal in-memory starting point. Replace EVENTS with a real database
(SQLite/PostgreSQL) once the event format is stable.
"""
from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Smart Classroom Monitoring API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

EVENTS: list[dict[str, Any]] = []


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/events")
def add_event(event: dict[str, Any]) -> dict[str, int]:
    """Modules post events here (see ai/shared/schemas/event.py for the format)."""
    EVENTS.append(event)
    return {"count": len(EVENTS)}


@app.get("/events")
def list_events(module: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
    items = [e for e in EVENTS if module is None or e.get("module") == module]
    return items[-limit:]
