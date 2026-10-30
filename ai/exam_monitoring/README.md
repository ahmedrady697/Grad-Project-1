# Module 2 - Exam Monitoring

**Goal:** flag suspicious behavior during exams: looking at neighbors, phone use, leaving the seat.

## Interface

```python
from ai.exam_monitoring.monitor import ExamMonitor
monitor = ExamMonitor()
events = monitor.process_frame(frame)   # -> list[ai.shared.schemas.Event]
```

## Plan

- [ ] Head pose estimation (MediaPipe Face Mesh) on a sample video
- [ ] Phone detection (pretrained YOLO "cell phone" class, fine-tune if needed)
- [ ] Temporal rules: suspicious only if the condition holds for N seconds, to avoid false alarms
- [ ] Seat zones / "left seat" detection
- [ ] Save short evidence clips/snapshots for each alert
- [ ] Evaluate on recorded test scenarios (acted cheating vs normal behavior) and report false positives
- [ ] Emit `Event` objects for the dashboard

## Structure

```
exam_monitoring/
├── monitor.py      # inference entry point
├── notebooks/
└── README.md
```
