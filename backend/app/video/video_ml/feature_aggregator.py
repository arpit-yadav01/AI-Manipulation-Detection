import numpy as np
from typing import List, Dict, Any


def _safe_float(x):
    try:
        return float(x)
    except Exception:
        return None


def _stats(values: List[float]) -> Dict[str, float]:
    """
    Compute robust statistics from a list of floats.
    Returns JSON-safe numbers only.
    """
    if not values:
        return {
            "mean": None,
            "std": None,
            "min": None,
            "max": None,
        }

    arr = np.array(values, dtype=np.float32)

    return {
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr)),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
    }


def aggregate_video_features(frames: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Phase 3 — Step 1
    Aggregate frame-level forensic signals into video-level features.
    """

    ml_probs = []
    yaw_vals = []
    pitch_vals = []
    roll_vals = []
    lighting_diffs = []

    for frame in frames:
        # ML probability
        ml_prob = frame.get("ml_fake_probability")
        if ml_prob is not None:
            ml_probs.append(_safe_float(ml_prob))

        # Geometry
        geom = frame
