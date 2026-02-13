import numpy as np
from typing import Dict, Optional


# ============================================================
# CROSS-SIGNAL DIFFUSION CORRELATION (NO THRESHOLDS)
# ============================================================

def _safe_array(values):
    arr = [v for v in values if v is not None]
    if len(arr) < 3:
        return None
    return np.asarray(arr, dtype=np.float32)


def _safe_corr(a: np.ndarray, b: np.ndarray) -> Optional[float]:
    if a is None or b is None:
        return None
    if len(a) != len(b):
        m = min(len(a), len(b))
        a = a[:m]
        b = b[:m]
    if np.std(a) < 1e-6 or np.std(b) < 1e-6:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def analyze_cross_signal_diffusion_correlation(
    *,
    ela_scores,
    ml_probs,
    head_pose_drift,
    lighting_drift,
    temporal_residual_signal,
):
    """
    Looks for unnatural coupling between otherwise independent signals.

    Diffusion artifacts tend to rise together:
    - ELA spikes
    - ML confidence
    - geometric instability
    - residual temporal stability

    REAL video → weak / noisy correlations
    DIFFUSION video → synchronized correlations

    ⚠️ No thresholds
    ⚠️ No verdict
    ⚠️ Research-only signal
    """

    ela = _safe_array(ela_scores)
    ml = _safe_array(ml_probs)

    geom = None
    if head_pose_drift and head_pose_drift.get("available", True):
        geom = _safe_array(head_pose_drift.get("per_frame_magnitude", []))

    light = None
    if lighting_drift and lighting_drift.get("available", True):
        light = _safe_array(lighting_drift.get("per_frame_difference", []))

    correlations = {}

    correlations["ela_vs_ml"] = _safe_corr(ela, ml)
    correlations["ela_vs_geometry"] = _safe_corr(ela, geom)
    correlations["ela_vs_lighting"] = _safe_corr(ela, light)

    correlations["ml_vs_geometry"] = _safe_corr(ml, geom)
    correlations["ml_vs_lighting"] = _safe_corr(ml, light)

    # --------------------------------------------------------
    # Residual temporal stability correlation (video-level)
    # --------------------------------------------------------
    residual_score = None
    if (
        temporal_residual_signal
        and temporal_residual_signal.get("available")
    ):
        residual_score = temporal_residual_signal.get(
            "temporal_stability_score"
        )

    correlations["residual_stability"] = residual_score

    # --------------------------------------------------------
    # Aggregate correlation strength (absolute mean)
    # --------------------------------------------------------
    valid_corrs = [
        abs(v) for v in correlations.values()
        if isinstance(v, (int, float))
    ]

    if valid_corrs:
        correlations["mean_absolute_correlation"] = round(
            float(np.mean(valid_corrs)), 6
        )
    else:
        correlations["mean_absolute_correlation"] = None

    return {
        "available": True,
        "correlations": correlations,
        "num_correlations": len(valid_corrs),
    }
