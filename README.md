# Real-Time Sign Language Translator

> A real-time system that captures hand gestures through a camera, recognizes sign language letters and words using computer vision and machine learning, and shows the result as live text (and optionally speech) on a web dashboard.

**Graduation Project** | Department of Computer Engineering | Academic Year 2026/2027

**Track:** Artificial Intelligence / Computer Vision / IoT

**Supervisor:** Dr. Walaa Omar

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [How It Works](#how-it-works)
- [Project Phases](#project-phases)
- [Tech Stack](#tech-stack)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Timeline](#timeline)
- [Team](#team)
- [Contribution Guide](#contribution-guide)

---

## Problem Statement

Deaf and hard-of-hearing people use sign language as their main way of communicating, but most hearing people do not understand it. This creates a communication barrier in education, healthcare, government services, and the workplace. Human interpreters are limited and not always available, especially in developing regions.

This project builds an automated, accessible, and low-cost system that translates sign language gestures into text and speech in real time.

## Objectives

- Capture hand gestures from a live camera stream.
- Recognize sign language letters/words using computer vision and machine learning.
- Output the result as text, and optionally as speech.
- Present everything on a live web dashboard to make a complete, demonstrable end-to-end solution.

## How It Works

```
Camera  ->  MediaPipe Hands  ->  ML Classifier  ->  Backend API  ->  Web Dashboard
(video)     (21 landmarks)       (letter / word)    (REST/WebSocket)  (live text + speech)
```

1. The camera captures a live video stream of the user's hand.
2. MediaPipe extracts 21 key points (landmarks) of the hand from each frame.
3. A trained model classifies the landmark pattern into a letter or word.
4. The result is streamed to the backend server.
5. The dashboard shows the translated text live, builds a running sentence, and can read it aloud.

## Project Phases

- [ ] **Phase 1: Static gestures (core deliverable)**: recognize individual alphabet letters from a single hand pose per frame.
- [ ] **Phase 2: Dynamic gestures (extension, time permitting)**: recognize words and short phrases that involve motion, using sequence models (LSTM/GRU).

Phase 1 guarantees a working system; Phase 2 adds a more advanced, research-worthy contribution.

## Tech Stack

| Layer                          | Technology                                              |
|--------------------------------|---------------------------------------------------------|
| Hand detection and landmarks   | MediaPipe Hands                                         |
| Classification (Phase 1)       | MLP / Random Forest on landmark coordinates             |
| Sequence modeling (Phase 2)    | LSTM / GRU                                              |
| Hardware                       | Webcam or Raspberry Pi Camera, laptop / Raspberry Pi    |
| Backend                        | Python (Flask / FastAPI)                                |
| Real-time communication        | REST API / WebSocket                                    |
| Frontend                       | Web dashboard (live text, sentence log, text-to-speech) |
| Database                       | SQLite / Firebase (session logs)                        |

## Dataset

- **Option A: ASL (American Sign Language):** public datasets such as the Kaggle ASL Alphabet dataset, used to validate the pipeline quickly.
- **Option B: Arabic / Egyptian Sign Language:** a custom dataset recorded by the team (multiple people, varied lighting and angles). Harder, but public Arabic sign language datasets are scarce, so it is a stronger research contribution.

> Large datasets and trained models are **not** stored in this repository. See `ai/README.md` for download links.

## Project Structure

```
sign-language-translator/
├── frontend/           # Web dashboard (live text, sentence log, speech)
├── backend/            # API server (Flask/FastAPI, WebSocket, database)
├── ai/                 # Model training, evaluation, MediaPipe + classifier
├── data-integration/   # Dataset collection, preprocessing, camera streaming
├── tests/              # Unit and integration tests
├── docs/               # Report, diagrams, presentations
├── .gitignore
└── README.md
```

## Getting Started

> The commands below are placeholders. Update them as the project takes shape.

### Prerequisites

- Git
- Python 3.10+
- Node.js 18+ (for the frontend, if used)
- A webcam

### Installation

```bash
# 1. Clone the repository
git clone git@github.com:username/sign-language-translator.git
cd sign-language-translator

# 2. Set up the Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Create your environment file
cp .env.example .env
# then fill in the values inside .env

# 4. Run the backend
cd backend
uvicorn main:app --reload

# 5. Run the frontend (in another terminal)
cd frontend
npm install
npm start
```

## Timeline

| Milestone                                              | Duration |
|--------------------------------------------------------|----------|
| Literature review and tool setup (MediaPipe, environment) | 2 weeks  |
| Dataset collection and preprocessing                   | 3 weeks  |
| Phase 1: static gesture classifier (training, testing) | 3 weeks  |
| Web dashboard development and system integration       | 3 weeks  |
| Phase 2 (optional): dynamic gestures (LSTM)            | 3 weeks  |
| Testing, documentation, and final report               | 2 weeks  |

## Team

| Name        | Role                      | GitHub                                    |
|-------------|---------------------------|-------------------------------------------|
| Your Name   | Team Leader, Integration  | [@username](https://github.com/username)  |
| Member 2    | AI / Model                | [@username](https://github.com/username)  |
| Member 3    | Backend                   | [@username](https://github.com/username)  |
| Member 4    | Frontend                  | [@username](https://github.com/username)  |
| Member 5    | Data, Testing             | [@username](https://github.com/username)  |

## Contribution Guide

1. Never push directly to `main`.
2. Before starting a task:
   ```bash
   git checkout main
   git pull
   git checkout -b feature/task-name
   ```
3. Commit with clear messages: `add ...`, `fix ...`, `update ...`
4. Push your branch and open a **Pull Request**.
5. At least one teammate must review before merging.

**Branch naming:** `feature/frontend-dashboard`, `feature/ai-landmark-classifier`, `feature/backend-websocket`, `fix/camera-lag`

## Screenshots

*(Add screenshots and demo GIFs here as the project progresses.)*

## License

For academic purposes.

For academic purposes.
