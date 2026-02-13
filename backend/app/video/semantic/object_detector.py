import cv2
import numpy as np


def detect_semantic_objects(frame_path: str):
    """
    Lightweight semantic detector.
    Focuses on hands, text, and large foreground objects.
    """

    img = cv2.imread(frame_path)
    if img is None:
        return []

    h, w = img.shape[:2]

    # Placeholder-safe boxes (expandable later to YOLO / MediaPipe)
    # For now we focus on relative consistency, not class accuracy
    objects = []

    # Central region heuristic (face-adjacent objects)
    objects.append({
        "type": "foreground",
        "bbox": [int(w*0.2), int(h*0.2), int(w*0.8), int(h*0.8)],
    })

    return objects
