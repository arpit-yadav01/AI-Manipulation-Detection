# app/video/audio_sync/lip_motion.py

import cv2
import mediapipe as mp
import numpy as np
import os
from typing import Optional, Dict

# 🔥 HARD FORCE CPU MODE (CRITICAL)
os.environ["MEDIAPIPE_DISABLE_GPU"] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["EGL_PLATFORM"] = "surfaceless"

mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# MediaPipe landmark indices
UPPER_LIP_ID = 13
LOWER_LIP_ID = 14


def extract_lip_motion(image_path: str) -> Optional[Dict]:
    """
    CPU-SAFE mouth openness estimator.
    NEVER touches GPU.
    """

    image = cv2.imread(image_path)
    if image is None:
        return None

    h, w = image.shape[:2]
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    try:
        result = mp_face_mesh.process(rgb)
    except Exception:
        # 🔒 ABSOLUTE SAFETY
        return None

    if not result.multi_face_landmarks:
        return None

    face = result.multi_face_landmarks[0]

    upper = face.landmark[UPPER_LIP_ID]
    lower = face.landmark[LOWER_LIP_ID]

    upper_pt = np.array([upper.x * w, upper.y * h])
    lower_pt = np.array([lower.x * w, lower.y * h])

    openness = float(np.linalg.norm(upper_pt - lower_pt))

    return {
        "mouth_openness": round(openness, 3)
    }
