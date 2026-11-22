# Backend (Module 4)

FastAPI service that receives events from the AI modules and serves them to the frontend.

```bash
uvicorn backend.main:app --reload
# docs: http://127.0.0.1:8000/docs
```

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Health check |
| `POST /events` | AI modules post events here. Validated against `ai/shared/schemas/event.py`; bad events get HTTP 422 |
| `GET /events?module=&type=&student_id=&limit=100` | Frontend reads recent events (all filters optional) |
| `GET /attendance?date=YYYY-MM-DD` | Students marked present (first sighting each, UTC date) |

`main.py` keeps events in memory for now, so they are lost on restart.

Tests: `pytest tests/test_backend.py` (needs `fastapi` and `httpx`).

## Plan

- [ ] Store events in SQLite (SQLAlchemy)
- [ ] Sessions (class + date) so attendance is per lecture, not per day
- [ ] WebSocket for live events and live video stream
- [ ] Authentication (teacher/admin)
- [ ] Export attendance to CSV/Excel
