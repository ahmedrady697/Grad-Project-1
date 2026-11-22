import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient

from backend.main import EVENTS, app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_events():
    EVENTS.clear()
    yield
    EVENTS.clear()


def present(student_id, timestamp="2026-11-22T08:00:00+00:00", confidence=0.9):
    return {
        "module": "attendance",
        "type": "student_present",
        "confidence": confidence,
        "timestamp": timestamp,
        "student_id": student_id,
        "bbox": [1, 2, 3, 4],
    }


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_post_and_list_events():
    assert client.post("/events", json=present("s1")).json() == {"count": 1}
    events = client.get("/events").json()
    assert len(events) == 1
    assert events[0]["student_id"] == "s1"
    assert events[0]["bbox"] == [1, 2, 3, 4]


def test_invalid_event_is_rejected():
    assert client.post("/events", json={"module": "nope", "type": "x", "confidence": 2}).status_code == 422
    assert client.post("/events", json={**present("s1"), "confidence": 1.5}).status_code == 422
    assert EVENTS == []


def test_filters():
    client.post("/events", json=present("s1"))
    client.post("/events", json={"module": "behavior", "type": "sleeping", "confidence": 0.8})
    assert len(client.get("/events", params={"module": "behavior"}).json()) == 1
    assert len(client.get("/events", params={"type": "student_present"}).json()) == 1
    assert len(client.get("/events", params={"student_id": "s1"}).json()) == 1
    assert len(client.get("/events", params={"limit": 1}).json()) == 1


def test_attendance_first_sighting_and_date_filter():
    client.post("/events", json=present("s1", "2026-11-22T08:00:00+00:00"))
    client.post("/events", json=present("s1", "2026-11-22T09:00:00+00:00"))
    client.post("/events", json=present("s2", "2026-11-23T08:00:00+00:00"))
    everyone = client.get("/attendance").json()
    assert everyone["count"] == 2
    day = client.get("/attendance", params={"date": "2026-11-22"}).json()
    assert [r["student_id"] for r in day["present"]] == ["s1"]
    assert day["present"][0]["first_seen"] == "2026-11-22T08:00:00+00:00"


def test_attendance_rejects_bad_date():
    assert client.get("/attendance", params={"date": "22/11/2026"}).status_code == 422
