# app/video/evaluation/length_scaler.py

"""
Phase 5.2 — Length-Aware Confidence Scaling (READ-ONLY)

Purpose:
---------
Reduce confidence for short videos where
forensic evidence is statistically weaker.

Rules:
------
- NO thresholds
- NO verdict logic
- NO learning
- Deterministic math only
"""

from typing import Optional
import math


def apply_length_scaling(
    confidence: Optional[float],
    duration_seconds: Optional[float],
) -> float:
    """
    Scales confidence based on video duration.

    Inputs:
    -------
    confidence        : float (0.0 – 1.0)
    duration_seconds  : float (video length in seconds)

    Output:
    -------
    scaled_confidence : float (0.0 – 1.0)
    """

    if not isinstance(confidence, (int, float)):
        return 0.0

    if not isinstance(duration_seconds, (int, float)):
        return round(float(confidence), 4)

    c = max(0.0, min(1.0, float(confidence)))
    t = max(0.0, float(duration_seconds))

    # Smooth saturation curve
    # <5s → noticeable penalty
    # ~15s → moderate
    # >30s → near full confidence
    scale = 1.0 - math.exp(-t / 15.0)

    scaled = c * scale

    return max(0.0, min(1.0, round(scaled, 4)))
