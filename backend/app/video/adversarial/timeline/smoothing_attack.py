import numpy as np
from typing import List


# --------------------------------------------------
# CONFIG (SOFT HEURISTICS ONLY)
# --------------------------------------------------
MIN_FRAMES = 10
SMOOTHING_SENSITIVITY = 0.4


def analyze_temporal_smoothing(values: List[float]) -> dict:
    """
    Phase 4 — Temporal Smoothing Analysis (READ-ONLY)

    PURPOSE:
    - Detect unnaturally suppressed frame-to-frame variation
    - Soft signal for temporal post-processing or generative smoothing
    """

    clean_values = [v for v in values if isinstance(v, (int, float))]

    if len(clean_values) < MIN_FRAMES:
        return {
            "available": False,
            "score": 0.0,
            "signals": [],
        }

    arr = np.array(clean_values, dtype=np.float32)

    diffs = np.abs(np.diff(arr))
    mean_diff = float(np.mean(diffs))
    variance = float(np.var(arr))

    if variance <= 0:
        return {
            "available": True,
            "score": 0.25,
            "signals": ["degenerate_temporal_variation"],
        }

    suppression_ratio = mean_diff / (variance + 1e-6)

    score = min(0.35, suppression_ratio * SMOOTHING_SENSITIVITY)
    signals = []

    if suppression_ratio < 0.15:
        signals.append("temporally_over_smoothed_signal")

    return {
        "available": True,
        "score": round(max(score, 0.0), 3),
        "signals": signals,
    }
