import cv2
import numpy as np
from typing import List


# --------------------------------------------------
# CONFIG (SOFT, NOT DECISIONS)
# --------------------------------------------------
DUPLICATE_DISTANCE_THRESHOLD = 6.0
MIN_RUN_LENGTH = 3


# --------------------------------------------------
# FRAME HASHING
# --------------------------------------------------

def compute_frame_hash(image_path: str) -> np.ndarray | None:
    """
    Computes perceptual hash (DCT-based).
    Robust to compression and resizing.
    """
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None

        img = cv2.resize(img, (32, 32))
        dct = cv2.dct(np.float32(img))
        return dct[:8, :8].flatten()

    except Exception:
        return None


def hash_distance(h1: np.ndarray, h2: np.ndarray) -> float:
    return float(np.linalg.norm(h1 - h2))


# --------------------------------------------------
# FRAME DUPLICATION ANALYSIS
# --------------------------------------------------

def analyze_frame_duplication(frame_paths: List[str]) -> dict:
    """
    Phase 4 — Frame Duplication Detector (READ-ONLY)

    PURPOSE:
    - Detect repeated frames suggesting freezing or reuse
    - Soft adversarial awareness only
    """

    hashes = [compute_frame_hash(p) for p in frame_paths]

    longest_run = 0
    current_run = 0

    for i in range(1, len(hashes)):
        h1, h2 = hashes[i - 1], hashes[i]

        if h1 is None or h2 is None:
            current_run = 0
            continue

        if hash_distance(h1, h2) < DUPLICATE_DISTANCE_THRESHOLD:
            current_run += 1
            longest_run = max(longest_run, current_run)
        else:
            current_run = 0

    score = 0.0
    signals = []

    if longest_run >= MIN_RUN_LENGTH:
        score = min(0.3, longest_run * 0.05)
        signals.append("consecutive_frame_similarity")

    return {
        "available": True,
        "score": round(score, 3),
        "signals": signals,
    }
