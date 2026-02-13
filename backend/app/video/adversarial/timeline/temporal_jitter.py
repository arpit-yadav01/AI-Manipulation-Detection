import numpy as np
from typing import List


# --------------------------------------------------
# CONFIG (SOFT HEURISTICS ONLY)
# --------------------------------------------------
MIN_FRAMES = 10
JITTER_SENSITIVITY = 0.35


def analyze_temporal_jitter(timestamps: List[float]) -> dict:
    """
    Phase 4 — Temporal Jitter Analysis (READ-ONLY)

    PURPOSE:
    - Detect irregular frame timing caused by resampling, dropping, or duplication
    - Soft adversarial awareness only
    """

    if not timestamps or len(timestamps) < MIN_FRAMES:
        return {
            "available": False,
            "score": 0.0,
            "signals": [],
        }

    deltas = np.diff(timestamps)

    if np.any(deltas <= 0):
        return {
            "available": True,
            "score": 0.2,
            "signals": ["non_monotonic_timestamps"],
        }

    mean_delta = float(np.mean(deltas))
    std_delta = float(np.std(deltas))

    if mean_delta <= 0:
        return {
            "available": True,
            "score": 0.25,
            "signals": ["invalid_frame_intervals"],
        }

    jitter_ratio = std_delta / mean_delta

    score = min(0.35, jitter_ratio * JITTER_SENSITIVITY)
    signals = []

    if jitter_ratio > 0.15:
        signals.append("irregular_frame_intervals")

    return {
        "available": True,
        "score": round(score, 3),
        "signals": signals,
    }
