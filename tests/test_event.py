from ai.shared.schemas import Event, EventType, Module


def test_event_to_dict_serializes_enums():
    e = Event(module=Module.BEHAVIOR, type=EventType.HAND_RAISED, confidence=0.9, track_id=3)
    d = e.to_dict()
    assert d["module"] == "behavior"
    assert d["type"] == "hand_raised"
    assert d["track_id"] == 3
    assert "timestamp" in d
