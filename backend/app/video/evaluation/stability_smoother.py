# app/video/evaluation/stability_smoother.py

"""
Phase 5.3 — Stability Smoothing (READ-ONLY)

Purpose:
---------
Reduce sudden confidence spikes caused by
temporal noise or single-frame artifacts.

Rules:
------
- NO verdict logic
- NO thresholds
- NO learning
- Deterministic math only
"""

from typing import List, Optional


def smooth_confidence_series(
    confidence_series: Optional[List[float]],
    window_size: int = 5,
) -> List[float]:
    """
    Applies moving-average smoothing to confidence values.

    Inputs:
    -------
    confidence_series : list of floats (0.0 – 1.0)
    window_size       : smoothing window (fixed)

    Output:
    -------
    smoothed_series   : list of floats
    """

    if not isinstance(confidence_series, list):
        return []

    if len(confidence_series) < 3:
        return confidence_series

    smoothed = []

    for i in range(len(confidence_series)):
        window = confidence_series[
            max(0, i - window_size // 2) :
            min(len(confidence_series), i + window_size // 2 + 1)
        ]

        valid = [v for v in window if isinstance(v, (int, float))]

        if not valid:
            smoothed.append(0.0)
        else:
            smoothed.append(round(sum(valid) / len(valid), 4))

    return smoothed
