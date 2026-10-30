# Module 3 - Smart Attendance

**Goal:** recognize students by face and record who is present in each session.

## Interface

```python
from ai.smart_attendance.attendance import AttendanceSystem
system = AttendanceSystem()
system.enroll("student_001", [img1, img2, img3])
events = system.process_frame(frame)    # -> list[ai.shared.schemas.Event]
```

## Plan

- [ ] Face detection + embeddings with InsightFace on sample images
- [ ] Enrollment: 5-10 photos per student (with consent), store embeddings (not raw photos if possible)
- [ ] Matching with cosine similarity + tuned threshold; handle "unknown"
- [ ] Mark a student present only after N consistent recognitions (avoid false positives)
- [ ] Handle classroom conditions: small faces, angles, masks/glasses, lighting
- [ ] Evaluate accuracy on the team's own test set
- [ ] Emit `Event` objects and attendance records for the dashboard

## Structure

```
smart_attendance/
├── attendance.py   # enrollment + recognition entry point
├── notebooks/
└── README.md
```
