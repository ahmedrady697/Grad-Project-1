# Team Roles

Fill in names and GitHub usernames. Suggested split for 6 people:

| Member | GitHub | Module | Responsibility |
|--------|--------|--------|----------------|
| 1 | | Module 1 - Behavior Detection | Dataset prep + model training (detection/classification) |
| 2 | | Module 1 - Behavior Detection | Real-time inference, pose-based rules, evaluation |
| 3 | | Module 2 - Exam Monitoring | Head pose / gaze, phone detection, suspicious-event rules |
| 4 | | Module 3 - Smart Attendance | Face detection + recognition, enrollment, attendance logging |
| 5 | | Module 4 - Dashboard | Backend API + database |
| 6 | | Module 4 - Dashboard | Frontend UI, charts, live feed, reports |

## Shared responsibilities

- `ai/shared/` (video input, event schema): everyone, reviewed by all.
- Integration and demo: rotate each milestone.
- Documentation and final report: split by module.

## Suggested timeline

| Phase | Goal |
|-------|------|
| 1 | Repo setup, datasets chosen, each module runs on a sample video |
| 2 | Baseline models working per module, events flowing to dashboard API |
| 3 | Dashboard UI + all modules integrated end to end |
| 4 | Evaluation, tuning, report, demo |
