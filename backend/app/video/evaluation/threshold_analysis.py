# app/video/evaluation/threshold_analysis.py

"""
Phase 5.4 — Threshold Analysis (OFFLINE ONLY)

Purpose:
---------
Support offline evaluation of confidence distributions
to study false positives and stability.

IMPORTANT:
----------
❌ DO NOT import this file at runtime
❌ DO NOT use inside workers or APIs
"""

from typing import List, Dict
import numpy as np


def analyze_confidence_distribution(
    confidences: List[float]
) -> Dict[str, float]:
    """
    Computes descriptive statistics for confidence values.
    """

    values = [c for c in confidences if isinstance(c, (int, float))]

    if not values:
        return {}

    arr = np.array(values, dtype=float)

    return {
        "count": int(len(arr)),
        "mean": round(float(np.mean(arr)), 4),
        "std": round(float(np.std(arr)), 4),
        "min": round(float(np.min(arr)), 4),
        "max": round(float(np.max(arr)), 4),
        "p90": round(float(np.percentile(arr, 90)), 4),
        "p95": round(float(np.percentile(arr, 95)), 4),
    }
