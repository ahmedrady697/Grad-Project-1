import numpy as np
import pytest

from ai.shared.schemas import EventType
from ai.smart_attendance.analyzer import DetectedFace
from ai.smart_attendance.attendance import AttendanceSystem
from ai.smart_attendance.gallery import Gallery

ALICE = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32)
BOB = np.array([0.0, 1.0, 0.0, 0.0], dtype=np.float32)
STRANGER = np.array([0.0, 0.0, 1.0, 0.0], dtype=np.float32)
FRAME = np.zeros((10, 10, 3), dtype=np.uint8)


def face(embedding, bbox=(0, 0, 10, 10), score=0.99):
    return DetectedFace(bbox=bbox, embedding=embedding, score=score)


class FakeAnalyzer:
    """Returns a prepared list of faces for each call, then no faces."""

    def __init__(self, script):
        self.script = list(script)

    def analyze(self, frame):
        return self.script.pop(0) if self.script else []


def make_system(script, **kwargs):
    system = AttendanceSystem(analyzer=FakeAnalyzer(script), **kwargs)
    system.gallery.add("alice", ALICE)
    system.gallery.add("bob", BOB)
    return system


# ------------------------------------------------------------------ gallery
def test_gallery_matches_known_and_rejects_unknown():
    gallery = Gallery()
    gallery.add("alice", ALICE)
    gallery.add("bob", BOB)
    assert gallery.match(ALICE * 5, 0.4)[0] == "alice"  # length of vector does not matter
    student_id, sim = gallery.match(STRANGER, 0.4)
    assert student_id is None
    assert sim == pytest.approx(0.0)


def test_gallery_empty_returns_unknown():
    assert Gallery().match(ALICE, 0.4) == (None, 0.0)


def test_gallery_keeps_several_embeddings_per_student():
    gallery = Gallery()
    gallery.add("alice", ALICE)
    gallery.add("alice", STRANGER)
    assert len(gallery) == 1
    assert gallery.match(STRANGER, 0.9)[0] == "alice"  # best of her embeddings


def test_gallery_save_and_load(tmp_path):
    gallery = Gallery()
    gallery.add("alice", ALICE)
    gallery.add("bob", BOB)
    path = tmp_path / "gallery.npz"
    gallery.save(path)
    loaded = Gallery.load(path)
    assert loaded.student_ids == ["alice", "bob"]
    assert loaded.match(BOB, 0.9)[0] == "bob"


def test_zero_embedding_is_rejected():
    with pytest.raises(ValueError):
        Gallery().add("alice", np.zeros(4))


# ------------------------------------------------------------------- enroll
def test_enroll_uses_largest_face_in_each_image():
    small = face(STRANGER, bbox=(0, 0, 2, 2))
    large = face(ALICE, bbox=(0, 0, 8, 8))
    system = AttendanceSystem(analyzer=FakeAnalyzer([[small, large]]))
    assert system.enroll("alice", [FRAME]) == 1
    assert system.gallery.match(ALICE, 0.9)[0] == "alice"
    assert system.gallery.match(STRANGER, 0.9)[0] is None


def test_enroll_without_any_face_raises():
    system = AttendanceSystem(analyzer=FakeAnalyzer([[]]))
    with pytest.raises(ValueError):
        system.enroll("alice", [FRAME])


# ------------------------------------------------------------ process_frame
def test_present_only_after_consecutive_recognitions():
    system = make_system([[face(ALICE)]] * 3, min_consistent=3)
    assert system.process_frame(FRAME) == []
    assert system.process_frame(FRAME) == []
    events = system.process_frame(FRAME)
    assert len(events) == 1
    event = events[0]
    assert event.type == EventType.STUDENT_PRESENT
    assert event.student_id == "alice"
    assert event.confidence == pytest.approx(1.0)
    assert "alice" in system.attendance_report()


def test_present_is_reported_only_once():
    system = make_system([[face(ALICE)]] * 6, min_consistent=2)
    all_events = [e for _ in range(6) for e in system.process_frame(FRAME)]
    assert len(all_events) == 1


def test_missed_frame_resets_the_streak():
    script = [[face(ALICE)], [face(ALICE)], [], [face(ALICE)], [face(ALICE)]]
    system = make_system(script, min_consistent=3)
    events = [e for _ in range(5) for e in system.process_frame(FRAME)]
    assert events == []
    assert system.present == {}


def test_two_students_in_one_frame():
    system = make_system([[face(ALICE), face(BOB)]] * 2, min_consistent=2)
    system.process_frame(FRAME)
    events = system.process_frame(FRAME)
    assert {e.student_id for e in events} == {"alice", "bob"}


def test_unknown_face_is_rate_limited():
    now = [0.0]
    system = make_system([[face(STRANGER)]] * 4, unknown_cooldown=10.0, clock=lambda: now[0])
    first = system.process_frame(FRAME)
    assert [e.type for e in first] == [EventType.UNKNOWN_FACE]
    now[0] = 5.0
    assert system.process_frame(FRAME) == []
    now[0] = 11.0
    assert len(system.process_frame(FRAME)) == 1


def test_reset_session_forgets_attendance():
    system = make_system([[face(ALICE)]] * 4, min_consistent=2)
    for _ in range(2):
        system.process_frame(FRAME)
    assert system.present
    system.reset_session()
    assert system.present == {}
    system.analyzer.script = [[face(ALICE)]] * 2
    events = [e for _ in range(2) for e in system.process_frame(FRAME)]
    assert len(events) == 1
