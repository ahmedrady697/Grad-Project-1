# Backend (Module 4)

FastAPI service that receives events from the AI modules and serves them to the frontend.

```bash
uvicorn backend.main:app --reload
# docs: http://127.0.0.1:8000/docs
```

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Health check |
| `POST /events` | AI modules post events here (format: `ai/shared/schemas/event.py`) |
| `GET /events?module=behavior&limit=100` | Frontend reads recent events |

`main.py` keeps events in memory for now.

## Plan

- [ ] Store events in SQLite (SQLAlchemy)
- [ ] Attendance records + endpoints per module
- [ ] WebSocket for live events and live video stream
- [ ] Authentication (teacher/admin)
- [ ] Export attendance to CSV/Excel
