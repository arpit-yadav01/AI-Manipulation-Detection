# app/video/human_behavior/micro_expression.py

import os
os.environ["MEDIAPIPE_DISABLE_GPU"] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import cv2
import numpy as np
from typing import Dict, List
import mediapipe as mp

_face_mesh = None

MOUTH = [13, 14]
BROW = [65, 295]


def _get_face_mesh():
    global _face_mesh
    if _face_mesh is None:
        _face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
        )
    return _face_mesh


def analyze_micro_expression_consistency(frames: List[Dict]) -> Dict:
    signals = []

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

        def dist(a, b):
            p1 = np.array([face.landmark[a].x * w, face.landmark[a].y * h])
            p2 = np.array([face.landmark[b].x * w, face.landmark[b].y * h])
            return np.linalg.norm(p1 - p2)

        mouth_open = dist(MOUTH[0], MOUTH[1])
        brow_raise = dist(BROW[0], BROW[1])

        signals.append(mouth_open + brow_raise)

    if len(signals) < 5:
        return {
            "verdict": "insufficient_data",
            "confidence": 0.0,
        }

    variance = float(np.var(signals))

    return {
        "verdict": "natural_expression" if variance > 2.0 else "flat_expression",
        "confidence": round(min(1.0, variance / 20), 3),
    }
