# app/video/evaluation/confidence_calibrator.py

"""
Phase 5.1 — Confidence Calibration (READ-ONLY)

Purpose:
---------
Map raw model confidence values into a calibrated,
human-interpretable probability scale.

Rules:
------
- NO thresholds
- NO verdict changes
- NO learning
- NO model updates
- Pure mathematical transformation
"""

from typing import Optional
import math


def calibrate_confidence(
    raw_confidence: Optional[float]
) -> float:
    """
    Calibrates raw confidence into a statistically safer range.

    Input:
    ------
    raw_confidence : float (0.0 – 1.0)

    Output:
    -------
    calibrated_confidence : float (0.0 – 1.0)

    Behavior:
    ---------
    - Dampens overconfidence near extremes
    - Preserves ordering (monotonic)
    - Conservative for borderline signals
    """

    if not isinstance(raw_confidence, (int, float)):
        return 0.0

    # Clamp to valid range
    x = max(0.0, min(1.0, float(raw_confidence)))

    # Logistic-style soft calibration
    # Centered at 0.5 to avoid bias
    k = 4.0  # slope (fixed, non-trainable)
    calibrated = 1.0 / (1.0 + math.exp(-k * (x - 0.5)))

    # Rescale back to [0, 1]
    calibrated = (calibrated - 0.5) * 1.2 + 0.5

    return max(0.0, min(1.0, round(calibrated, 4)))
