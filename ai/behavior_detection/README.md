# Module 1 - Student Behavior Detection

**Goal:** detect student behaviors (hand raised, writing, reading, using phone, sleeping, talking, looking away) from classroom video.

## Interface

```python
from ai.behavior_detection.detector import BehaviorDetector
detector = BehaviorDetector("models/weights/behavior.pt")
events = detector.process_frame(frame)   # -> list[ai.shared.schemas.Event]
```

## Plan

- [ ] Pick and download datasets (see `docs/datasets.md`), log them in `data/README.md`
- [ ] Baseline: pretrained YOLO person + pose on a sample video
- [ ] Fine-tune detector on classroom behavior data
- [ ] Add tracking so each student keeps an id across frames
- [ ] Smooth predictions over time (avoid flicker)
- [ ] Evaluate (mAP, per-class precision/recall) and save results for the report
- [ ] Emit `Event` objects for the dashboard

## Structure

```
behavior_detection/
├── detector.py     # inference entry point
├── train/          # training scripts / configs
├── notebooks/      # experiments (clear outputs before commit)
└── README.md
```
