# Smart Classroom Monitoring

**Graduation Project** | Department of Computer Engineering | Academic Year 2026/2027

**Track:** Artificial Intelligence / Computer Vision / IoT

**Supervisor:** Dr. Walaa Omar

## Modules

| # | Module | Folder | Goal |
|---|--------|--------|------|
| 1 | Student Behavior Detection | `modules/behavior_detection` | Detect behaviors such as raising hand, writing, reading, using phone, sleeping, talking |
| 2 | Exam Monitoring | `modules/exam_monitoring` | Flag suspicious events: head/gaze turning, phone use, looking at neighbors |
| 3 | Smart Attendance | `modules/smart_attendance` | Recognize students by face and log attendance |
| 4 | Web Dashboard | `dashboard/` | Show live and historical results, reports, alerts |

## Architecture (high level)

```
Camera / Video  ->  shared/video_io  ->  Module 1 / 2 / 3  ->  events (JSON)  ->  Dashboard API  ->  Web UI
```

Each module exposes the same interface: it takes frames and returns a list of events following `shared/schemas/event.py`. The dashboard only talks to modules through these events, so everyone can work independently.

## Repo structure

```
.
├── modules/
│   ├── behavior_detection/   # Module 1
│   ├── exam_monitoring/      # Module 2
│   └── smart_attendance/     # Module 3
├── dashboard/
│   ├── backend/              # Module 4 - API (FastAPI)
│   └── frontend/             # Module 4 - UI (React)
├── shared/                   # video input, event schema, utils used by all modules
├── data/                     # datasets (NOT committed, see data/README.md)
├── docs/                     # datasets list, team roles, design notes
├── scripts/                  # helper scripts
└── .github/                  # PR template + CI
```

## Getting started

```bash
git clone <repo-url>
cd smart-classroom-monitoring
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Then see the README inside your module's folder.

## Team

See [docs/team-roles.md](docs/team-roles.md).

## Workflow

See [CONTRIBUTING.md](CONTRIBUTING.md).


## License

For academic purposes.

For academic purposes.
