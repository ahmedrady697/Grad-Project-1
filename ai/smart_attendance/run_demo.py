"""Run attendance on a webcam or video file.

Enrollment photos go in one folder per student:

    data/enroll/student_001/1.jpg
    data/enroll/student_001/2.jpg
    data/enroll/student_002/1.jpg

Examples (from the repo root):

    python -m ai.smart_attendance.run_demo --enroll data/enroll --source 0
    python -m ai.smart_attendance.run_demo --enroll data/enroll --source class.mp4 --skip 10
    python -m ai.smart_attendance.run_demo --gallery gallery.npz --source 0 \
        --backend http://127.0.0.1:8000

Photos and videos are personal data: keep them out of git (see data/README.md).
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
import urllib.error
from pathlib import Path

import cv2
import numpy as np

from ai.shared.video_io import read_frames
from ai.smart_attendance.attendance import AttendanceSystem

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}
REPO_ROOT = Path(__file__).resolve().parents[2]


def resize_to_width(frame: np.ndarray, width: int) -> np.ndarray:
    h, w = frame.shape[:2]
    if w <= width:
        return frame
    return cv2.resize(frame, (width, int(h * width / w)))


def enroll_from_folder(system: AttendanceSystem, folder: Path) -> None:
    for student_dir in sorted(p for p in folder.iterdir() if p.is_dir()):
        images = []
        for path in sorted(student_dir.iterdir()):
            if path.suffix.lower() in IMAGE_SUFFIXES:
                image = cv2.imread(str(path))
                if image is not None:
                    images.append(image)
        try:
            added = system.enroll(student_dir.name, images)
            print(f"enrolled {student_dir.name}: {added}/{len(images)} photos used")
        except ValueError as err:
            print(f"WARNING: {err}", file=sys.stderr)


def load_send_events():
    """data-integration/ has a hyphen, so it cannot be imported normally."""
    path = REPO_ROOT / "data-integration" / "client.py"
    spec = importlib.util.spec_from_file_location("data_integration_client", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.send_events


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--enroll", type=Path, help="folder with one sub-folder per student")
    parser.add_argument("--gallery", type=Path, help=".npz file to load from / save to")
    parser.add_argument("--source", default="0", help="webcam index or video file (default 0)")
    parser.add_argument("--skip", type=int, default=5, help="frames to drop between frames used")
    parser.add_argument("--width", type=int, default=640, help="resize frames to this width")
    parser.add_argument("--threshold", type=float, default=0.4)
    parser.add_argument("--min-consistent", type=int, default=3)
    parser.add_argument("--backend", help="backend URL, for example http://127.0.0.1:8000")
    args = parser.parse_args()

    system = AttendanceSystem(args.threshold, min_consistent=args.min_consistent)

    if args.gallery and args.gallery.exists():
        system.load_gallery(args.gallery)
        print(f"loaded gallery: {len(system.gallery)} students")
    if args.enroll:
        enroll_from_folder(system, args.enroll)
        if args.gallery:
            system.save_gallery(args.gallery)
    if len(system.gallery) == 0:
        sys.exit("No enrolled students. Use --enroll or --gallery.")

    send_events = load_send_events() if args.backend else None
    source: int | str = int(args.source) if args.source.isdigit() else args.source

    try:
        for frame in read_frames(source, skip=args.skip):
            events = system.process_frame(resize_to_width(frame, args.width))
            for event in events:
                who = event.student_id or "unknown"
                print(f"{event.timestamp}  {event.type.value:16s} {who}  conf={event.confidence:.2f}")
            if events and send_events:
                try:
                    send_events(events, args.backend)
                except (urllib.error.URLError, OSError) as err:
                    print(f"WARNING: could not reach backend: {err}", file=sys.stderr)
    except KeyboardInterrupt:
        pass

    print(f"\nPresent ({len(system.present)}): {', '.join(sorted(system.present)) or '-'}")


if __name__ == "__main__":
    main()
