# Module 3 - Smart Attendance

**Goal:** recognize students by face and record who is present in each session.

## Interface

```python
from ai.smart_attendance.attendance import AttendanceSystem
system = AttendanceSystem()
system.enroll("student_001", [img1, img2, img3])
events = system.process_frame(frame)    # -> list[ai.shared.schemas.Event]
system.attendance_report()              # student_id -> time first marked present
```

## Run it

Put enrollment photos in one folder per student (not committed to git, see `data/README.md`):

```
data/enroll/student_001/1.jpg
data/enroll/student_002/1.jpg
```

```bash
python -m ai.smart_attendance.run_demo --enroll data/enroll --gallery gallery.npz --source 0
python -m ai.smart_attendance.run_demo --gallery gallery.npz --source class.mp4 --backend http://127.0.0.1:8000
```

The first run downloads the InsightFace model (internet needed once). On a CPU-only laptop the
default `buffalo_s` model with `--width 640 --skip 5` is the starting point; see `docs/setup-old-mac.md`.

## How it works

1. `analyzer.py`: detects faces and computes an embedding for each (`InsightFaceAnalyzer`, CPU only).
2. `gallery.py`: stores embeddings per student and matches by cosine similarity (threshold default 0.4).
3. `attendance.py`: a student is marked present after `min_consistent` (default 3) consecutive
   frames recognize them, and is reported once. Unknown faces are reported at most every 10 seconds.

The analyzer is swappable, so the matching logic is tested without any model (`tests/test_attendance.py`).

## Plan

- [x] Enrollment, matching with cosine similarity, "unknown" handling
- [x] Present only after N consistent recognitions
- [x] Emit `Event` objects; demo script that posts them to the backend
- [ ] Run on real photos and videos; tune the threshold (0.4 is a placeholder, measure it)
- [ ] Liveness check (photo spoofing)
- [ ] Handle classroom conditions: small faces, angles, masks/glasses, lighting
- [ ] Evaluate accuracy on the team's own test set (accuracy, false accept rate)
- [ ] Attendance records stored per session in the backend

## Structure

```
smart_attendance/
├── attendance.py   # enrollment + recognition entry point
├── analyzer.py     # face detection + embeddings
├── gallery.py      # stored embeddings + matching
├── run_demo.py     # webcam / video demo
├── notebooks/
└── README.md
```
