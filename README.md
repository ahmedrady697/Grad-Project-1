# Smart Classroom Monitoring

Graduation project, Department of Computer Engineering. A computer-vision system that monitors classrooms and exams, takes attendance automatically, and shows everything in a web dashboard.

## Modules

| # | Module | Where | Goal |
|---|--------|-------|------|
| 1 | Student Behavior Detection | `ai/behavior_detection` | Detect hand raising, writing, reading, phone use, sleeping, talking |
| 2 | Exam Monitoring | `ai/exam_monitoring` | Flag suspicious events: head/gaze turning, phone use, leaving seat |
| 3 | Smart Attendance | `ai/smart_attendance` | Recognize students by face and log attendance |
| 4 | Web Dashboard | `backend/` + `frontend/` | Live view, alerts, attendance sheet, reports |

## Architecture

```
Camera / Video -> ai/shared/video_io -> Module 1 / 2 / 3 -> Event (JSON)
                                                     |
                                    data-integration/client.py (POST /events)
                                                     |
                                              backend (FastAPI) -> frontend (React)
```

Every AI module returns a list of `Event` objects (`ai/shared/schemas/event.py`). That schema is the only contract between the AI side and the dashboard, so everyone can work independently.

## Repo structure

```
.
├── ai/
│   ├── behavior_detection/   # Module 1
│   ├── exam_monitoring/      # Module 2
│   ├── smart_attendance/     # Module 3
│   └── shared/               # Event schema + video input used by all modules
├── backend/                  # Module 4 - FastAPI API
├── frontend/                 # Module 4 - React UI
├── data-integration/         # sends AI events to the backend
├── data/                     # datasets (NOT committed, see data/README.md)
├── docs/                     # datasets guide, team roles
├── tests/
└── .github/                  # PR template + CI
```

## Getting started

```bash
git clone https://github.com/ahmedrady697/Grad-Project-1.git
cd Grad-Project-1
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn backend.main:app --reload     # http://127.0.0.1:8000/docs
```

See each module's README for its own steps.

## Team

See [docs/team-roles.md](docs/team-roles.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Never push directly to `main`; open a Pull Request and get at least one review.

## License

Academic use only.
