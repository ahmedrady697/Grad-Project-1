"""Send AI events to the backend (POST /events).

Standalone: only uses the standard library. Run `python data-integration/client.py`
from the repo root to post one test event to a locally running backend.
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

# allow running this file directly from anywhere
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ai.shared.schemas import Event, EventType, Module

BACKEND_URL = "http://127.0.0.1:8000"


def send_events(events: list[Event], base_url: str = BACKEND_URL) -> None:
    for event in events:
        req = urllib.request.Request(
            f"{base_url}/events",
            data=json.dumps(event.to_dict()).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            resp.read()


if __name__ == "__main__":
    send_events([Event(module=Module.BEHAVIOR, type=EventType.HAND_RAISED, confidence=0.9)])
    print("sent 1 test event")
