# app/video/human_behavior/gaze_dynamics.py

import os
os.environ["MEDIAPIPE_DISABLE_GPU"] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import cv2
import numpy as np
from typing import Dict, List
import mediapipe as mp

_face_mesh = None

LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]


def _get_face_mesh():
    global _face_mesh
    if _face_mesh is None:
        _face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
        )
    return _face_mesh


def analyze_gaze_dynamics(frames: List[Dict]) -> Dict:
    gaze_positions = []

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

        def center(ids):
            pts = np.array([
                [face.landmark[i].x * w, face.landmark[i].y * h]
                for i in ids
            ])
            return pts.mean(axis=0)

        gaze = (center(LEFT_IRIS) + center(RIGHT_IRIS)) / 2.0
        gaze_positions.append(gaze)

    if len(gaze_positions) < 5:
        return {
            "verdict": "insufficient_data",
            "confidence": 0.0,
        }

    diffs = np.linalg.norm(
        np.diff(np.array(gaze_positions), axis=0),
        axis=1
    )

    variance = float(np.var(diffs))

    return {
        "verdict": "natural_gaze" if variance > 1.0 else "static_gaze",
        "confidence": round(min(1.0, variance / 10), 3),
    }
