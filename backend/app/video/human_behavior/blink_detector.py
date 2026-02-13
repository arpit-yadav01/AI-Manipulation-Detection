# app/video/human_behavior/blink_detector.py

import os
os.environ["MEDIAPIPE_DISABLE_GPU"] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import cv2
import numpy as np
from typing import Dict, List

import mediapipe as mp

# Lazy singleton
_face_mesh = None

# Eye landmarks (MediaPipe)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]


def _get_face_mesh():
    global _face_mesh
    if _face_mesh is None:
        _face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=False,
        )
    return _face_mesh


def _eye_aspect_ratio(pts):
    v1 = np.linalg.norm(pts[1] - pts[5])
    v2 = np.linalg.norm(pts[2] - pts[4])
    h = np.linalg.norm(pts[0] - pts[3])
    return (v1 + v2) / (2.0 * h + 1e-6)


def analyze_blink_consistency(frames: List[Dict]) -> Dict:
    """
    CPU-safe blink detection.
    Conservative.
    """

    ear_values = []

    for f in frames:
        img = cv2.imread(f["path"])
        if img is None:
            continue

        h, w = img.shape[:2]
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        res = _get_face_mesh().process(rgb)
        if not res.multi_face_landmarks:
            continue

        face = res.multi_face_landmarks[0]

        def pts(ids):
            return np.array([
                [face.landmark[i].x * w, face.landmark[i].y * h]
                for i in ids
            ])

        ear = (_eye_aspect_ratio(pts(LEFT_EYE)) +
               _eye_aspect_ratio(pts(RIGHT_EYE))) / 2.0

        ear_values.append(ear)

    if len(ear_values) < 5:
        return {
            "verdict": "insufficient_data",
            "confidence": 0.0,
        }

    variance = float(np.var(ear_values))

    return {
        "verdict": "natural_blink" if variance > 0.0005 else "rigid_blink",
        "confidence": round(min(1.0, variance * 50), 3),
    }
