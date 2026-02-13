from typing import List, Dict, Optional
import numpy as np


def compute_geometry_drift(
    head_poses: List[Optional[Dict[str, float]]]
) -> Dict:
    """
    Analyze temporal head pose drift across frames.
    Input: list of head_pose dicts or None
    """

    # Filter invalid frames
    poses = [p for p in head_poses if p is not None]

    if len(poses) < 3:
        return {
            "verdict": "insufficient_data",
            "mean_drift": 0.0,
            "max_drift": 0.0,
        }

    deltas = []

    for i in range(1, len(poses)):
        prev = poses[i - 1]
        curr = poses[i]

        dy = abs(curr["yaw"] - prev["yaw"])
        dp = abs(curr["pitch"] - prev["pitch"])
        dr = abs(curr["roll"] - prev["roll"])

        deltas.append(max(dy, dp, dr))

    deltas = np.array(deltas)

    mean_drift = float(np.mean(deltas))
    max_drift = float(np.max(deltas))

    # Conservative verdict
    if max_drift > 12.0:
        verdict = "unstable_geometry"
    else:
        verdict = "stable"

    return {
        "verdict": verdict,
        "mean_drift": round(mean_drift, 2),
        "max_drift": round(max_drift, 2),
    }
