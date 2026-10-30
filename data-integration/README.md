# Data Integration

Connects the AI modules to the backend. AI code produces `Event` objects (`ai/shared/schemas/event.py`); `client.py` sends them to `POST /events`.

```python
# the folder name has a hyphen, so import it by path from the repo root:
import importlib.util
spec = importlib.util.spec_from_file_location("client", "data-integration/client.py")
client = importlib.util.module_from_spec(spec); spec.loader.exec_module(client)

client.send_events(events)   # events: list[ai.shared.schemas.Event]
```

Quick test (backend running):

```bash
python data-integration/client.py
```

If you change the event format, change `ai/shared/schemas/event.py` first (in its own PR), then update the backend and frontend.
