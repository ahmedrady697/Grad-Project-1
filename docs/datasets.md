# Datasets and Pretrained Models

> Dataset names below are real and widely used, but **check the current link, size and license of each one before building on it**. For roboflow/Kaggle datasets, search by the keywords given, since individual uploads come and go. Record what you actually use in `data/README.md`.

## Module 1 - Student Behavior Detection

Goal: detect behaviors like raising hand, writing, reading, using phone, sleeping, talking, looking away.

| Dataset | What it gives you | Notes |
|---------|-------------------|-------|
| **SCB-Dataset** (Student Classroom Behavior) | Real classroom images annotated for hand-raising, reading, writing and more, in YOLO format | Best starting point: made for this exact task |
| Roboflow Universe: "classroom behavior", "student behavior", "hand raising" | Many small YOLO-ready datasets | Merge several to get more data; check class names match |
| **COCO** / **COCO Keypoints** | Persons, cell phones, pose keypoints | Pretrained YOLO models already know "person" and "cell phone" |
| **AVA** (Atomic Visual Actions) | Large action-recognition set | Heavy, only if you go video-based |
| Kaggle: "student sleeping / drowsiness" | Sleeping/drowsy datasets | Search keywords: drowsiness, sleeping student |

**Practical approach (recommended):**
1. Start with a pretrained YOLO pose model (Ultralytics) to get people + skeleton.
2. Fine-tune a YOLO detector on SCB-Dataset for hand-raise / write / read.
3. Add rules on pose (for example wrist above shoulder = raising hand) as a fallback and for comparison in your report.

## Module 2 - Exam Monitoring

Goal: flag suspicious events such as looking at neighbors, phone use, leaving seat, passing objects.

| Dataset | What it gives you | Notes |
|---------|-------------------|-------|
| **COCO** (cell phone, book classes) | Phone detection via pretrained YOLO | Good enough for a baseline |
| Roboflow Universe: "cheating detection", "exam cheating", "mobile phone detection" | Cheating-behavior and phone datasets | Quality varies a lot, inspect labels |
| **300W-LP**, **AFLW2000**, **BIWI** | Head pose (yaw/pitch/roll) | For training/evaluating head-pose models |
| **Gaze360**, **MPIIGaze**, **ETH-XGaze** | Gaze direction | Heavy; usually use a pretrained model instead |
| Kaggle: "online exam proctoring" | Webcam proctoring sets | Search keywords: proctoring, cheating |

**Practical approach:** use MediaPipe Face Mesh to compute head pose (no training needed), flag when yaw stays beyond a threshold for N seconds, combine with phone detection and "person left seat" logic. Training a cheating classifier from scratch is risky because public data is small; rule-based plus pretrained is more reliable for a graduation project.

## Module 3 - Smart Attendance

Goal: identify students by face and mark attendance.

| Resource | Use |
|----------|-----|
| **WIDER FACE** | Face detection training/evaluation |
| **LFW** (Labeled Faces in the Wild) | Face verification benchmark |
| **VGGFace2**, **CASIA-WebFace** | Face recognition training (you usually do not need to train) |
| **InsightFace** (ArcFace, buffalo_l models) | **Recommended**: pretrained detection + embeddings, high accuracy |
| `face_recognition` (dlib) / **DeepFace** | Simpler alternatives, easier but less accurate |

**Practical approach:** do not train a face model. Use InsightFace to detect faces and compute embeddings, store one or more embeddings per enrolled student, and match new faces by cosine similarity with a threshold. Your own collected data (enrollment photos of classmates, **with their consent**) is the most important dataset: take 5-10 photos per person under different angles/lighting, and test in the real classroom camera conditions.

## Module 4 - Web Dashboard

No dataset needed. Suggested stack:

- Backend: **FastAPI** + SQLite (later PostgreSQL if needed)
- Frontend: **React** (Vite) + a chart library (Recharts / Chart.js)
- Live video: MJPEG stream or WebSocket from the backend
- Realtime events: WebSocket

## Tools Summary

- **Ultralytics YOLO**: detection, pose, tracking. Note it uses the AGPL license, fine for a graduation project.
- **MediaPipe**: face mesh, head pose, hands.
- **InsightFace**: face recognition.
- **OpenCV**: video I/O and drawing.
- **Roboflow / CVAT / Label Studio**: annotation if you need to label your own classroom data.

## Privacy and Ethics

Students are being recorded and identified. Get permission from your supervisor and from the classmates who appear in your test data, store face embeddings rather than raw photos where possible, and mention privacy in your final report.
