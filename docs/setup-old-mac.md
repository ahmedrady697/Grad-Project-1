# Setup on an older Mac (CPU only)

Written for a MacBook Pro mid-2012 (13.6.1). The same steps work on any machine without a GPU. These steps have not been tested on every Mac, so report problems in an issue.

## 1. Python environment

Use Python 3.10 or 3.11.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

## 2. Install in stages

Install in this order and test each import. If a step fails, you know which package is the problem.

```bash
pip install numpy opencv-python onnxruntime
python -c "import numpy, cv2, onnxruntime"

pip install mediapipe insightface
python -c "import mediapipe, insightface"

pip install ultralytics          # pulls in PyTorch, large download
python -c "import ultralytics"

pip install fastapi "uvicorn[standard]" pydantic pytest ruff
```

## 3. Known problems

- **"Illegal instruction"**: the 2012 CPU lacks some newer instructions. Install an older version of the failing package (`pip install "package==older.version"`) or use the ONNX Runtime CPU build.
- **ultralytics will not install**: skip it for now. Export models to ONNX on Google Colab and run them with `onnxruntime` on the Mac.
- **Slow video**: resize frames to 640 pixels wide, process 1 to 2 frames per second, and use small models (YOLOv8n, MediaPipe).

## 4. Training

Do not train on the Mac. Train on Google Colab or Kaggle (free GPU), save weights to Google Drive, and put the link in `data/README.md`. Never commit weights or datasets.

## 5. Check the camera

```bash
python -c "import cv2; c = cv2.VideoCapture(0); ok, f = c.read(); print(ok, None if f is None else f.shape)"
```

Expected output: `True (480, 640, 3)`. On macOS, allow camera access for Terminal in System Settings, Privacy and Security.
